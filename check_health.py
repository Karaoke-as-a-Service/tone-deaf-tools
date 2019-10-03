#!/usr/bin/env python3

import argparse
import sys
import os

from _utils import get_attribute, get_attribut_names

HELP = '''
For each given file, check the following conditions. Exit with exit-code 1, if at least one is not met.
'''


checks = []


def check(description):
    def inner(func):
        checks.append((description, func))
    return inner


def required_attribute(attr):
    @check(f'Attribute {attr} must be present')
    def has_attr(text, path):
        try:
            if not get_attribute(text, attr):
                yield f'attribute {attr} empty'
        except KeyError:
            yield f'attribute {attr} missing'


def file_exists(attr):
    @check(f'File referenced in {attr} must exist, if present')
    def file_exists(text, path):
        try:
            songdir = os.path.dirname(path)
            attr_path = get_attribute(text, attr)
            if not os.path.isfile(os.path.join(songdir, attr_path)):
                yield f'file referenced in attribute {attr} not found: {attr_path}'
        except KeyError:
            pass

required_attribute('MP3')
required_attribute('TITLE')
required_attribute('ARTIST')
required_attribute('LANGUAGE')

file_exists('MP3')
file_exists('COVER')
file_exists('VIDEO')
file_exists('BACKGROUND')


@check(f'Must have BACKGROUND or VIDEO')
def has_background_or_video(text, path):
    attrs = get_attribut_names(text)

    if 'BACKGROUND' not in attrs and 'VIDEO' not in attrs:
        yield f'has neither BACKGROUND nor VIDEO'


@check('All attribute names must be UPPERCASE')
def lower_case_attribute(text, path):
    for attr in get_attribut_names(text):
        if any(c.islower() for c in attr):
            yield f'attribute {attr} is lower case'


@check('There is an E line')
def lower_case_attribute(text, path):
    if '\nE\n' not in text:
        yield 'there is no E line'


def check_health(path, only_check):

    try:
        with open(path) as f:
            text = f.read()
    except UnicodeDecodeError:
        return ['not utf-8/ascii encoded.']

    problems = []

    for description, check in checks:
        if only_check and description not in only_check:
            continue
        problems.extend(check(text, path))

    return problems


def main(argv):
    found_problems = False

    description = HELP.strip() + '\n\n'
    description += ' File is utf-8/ascii'
    description += '\n' + '\n'.join(' ' + c[0] for c in checks)

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--only-check', action='append', help='restrict checking to the given ones. encoding is always checked.')
    parser.add_argument('files', nargs='+')

    args = parser.parse_args(argv)

    for path in args.files:
        problems = check_health(path, args.only_check)
        if problems:
            print(path)
            print('\n'.join('  ' + p for p in problems))
            found_problems = True

    return 0 if not found_problems else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
