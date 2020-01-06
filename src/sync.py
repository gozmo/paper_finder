import os
from src import arxiv
from src import database
from src.constants import Labels
from src.constants import Paths
from run import Bert
from src.dataset import ClassificationDataset
from src import io_utils

def sync_label(label, pdf_path):
    label_abstracts_ids = io_utils.read_label_ids(label)
    label_pdfs_ids = [filename.replace(".pdf", "").replace("v1", "").replace("v2","") for filename in os.listdir(pdf_path)]

    new_ids = set(label_pdfs_ids).difference(set(label_abstracts_ids))

    new_papers = []
    for new_id in new_ids:
        if arxiv.is_arxiv_id(new_id):
            paper = arxiv.download_paper_info(new_id)
            database.add(paper)
            database.add_paper_to_label(paper, label)
            new_papers.append(paper)

    return new_papers

def sync_pdfs():
    unread_papers = sync_label(Labels.UNREAD, Paths.PDF_UNREAD)
    read_papers = sync_label(Labels.READ, Paths.PDF_READ)
    return unread_papers + read_papers

def sync_abstracts():
    registered_paper_ids= []
    for label in [Labels.UNREAD, Labels.READ, Labels.NEGATIVE, Labels.UNLABELED]:
        paper_ids = database.get_ids_from_label(label)
        registered_paper_ids.extend(paper_ids)
    registered_paper_ids = set(registered_paper_ids)

    all_ids = set([paper.paper_id for paper in database.all_papers()])

    new_ids = all_ids.difference(registered_paper_ids)
    new_papers = [database.read_paper(paper_id) for paper_id in new_ids]

    bert = Bert()
    bert.load()
    dataset = ClassificationDataset(new_papers)
    classifications = bert.classify(dataset)

    for score, paper in zip(classifications, new_papers):
        paper.score = round(score[0], 3)
        database.add(paper)
        database.add_paper_to_label(paper, Labels.UNLABELED)

    return new_papers 
