from bs4 import BeautifulSoup
import pudb
import feedparser
import urllib
from src.paper import Paper

def is_arxiv_id(paper_id):
    split = paper_id.split(".")
    return len(split[0]) == 4 and 5 <= len(split[1])

def download_paper_info(arxiv_id):
    base_url = f"http://www.arxiv.org/abs/{arxiv_id}"
    print("Downloading:", base_url)
    with urllib.request.urlopen(base_url) as request:
        response = request.read()

    html = BeautifulSoup(response)
    all_meta = html.findAll("meta")
    paper_kw = {"score": 0.0,
                "link": base_url}
    for meta in all_meta:
        if meta.get("property") == "og:title":
            paper_kw["title"] = meta.get("content")
        elif meta.get("property") == "og:description":
            paper_kw["summary"] = meta.get("content")
        elif meta.get("property") == "og:url":
            paper_kw["summary"] = meta.get("content")
        elif meta.get("name") == "citation_arxiv_id":
            paper_kw["paper_id"] = meta.get("content")
        elif meta.get("name") == "citation_pdf_url":
            paper_kw["pdf_link"] = meta.get("content")
    paper = Paper(**paper_kw)
    return paper

def read():
    rss_feed_ids = ["cs", "stat"]
    base_url = "http://export.arxiv.org/rss/"

    papers = []
    for feed_id in rss_feed_ids:
        feed_url = urllib.parse.urljoin(base_url, feed_id)

        posts = feedparser.parse(feed_url)

        for item in posts.entries:
            title = item.title
            summary = item.summary
            link = item.link
            temp = urllib.parse.urlparse(link)
            paper_id = temp.path.replace("/abs/","")
            paper_url = temp.path.replace("/abs/","/pdf/")
            paper = Paper(title, summary, 0.0, paper_id, link, paper_url)

            papers.append(paper)
    return papers
