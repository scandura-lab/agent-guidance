"""Witness for toolkit/codex_worker.py: the sandbox facts every architect relearned (C-038).

A fake `codex` on the PATH records its arguments and stdin. Run from the repository root:
`python3 -m unittest discover -s tests`.
Guarantee protected: a Codex worker started by the toolkit has local network, no desktop notifier,
the effort it was given, a read-only sandbox for a census, and the rules before the brief.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "toolkit" / "codex_worker.py"
FAKE = """#!/bin/sh
printf '%s\\n' "$@" > "$FAKE_ARGS"
cat > "$FAKE_STDIN"
"""


class CodexWorkerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "bin").mkdir()
        fake = self.tmp / "bin" / "codex"
        fake.write_text(FAKE)
        fake.chmod(0o755)
        self.env = {**os.environ, "PATH": f"{self.tmp / 'bin'}:{os.environ['PATH']}",
                    "FAKE_ARGS": str(self.tmp / "args"), "FAKE_STDIN": str(self.tmp / "stdin")}
        (self.tmp / "rules.md").write_text("RULES")
        (self.tmp / "brief.md").write_text("BRIEF")

    def run_tool(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--workdir", str(self.tmp), "--brief", str(self.tmp / "brief.md"),
             "--rules", str(self.tmp / "rules.md"), "--out", str(self.tmp / "w"), *extra],
            env=self.env, capture_output=True, text=True,
        )

    def test_a_build_has_network_no_notifier_and_its_effort(self) -> None:
        done = self.run_tool("--effort", "low")
        self.assertEqual(done.returncode, 0, done.stderr)
        args = (self.tmp / "args").read_text().split("\n")
        self.assertEqual(args[:3], ["exec", "-s", "workspace-write"])
        for setting in ("notify=[]", 'model_reasoning_effort="low"', "sandbox_workspace_write.network_access=true"):
            self.assertIn(setting, args)

    def test_a_census_is_read_only(self) -> None:
        self.run_tool("--census")
        args = (self.tmp / "args").read_text().split("\n")
        self.assertEqual(args[:3], ["exec", "-s", "read-only"])

    def test_the_rules_come_before_the_brief(self) -> None:
        self.run_tool()
        self.assertEqual((self.tmp / "stdin").read_text(), "RULES\n\nBRIEF")

    def test_print_runs_nothing(self) -> None:
        done = self.run_tool("--print")
        self.assertIn("exec -s workspace-write", done.stdout)
        self.assertFalse((self.tmp / "args").exists())


if __name__ == "__main__":
    unittest.main()
