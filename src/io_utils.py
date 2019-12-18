import os
import json
import random
from tqdm import tqdm
import json
from src.constants import Paths
from src.constants import Labels
from src.paper import Paper

def get_label_path(label):
    if label == Labels.READ:
        target = Paths.READ
    elif label == Labels.UNREAD:
        target = Paths.UNREAD
    elif label == Labels.LATEST:
        target = Paths.LATEST
    elif label == Labels.NEGATIVE:
        target = Paths.NEGATIVE
    elif label == Labels.UNLABELED:
        target = Paths.UNLABELED
    return target

def read_paper(paper_id):
    paper_path = os.path.join(Paths.ABSTRACTS, paper_id + ".json")
    with open(paper_path, "r") as f:
        json_content = json.load(f)
    return Paper(**json_content)

def read_label_ids(label):
    target = get_label_path(label)

    if os.stat(target).st_size < 5:
        return []
    
    with open(target) as f:
        json_content = json.load(f)

    return json_content 

def write_label_ids(label, content):
    target = get_label_path(label)

    with open(target, "w") as f:
        json.dump(content, f)

def append_label(label, paper):
    content = read_label_ids(label)
    content.append(paper.to_list_elem())
    write_label_ids(label, content)


def write_abstract(paper):
    paper_path = os.path.join(Paths.ABSTRACTS, paper.paper_id + ".json")
    json_content = json.dumps(paper.to_dict())
    with open(paper_path, "w") as f:
        f.write(json_content)

def search(keyword_list):
    unlabeled = read_unlabeled()

    search_hits = []
    for paper in unlabeled:
        for keyword in keyword_list:
            if keyword in paper["summary"].lower():
                search_hits.append(paper)
    return search_hits 

def move(paper_id, label):
    pass
