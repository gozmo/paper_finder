import os
import json
import random
from tqdm import tqdm

from constants import Dir

def write_latest_papers(papers):
    os.makedirs(os.path.join("data", "latest"), exist_ok=True)

    for paper in papers:
        paper_id = os.path.join("data",
                                "latest",
                                paper["filename"] + ".json")
        json_content = json.dumps(paper)
        if not os.path.isfile(paper_id):
            with open(paper_id, "w") as f:
                f.write(json_content)


_unlabeled = []
def read_unlabeled():
    files = os.listdir("data/unlabeled")

    if len(_unlabeled) == 0:
        for paper_file in files:
            filepath = os.path.join("data/unlabeled", paper_file)
            with open(filepath, "r") as f:
                paper_content = json.loads(f.read())
                _unlabeled.append(paper_content)


    return _unlabeled

def read_latest():
    files = os.listdir("data/latest")

    latest = list()
    for paper_file in files:
        filepath = os.path.join("data/latest", paper_file)
        with open(filepath, "r") as f:
            paper_content = json.loads(f.read())
            latest.append(paper_content)

    return latest

def search_unlabeled(keyword_list):
    unlabeled = read_unlabeled()

    search_hits = []
    for paper in unlabeled:
        for keyword in keyword_list:
            if keyword in paper["summary"].lower():
                search_hits.append(paper)
    return search_hits 


def move(source, paper_id, label):
    paper_id = paper_id.replace('/','_')
    source_path = os.path.join("data", source, paper_id + ".json")
    target_path = os.path.join(Dir.DATA, label, paper_id + ".json")
    os.rename(source_path, target_path)


