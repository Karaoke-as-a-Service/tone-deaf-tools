#!/usr/bin/env python3

import argparse
import sys

from _utils import get_attribute

HELP = """
For a list of ultrastar text files, read an attribute like #VIDEO and print
its value. Files without the attribute are ignored. Only accepts UTF-8 encoded
files.
"""


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("attribute")
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "--no-filename",
        action="store_true",
        help="just print the value, not the file path.",
    )
    args = parser.parse_args(argv)

    for path in args.files:
        with open(path) as f:
            try:
                value = get_attribute(f.read(), args.attribute)
            except KeyError:
                continue

            if args.no_filename:
                print(f"{value}")
            else:
                print(f"{value}\t{path}")


if __name__ == "__main__":
    main(sys.argv[1:])
