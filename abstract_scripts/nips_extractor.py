from bs4 import BeautifulSoup
import urllib
import pudb
import re
import os
import json

base_url = "https://papers.nips.cc"
abstract_target = ""
def get_year_urls():
    global base_url
    print(base_url)
    with urllib.request.urlopen(base_url) as request:
        response = request.read()

    html = BeautifulSoup(response)
    all_a = html.findAll("a")
    urls = []
    
    for a in all_a:
        if "NIPS" in a.text and "Advances" in a.text:
            url = a.get("href")
            urls.append(url)
    return urls

def get_paper_urls(year):
    global base_url
    url = base_url + year
    year_html = urllib.request.urlopen(url).read()
    urls = []
    for a in BeautifulSoup(year_html).findAll("a"):
        if "paper" in a.get("href"):
            urls.append(a.get("href"))
    return urls

def write_to_file(summary):
    global abstract_target
    paper_id = summary["paper_id"]
    filename = f"nips-{paper_id}.json"
    target_path = os.path.join(abstract_target, filename)
    
    with open(target_path, "w") as f:
        json.dump(summary, f)

def get_summaries(paper_urls):
    global base_url
    summaries = []
    for paper_url in paper_urls:
        try:
            url = base_url + paper_url
            paper_html = urllib.request.urlopen(url).read()
            html = BeautifulSoup(paper_html)
            ps = html.findAll("p")
            abstract = ps[1].text
            title = html.findAll("h2")[0].text
            paper_id = re.search(r"[0-9]+", paper_url).group(0)

            json_blob = {"title": title,
                    "summary": abstract,
                    "paper_id": paper_id,
                    "pdf_url": url + ".pdf"
                    "score": 0.0,
                    "link": url}
            write_to_file(json_blob)
        except:
            print("failed: ", paper_url)


years = get_year_urls()
for year in years:
    paper_urls = get_paper_urls(year)
    summaries = get_summaries(paper_urls)

