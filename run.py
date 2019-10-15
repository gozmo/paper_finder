from src.dataset import Dataset
from torch.utils.data import DataLoader
from transformers import BertModel
from transformers import BertTokenizer
from transformers import AdamW
import torch
from torch.nn import Module
from torch import tensor
from torch.nn import BCEWithLogitsLoss
import time
import pudb
from tqdm import tqdm

class FeedForwardModel(Module):
    def __init__(self, max_length):
        super().__init__()
        self.dense_1 = torch.nn.Linear( 768 * max_length, 1)
        self.sigmoid_1 = torch.nn.Sigmoid()

    def forward(self, x):
        output_1 = self.dense_1(x)
        output_2 = self.sigmoid_1(output_1)
        return output_2

class Bert:
    def __init__(self):
        self.max_length = 100
        self.batch_size = 8
        self.pad_token = "<pad>"
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', max_length=self.max_length)
        self.ffn_model = FeedForwardModel(self.max_length)
        self.bert = BertModel.from_pretrained('bert-base-uncased')

    def tokenize(self, batch_strings:list):
        batch_list = []
        for string in batch_strings:
            input_ids = torch.tensor(self.tokenizer.encode(string, max_length=self.max_length))
            batch_list.append(input_ids)
        batch = torch.stack(batch_list)
        return batch

    def forward(self, x):
        predictions, _ = self.bert(x)
        output_1 = torch.reshape(predictions, [self.batch_size, 768*self.max_length])
        output_2 = self.ffn_model(output_1)
        return output_2

    def train(self, dataset):
        print("starting training")

        parameters = [{"params": self.ffn_model.parameters(), "lr":0.001},
                      {"params": self.bert.parameters(), "lr": 0.00001}]


        optimizer = AdamW(self.ffn_model.parameters())
        loss_function = BCEWithLogitsLoss(reduce="sum")

        self.ffn_model.train()
        self.bert.train()

        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collate_fn, drop_last=True)

        epochs = 10
        batches = int(len(dataset) / self.batch_size)
        self.ffn_model = self.ffn_model.to("cuda")
        self.bert = self.bert.to("cuda")

        previous_running_loss = 1.0
        for epoch in range(epochs):
            epoch_start_time = time.time()
            running_loss = 0
            progress_bar = tqdm(total=batches)

            for encoded_abstracts, targets in dataloader:
                encoded_abstracts = encoded_abstracts.to("cuda")
                targets = targets.to("cuda")


                # # zero the parameter gradients
                optimizer.zero_grad()

                with torch.set_grad_enabled(True):
                    output = self.forward(encoded_abstracts)
                    loss = loss_function(output, targets)
                    loss.backward()
                    optimizer.step()

                running_loss += loss.item()
                progress_bar.update(1)

            if running_loss == previous_running_loss:
                break

            previous_running_loss = running_loss

            epoch_time_elapsed = time.time() - epoch_start_time
            print(f"Epoch time: {epoch_time_elapsed}, loss:{running_loss}")

    def collate_fn(self, elems):
        abstracts = [elem[0] for elem in elems]
        targets = [elem[1] for elem in elems]
        tokenized_abstracts = [self.tokenizer.tokenize(abstract) for abstract in abstracts]
        padded_abstracts = [self.pad(abstract) for abstract in tokenized_abstracts]
        encoded_abstracts = [self.tokenizer.convert_tokens_to_ids(abstract) for abstract in padded_abstracts]

        x = torch.tensor(encoded_abstracts)
        targets= torch.tensor([targets]).t()

        return x, targets

    def classify(self, dataset):
        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collate_fn, drop_last=True)

        batches = int(len(dataset) / self.batch_size)
        progress_bar = tqdm(total=batches, desc="classifying")

        self.ffn_model = self.ffn_model.to("cuda")
        self.bert = self.bert.to("cuda")

        outputs = []
        for encoded_abstracts, targets in dataloader:
            encoded_abstracts = encoded_abstracts.to("cuda")

            output = self.forward(encoded_abstracts)
            outputs.extend(output.tolist())

            progress_bar.update(1)

        return outputs

    def pad(self, abstract):
        if len(abstract) < self.max_length:
            pads = self.max_length - len(abstract)
            padded_abstract = abstract + [self.pad_token]*pads
        else:
            padded_abstract = abstract[0:self.max_length]
        return padded_abstract

    def save(self):
        torch.save(self.ffn_model, "ffn_model.pt")
        torch.save(self.bert, "bert.pt")

    def load(self):
        self.ffn_model = torch.load("ffn_model.pt")
        self.bert = torch.load("bert.pt")


