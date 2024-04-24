#!/usr/bin/env python3

import argparse
import json.decoder
import re
import sys

import requests

from _utils import find_decodings, get_artisttitle, get_lyrics

HELP = """
Experimental and probably not what you want. Try to find the correct encoding
for a given ultrastar text file. Extracts a part of the lyrics, and put it into
a lyric search engine for all supported encodings. Decode using the encoding
with the most results. Changes the file in place.
"""

non_ascii = re.compile("[^a-zA-Z0-9,. !?-]")


def count_results(lyrics):
    response = requests.get("https://songsear.ch/api/search", {"q": lyrics})

    try:
        data = response.json()
        return data["total"]
    except KeyError:
        raise Exception("API error: " + data["error"])
    except json.decoder.JSONDecodeError:
        raise Exception("Unexpected API response: " + response.content.decode())


def guess_encoding(content):
    best = "ascii"
    best_count = 0

    for encoding, text in find_decodings(content):
        artisttitle = get_artisttitle(text)
        lyrics = get_lyrics(text)

        non_ascii_lyrics = ""

        for line in lyrics:
            if line in non_ascii_lyrics:
                continue
            if non_ascii.search(line):
                for word in line.split():
                    if len(non_ascii_lyrics) + len(word) < 200:
                        non_ascii_lyrics += word + " "

        if non_ascii_lyrics:
            search_string = non_ascii_lyrics
        elif non_ascii.search(artisttitle):
            search_string = artisttitle

        if not search_string:
            continue

        results = count_results(search_string)

        if results > best_count:
            best = encoding
            best_count = results

    return best


def fix_encoding(path, dry_run=False):
    with open(path, "rb") as f:
        content = f.read()

    encoding = guess_encoding(content)
    content = content.decode(encoding)

    print(encoding)

    if not dry_run:
        with open(path, "w") as f:
            f.write(content)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="just find the encoding, do not change the file.",
    )
    args = parser.parse_args(argv)

    for path in args.files:
        fix_encoding(path)


if __name__ == "__main__":
    main(sys.argv[1:])
