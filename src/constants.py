from pathlib import Path


class Labels: 
    UNREAD = "unread"
    READ = "read"
    NEGATIVE = "negative"
    UNLABELED = "unlabeled"
    LATEST = "latest"

class Paths:
    HOME = str(Path.home())
    READ = f"{HOME}/Dropbox/paper_finder/read.json"
    UNREAD = f"{HOME}/Dropbox/paper_finder/unread.json"
    NEGATIVE = f"{HOME}/Dropbox/paper_finder/negative.json"
    UNLABELED = f"{HOME}/Dropbox/paper_finder/unlabeled.json"
    LATEST = f"{HOME}/Dropbox/paper_finder/latest.json"

    ABSTRACTS = f"{HOME}/Dropbox/paper_finder/abstracts/"

    PDF_READ= f"{HOME}/Dropbox/paper_finder/pdfs/read"
    PDF_UNREAD= f"{HOME}/Dropbox/paper_finder/pdfs/unread"

    BERT_MODEL = f"{HOME}/Dropbox/paper_finder/models/bert.pt"
    FFN_MODEL = f"{HOME}/Dropbox/paper_finder/models/ffn_model.pt"

    CACHE = f"{HOME}/Dropbox/paper_finder/cache.json"


DEVICE = "cpu"
