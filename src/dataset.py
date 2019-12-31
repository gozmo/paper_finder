import json
import random
import random
import os
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from src import database
from src.constants import Labels

class BaseDataset(Dataset):
    def __init__(self, papers):
        self.papers= papers

    def __len__(self):
        return len(self.papers)

    def get_paper(self, idx):
        return self.papers[idx]

class TrainingDataset(BaseDataset):
    def __init__(self):
        read = database.get_papers_of_label(Labels.READ)
        unread = database.get_papers_of_label(Labels.UNREAD)
        positives = read + unread
        positives = zip(positives, [1.0]*len(positives))

        negatives = database.get_papers_of_label(Labels.NEGATIVE)
        negatives = zip(negatives, [0.0]*len(negatives))

        papers = list(positives) + list(negatives)
        BaseDataset.__init__(self, papers)

    def __getitem__(self, idx):
        text = self.papers[idx][0].summary
        label = self.papers[idx][1]

        return text, label

class ClassificationDataset(BaseDataset):
    def __init__(self, papers):
        BaseDataset.__init__(self, papers)

    def __getitem__(self, idx):
        text = self.papers[idx].summary
        return text, 0.0

