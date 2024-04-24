#!/usr/bin/env python3

import argparse
import contextlib
import glob
import subprocess
import sys

HELP = """
For maintainer use only. Get the --help of all .py files in the current
directory and add them to the given README markdown file, starting at
"## Tools". Ignores scripts whose name starts with an underscore and scripts
that don't exit with 0, when called with --help.
"""


def get_readme_preface(path, stopline="## Tools"):
    preface = ""

    with open(path) as f:
        for l in f.readlines():
            preface += l

            if l.strip() == stopline:
                break

    return preface


def get_help_texts():
    for script in glob.glob("*.py"):
        if script.startswith("_"):
            continue

        with contextlib.suppress(subprocess.CalledProcessError):
            output = subprocess.check_output(f"./{script} --help", shell=True)
            yield script, output.decode()


def generate_tools_toc(help_texts):
    return "".join(f'* [{s}](#{s.replace(".", "")})\n' for s, _ in help_texts)


def generate_tools_markdown(help_texts):
    return "\n".join(
        f"""### {script}

```console
$ ./{script} --help
{help}
```
"""
        for script, help in help_texts
    )


def generate_readme(readme_path):
    readme_preface = get_readme_preface(readme_path)
    help_texts = list(get_help_texts())
    toc = generate_tools_toc(help_texts)
    tools_markdown = generate_tools_markdown(help_texts)

    markdown = readme_preface + "\n" + toc + "\n" + tools_markdown

    with open(readme_path, "w") as f:
        f.write(markdown)


def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument(
        "--readme-path", default="README.md", help="file to read and write to"
    )
    args = parser.parse_args(argv)

    generate_readme(args.readme_path)


if __name__ == "__main__":
    main(sys.argv[1:])
