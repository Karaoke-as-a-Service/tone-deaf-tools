# USDX Tools

A collection of scripts to mass-edit ultrastar deluxe text files, which are also
used by performous and others. See the list below for details. All scripts are
written with pluggability in mind, so you can import them from other python
programs. There is no packaging or proper module, though.

When using potentially destructive scripts like `recode_language.py`, make a
backup of your files beforehand or work on a copy in the first place. Some tools
like `debug_encoding.py` also need the original.

Many of these scripts are write-and-forget - we needed them, wrote them, ran
them and forgot about them. Even though the code quality is not up to most
standards, they might still be useful to you. Have fun and send us fixes! ;)

If you want to experiment, put your files into the `songs` directory, which
is ignored by git.

## Setup

```console
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Typical Workflows

All of the tools read files from your disk, do something with them and, if
applicable, write changed content back to the disk, into the same file. If they
write, they also provide a `--dry-run` to disable that step. All commands support
a list of files as command line arguments, so you can process multiple files
easily.

To run a command on all of your files, you can use `find(1)` or a combination
of `find(1)` and `xargs(1)` for better performance:

* `find songs -type f -iname '*.txt' -exec python script.py "{}" \;`
* `find songs -type f -iname '*.txt' -print0 | xargs -0 -P8 -n10 python`

### Unknown Encoding

Scenario: you are given a library of usdx files in unknown, mixed encodings. In
order to edit the files with standard tools and display them properly in
ultrastar, you'd like to convert all of them to UTF-8.

Run the following commands on each of your files:

1. run `normalize_line_endings.py`
2. run `recode_language.py`
3. Have a good look at your files, by inspecting any non-ascii characters. Use
   `debug_encoding.py` on the original file, if in doubt. You can use `iconv(1)`
   to convert the files to a different encoding. Pass the original, untouched
   file. Note that iconv names for encodings might be slightly different,
   consult `iconv -l`.
4. run `fix_file_links.py`, prints multiple lines per file - so run it without
   parallelism (i.e. without `-P`, if you're using xargs).
5. run `find_unused_files.py`
6. on a case-by-case basis, try to fix the issues by deleting the files,
   ignoring them or adding the correct VIDEO/MP3/COVER/... attributes.
7. run `check_health.py`
8. on a case-by-case basis, try to fix the issues

### Normalize Language (or other attributes)

Scenario: your collection has mixed `#LANGUAGE` attributes like  "English",
"Englisch", "angielski" and so on. You'd like to have only "English".

1. run `./get_attribute.py LANGUAGE --no-filename (...) | sort | uniq` to get a
   list of used languages.
2. choose a wrong language name like "Englisch"
3. run `./set_attribute.py LANGUAGE English --search Anglais` to set the new
   name
4. repeat 2. & 3.

## Tools

