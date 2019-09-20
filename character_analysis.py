#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

from _utils import get_artisttitle, get_lyrics


HELP='''
For a list of files, collect all characters in artist, title and lyrics. Print
the count of each character, the filename as well as the artist/title.
'''


def count_characters(text):
    artisttitle = get_artisttitle(text)
    lyrics = get_lyrics(text)
    return Counter(f'{artisttitle}{lyrics}')


def print_character_frequencies(path):
    with open(path) as f:
        text = f.read()

    print(path)

    artisttitle = get_artisttitle(text)
    frequencies = count_characters(text)
    del frequencies[' ']

    print('\n'.join(f'{char} {count}' for char, count in sorted(frequencies.items(), key=lambda x: -x[1])))
    print(path)
    print(artisttitle)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('files', nargs='+')
    args = parser.parse_args(argv)

    for path in args.files:
        print_character_frequencies(path)



if __name__ == '__main__':
    main(sys.argv[1:])
