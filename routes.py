from flask import Flask, request, render_template
import main
from cache import cache

app = Flask(__name__, template_folder="templates", static_url_path="")

@app.route("/latest", methods=["GET", "POST"])
def latest():
    if request.method == "POST":
        post_dict = request.form.to_dict()
        label = post_dict["label"]
        paper_id = post_dict["paper_id"]

        main.annotate("latest", paper_id, label)
        cache.remove("latest", paper_id)

    latest = main.latest()
    return render_template("latest.html", papers=latest[:20])

keywords = ""
@app.route("/annotate", methods=["GET", "POST"])
def annotate():
    if request.method == "POST":
        post_dict = request.form.to_dict()

        label = post_dict["label"]
        paper_id = post_dict["paper_id"]
        main.annotate("unlabeled", paper_id, label)
        annotate_cache = [paper for paper in annotate_cache if paper_id != paper["id"]]
    elif "keywords" in request.args:
        keywords = request.args["keywords"]
        annotate_cache = main.search_unlabeled(keywords)
    else:
        annotate_cache = main.read_unlabeled()

    return render_template("annotate.html", papers=annotate_cache[:10])

@app.route("/train", methods=["POST", "GET"])
def train():
    if request.method == "POST":
        main.train()
    return render_template("train.html")

@app.route("/suggestions", methods=["POST", "GET"])
def suggestions():
    if request.method == "POST":
        post_dict = request.form.to_dict()
        label = post_dict["label"]
        paper_id = post_dict["paper_id"]

        main.annotate("unlabeled", paper_id, label)

        cache.remove("suggestions", paper_id)

    suggestions = main.suggestions()

    return render_template("suggestions.html", papers=suggestions[:10])
