#!/usr/bin/env python3

import re

from _builtinencodings import encodings


box_char = re.compile('[─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿]')


def find_decodings(content):
    seen = set()
    unlikely_encodings = []

    for encoding in encodings:
        try:
            text = content.decode(encoding)
        except ValueError:
            continue

        if text in seen:
            continue
        if '\n#' not in text:  # some encodings produce complete gibberish - skip them
            continue

        if box_char.findall(text):
            unlikely_encodings.append((encoding, text))
            continue

        yield encoding, text

    yield from unlikely_encodings



def get_attribute(text, attribute):
    try:
        return re.search('#' + attribute + ':(.*)', text).groups(1)[0]
    except AttributeError:
        raise KeyError()


def set_attribute(lines, attr, value):
    found = False
    for line in lines:
        if line.startswith(f'#{attr}:'):
            found = True
            if value is not None:
                yield f'#{attr}:{value}\n'
        else:
            line = line.strip('\n')
            if not found and not line.startswith('#'):
                found = True
                yield f'#{attr}:{value}\n'
            yield f'{line}\n'


def get_artisttitle(text):
    artist = get_attribute(text, 'ARTIST')
    title = get_attribute(text, 'TITLE')
    return artist + ' - ' + title
