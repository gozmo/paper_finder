import json
import random
import random
import os
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

class BaseDataset(Dataset):
    def __init__(self, papers):
        self.papers= papers

    def __len__(self):
        return len(self.papers)

    def get_paper(self, idx):
        return self.papers[idx]

class TrainingDataset(BaseDataset):
    def __init__(self):
        positives = read_file(READ)
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
    def __init__(self, papers):
        BaseDataset.__init__(self, dataset)

    def __getitem__(self, idx):
        text = self.data[idx]["summary"]
        return text, 0.0

