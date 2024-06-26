#!/usr/bin/env python3

import argparse
import re
import sys
import traceback

from icu import LocaleData
from langdetect import detect

from _utils import find_decodings, get_artisttitle, get_lyrics

HELP = """
Try to find the correct encoding for a given ultrastar text file. Tries to
determine which language a song is written in, get the alphabet for that
language and find the encoding, that produces the fewest non-alphabet
characters. Does not work well for multi-language songs.
Changes the file in place.
"""

non_ascii = re.compile("[^a-zA-Z0-9\"',. !?~\n\r*: #&_()\\[\\]-]")


def guess_lyric_language(text, remove_non_ascii=True):
    lyrics = get_lyrics(text)

    if remove_non_ascii:
        ascii_lyrics = ""

        for line in lyrics:
            if line in ascii_lyrics:
                continue
            if not non_ascii.search(line):
                ascii_lyrics += line + " "

        if not ascii_lyrics:
            raise Exception("no ascii-only lyrics found")

        ascii_lyrics = ascii_lyrics.replace("~", " ")
        lyrics = ascii_lyrics
    else:
        lyrics = " ".join(lyrics)

    return detect(lyrics)


def get_anti_alphabet(language):
    data = LocaleData(language)
    alphabet = data.getExemplarSet()
    return re.compile(
        "[^" + "".join(alphabet) + "0-9\"',. !?&~\n\r*: #_()\\[\\]…-]", re.IGNORECASE
    )


def guess_encoding(content, anti_alphabet, verbose=False):
    best = None
    best_count = len(content) * 2

    for encoding, text in find_decodings(content):
        lyrics = " ".join(get_lyrics(text))
        metadata = get_artisttitle(text)

        non_alphabet_chars = set(
            anti_alphabet.findall(lyrics) + anti_alphabet.findall(metadata)
        )
        non_alphabet_count = len(non_alphabet_chars)

        if verbose:
            print(encoding, non_alphabet_chars, lyrics)

        if non_alphabet_count < best_count:
            best = encoding
            best_count = non_alphabet_count

    if not best:
        raise Exception("could not find encoding")

    return best


def fix_encoding(path, dry_run=False, verbose=False):
    with open(path, "rb") as f:
        content = f.read()

    try:
        text = next(find_decodings(content))[1]
    except StopIteration:
        print(f"ERROR\tcoult not find encoding\t{path}")
        return

    try:
        language = guess_lyric_language(text)
        anti_alphabet = get_anti_alphabet(language)
        encoding = guess_encoding(content, anti_alphabet, verbose)
        content = content.decode(encoding)

        if encoding not in ("ascii", "utf_8") and not dry_run:
            with open(path, "w") as f:
                f.write(content)
    except Exception as ex:
        print(f"ERROR\t{ex}\t{path}")
        raise

    print(f"SUCCESS\t{language}/{encoding}\t{path}")


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="just find the encoding, do not change the file.",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    for path in args.files:
        try:
            fix_encoding(path, args.dry_run, args.verbose)
        except Exception as ex:
            traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])
