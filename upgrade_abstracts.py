import json
import os
import pudb
pu.db


dirpath = "/home/goz/Dropbox/paper_finder/abstracts/"


files = os.listdir(dirpath)

for abstract_file in files:
    path = os.path.join(dirpath, abstract_file)
    with open(path, "r") as f:
        paper = json.load(f)
    if "nips" in abstract_file:
        paper["pdf_link"] = paper["link"] + ".pdf"
        if "nips" not in paper["paper_id"]:
            paper["paper_id"] = "nips-" + paper["paper_id"] 
    else:
        paper["pdf_link"] = paper["link"].replace("abs","pdf")

    if "score" not in paper:
        paper["score"] = 0.0
    if "paper_link" in paper:
        del paper["paper_link"]
    if "filename" in paper:
        del paper["filename"]
    if "pdf_url" in paper:
        paper["pdf_link"] = paper["pdf_url"]
        del paper["pdf_url"]

    if "id" in paper:
        paper["paper_id"] = paper["id"]
        del paper["id"]

    with open(path, "w") as f:
        json.dump(paper, f)
