#!/usr/bin/env python3

import argparse
import sys
import os
from contextlib import suppress
import itertools

from _utils import get_attribute

HELP='''
Given a directory, look for all files non ultrastar text files, which are not
referenced in any VIDEO, MP3, COVER or BACKGROUND attribute. Print their names.
'''

ignored_files = {
    'thumbs.db',
    'license.txt',
    '.ds_store',
    'desktop.ini',
    'notes.xml',
    '.listing',
}


def list_files(path):
    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.lower() not in ignored_files:
                yield os.path.join(path, name)


def get_linked_files(txt_path):
    songdir = os.path.dirname(txt_path)

    try:
        with open(txt_path) as f:
            text = f.read()
    except UnicodeDecodeError:
        return

    if '#TITLE' in text:
        yield txt_path

    for attribute in ('VIDEO', 'MP3', 'COVER', 'BACKGROUND'):
        with suppress(KeyError):
            yield os.path.join(songdir, get_attribute(text, attribute))


def get_all_linked_files(paths):
    return itertools.chain(*(get_linked_files(path) for path in paths if path.endswith('.txt')))


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('directory')
    args = parser.parse_args(argv)

    all_files = set(list_files(args.directory))
    linked_files = set(get_all_linked_files(all_files))

    print('\n'.join(all_files - linked_files))


if __name__ == '__main__':
    main(sys.argv[1:])
