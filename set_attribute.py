#!/usr/bin/env python3

import argparse
import sys
from contextlib import suppress

from _utils import set_attribute, get_attribute

HELP='''
For a list of ultrastar text files, set an attribute like #VIDEO to the given
value. Prints the paths of all changed files. Only accepts UTF-8 encoded files.
'''


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('attribute')
    parser.add_argument('value')
    parser.add_argument('files', nargs='+')
    parser.add_argument('--search', help='only replace, if the old value matches')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)

    for path in args.files:
        with open(path) as f:
            text = f.read()
            try:
                value = get_attribute(text, args.attribute)
            except:
                value = None
            if args.search and value != args.search:
                continue
            if value == args.value:
                continue
            lines = set_attribute(text.splitlines(), args.attribute, args.value)

        if not args.dry_run:
            with open(path, 'w') as f:
                f.writelines(lines)

        print(path)

if __name__ == '__main__':
    main(sys.argv[1:])
