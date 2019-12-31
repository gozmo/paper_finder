from src.constants import Paths
from src.constants import Labels
import src.io_utils as io_utils

def add(paper):
    io_utils.write_paper(paper)

def add_paper_to_label(paper, label):
    io_utils.add_to_label(label, paper)

def get_ids_from_label(label):
    label_ids = io_utils.read_label_ids(label)
    return label_ids

def get_papers_of_label(label):
    paper_ids= io_utils.read_label_ids(label)
    papers = [io_utils.read_paper(paper_id) for paper_id in paper_ids]
    return papers

def all_papers():
    abstract_files_ids = io_utils.list_all_abstract_ids()
    papers = [io_utils.read_paper(abstract_id) for abstract_id in abstract_files_ids]
    return papers

def read_paper(paper_id):
    print(paper_id)
    return io_utils.read_paper(paper_id)

def update_paper_label(paper, label):
    if label == Labels.NEGATIVE or label == Labels.UNREAD:
        io_utils.remove_from_label(Labels.UNLABELED, paper)
        io_utils.remove_from_label(Labels.LATEST, paper)
    elif label == Labels.READ:
        io_utils.remove_from_label(Labels.UNREAD, paper)
        io_utils.remove_from_label(Labels.UNLABELED, paper)
        io_utils.remove_from_label(Labels.LATEST, paper)
    else:
        raise Exception("Label not supported")

    io_utils.add_to_label(label, paper)

