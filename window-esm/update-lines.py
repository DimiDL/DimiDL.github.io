#!/usr/bin/env python3
"""Refresh the `lines` field of every item in data.json from a gecko checkout.

Usage:
    update-lines.py /path/to/gecko [--rev origin/bookmarks/central]

With --rev, files are read with `git show REV:path`, so the checkout does not
need to be updated. A whole-file item counts every line of the file. An item
with an `object` counts the lines of that object's top-level definition, from
its `var NAME =` or `defineLazyGetter(this, "NAME"` line through the first
following line that starts with `}`.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data.json"


def read_source(gecko, rev, path):
    if rev:
        return subprocess.run(
            ["git", "-C", gecko, "show", f"{rev}:{path}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    return (Path(gecko) / path).read_text()


def object_span(lines, name):
    start = re.compile(
        rf'^(?:var|let|const)\s+{re.escape(name)}\b'
        rf'|^ChromeUtils\.defineLazyGetter\(this,\s*"{re.escape(name)}"'
    )
    for i, line in enumerate(lines):
        if start.match(line):
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("}"):
                    return j - i + 1
            break
    raise LookupError(name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gecko")
    parser.add_argument("--rev")
    args = parser.parse_args()

    data = json.loads(DATA.read_text())
    cache = {}
    failed = False
    for item in data["items"]:
        path = item["path"]
        if path not in cache:
            cache[path] = read_source(args.gecko, args.rev, path).splitlines()
        lines = cache[path]
        try:
            item["lines"] = (
                object_span(lines, item["object"]) if item.get("object") else len(lines)
            )
        except LookupError:
            print(f"{path}: definition of {item['object']} not found", file=sys.stderr)
            failed = True

    if args.rev:
        data["linesFrom"] = subprocess.run(
            ["git", "-C", args.gecko, "log", "-1", "--format=%h %cs", args.rev],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    DATA.write_text(json.dumps(data, indent=2) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
