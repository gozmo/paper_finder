from bs4 import BeautifulSoup
import urllib
import pudb
import re
import os
import json
from tqdm import tqdm

base_url = "http://proceedings.mlr.press/"

root_page = urllib.request.urlopen(base_url).read()
root_html = BeautifulSoup(root_page, features="html.parser")

all_a = [a.get("href") for a in root_html.find_all("a") if "Volume" in a.text]
pu.db

for a in tqdm(all_a, desc="Volumes"):
    volume_url = base_url + a
    volume_page = urllib.request.urlopen(volume_url)
    volume_html = BeautifulSoup(volume_page, features="html.parser")
    volume_as = [volume_a.get("href") for volume_a in volume_html.findAll("a") if "abs" in volume_a.text]
    for volume_a in tqdm(volume_as, desc="papers"):
        paper_page = urllib.request.urlopen(volume_a)
        paper_html = BeautifulSoup(paper_page, features="html.parser")

        metas = paper_html.find_all("meta")
        authors = []

        for meta in metas:
            if meta.get("name") == "citation_title":
                title = meta.get("content")
            elif meta.get("name") == "citation_title":
                title = meta.get("content")
            elif meta.get("name") == "citation_pdf_url":
                pdf_link = meta.get("content")
            elif meta.get("name") == "citation_author":
                authors.append(meta.get("content"))

        divs = [div for div in paper_html.find_all("div") if div.get("id") == "abstract"]
        abstract = divs[0].text
        url = urllib.parse.urlparse(volume_a)
        filename = os.path.basename(url.path)
        paper_id = filename.replace(".html", "")

        paper_dict = {"summary" : abstract,
                      "title" : title,
                      "pdf_link" : pdf_link,
                      "link": volume_a,
                      "score": 0,
                      "paper_id": paper_id}
        abstract_file = f"abstracts/{paper_id}.json"
        with open(abstract_file, "w") as f:
            json.dump(paper_dict, f)






