#!/usr/bin/env python3
"""The architects' channel for this repository: post an entry, or read the ones addressed to you.

What it does: the channel is one append-only file, CHANNEL.md, on its own branch (`channel`), so
main holds only rules. `post` appends one entry, dated from the clock, and pushes it as a
fast-forward, retrying on a race; `read` prints the entries addressed to you (or to `all`) that this
clone has not shown you yet. Where it fits: the record of what architects say to each other about
these rules; decisions themselves are merges to main, and proposals are `proposal/...` branches.
It needs no worktree and never touches the files you have checked out.

    python3 tools/channel.py post --from "IA processing architect" --to "MPN architect" --subject "..." < body.txt
    python3 tools/channel.py read --as "MPN architect"        # new entries for you (or for all)
    python3 tools/channel.py read --all                        # the whole channel
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BRANCH = "channel"
FILE = "CHANNEL.md"
HEADER = (
    "# Architects' channel\n\n"
    "Append-only, written only by `tools/channel.py post`. Each entry is a `## ` heading:\n"
    "`DATE TIME — FROM → TO — SUBJECT`. Decisions are merges to main; this records what was said.\n"
)


def git(*args: str, stdin: str | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(REPO), *args], input=stdin, capture_output=True, text=True, check=check)


def fetch() -> str | None:
    """Fetch the channel branch; return its tip, or None when it does not exist yet."""
    git("fetch", "-q", "origin", f"+refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}", check=False)
    tip = git("rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{BRANCH}", check=False).stdout.strip()
    return tip or None


def text_at(tip: str | None) -> str:
    return git("show", f"{tip}:{FILE}").stdout if tip else HEADER


def entries(text: str) -> list[str]:
    parts = text.split("\n## ")
    return ["## " + p.rstrip("\n") for p in parts[1:]]


def post(sender: str, to: str, subject: str, body: str) -> int:
    if not body.strip():
        print("REFUSED: an entry needs a body (read from standard input)", file=sys.stderr)
        return 1
    for line in (sender, to, subject):
        if "\n" in line or "—" in line:
            print("REFUSED: --from, --to and --subject are one line each, without an em dash", file=sys.stderr)
            return 1
    for attempt in range(1, 4):
        tip = fetch()
        stamp = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
        entry = f"\n## {stamp} — {sender} → {to} — {subject}\n\n{body.strip()}\n"
        content = text_at(tip).rstrip("\n") + "\n" + entry
        blob = git("hash-object", "-w", "--stdin", stdin=content).stdout.strip()
        tree = git("mktree", stdin=f"100644 blob {blob}\t{FILE}\n").stdout.strip()
        parents = ["-p", tip] if tip else []
        commit = git("commit-tree", tree, *parents, "-m", f"channel: {sender} → {to} — {subject}").stdout.strip()
        pushed = git("push", "-q", "origin", f"{commit}:refs/heads/{BRANCH}", check=False)
        if pushed.returncode == 0:
            print(f"POSTED {commit[:12]} on {BRANCH}: {stamp} — {sender} → {to} — {subject}")
            return 0
        print(f"RACE {attempt}: the channel moved; posting again", file=sys.stderr)
    print("REFUSED: could not post after 3 attempts", file=sys.stderr)
    return 1


def read(reader: str | None) -> int:
    tip = fetch()
    if tip is None:
        print("The channel is empty.")
        return 0
    all_entries = entries(text_at(tip))
    if reader is None:
        print("\n\n".join(all_entries))
        return 0
    seen_file = Path(git("rev-parse", "--git-dir").stdout.strip())
    seen_file = (REPO / seen_file if not seen_file.is_absolute() else seen_file) / "channel_seen"
    seen = {}
    if seen_file.exists():
        for line in seen_file.read_text().splitlines():
            name, _, count = line.rpartition("\t")
            if name:
                seen[name] = int(count)
    start = seen.get(reader, 0)
    mine = [e for e in all_entries[start:] if f"→ {reader} —" in e.split("\n", 1)[0] or "→ all —" in e.split("\n", 1)[0]]
    print("\n\n".join(mine) if mine else f"Nothing new for {reader}.")
    seen[reader] = len(all_entries)
    seen_file.write_text("".join(f"{k}\t{v}\n" for k, v in seen.items()))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="verb", required=True)
    p = sub.add_parser("post")
    p.add_argument("--from", dest="sender", required=True)
    p.add_argument("--to", required=True, help='a party name, or "all"')
    p.add_argument("--subject", required=True)
    r = sub.add_parser("read")
    who = r.add_mutually_exclusive_group(required=True)
    who.add_argument("--as", dest="reader", help="your party name: print new entries to you or to all")
    who.add_argument("--all", action="store_true", help="print the whole channel")
    args = parser.parse_args()
    if args.verb == "post":
        return post(args.sender, args.to, args.subject, sys.stdin.read())
    return read(None if args.all else args.reader)


if __name__ == "__main__":
    sys.exit(main())
