import json
import random
import random
import os
from torch.utils.data import Dataset, DataLoader

POSITIVE = "data/positive"
NEGATIVE = "data/negative"
UNLABELED = "data/unlabeled"
LATEST = "data/latest"


def read_file(directory):
    jsons = []
    for dirpath, dirs, files in os.walk(directory):
        for filename in files:
            source_file = os.path.join(dirpath, filename)
            with open(source_file, "r") as f:
                json_content = json.loads(f.read())
                jsons.append(json_content)
    return jsons

class BaseDataset(Dataset):
    def __init__(self, dataset):
        self.data = dataset

    def __len__(self):
        return len(self.data)

    def get_paper(self, idx):
        return self.data[idx]

class TrainingDataset(BaseDataset):
    def __init__(self):
        positives = read_file(POSITIVE)
        positives = zip(positives, [1.0]*len(positives))

        negatives = read_file(NEGATIVE)
        negatives = zip(negatives, [0.0]*len(negatives))

        dataset = list(positives) + list(negatives)
        random.shuffle(dataset)
        BaseDataset.__init__(self, dataset)

    def __getitem__(self, idx):
        text = self.data[idx][0]["summary"]
        label = self.data[idx][1]

        return text, label

class ClassificationDataset(BaseDataset):
    def __init__(self):
        dataset = read_file(UNLABELED)
        dataset = random.sample(self.dataset, 1000)
        BaseDataset.__init__(self, dataset)

    def __getitem__(self, idx):
        text = self.data[idx]["summary"]
        return text, 0.0

class LatestDataset(BaseDataset):
    def __init__(self):
        dataset = read_file(LATEST)
        BaseDataset.__init__(self, dataset)

    def __getitem__(self, idx):
        text = self.data[idx]["summary"]
        return text, 0.0
