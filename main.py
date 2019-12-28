from readers import arxiv
from src.dataset import TrainingDataset
from src.dataset import ClassificationDataset
from run import Bert
from src import database
from src.constants import Labels
import pudb
from tqdm import tqdm
from transformers import BertConfig


def latest_update():
    latest_papers = arxiv.read()
    print(f"New papers: {len(latest_papers)}")
    
    bert = Bert()
    dataset = ClassificationDataset(latest_papers)
    classifications = bert.classify(dataset)

    for score, paper in zip(classifications, latest_papers):
        paper.score = round(score[0], 3)
        database.add(paper)
        database.add_paper_to_label(paper, Labels.LATEST)
        database.add_paper_to_label(paper, Labels.UNLABELED)

    return latest_papers

def latest(print_papers=True):
    latest = database.get_latest_papers()
    latest = sorted(latest , key= lambda x: x.score)
    return latest

def annotate(numbers, target, papers):
    for idx in numbers:
        database.update(papers[idx], target)
    

def search(keywords):
    keywords = [kw.lower() for kw in keywords]
    all_papers = database.all_abstracts()
    hits = []
    for paper in all_papers:
        for keyword in keywords:
            if keyword in paper.summary.lower() or \
               keyword in paper.title.lower():
                hits.append(paper)
    return hits

def train():
    dataset = TrainingDataset()

    distilBert = Bert()
    distilBert.train(dataset)
    distilBert.save()

def suggestions():
    distilBert = DistilBert()
    distilBert.load()
    dataset = ClassificationDataset()

    classifications = distilBert.classify(dataset)
    classifications = sorted(enumerate(classifications), key=lambda x: x[1], reverse=True)
    suggested_papers = list(map(lambda x: dataset.get_paper(x[0]), classifications))

def show(cmd, numbers):
    if cmd == "latest":
        papers = latest(False)
    for idx in numbers:
        print(papers[idx].title)
        print(papers[idx].summary)
        print()

def sync():
    registered_paper_ids= []
    for label in [Labels.UNREAD, Labels.READ, Labels.NEGATIVE, Labels.UNLABELED]:
        paper_ids = [paper_list_elem["paper_id"] for paper_list_elem in database.get_ids_from_label(label)]
        registered_paper_ids.extend(paper_ids)
    registered_paper_ids = set(registered_paper_ids)

    all_ids = set([paper.paper_id for paper in database.all_abstracts()])

    new_ids = all_ids.difference(registered_paper_ids)
    new_papers = [database.read_paper(paper_id) for paper_id in new_ids]

    bert = Bert()
    dataset = ClassificationDataset(new_papers)
    classifications = bert.classify(dataset)

    for score, paper in zip(classifications, latest_papers):
        paper.score = round(score[0], 3)
        database.add(paper)
        database.add_paper_to_label(paper, Labels.UNLABELED)

    return new_papers 



    
    