* [update_readme.py](#update_readmepy)
* [recode_asktheweb.py](#recode_askthewebpy)
* [get_attribute.py](#get_attributepy)
* [guess_language.py](#guess_languagepy)
* [list_attributes.py](#list_attributespy)
* [integrate_collection.py](#integrate_collectionpy)
* [download_cover.py](#download_coverpy)
* [find_unused_files.py](#find_unused_filespy)
* [fix_2024_mojibake.py](#fix_2024_mojibakepy)
* [set_attribute.py](#set_attributepy)
* [check_health.py](#check_healthpy)
* [fix_file_links.py](#fix_file_linkspy)
* [recode_language.py](#recode_languagepy)
* [character_analysis.py](#character_analysispy)
* [get_lyrics.py](#get_lyricspy)
* [debug_encoding.py](#debug_encodingpy)
* [normalize_line_endings.py](#normalize_line_endingspy)

### update_readme.py

```console
$ ./update_readme.py --help
usage: update_readme.py [-h] [--readme-path README_PATH]

For maintainer use only. Get the --help of all .py files in the current
directory and add them to the given README markdown file, starting at "##
Tools". Ignores scripts whose name starts with an underscore and scripts that
don't exit with 0, when called with --help.

options:
  -h, --help            show this help message and exit
  --readme-path README_PATH
                        file to read and write to

```

### recode_asktheweb.py

```console
$ ./recode_asktheweb.py --help
usage: recode_asktheweb.py [-h] [--dry-run] files [files ...]

Experimental and probably not what you want. Try to find the correct encoding
for a given ultrastar text file. Extracts a part of the lyrics, and put it
into a lyric search engine for all supported encodings. Decode using the
encoding with the most results. Changes the file in place.

positional arguments:
  files

options:
  -h, --help  show this help message and exit
  --dry-run   just find the encoding, do not change the file.

```

### get_attribute.py

```console
$ ./get_attribute.py --help
usage: get_attribute.py [-h] [--no-filename] attribute files [files ...]

For a list of ultrastar text files, read an attribute like #VIDEO and print
its value. Files without the attribute are ignored. Only accepts UTF-8 encoded
files.

positional arguments:
  attribute
  files

options:
  -h, --help     show this help message and exit
  --no-filename  just print the value, not the file path.

```

### guess_language.py

```console
$ ./guess_language.py --help
usage: guess_language.py [-h] [--dry-run] target files [files ...]

Try to find the correct language for a given ultrastar text file and write it
to the file's #LANGUAGE tag.

positional arguments:
  target
  files

options:
  -h, --help  show this help message and exit
  --dry-run   just find the encoding, do not change the file.

```

### list_attributes.py

```console
$ ./list_attributes.py --help
usage: list_attributes.py [-h] [--no-filename] files [files ...]

For a list of ultrastar text files, find all attribute names and print them.

positional arguments:
  files

options:
  -h, --help     show this help message and exit
  --no-filename  just print the name, not the file path.

```

### integrate_collection.py

```console
$ ./integrate_collection.py --help
usage: integrate_collection.py [-h] [--dry-run] MAIN NEW SCORE_RANGE TARGET

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

positional arguments:
  MAIN
  NEW
  SCORE_RANGE
  TARGET

options:
  -h, --help   show this help message and exit
  --dry-run

```

### download_cover.py

```console
$ ./download_cover.py --help
usage: download_cover.py [-h] [--force] service files [files ...]

Try to find a cover image for given ultrastar text files online, download
them, set the #COVER attribute and rewrite the file. Does nothing, if there
already is a cover file. Prints the paths of all changed files. Only accepts
UTF-8 encoded files.

positional arguments:
  service     name of the service to download covers from, a possible one ends
              with "enius.com"
  files

options:
  -h, --help  show this help message and exit
  --force     download a new cover regardless of an existing one; do not
              remove the old one.

```

### find_unused_files.py

```console
$ ./find_unused_files.py --help
usage: find_unused_files.py [-h] directory

Given a directory, look for all files non ultrastar text files, which are not
referenced in any VIDEO, MP3, COVER or BACKGROUND attribute. Print their
names.

positional arguments:
  directory

options:
  -h, --help  show this help message and exit

```

### fix_2024_mojibake.py

```console
$ ./fix_2024_mojibake.py --help
usage: fix_2024_mojibake.py [-h] [--dry-run] files [files ...]

Try to fix the mojibake found in the 2024 CAMP23 collection. It contains many
'Korean' characters like 큄 which are actually Czech characters like š. This
script uses a simple mapping table to concert wrong into right characters. The
original file is then replaces with a fixed version. Run with --dry-run to
just print the broken characters. You may extend the mapping by adding entries
to the char_map line of this script. Be careful to keep the encoding of the
script as UTF-8.

positional arguments:
  files

options:
  -h, --help  show this help message and exit
  --dry-run

```

### set_attribute.py

```console
$ ./set_attribute.py --help
usage: set_attribute.py [-h] [--search SEARCH] [--dry-run]
                        attribute value files [files ...]

For a list of ultrastar text files, set an attribute like #VIDEO to the given
value. Prints the paths of all changed files. Only accepts UTF-8 encoded
files.

positional arguments:
  attribute
  value
  files

options:
  -h, --help       show this help message and exit
  --search SEARCH  only replace, if the old value matches
  --dry-run

```

### check_health.py

```console
$ ./check_health.py --help
usage: check_health.py [-h] [--only-check ONLY_CHECK] files [files ...]

For each given file, check the following conditions. Exit with exit-code 1, if at least one is not met.

 File is utf-8/ascii
 Attribute MP3 must be present
 Attribute TITLE must be present
 Attribute ARTIST must be present
 Attribute LANGUAGE must be present
 File referenced in MP3 must exist, if present
 File referenced in COVER must exist, if present
 File referenced in VIDEO must exist, if present
 File referenced in BACKGROUND must exist, if present
 COVER is an image file
 BACKGROUND is an image file
 Must have BACKGROUND or VIDEO
 All attribute names must be UPPERCASE
 There is an E line

positional arguments:
  files

options:
  -h, --help            show this help message and exit
  --only-check ONLY_CHECK
                        restrict checking to the given ones. encoding is always checked.

```

### fix_file_links.py

```console
$ ./fix_file_links.py --help
usage: fix_file_links.py [-h] [--keep-nullpointer-lines] [--dry-run]
                         [--verbose]
                         files [files ...]

Try to fix file links in #COVER, #MP3, #VIDEO and #BACKGROUND, which do not
resolve correctly, due to differing encodings of filenames on the disk and in
the attributes. Once the correct files have been found, rename them to
"<artist> - <song>.<extension>", update the attributes and rewrite the file
in-place. Remove any attributes, which cannot be resolved. Expects the text
files to be in the same directory as the media files. Only accepts UTF-8
encoded text files.

positional arguments:
  files

options:
  -h, --help            show this help message and exit
  --keep-nullpointer-lines
                        do not delete attributes, which reference non-existing
                        files
  --dry-run
  --verbose

```

### recode_language.py

```console
$ ./recode_language.py --help
usage: recode_language.py [-h] [--dry-run] [--verbose] files [files ...]

Try to find the correct encoding for a given ultrastar text file. Tries to
determine which language a song is written in, get the alphabet for that
language and find the encoding, that produces the fewest non-alphabet
characters. Does not work well for multi-language songs. Changes the file in
place.

positional arguments:
  files

options:
  -h, --help  show this help message and exit
  --dry-run   just find the encoding, do not change the file.
  --verbose

```

### character_analysis.py

```console
$ ./character_analysis.py --help
usage: character_analysis.py [-h] [--ignore-chars IGNORE_CHARS]
                             files [files ...]

For a list of files, collect all characters in artist, title and lyrics. Print
the count of each character, the filename as well as the artist/title. This
can be helpful to determine, if a file has been recoded correctly. For
example, seeing ³, 文 or ╣ in a polish song suggests a problem.

positional arguments:
  files

options:
  -h, --help            show this help message and exit
  --ignore-chars IGNORE_CHARS
                        letters or symbols to skip during analysis, as a regex
                        character class. passing "qwerty" ignores q, w, e, ...

```

### get_lyrics.py

```console
$ ./get_lyrics.py --help
usage: get_lyrics.py [-h] files [files ...]

For a list of ultrastar text files, parse the lyrics and dump them line-by-
line.

positional arguments:
  files

options:
  -h, --help  show this help message and exit

```

### debug_encoding.py

```console
$ ./debug_encoding.py --help
usage: debug_encoding.py [-h] file

View the given file in all encodings supported by python, while highlighting
all non-ascii characters. This tool can be used to manually figure out, which
encoding should be used to decode a file. Pass the original file, which has
not been touched by recode_language.py and friends. Displays 3 encodings side-
by-side. If two encodings produce the same output, only the first one is
shown. Navigate with LEFT/RIGHT, remove the middle candidate using SPACE. Quit
by pressing 'q'.

positional arguments:
  file

options:
  -h, --help  show this help message and exit

```

### normalize_line_endings.py

```console
$ ./normalize_line_endings.py --help
usage: normalize_line_endings.py [-h] files [files ...]

Read files, convert their line to end with just \n (no \r\n, \r, ...) and
write them again. Accepts all line endings accepted by pythons str.splitlines,
which includes all classic combinations, as well as a few unicode extras.

positional arguments:
  files

options:
  -h, --help  show this help message and exit

```
