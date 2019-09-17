#!/usr/bin/env python3

import argparse
import sys
import re

from langdetect import detect
from icu import LocaleData

from _utils import find_decodings, get_artisttitle

HELP = '''
Try to find the correct encoding for a given ultrastar text file. Tries to
determine which language a song is written in, get the alphabet for that
language and find the encoding, that produces the fewest non-alphabet
characters. Does not work well for multi-language songs.
Changes the file in place.
'''

non_ascii = re.compile('[^a-zA-Z0-9"\',. !?~\n\r*: #&_()\\[\\]-]')


def get_lyrics(text):
    songline = ""

    for line in text.splitlines():
        if not line:
            continue
        if line[0] in (':', '*', 'F'):
            songline += line.split(' ', 4)[-1]
        if line[0] == '-':
            yield songline
            songline = ""

    if songline:
        yield songline


def guess_lyric_language(text):
    lyrics = get_lyrics(text)

    ascii_lyrics = ''

    for line in lyrics:
        if line in ascii_lyrics:
            continue
        if not non_ascii.search(line):
            ascii_lyrics += line + ' '

    if not ascii_lyrics:
        raise Exception('no ascii-only lyrics found')

    ascii_lyrics = ascii_lyrics.replace('~', ' ')

    return detect(ascii_lyrics)


def get_anti_alphabet(language):
    data = LocaleData(language)
    alphabet = data.getExemplarSet()
    return re.compile('[^' + ''.join(alphabet) + '0-9"\',. !?&~\n\r*: #_()\\[\\]…-]', re.IGNORECASE)


def guess_encoding(content, anti_alphabet):
    best = None
    best_count = len(content) * 2

    for encoding, text in find_decodings(content):
        lyrics = ' '.join(get_lyrics(text))
        metadata = get_artisttitle(text)

        non_alphabet_chars = set(anti_alphabet.findall(lyrics) + anti_alphabet.findall(metadata))
        non_alphabet_count = len(non_alphabet_chars)

        if non_alphabet_count < best_count:
            best = encoding
            best_count = non_alphabet_count

    if not best:
        raise Exception('could not find encoding')

    return best


def fix_encoding(path, dry_run=False):
    with open(path, 'rb') as f:
        content = f.read()

    try:
        text = next(find_decodings(content))[1]
    except StopIteration:
        return

    language = guess_lyric_language(text)
    anti_alphabet = get_anti_alphabet(language)
    encoding = guess_encoding(content, anti_alphabet)
    content = content.decode(encoding)

    print(language + '/' + encoding)

    if not dry_run:
        with open(path, 'w') as f:
            f.write(content)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('files', nargs='+')
    parser.add_argument('--dry-run', action='store_true', help='just find the encoding, do not change the file.')
    args = parser.parse_args(argv)

    for path in args.files:
        fix_encoding(path, args.dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
