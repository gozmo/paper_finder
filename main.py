from readers import arxiv
from src.dataset import TrainingDataset
from src.dataset import ClassificationDataset
from src.dataset import LatestDataset 
import io_utils
from run import Bert
from cache import cache

def latest():
    key = "latest"
    if cache.is_empty(key):
        papers = arxiv.read()
        io_utils.write_latest_papers(papers)

        distilBert = Bert()
        distilBert.load()
        dataset = LatestDataset()

        classifications = distilBert.classify(dataset)
        classifications = sorted(enumerate(classifications), key=lambda x: x[1], reverse=True)
        suggested_papers = list(map(lambda x: dataset.get_paper(x[0]), classifications))
        cache.set(key, suggested_papers)

    return cache.get(key)

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

    distilBert.save()

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
