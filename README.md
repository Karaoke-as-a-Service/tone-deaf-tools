# USDX Tools

A collection of scripts to mass-edit ultrastar deluxe text files, which are also
used by performous and others. See the list below for details. All scripts are
written with plugabiltiy in mind, so you can import them from other python
programs. There is no packaging or proper module, though.

Many of these scripts are write-and-forget - we needed them, wrote them, ran
them and forgot about them. Even though the code quality is not up to most
standards, they might still be useful to you. Have fun and send us fixes! ;)

## Typical Workflows

All of the tools read files from your disk, do something with them and, if
applicable, write changed content back to the disk, into th same file. If they
write, they also provid a `--dry-run` to disable that step. All commands support
a list of files as command line arguments, so you can process multiple files
easily.

To run a command on all of your files, you can use `find(1)` or a combination
of `find(1)` and `xargs(1)` for better performance:

* `find songs -type f -name '*.txt' -exec python script.py "{}" \;`
* `find songs -type f -name '*.txt' -print0 | xargs -0 -P8 -n10 python`

### Unknown Encoding

Scenario: you are given a library of usdx files in unknown, mixed encodings. In
order to edit the files with standard tools and display them properly in
ultrastar, you'd like to convert all of them to UTF-8.

Run the following commands on each of your files:

1. run `normalize_line_endings.py`
2. run `recode_language.py`
3. Have a good look at your files, by inspecting any non-ascii characters. Use
   `debug_encoding.py`, if in doubt. You can use `iconv(1)` to convert the files
   to a different encoding. Pass the original, untouched file. Note that iconv
   names for encodings might be slightly different, consult `iconv -l`.
4. run `fix_file_links.py`
5. run `find_unlinked_files.py` (not yet implemented)

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
