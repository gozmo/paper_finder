import argparse
from main import latest_update
from main import latest


parser = argparse.ArgumentParser(description='Paper finder cli')

subparsers = parser.add_subparsers(dest="cmd")

latest_parser = subparsers.add_parser("latest")
latest_parser.add_argument("--update", action="store_true")

args = parser.parse_args()


if args.update and args.cmd == "latest":
    latest_update()
elif args.cmd == "latest":
    latest()
