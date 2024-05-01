#!/usr/bin/env python3

import argparse
import os
import sys
import traceback
from pathlib import Path

from _utils import get_attribute, set_attribute
from recode_language import guess_lyric_language

HELP = """
Try to find the correct language for a given ultrastar text file and sort its
directory into TARGET/language, e.g. TARGET/en.

$ guess_language.py sorted_songs songs/*/*.txt

moves to

    sorted_songs/en/xxx/something_english.txt
    sorted_songs/de/xxx/something_german.txt
    sorted_songs/es/xxx/something_spanish.txt
"""


def guess_language(path):
    with open(path) as f:
        text = f.read()

    try:
        language = guess_lyric_language(text)
        try:
            old_language = get_attribute(text, "LANGUAGE")
        except KeyError:
            old_language = None
        print(f"SUCCESS\t{old_language}\t{language}")
        return language
    except Exception as ex:
        print(f"ERROR\t{ex}\t{path}")
        raise


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("target")
    parser.add_argument("files", nargs="+")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="just find the encoding, do not change the file.",
    )
    args = parser.parse_args(argv)

    for path in args.files:
        print(path)
        try:
            language = guess_language(path)

            song_directory = Path(path).parent
            new_name = Path(args.target) / language / song_directory.name

            print(f"{song_directory} => {new_name}")
            if not args.dry_run:
                if not song_directory.exists():
                    print(f"WARNING directory vanished: {song_directory}")
                else:
                    os.renames(song_directory, new_name)
        except Exception as ex:
            traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])
