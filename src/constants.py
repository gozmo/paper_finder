from pathlib import Path

class Labels: 
    UNREAD = "unread"
    READ = "read"
    NEGATIVE = "negative"
    UNLABELED = "unlabeled"
    LATEST = "latest"

class Paths:
    HOME = str(Path.home())
    READ = f"{HOME}/Dropbox/paper_finder/read.txt"
    UNREAD = f"{HOME}/Dropbox/paper_finder/unread.txt"
    NEGATIVE = f"{HOME}/Dropbox/paper_finder/negative.txt"
    UNLABELED = f"{HOME}/Dropbox/paper_finder/unlabeled.txt"
    LATEST = f"{HOME}/Dropbox/paper_finder/latest.json"

    ABSTRACTS = f"{HOME}/Dropbox/paper_finder/abstracts/"

    PDFS_READ= f"{HOME}/Dropbox/paper_finder/pdfs/read"
    PDFS_UNREAD= f"{HOME}/Dropbox/paper_finder/pdfs/unread"

    BERT_MODEL = f"{HOME}/Dropbox/paper_finder/models/bert.pt"
    FFN_MODEL = f"{HOME}/Dropbox/paper_finder/models/ffn_model.pt"

DEVICE = "cpu"
