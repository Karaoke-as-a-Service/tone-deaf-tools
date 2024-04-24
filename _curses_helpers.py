import curses
import re

re_nonascii = re.compile("[^a-zA-Z0-9#:~,._ -\[\]]")
KEY_SPACEBAR = 32


class Window:
    def __init__(self, y, x):
        self.height = 15
        self.width = 55
        self.win = curses.newwin(self.height, self.width, y, x)
        self.title = ""
        self.text = ""

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
            line = line[: self.width - 2]
            self.win.addstr(y, 2, line)
            for x in (m.start() for m in re_nonascii.finditer(line)):
                self.win.chgat(y, 2 + x, 1, curses.color_pair(3))
            y += 1
            if y > self.height - 3:
                break

        self.win.refresh()
