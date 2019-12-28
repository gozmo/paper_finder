import pudb
import feedparser
import urllib
from src.paper import Paper

def read():
    pu.db
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
