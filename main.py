from readers import arxiv
import pprint
from src.dataset import TrainingDataset
from src.dataset import ClassificationDataset
from src.cache import cache
from run import Bert
from src import database
from src.constants import Labels
import pudb
from tqdm import tqdm
from transformers import BertConfig
from src.sync import sync_pdfs
from src.sync import sync_abstracts

def get_papers(paper_source):
    if paper_source== "latest":
        papers = show_latest()
    elif paper_source == "search":
        papers = cache.get("search")
    elif paper_source == "sync":
        papers = cache.get("sync")
    elif paper_source == "suggestions":
        papers = show_suggestions()
    elif paper_source == "read":
        papers = show_read()
    elif paper_source == "unread":
        papers = show_unread()
    elif paper_source == "negative":
        papers = show_negative()
    else:
        raise Exception("Paper source not supported")
    return papers 

def latest_update():
    latest_papers = arxiv.read()
    latest_papers = list(set(latest_papers))
    
    bert = Bert()
    bert.load()
    dataset = ClassificationDataset(latest_papers)
    classifications = bert.classify(dataset)

    for score, paper in zip(classifications, latest_papers):
        paper.score = round(score[0], 3)
        database.add(paper)
        database.add_paper_to_label(paper, Labels.LATEST)
        database.add_paper_to_label(paper, Labels.UNLABELED)

    latest_papers = sorted(latest_papers , key= lambda x: x.score, reverse=True)
    return latest_papers

def show_latest():
    latest = database.get_papers_of_label(Labels.LATEST)
    latest = list(set(latest))
    latest = sorted(latest , key= lambda x: x.score, reverse=True)
    return latest

def annotate(paper_source, indices, label):
    papers = get_papers(paper_source)

    for idx in indices:
        database.update_paper_label(papers[idx], label)

def search_keywords(keywords):
    keywords = [kw.lower() for kw in keywords]
    all_papers = database.all_papers()
    hits = []
    for paper in all_papers:
        for keyword in keywords:
            if keyword in paper.summary.lower() or \
               keyword in paper.title.lower():
                hits.append(paper)
    hits = sorted(hits, key=lambda x: x.score, reverse=True)
    cache.set("search", hits)
    return hits

def search_hits():
    return cache.get("search")

def train():
    dataset = TrainingDataset()

    bert = Bert()
    bert.load()
    bert.train(dataset)
    bert.save()

def generate_suggestions():
    unlabeled_papers = database.get_papers_of_label(Labels.UNLABELED)
    bert = Bert()
    bert.load()
    dataset = ClassificationDataset(unlabeled_papers)
    classifications = bert.classify(dataset)

    for score, paper in zip(classifications, unlabeled_papers):
        paper.score = round(score[0], 3)
        database.add(paper)

    unlabeled_papers = sorted(unlabeled_papers, key=lambda x:x.score, reverse=True)
    return unlabeled_papers

def show_suggestions():
    suggested_papers = database.get_papers_of_label(Labels.UNLABELED)
    suggested_papers = sorted(suggested_papers, key= lambda x: x.score, reverse=True)
    return suggested_papers

def show(paper_source, numbers):
    papers = get_papers(paper_source)

    for idx in numbers:
        print(papers[idx].title)
        print(papers[idx].summary)
        print()

def sync_command():
    abstract_papers = sync_abstracts()
    pdf_papers = sync_pdfs()
    sync_papers = abstract_papers + pdf_papers
    cache.set("sync", sync_papers)
    return sync_papers

def show_read():
    read_papers = database.get_papers_of_label(Labels.READ)
    read_papers = sorted(read_papers, key= lambda x: x.score, reverse=True)
    return read_papers

def show_unread():
    unread_papers = database.get_papers_of_label(Labels.UNREAD)
    unread_papers = sorted(unread_papers, key= lambda x: x.score, reverse=True)
    return unread_papers

def show_negative():
    negative_papers = database.get_papers_of_label(Labels.NEGATIVE)
    negative_papers = sorted(negative_papers, key= lambda x: x.score, reverse=True)
    return negative_papers

def notes():
    pass
