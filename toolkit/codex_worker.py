#!/usr/bin/env python3
"""Start one Codex worker on one brief, in one working copy, the way every architect does (C-038).

    python3 toolkit/codex_worker.py --workdir WT --brief BRIEF.md --out PREFIX [--rules RULES.md ...]
                                    [--effort low|medium|high|xhigh] [--census] [--print]

The worker reads the rules files and then the brief, as one prompt on stdin. Its last message is
written to PREFIX.final.md and its whole log to PREFIX.log. The sandbox facts this encodes are in
toolkit/README.md: the workspace sandbox needs local network for any test that starts a server, and
version-control data stays read-only, so the architect prepares merges and commits (C-032).
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_codex() -> str:
    """The `codex` on PATH, else the newest copy shipped inside the VS Code extension."""
    on_path = shutil.which("codex")
    if on_path:
        return on_path
    pattern = os.path.expanduser("~/.vscode/extensions/openai.chatgpt-*/bin/*/codex")
    found = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not found:
        sys.exit("codex_worker: no `codex` on PATH and none inside ~/.vscode/extensions/openai.chatgpt-*")
    return found[-1]


def command(codex: str, *, effort: str, census: bool, final: Path) -> list[str]:
    sandbox = "read-only" if census else "workspace-write"
    return [
        codex, "exec", "-s", sandbox,
        "-c", "notify=[]",
        "-c", f'model_reasoning_effort="{effort}"',
        "-c", "sandbox_workspace_write.network_access=true",
        "-o", str(final),
        "-",
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--brief", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="prefix for PREFIX.final.md and PREFIX.log")
    parser.add_argument("--rules", action="append", default=[], type=Path)
    parser.add_argument("--effort", default="medium", choices=("low", "medium", "high", "xhigh"))
    parser.add_argument("--census", action="store_true", help="read-only sandbox, for a census or a review")
    parser.add_argument("--print", dest="print_only", action="store_true", help="print the command and stop")
    args = parser.parse_args(argv)

    final = Path(f"{args.out}.final.md")
    cmd = command(find_codex(), effort=args.effort, census=args.census, final=final)
    if args.print_only:
        print(" ".join(cmd))
        return 0
    prompt = "\n\n".join(p.read_text(encoding="utf-8") for p in (*args.rules, args.brief))
    with open(f"{args.out}.log", "w", encoding="utf-8") as log:
        code = subprocess.run(cmd, cwd=args.workdir, input=prompt, text=True, stdout=log, stderr=subprocess.STDOUT).returncode
    print(f"EXIT {code}")
    status = subprocess.run(["git", "-C", str(args.workdir), "status", "--short"], capture_output=True, text=True).stdout
    print(f"UNCOMMITTED {len(status.splitlines())} path(s)")
    if final.exists():
        print(final.read_text(encoding="utf-8"))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
