#!/usr/bin/env python3

import argparse
import sys

from _utils import get_attribut_names

HELP = """
For a list of ultrastar text files, find all attribute names and print them.
"""


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "--no-filename",
        action="store_true",
        help="just print the name, not the file path.",
    )
    args = parser.parse_args(argv)

    for path in args.files:
        with open(path) as f:
            text = f.read()
            attrs = get_attribut_names(text)

            if args.no_filename:
                print("\n".join(attrs))
            else:
                print("\n".join(f"{attr}\t{path}" for attr in attrs))


if __name__ == "__main__":
    main(sys.argv[1:])
