import argparse
import main

def display_papers(papers):
    papers = sorted(papers, key=lambda x: x.score)
    for i, paper in enumerate(papers[:10]):
        print(f"[{i}] {paper.title}")

def setup_annotation(subparser):
    subparser.add_argument("--negative", type=int, nargs="+",metavar="N")
    subparser.add_argument("--positive", type=int, nargs="+",metavar="N")
    subparser.add_argument("--show", type=int, nargs="+",metavar="N")

def annotate(args):
    return args.negative or args.positive or args.show

def handle_annotate(args):
    if args.negative and len(args.negative) > 0:
        main.annotate(args.cmd, args.negative, "negative")
    if args.positive and len(args.positive) > 0:
        main.annotate(args.cmd, args.positive, "unread")
    if args.show and len(args.show) > 0:
        main.show(args.cmd, args.show)

parser = argparse.ArgumentParser(description='Paper finder cli')

subparsers = parser.add_subparsers(dest="cmd")

latest_parser = subparsers.add_parser("latest")
latest_parser.add_argument("--update", action="store_true")
setup_annotation(latest_parser)

train_parser = subparsers.add_parser("train")

sync_parser = subparsers.add_parser("sync")

search_parser = subparsers.add_parser("search")
search_parser.add_argument("--keywords", type=str, nargs="+", metavar="N")
setup_annotation(search_parser)

args = parser.parse_args()

if args.cmd == "latest":
    if annotate(args):
        handle_annotate(args)
    elif args.update:
        latest_papers = main.latest_update()
        display_papers(latest_papers)
    else:
        latest_papers = main.latest()
        display_papers(latest_papers)

elif args.cmd == "train":
    main.train()

elif args.cmd == "search":
    if annotate(args):
        handle_annotate(args)
    elif 0 < len(args.keywords):
        keywords = args.keywords
        search_hits = main.search(keywords)
        display_papers(search_hits)

elif args.cmd == "sync":
    new_papers = main.sync()
    display_papers(new_papers)
