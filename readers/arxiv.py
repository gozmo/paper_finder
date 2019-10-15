import pudb
import feedparser
import urllib

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
            filename = temp.path.replace("/abs/","")
            paper = {"title": title,
                     "summary": summary,
                     "filename": filename,
                     "id": filename,
                     "link": link}
            papers.append(paper)
    return papers
