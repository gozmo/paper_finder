from src.constants import Paths
from src.constants import Labels
from src.io_utils import write_abstract
from src.io_utils import append_label
from src.io_utils import read_paper
from src.io_utils import read_label_ids 

def add(paper):
    write_abstract(paper)

def add_paper_to_label(paper, label):
    append_label(label, paper)

def move(paper_id, source_label, target_label):
    source_label_ids = io_utils.read_label_ids(source_label)
    target_label_ids = io_utils.read_label_ids(target_label)


def get_label(label):
    return io_utils.read_label_ids(source_label)

def get_abstract(paper_id):
    return io_utils.read_paper(paper_id)

def get_unread_papers():
    unread_paper_ids= io_utils.read_label_ids(Labels.UNREAD)
    unread_papers = [io_utils.read_paper(paper_id) for paper_id in unread_paper_ids]
    return unread_papers

def get_read_papers():
    read_paper_ids= io_utils.read_label_ids(Labels.READ)
    read_papers = [io_utils.read_paper(paper_id) for paper_id in read_paper_ids]
    return read_papers

def get_latest_papers():
    latest_paper_ids= read_label_ids(Labels.LATEST)
    latest_papers = [read_paper(paper_list_elem["paper_id"]) for paper_list_elem in latest_paper_ids]
    return latest_papers
