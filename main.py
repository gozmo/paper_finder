from readers import arxiv
from src.dataset import TrainingDataset
from src.dataset import ClassificationDataset
from run import Bert
from cache import cache
from src import database
from src.constants import Labels
import pudb
from tqdm import tqdm


def latest_update():
    # new_latest_papers = arxiv.read()

    # old_latest_papers = database.get_latest_papers()
    
    # new_latest_papers = set(new_latest_papers)
    # old_latest_papers = set(old_latest_papers)
    
    # new_papers = new_latest_papers.difference(old_latest_papers)
    # phase_out = old_latest_papers.difference(new_latest_papers) 
    latest_papers = database.get_latest_papers()
    bert = Bert()
    bert.load()
    dataset = ClassificationDataset(latest_papers)

    classifications = bert.classify(dataset)

    for score, paper in zip(classifications, new_papers):
        paper.score = score
        # database.add(paper)
        # database.add_paper_to_label(paper, Labels.LATEST)

    # for paper in phase_out:
        # database.update(paper.paper_id, Labels.LATEST, Labels.UNLABELED)
    return

def latest():
    latest = database.get_latest_papers()
    for paper in latest[:10]:
        print(paper.title)


def read_unlabeled():
    key = "unlabel"
    if cache.is_empty(key):

        unlabeled_papers = io_utils.read_unlabeled()

        papers = random.shuffle(unlabel_papers)
        cache.set(key, papers)

    return cache.get(key)

def search_unlabeled(keywords):
    key = "unlabel_search"
    if cache.is_empty(key):
        keyword_list = keywords.split(",")

        search_hits = io_utils.search_unlabeled(keyword_list)
        cache.set(key, search_hits)

    return cache.get(key)

def annotate(source_folder, paper_id, label):
    io_utils.move(source_folder, paper_id, label)

def train():
    dataset = TrainingDataset()

    distilBert = Bert()

    distilBert.train(dataset)

    #distilBert.save()

    cache.reset("suggestions")
    cache.reset("latest")

def suggestions():
    key = "suggestions"
    if cache.is_empty(key):
        distilBert = DistilBert()
        distilBert.load()
        dataset = ClassificationDataset()

        classifications = distilBert.classify(dataset)
        classifications = sorted(enumerate(classifications), key=lambda x: x[1], reverse=True)
        suggested_papers = list(map(lambda x: dataset.get_paper(x[0]), classifications))
        cache.set(key, suggested_papers)

    return cache.get(key)
