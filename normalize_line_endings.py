#!/usr/bin/env python3

import argparse
import sys

HELP = """
Read files, convert their line to end with just \\n
(no \\r\\n, \\r, ...) and write them again. Accepts all
line endings accepted by pythons str.splitlines, which
includes all classic combinations, as well as a few
unicode extras.
"""


def normalize_line_endings(path):
    with open(path, "rb") as f:
        content = f.read()
    with open(path, "wb") as f:
        f.writelines(l + b"\n" for l in content.splitlines())


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)

    for path in args.files:
        normalize_line_endings(path)


if __name__ == "__main__":
    main(sys.argv[1:])
