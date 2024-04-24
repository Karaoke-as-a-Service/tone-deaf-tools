#!/usr/bin/env python3

import argparse
import sys

from _utils import get_lyrics

HELP = """
For a list of ultrastar text files, parse the lyrics and dump them line-by-line.
"""


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)

    for path in args.files:
        with open(path) as f:
            lyrics = get_lyrics(f.read())
            print("\n".join(lyrics))


if __name__ == "__main__":
    main(sys.argv[1:])
