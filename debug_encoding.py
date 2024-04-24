#!/usr/bin/env python3

import argparse
import sys
import re

import curses

from _builtinencodings import encodings


HELP='''
View the given file in all encodings supported by python, while highlighting all
non-ascii characters. This tool can be used to manually figure out, which
encoding should be used to decode a file. Pass the original file, which has not
been touched by recode_language.py and friends.

Displays 3 encodings side-by-side. If two encodings produce the same output,
only the first one is shown. Navigate with LEFT/RIGHT, remove the middle
candidate using SPACE.

Quit by pressing 'q'.
'''


nonascii = re.compile('[^a-zA-Z0-9#:~,._ -\[\]]')
KEY_SPACEBAR = 32


class Window():
    def __init__(self, y, x):
        self.height = 15
        self.width = 55
        self.win = curses.newwin(self.height, self.width, y, x)
        self.title = ''
        self.text = ''

    def set_title(self, title):
        self.title = title
        self.refresh()

    def set_text(self, text):
        self.text = text
        self.refresh()

    def refresh(self):
        self.win.clear()
        self.win.border()
        self.win.addstr(0, 1, self.title)

        y = 2
        for line in self.text.splitlines():
            line = line[:self.width - 2]
            self.win.addstr(y, 2, line)
            for x in (m.start() for m in nonascii.finditer(line)):
                self.win.chgat(y, 2 + x, 1, curses.color_pair(3))
            y += 1
            if y > self.height - 3:
                break

        self.win.refresh()


class Navigator():
    def __init__(self, items):
        self.last = Window(1, 1)
        self.now = Window(1, 1 + self.last.width + 2)
        self.next = Window(1, 1 + self.last.width + self.now.width + 4)

        self.pointer = 0
        self.items = [[i[0], i[1]] for i in items]

    def go_left(self):
        self.pointer -= 1
        self.pointer = max(self.pointer, 0)
        self.refresh()

    def go_right(self):
        self.pointer += 1
        self.pointer = min(self.pointer, len(self.items) - 1)
        self.refresh()

    def remove(self):
        if len(self.items) > 1:
            del self.items[self.pointer]
            self.pointer = min(self.pointer, len(self.items) - 1)

    @property
    def item_last(self):
        if self.pointer == 0:
            return '', '', None

        return self.items[self.pointer - 1]

    @property
    def item_now(self):
        return self.items[self.pointer]

    @property
    def item_next(self):
        if self.pointer == len(self.items) -1:
            return '', '', None

        return self.items[self.pointer + 1]

    def refresh(self):
        self.last.set_title(self.item_last[0])
        self.last.set_text(self.item_last[1])
        self.last.refresh()

        self.now.set_title(self.item_now[0])
        self.now.set_text(self.item_now[1])
        self.now.refresh()

        self.next.set_title(self.item_next[0])
        self.next.set_text(self.item_next[1])
        self.next.refresh()


def variants(content):
    seen = set()

    for enc in encodings:
        try:
            text = content.decode(enc)
        except:
            continue

        if text in seen:
            continue
        if '#' not in text:
            continue

        seen.add(text)

        text = text.replace('\0', '')  # null bytes confuse ncurses
        demo_lines = [l for l in text.splitlines() if nonascii.search(l)]

        yield enc, '\n'.join(demo_lines)


def run(stdscr, path):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(3, curses.COLOR_BLUE, -1)   # non-ascii char
    curses.curs_set(0)
    stdscr.refresh()

    with open(path, 'rb') as f:
        content = f.read()

    n = Navigator(list(variants(content)))
    n.refresh()

    while True:
        c = stdscr.getch()

        if c == curses.KEY_LEFT:
            n.go_left()
        elif c == curses.KEY_RIGHT:
            n.go_right()
        elif c == KEY_SPACEBAR:
            n.remove()
        elif c == ord('q'):
            break

        n.refresh()


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('file')
    args = parser.parse_args(argv)
    curses.wrapper(run, args.file)


if __name__ == '__main__':
    main(sys.argv[1:])
