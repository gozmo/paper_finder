from bs4 import BeautifulSoup
import urllib
import pudb
import re
import os
import json
years = abstract_link_pattern = re.compile("/anthology/[A-Z][0-9]{2}-[0-9]{4}/")
pdf_pattern = re.compile(".*[A-Z][0-9]{2}-[0-9]{4}.pdf")

all_paper_urls = []
for year in range(1996, 2017).__reversed__():
    base_url = f"https://www.aclweb.org/anthology/events/emnlp-{year}/"
    print(base_url)
    with urllib.request.urlopen(base_url) as request:
        response = request.read()

    html = BeautifulSoup(response)
    all_a = html.findAll("a")
    paper_urls = [a.get("href") for a in all_a if abstract_link_pattern.match(a.get("href"))]
    all_paper_urls.extend(paper_urls)
    break

pu.db
for paper_url in all_paper_urls:
    try:
        paper_uri = "https://www.aclweb.org" + paper_url
        print(paper_uri)
        paper_response = urllib.request.urlopen(paper_uri).read()
        paper_html = BeautifulSoup(paper_response)
        title = [a for a in paper_html.findAll("h2") if a.get("id") == "title"][0].text
        summary = [d for d in paper_html.findAll("div") if "acl-abstract" in d.get("class")][0].text
        summary = summary.replace("Abstract", "")
        paper_id = paper_html.findAll("dd")[0].text
        pdf_url = [a.get("href") for a in paper_html.findAll("a") if pdf_pattern.match(a.get("href"))][0]

        json_blob = {"title": title,
                "summary": summary,
                "paper_id": paper_id,
                "pdf_link": pdf_url,
                "score": 0.0,
                "link": paper_uri}
        with open("abstracts/" + paper_id + ".json", "w") as f:
            json.dump(json_blob, f)
    except Exception as e:
        print("Failed:", paper_uri)
        print(e)






