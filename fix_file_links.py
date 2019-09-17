#!/usr/bin/env python3

import sys
import shutil
import os
import argparse

from _utils import set_attribute, get_attribute, get_artisttitle

HELP = '''
Try to fix file links in #COVER, #MP3, #VIDEO and #BACKGROUND, which do not
resolve correctly, due to differing encodings of filenames on the disk and in
the attributes. Once the correct files have been found, rename them to
"<artist> - <song>.<extension>", update the attributes and rewrite the file
in-place. Remove any attributes, which cannot be resolved. Expects the text
files to be in the same directory as the media files. Only accepts UTF-8 encoded
text files.
'''

def force_ascii(text):
    return text.encode('ascii', errors='ignore').decode()


def fix_file_links(path, dry_run=False):
    song_dir = os.path.dirname(path)
    song_files = os.listdir(song_dir)
    song_files = {force_ascii(s): s for s in song_files}

    with open(path) as f:
        text = f.read()

    try:
        artisttitle = get_artisttitle(text)
    except KeyError:
        return

    print(path)

    new_path = song_dir + '/' + artisttitle + '.txt'
    if new_path != path:
        print(f'rename {new_path}')

        if not dry_run:
            os.rename(path, new_path)

    lines = text.splitlines(True)

    for attr in ('MP3', 'VIDEO', 'COVER', 'BACKGROUND'):
        try:
            attr_path = get_attribute(text, attr)
            attr_path_ascii = force_ascii(attr_path)
        except KeyError:
            continue

        if attr_path == attr_path_ascii:
            print(f"ignore {attr}, ascii")
            continue

        candidates = [
            original
            for ascii, original in song_files.items()
            if ascii.lower() == attr_path_ascii.lower()
        ]

        if not candidates:
            print(f"remove {attr}, no file found")
            lines = set_attribute(lines, attr, None)
            continue

        old_attr_name = candidates[0]
        attr_ext = os.path.splitext(old_attr_name)[1]
        new_attr_name = artisttitle + ' ' + attr + attr_ext
        new_attr_path = song_dir + '/' + new_attr_name

        if old_attr_name == new_attr_name:
            print(f"ignore {attr}, no change")
            continue

        print(f"rewrite {attr}: {old_attr_name} => {new_attr_name}")

        if not dry_run:
            os.rename(song_dir + '/' + old_attr_name, new_attr_path)
        lines = set_attribute(lines, attr, new_attr_name)

    if not dry_run:
        with open(path, 'w') as f:
            f.writelines(lines)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('files', nargs='+')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)

    for path in args.files:
        fix_file_links(path, args.dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
