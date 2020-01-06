import argparse
import main
from src.constants import Labels
from colorama import Fore,Style

def display_papers(papers, num):
    for i, paper in enumerate(papers[:num]):
        if paper.score < 0.3:
            color = Fore.RED
        elif paper.score < 0.5:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN
        score_str = f"{color} {paper.score} {Style.RESET_ALL}"
        print(f"[{i}] {score_str}, {paper.title}")

def setup_annotation(subparser):
    subparser.add_argument("--negative", type=int, nargs="+",metavar="N")
    subparser.add_argument("--positive", type=int, nargs="+",metavar="N")
    subparser.add_argument("--show", type=int, nargs="+",metavar="N")
    subparser.add_argument("--download", type=int, nargs="+",metavar="N")
    subparser.add_argument("--read", type=int, nargs="+",metavar="N")
    subparser.add_argument("--unread", type=int, nargs="+",metavar="N")
    subparser.add_argument("--n", type=int, default=10)
    subparser.add_argument("--notes", type=int)

def annotate(args):
    return args.negative or args.positive or args.show or args.negative or args.read or args.unread

def handle_annotate(args):
    if args.negative and len(args.negative) > 0:
        main.annotate(args.cmd, args.negative, Labels.NEGATIVE )
    if args.positive and len(args.positive) > 0:
        main.annotate(args.cmd, args.positive, Labels.UNREAD)
    if args.read and len(args.read) > 0:
        main.annotate(args.cmd, args.read, Labels.READ)
    if args.unread and len(args.unread) > 0:
        main.annotate(args.cmd, args.unread, Labels.UNREAD)
    if args.show and len(args.show) > 0:
        main.show(args.cmd, args.show)

parser = argparse.ArgumentParser(description='Paper finder cli')

subparsers = parser.add_subparsers(dest="cmd")

#Latest
latest_parser = subparsers.add_parser("latest")
setup_annotation(latest_parser)
latest_parser.add_argument("--update", action="store_true")

#Train
train_parser = subparsers.add_parser("train")

#Sync
sync_parser = subparsers.add_parser("sync")
setup_annotation(sync_parser)

#Search
search_parser = subparsers.add_parser("search")
search_parser.add_argument("--keywords", type=str, nargs="+", metavar="N")
setup_annotation(search_parser)

#Suggestions
suggestion_parser = subparsers.add_parser("suggestions")
suggestion_parser.add_argument("--generate", action="store_true")
setup_annotation(suggestion_parser)

#Read
read_parser = subparsers.add_parser("read")
setup_annotation(read_parser)

#Unread
unread_parser = subparsers.add_parser("unread")
setup_annotation(unread_parser)

#Negative
negative_parser = subparsers.add_parser("negative")
setup_annotation(negative_parser)

args = parser.parse_args()
if args.cmd == "latest":

    if annotate(args):
        handle_annotate(args)
    elif args.update:
        latest_papers = main.latest_update()
        display_papers(latest_papers, args.n)
    else:
        latest_papers = main.show_latest()
        display_papers(latest_papers, args.n)

elif args.cmd == "train":
    main.train()

elif args.cmd == "search":
    if annotate(args):
        handle_annotate(args)
    elif args.keywords and 0 < len(args.keywords):
        keywords = args.keywords
        search_hits = main.search_keywords(keywords)
        display_papers(search_hits, args.n)
    else:
        search_hits = main.search_hits()
        display_papers(search_hits, args.n)

elif args.cmd == "sync":
    if annotate(args):
        handle_annotate(args)
    else:
        new_papers = main.sync_command()
        display_papers(new_papers, args.n)

elif args.cmd == "suggestions":
    if annotate(args):
        handle_annotate(args)
    elif args.generate:
        suggestions = main.generate_suggestions()
        display_papers(suggestions, args.n)
    else:
        suggestions = main.show_suggestions()
        display_papers(suggestions, args.n)

elif args.cmd == "read":
    if annotate(args):
        handle_annotate(args)
    else:
        read = main.show_read()
        display_papers(read, 40)
elif args.cmd == "unread":
    if annotate(args):
        handle_annotate(args)
    else:
        unread = main.show_unread()
        display_papers(unread, 40)

elif args.cmd == "negative":
    if annotate(args):
        handle_annotate(args)
    else:
        negative = main.show_negative()
        display_papers(negative, 20)
