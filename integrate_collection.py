#!/usr/bin/env python3

import argparse
import dataclasses
import functools
import glob
import math
import sys
from pathlib import Path

import Levenshtein

from _utils import get_attribut_names, get_attribute, get_number_of_singers

HELP = """
Integrate songs from a NEW collection into an existing MAIN collection. Each
song in NEW is scored from 0 to 100. If the score is within the given range,
the song is the moved to TARGET.

./integrate_collection.py my_collection new_songs 80-100 duplicate_songs
=> move all songs from new_songs with a score between 80 and 100 to duplicate_songs

./integrate_collection.py my_collection new_songs -50 unknown_songs
=> move all songs from new_songs with a score below 50 to unknown_songs

Score may be given as
  80-100 (=> 80 to 100)
    -50  (=> 0 to 50)
  80-    (=> 80 to 100)

Scoring cirteria:

* file matches byte-wise
* title matches
* title and artist match
* number of singers matches
* ... and many more
"""


class Song:
    path: Path
    text: str
    attributes: dict[str, str]

    def __init__(self, path):
        self.path = Path(path)
        self.text = Path(path).read_text("utf-8", errors="ignore").strip()
        # this is stupidly slow, but we don't have so many files
        self.attributes = {
            k: get_attribute(self.text, k).strip()
            for k in get_attribut_names(self.text)
        }

    @functools.cached_property
    def singers(self):
        return get_number_of_singers(self.text)

    @functools.cache
    def __getattr__(self, attr):
        return self.attributes.get(attr, None)

    def __repr__(self):
        return f"{self.ARTIST} - {self.TITLE}"

    def match(self, needle):
        if self.text == needle.text:
            return 100, ["TEXT"]

        lev_artist = lev(self.ARTIST, needle.ARTIST)
        lev_title = lev(self.TITLE, needle.TITLE)

        matchers = {
            "TITLE": (lambda: lev_title * (1 if lev_artist > 90 else 0.5)),
            "ARTIST": (lambda: 10 if lev_artist > 90 else 0),
            "SINGERS": (lambda: -100 if self.singers != needle.singers else 0),
        }

        matched_matchers = []
        score = 0

        for name, mfunc in matchers.items():
            mscore = mfunc()

            if mscore > 0:
                matched_matchers.append(name)
                score += mscore

        return score, matched_matchers


@functools.cache
def lev(a, b):
    if a is None or b is None:
        return 0

    remove = [
        "[video]",
        "(duett)",
        "-",
        ",",
        ".",
        "&",
        " ",
        "the",
    ]

    a = a.lower()
    b = b.lower()

    for r in remove:
        a = a.replace(r, "")
        b = b.replace(r, "")

    return int(Levenshtein.ratio(a, b) * 100)


class SongCollection:
    def __init__(self, root):
        self.root = Path(root)
        self.songs = []

    def load(self):
        if not self.root.exists():
            raise FileNotFoundError(self.root)

        for path in self.root.glob("**/*.txt"):
            self.songs.append(Song(path))

    def find_matches(self, needle):
        matched_songs = []

        for song in self.songs:
            score, matched_matchers = song.match(needle)

            if matched_matchers:
                matched_songs.append(
                    (song, int(max(min(score, 100), 0)), matched_matchers)
                )

        matched_songs.sort(key=(lambda s: s[1]), reverse=True)

        return matched_songs


def main(argv):
    parser = argparse.ArgumentParser(
        description=HELP, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("MAIN")
    parser.add_argument("NEW")
    parser.add_argument("SCORE_RANGE")
    parser.add_argument("TARGET")
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument(
        "--filter",
        help="only check songs in NEW that contain the given string in artist or title",
    )
    args = parser.parse_args(argv)

    score_min, sep, score_max = args.SCORE_RANGE.partition("-")
    if sep:
        score_min = int(score_min if score_min else 0)
        score_max = int(score_max if score_max else 100)
    else:
        score_min = score_max = int(score_min)

    col_main = SongCollection(args.MAIN)
    col_main.load()

    col_new = SongCollection(args.NEW)
    col_new.load()

    for n, song in enumerate(col_new.songs):
        if args.filter and args.filter.lower() not in str(song).lower():
            continue

        matches = col_main.find_matches(song)
        max_score = max([m[1] for m in matches] or [0])

        if not (score_min <= max_score <= score_max):
            continue

        if args.dry_run and matches:
            print()
            print(f"{n}/{len(col_new.songs)-1} {song}")
            for m in matches[:3]:
                print(f"=> {m}")

        if matches:
            song_directory = song.path.parent
            new_name = Path(args.TARGET) / song_directory.name

            print(f"{song_directory} => {new_name}")
            if not args.dry_run:
                song_directory.renames(new_name)


if __name__ == "__main__":
    main(sys.argv[1:])
