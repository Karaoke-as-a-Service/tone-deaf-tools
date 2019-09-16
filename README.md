# USDX Tools

A collection of scripts to mass-edit ultrastar deluxe text files, which are also
used by performous and others. See the list below for details. All scripts are
written with plugabiltiy in mind, so you can import them from other python
programs. There is no packaging or proper module, though.

Many of these scripts are write-and-forget - we needed them, wrote them, ran
them and forgot about them. Even though the code quality is not up to most
standards, they might still be useful to you. Have fun and send us fixes! ;)

## Tools

### update_readme.py

```console
$ ./update_readme.py --help
usage: update_readme.py [-h] [--readme-path README_PATH]

For maintainer use only. Get the --help of all .py files in the current
directory and add them to the given README markdown file, starting at "##
Tools". Ignores scripts whose name starts with an underscore and scripts that
don't exit with 0, when called with --help.

optional arguments:
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

optional arguments:
  -h, --help  show this help message and exit
  --dry-run   just find the encoding, do not change the file.

```

### recode_language.py

```console
$ ./recode_language.py --help
usage: recode_language.py [-h] [--dry-run] files [files ...]

Try to find the correct encoding for a given ultrastar text file. Tries to
determine which language a song is written in, get the alphabet for that
language and find the encoding, that produces the fewest non-alphabet
characters. Does not work well for multi-language songs. Changes the file in
place.

positional arguments:
  files

optional arguments:
  -h, --help  show this help message and exit
  --dry-run   just find the encoding, do not change the file.

```

### debug_encoding.py

```console
$ ./debug_encoding.py --help
usage: debug_encoding.py [-h] file

View the given file in all encodings supported by python, while highliting all
non-ascii characters. This tool can be used to manually figure out, which
encoding should be used to decode a file. Displays 3 encodings side-by-side.
If two encodings produce the same output, only the first one is shown.
Navigate with LEFT/RIGHT, remove the middle candiate using SPACE.

positional arguments:
  file

optional arguments:
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

optional arguments:
  -h, --help  show this help message and exit

```
