#!/usr/bin/env python

import argparse
import re
import sys
import traceback

from _utils import get_lyrics

HELP = """
Try to fix the mojibake found in the 2024 CAMP23 collection. It contains many
'Korean' characters like 큄 which are actually Czech characters like š. This
script uses a simple mapping table to concert wrong into right characters. The
original file is then replaces with a fixed version. Run with --dry-run to just
print the broken characters. You may extend the mapping by adding entries to
the char_map line of this script. Be careful to keep the encoding of the script
as UTF-8.
"""

char_map = str.maketrans(
    {
        "큄": "š",
        "처": "ó",
        "챕": "é",
        "챌": "ç",
        "찾": "ã",
        "첵": "ý",
        "챠": "í",
        "큄": "š",
        "찼": "á",
        "탑": "Ž",
        "흫": "ň",
        "찼": "á",
        "휁": "ď",
        "척": "ô",
        "첬": "ú",
        "컁": "ľ",
        "첬": "ú",
        "챕": "é",
        "훾": "Č",
        "큐": "ť",
        "흦": "ń",
        "철": "ö",
        "첫": "ù",
        "챘": "ë",
        "혻": "é",
        "훳": "ą",
        "탉": "ż",
        "탄": "ź",
        "휌": "ę",
        "챵": "ò",
        "횪": "à",
        "체": "ü",
        "횩": "ß",
        "채": "ä",
        "횥": "Ü",
        "체": "ü",
        "횉": "Ç",
        "횙": "Ó",
        "횒": "Í",
        "횁": "Á",
        "창": "â",
        "챕": "é",
        "챗": "ê",
        "청": "û",
    }
)

RE_KOREAN_CHARACTER = re.compile(r"[가-힣]")
RE_KOREAN_CHARACTER_WITH_CONTEXT = re.compile(r"[가-힣]")


def fix_2024_mojibake(path, dry_run):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        text = text.translate(char_map)
        unknown_chars = RE_KOREAN_CHARACTER.findall(text)
        print("unknown characters: " + " ".join(set(unknown_chars)))

    if not dry_run:
        with open(path, "w") as f:
            f.write(text)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    for path in args.files:
        try:
            fix_2024_mojibake(path, args.dry_run)
        except Exception as ex:
            traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])
