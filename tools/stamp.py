#!/usr/bin/env python3
"""Put a stamped copy of the general pages into a project, and check such a copy.

What it does: `into DEST [--with SET ...]` writes the general pages (general/ENGINEERING_PRINCIPLES,
DECISIONS and OPERATING_MODEL) into the folder DEST, plus each opt-in set named (for example
`--with science`: domains/science/SCIENCE_PRINCIPLES and SCIENCE_DECISIONS), each under one stamp
line naming this repository's commit; `check DEST [--with SET ...]` reports, for each copy, whether
it is current, behind the source, or edited in place (G-048).
Where it fits: the one door between this repository and a project's copy. It reads this
repository's git history and writes only DEST. Called by an architect from a clone of this
repository.

A copy is: the project's own header lines (kept as they are, for example a document-tier line),
then the stamp line, a blank line, and the source page byte for byte. Lines above the stamp are
the project's; everything below it belongs to the source.

Exit status: 0 current; 1 a refusal or a copy edited in place or missing; 2 a copy behind the source.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SETS = {
    "general": ("general/ENGINEERING_PRINCIPLES.md", "general/DECISIONS.md", "general/OPERATING_MODEL.md"),
    "science": ("domains/science/SCIENCE_PRINCIPLES.md", "domains/science/SCIENCE_DECISIONS.md"),
}
REPO = Path(__file__).resolve().parent.parent
STAMP = re.compile(r"^Copied from agent-guidance (?P<page>\S+) at (?P<sha>[0-9a-f]{12}) \((?P<date>\d{4}-\d{2}-\d{2})\)\. ")
STAMP_TAIL = "Do not edit here; propose changes to that repository."


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True).stdout


def pages(sets: list[str]) -> list[str]:
    """The source paths of the general set plus each opt-in set named."""
    unknown = [name for name in sets if name not in SETS]
    if unknown:
        raise SystemExit(f"REFUSED: unknown set(s) {unknown}; known: {sorted(SETS)}")
    return [p for name in ["general", *[n for n in sets if n != "general"]] for p in SETS[name]]


def last_commit(page: str) -> str:
    """The latest commit on HEAD that changed <page> (a path in this repository)."""
    sha = git("log", "-1", "--format=%H", "HEAD", "--", page).strip()
    if not sha:
        raise SystemExit(f"REFUSED: {page} has no commit in this repository")
    return sha


def split_copy(text: str) -> tuple[list[str], re.Match | None, str]:
    """(project header lines, stamp match, body below the stamp and its blank line)."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        m = STAMP.match(line)
        if m:
            rest = lines[i + 1 :]
            if rest and rest[0] == "":
                rest = rest[1:]
            return lines[:i], m, "\n".join(rest)
    return [], None, text


def into(dest: Path, sets: list[str]) -> int:
    if git("status", "--porcelain", "--", "general", "domains").strip():
        print("REFUSED: general/ or domains/ has uncommitted changes; commit them first, so the stamp names the text", file=sys.stderr)
        return 1
    if not dest.is_dir():
        print(f"REFUSED: {dest} is not a folder", file=sys.stderr)
        return 1
    for page in pages(sets):
        sha = last_commit(page)
        date = git("log", "-1", "--format=%cs", sha).strip()
        body = git("show", f"{sha}:{page}")
        target = dest / Path(page).name
        header: list[str] = []
        if target.exists():
            header, stamp, _ = split_copy(target.read_text())
            if stamp is None:
                print(f"REFUSED: {target} exists without a stamp line; move it aside or add the stamp by hand first", file=sys.stderr)
                return 1
        stamp_line = f"Copied from agent-guidance {page} at {sha[:12]} ({date}). {STAMP_TAIL}"
        target.write_text("\n".join([*header, stamp_line, "", body]) if header else "\n".join([stamp_line, "", body]))
        print(f"STAMPED {target} at {sha[:12]}")
    return 0


def check(dest: Path, sets: list[str]) -> int:
    worst = 0
    for page in pages(sets):
        target = dest / Path(page).name
        if not target.exists():
            print(f"MISSING {target}")
            worst = 1
            continue
        _, stamp, body = split_copy(target.read_text())
        if stamp is None or stamp["page"] != page:
            print(f"NO STAMP {target}: not a copy this tool made")
            worst = 1
            continue
        stamped = stamp["sha"]
        try:
            source = git("show", f"{stamped}:{page}")
        except subprocess.CalledProcessError:
            print(f"UNKNOWN COMMIT {target}: {stamped} is not in this clone (pull first)")
            worst = 1
            continue
        if body != source:
            print(f"EDITED IN PLACE {target}: differs from {page} at {stamped}; propose the change here instead")
            worst = 1
            continue
        latest = last_commit(page)
        if not latest.startswith(stamped):
            behind = git("rev-list", "--count", f"{stamped}..{latest}", "--", page).strip()
            again = "".join(f" --with {n}" for n in sets)
            print(f"BEHIND {target}: stamped {stamped}, source {latest[:12]} ({behind} commit(s) to {page}); run: python3 tools/stamp.py into {dest}{again}")
            worst = max(worst, 2) if worst != 1 else 1
            continue
        print(f"CURRENT {target} at {stamped}")
    return worst


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="verb", required=True)
    for verb in ("into", "check"):
        cmd = sub.add_parser(verb)
        cmd.add_argument("dest", type=Path, help="the project folder that holds the copies")
        cmd.add_argument("--with", dest="sets", action="append", default=[], metavar="SET", help=f"an opt-in set besides general: {sorted(set(SETS) - {'general'})}")
    args = parser.parse_args()
    return into(args.dest, args.sets) if args.verb == "into" else check(args.dest, args.sets)


if __name__ == "__main__":
    sys.exit(main())
