from src.dataset import Dataset
from src.constants import Paths
from src.constants import DEVICE
from torch.utils.data import DataLoader
from transformers import BertModel
from transformers import BertTokenizer
from transformers import AdamW
import torch
from torch.nn import Module
from torch import tensor
from torch.nn import BCELoss
import time
import pudb
from tqdm import tqdm
import os

class FeedForwardModel(Module):
    def __init__(self, max_length):
        super().__init__()
        self.dense_1 = torch.nn.Linear(768, 1)
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

    def forward_xlm(self, x, attention_mask, langs):
        xlm_output = self.pretrained_xlm(x, attention_mask=attention_mask, langs=langs)
        xlm_output = xlm_output[0]
        output_1 = torch.zeros((self.config.batch_size, 2*self.transformer_output_dim)).to(self.config.device)
        for i in range(self.config.batch_size):
            masked_output = xlm_output[i][attention_mask[i].nonzero(), :]
            cls = masked_output[0][0]
            output_1[i] = cls
        return output_1


    def forward(self, x, attention_mask, langs):
        output_1 = self.forward_bert(x, attention_mask, langs)

        output_2 = self.ffn_model(output_1)
        return output_2

    def train(self, dataset):
        print("starting training")

        parameters = [{"params": self.ffn_model.parameters(), "lr":0.001},
                      {"params": self.bert.parameters(), "lr": 0.00001}]


        optimizer = AdamW(self.ffn_model.parameters())
        loss_function = BCELoss(reduce="sum")

        self.ffn_model.train()
        self.bert.train()

        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collate_fn, drop_last=True)

        epochs = 10
        batches = int(len(dataset) / self.batch_size)
        self.ffn_model = self.ffn_model.to(DEVICE)
        self.bert = self.bert.to(DEVICE)


        previous_running_loss = 1.0
        for epoch in range(epochs):
            running_loss = 0
            progress_bar = tqdm(total=batches)

            for encoded_abstracts, targets, attention_mask in dataloader:
                encoded_abstracts = encoded_abstracts.to(DEVICE)
                targets = targets.to(DEVICE)


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


    def collate_fn(self, elems):
        sentences = list(map(lambda x: x[0], elems))
        targets = list(map(lambda x: x[1], elems))

        tokenized_sentences = [self.tokenizer.tokenize(sentence) for sentence in sentences]
        safe_tokenized_sentences = [self.cut_sentences(tokenized_sentence) for tokenized_sentence in tokenized_sentences]

        encoded_sentences = [self.tokenizer.convert_tokens_to_ids(tokenized_sentence) for tokenized_sentence in safe_tokenized_sentences]
        encoded_sentences_with_spec_tokens  = [self.tokenizer.add_special_tokens_single_sequence(encoded_sentence) for encoded_sentence in encoded_sentences]
        padded_encoded_sentences = [self.pad_token_ids(encoded_sentence) for encoded_sentence in encoded_sentences_with_spec_tokens]

        attention_mask = self.create_attention_mask(safe_tokenized_sentences)

        return tensor(padded_encoded_sentences), tensor([targets]).t(), attention_mask 

    def cut_sentences(self, tokenized_sentence):
        sentence_length = len(tokenized_sentence)
        if sentence_length  == 0:
            return [self.tokenizer.unk_token]
        elif self.config.max_length <= sentence_length + 2:
            # -2 Offset is because <\s> and <\s> will be added
            return tokenized_sentence[:self.config.max_length - 2]
        else:
            return tokenized_sentence

    def pad_token_ids(self, token_ids):
        if len(token_ids) < self.config.max_length:
            pad_tokens = self.config.max_length - len(token_ids)
            padding = [self.tokenizer.pad_token_id] * pad_tokens
            padded_tokenized_sentence = token_ids + padding
            return padded_tokenized_sentence
        else:
            return token_ids

    def create_attention_mask(self, safe_tokenized_sentences):
        sentence_lengths = list(map(lambda x: min(len(x), self.config.max_length), safe_tokenized_sentences))
        attention_mask = torch.zeros(self.config.batch_size, self.config.max_length)
        for i in range(self.config.batch_size):
            length = sentence_lengths[i]
            attention_mask[i][0:length] = 1
        return attention_mask

    def classify(self, dataset):
        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collate_fn, drop_last=True)

        batches = int(len(dataset) / self.batch_size)
        progress_bar = tqdm(total=batches, desc="classifying")

        self.ffn_model = self.ffn_model.to(DEVICE)
        self.bert = self.bert.to(DEVICE)

        outputs = []
        for encoded_abstracts, targets in dataloader:
            encoded_abstracts = encoded_abstracts.to(DEVICE)

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
        torch.save(self.ffn_model, os.path.join(models_path, "ffn_model.pt"))
        torch.save(self.bert, os.path.join(models_path, "bert.pt"))

    def load(self):
        self.ffn_model = torch.load(Paths.FFN_MODEL)
        self.bert = torch.load(Paths.BERT_MODEL)


