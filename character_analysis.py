#!/usr/bin/env python3

import argparse
import sys
import re
from collections import Counter

from _utils import get_artisttitle, get_lyrics


HELP='''
For a list of files, collect all characters in artist, title and lyrics. Print
the count of each character, the filename as well as the artist/title. This can
be helpful to determine, if a file has been recoded correctly. For example,
seeing ³, 文 or ╣ in a polish song suggests a problem.
'''


def count_characters(text):
    artisttitle = get_artisttitle(text)
    lyrics = get_lyrics(text)
    return Counter(f'{artisttitle}{lyrics}')


def print_character_frequencies(path, ignore_chars):
    try:
        with open(path) as f:
            text = f.read()

        artisttitle = get_artisttitle(text)
        frequencies = count_characters(text)
        del frequencies[' ']
    except Exception as ex:
        print(path)
        raise

    print(
        '\n'.join(
            f'{char} {count}'
            for char, count in sorted(frequencies.items(), key=lambda x: -x[1])
            if not ignore_chars.match(char)
        )
    )
    print(path)
    print(artisttitle)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('files', nargs='+')
    parser.add_argument('--ignore-chars', default='', help='letters or symbols to skip during analysis, as a regex character class. passing "qwerty" ignores q, w, e, ...')
    args = parser.parse_args(argv)

    ignore_chars = re.compile(f'^[{args.ignore_chars}]$')

    for path in args.files:
        print_character_frequencies(path, ignore_chars)



if __name__ == '__main__':
    main(sys.argv[1:])
