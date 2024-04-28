#!/usr/bin/env python3

import argparse
import curses
import os
import re
import sys

from _curses_helpers import KEY_SPACEBAR, Window, re_nonascii

HELP = """
Integrate new songs into an existing collection. Given a MAIN collection and one
of NEW songs, for each song in the NEW collection try to determine, if the song
is missing in the MAIN collection.

For each song in NEW, this script offers you to

A) mark the song as "done" and do nothing
B) mark the song as "done" and copy it to MAIN
C) do nothing

Quit by pressing 'q'.
"""


class Desktop:
    def __init__(self):
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)

    def refresh(self):
        for w in self.windows:
            w.refresh()


class ListWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list = []

    def refresh(self):
        self.text = "\n".join(self.list) + "\n"
        return super().refresh()


def run(stdscr, collection_main, collection_new):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(3, curses.COLOR_BLUE, -1)  # non-ascii char
    curses.curs_set(0)
    stdscr.refresh()

    desktop = Desktop()

    files_main = os.listdir(collection_main)
    print(files_main)

    w_new = ListWindow(1, 20, 1, 30, "NEW")
    w_new.list = files_main
    desktop.add_window(w_new)

    w_main = ListWindow(1, 20, w_new.x + 2 + w_new.width, 30, "MAIN")
    desktop.add_window(w_main)

    desktop.refresh()

    while True:
        c = stdscr.getch()

        if c == KEY_SPACEBAR:
            pass
        elif c == ord("q"):
            break

        desktop.refresh()


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument("collection_main")
    parser.add_argument("collection_new")
    args = parser.parse_args(argv)
    curses.wrapper(run, args.collection_main, args.collection_new)


if __name__ == "__main__":
    main(sys.argv[1:])
