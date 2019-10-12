#!/usr/bin/env python3

import argparse
from contextlib import suppress
import requests
import os
import io
import sys
import traceback

from PIL import Image

from _utils import set_attribute, get_attribute, get_artisttitle

HELP='''
Try to find a cover image for given ultrastar text files online, download them,
set the #COVER attribute and rewrite the file. Does nothing, if there already
is a cover file. Prints the paths of all changed files. Only accepts UTF-8
encoded files.
'''


def get_cover_url(name, service):
    r = requests.get(f'https://{service}/api/search/multi', params={
        'per_page': '1',
        'q': name,
    })
    return r.json()['response']['sections'][0]['hits'][0]['result']['song_art_image_url']


def download_cover_file(artisttitle, service):
    try:
        cover_url = get_cover_url(os.path.basename(artisttitle), service)
    except:
        return None

    if 'default_cover_image' in cover_url:
        return None

    extension = os.path.splitext(cover_url)[1].partition('?')[0]
    return extension, requests.get(cover_url).content


def has_working_cover(songdir, text):
    with suppress(KeyError):
        if os.path.exists(songdir + '/' + get_attribute(text, 'COVER')):
            return True

    return False


def add_cover_to_song(path, force, service):
    songdir = os.path.dirname(path)

    with open(path) as f:
        text = f.read()

    if not force and has_working_cover(songdir, text):
        return

    artisttitle = get_artisttitle(text)
    extension, cover_content = download_cover_file(artisttitle, service)
    coverfile = 'cover' + extension
    coverpath = songdir + '/' + coverfile

    im = Image.open(io.BytesIO(cover_content))
    width, height = im.size
    ratio = width / height

    if ratio < 0.7 or ratio > 1.3:
        return

    with open(coverpath, 'wb') as f:
        f.write(cover_content)

    with open(path, 'w') as f:
        f.writelines(set_attribute(text.splitlines(), 'COVER', coverfile))

    print(path)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('service', help='name of the service to download covers from, a possible one ends with "enius.com"')
    parser.add_argument('files', nargs='+')
    parser.add_argument('--force', action='store_true', help='download a new cover regardless of an existing one; do not remove the old one.')
    args = parser.parse_args(argv)

    for path in args.files:
        try:
            add_cover_to_song(path, args.force, args.service)
        except Exception as ex:
            traceback.print_exc()


if __name__ == '__main__':
    main(sys.argv[1:])
