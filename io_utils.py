import os
import json
import random
from tqdm import tqdm

from constants import Dir

def get_path(dir_name):
    home_dir = os.getenv("HOME")
    root_dir = os.path.join(home_dir, "Dropbox", "paper_finder")
    if dir_name == "unlabeled":
        return os.path.join(root_dir, "abstracts", "unlabeled")
    elif dir_name == "new":
        return os.path.join(root_dir, "abstracts", "new")
    elif dir_name == "read":
        return os.path.join(root_dir, "abstracts", "read")
    elif dir_name == "unread":
        return os.path.join(root_dir, "abstracts", "unread")
    elif dir_name == "negative":
        return os.path.join(root_dir, "abstracts", "negative")
    elif dir_name == "models":
        return os.path.join(root_dir, "models")

def write_new_papers(papers):
    root_dir = get_root_dir()
    target_dir = os.join.path(root_dir, "abstracts", "new")

    for paper in papers:
        paper_id = os.path.join(target_dir
                                paper["filename"] + ".json")
        json_content = json.dumps(paper)
        if not os.path.isfile(paper_id):
            with open(paper_id, "w") as f:
                f.write(json_content)


_unlabeled = []
def read_unlabeled():
    unlabeled_dir = get_path("unlabeled")
    files = os.listdir(unlabeled_dir)

    if len(_unlabeled) == 0:
        for paper_file in files:
            filepath = os.path.join(unlabeled_dir, paper_file)
            with open(filepath, "r") as f:
                paper_content = json.loads(f.read())
                _unlabeled.append(paper_content)


    return _unlabeled

def read_new():
    new_dir = get_dir("new")
    files = os.listdir(new_dir)

    new = list()
    for paper_file in files:
        filepath = os.path.join(new_dir, paper_file)
        with open(filepath, "r") as f:
            paper_content = json.loads(f.read())
            new.append(paper_content)

    return new

def search_unlabeled(keyword_list):
    unlabeled = read_unlabeled()

    search_hits = []
    for paper in unlabeled:
        for keyword in keyword_list:
            if keyword in paper["summary"].lower():
                search_hits.append(paper)
    return search_hits 

def get_filepath(paper_id):
    for dirname in ["new", "unlabeled", "negative", "unread", "read"]:
        dirpath = get_dir(dirname)
        files = [filename for filename in os.listdir(dirpath) if paper_id in filename]
        if 0 < len(files):
            return files[0]

def move(paper_id, label):
    paper_id = paper_id.replace('/','_')
    source_path = get_filepath(paper_id)
    target_path = os.path.join(get_dir(label), paper_id + ".json")
    os.rename(source_path, target_path)
