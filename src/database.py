from src.constants import Paths
from src.constants import Labels
import src.io_utils as io_utils

def add(paper):
    io_utils.write_abstract(paper)

def add_paper_to_label(paper, label):
    io_utils.append_label(label, paper)

def get_ids_from_label(label):
    label_ids = io_utils.read_label_ids(label)
    return label_ids

def get_latest_papers():
    latest_paper_ids= io_utils.read_label_ids(Labels.LATEST)
    latest_papers = [io_utils.read_paper(paper_list_elem["paper_id"]) for paper_list_elem in latest_paper_ids]
    return latest_papers

def update(paper, source_label, target_label):
    io_utils.append_label(target_label, paper)
    io_utils.remove_from_label(source_label, paper)

def all_abstracts():
    abstract_files_ids = io_utils.list_all_abstract_ids()
    papers = [io_utils.read_paper(abstract_id) for abstract_id in abstract_files_ids]
    return papers

def read_paper(paper_id):
    return io_utils.read_paper(paper_id)

def update_paper_label(paper, label):
    if label == Labels.NEGATIVE or label == Labels.UNREAD:
        io_utils.remove_from_label(Labels.UNLABELED, paper)
        io_utils.remove_from_label(Labels.LATEST, paper)
    elif label == Labels.READ:
        io_utils.remove_from_label(Labels.UNREAD, paper)
        io_utils.remove_from_label(Labels.UNLABELED, paper)
        io_utils.remove_from_label(Labels.LATEST, paper)
    io_utils.append_label(label, paper)

