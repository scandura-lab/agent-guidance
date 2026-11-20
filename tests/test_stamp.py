"""Witness for the stamp's sha256 and the project-side check (`tools/copy_check.py`).

Each test builds a small source repository with the real `tools/stamp.py` and `tools/copy_check.py`,
stamps a project folder from it, and runs both tools as a project would. Run from the repository
root: `python3 -m unittest discover -s tests`.
Guarantee protected: a copy is never edited in place (G-048 sub-point 4), and a project's own test
can detect such an edit without a clone of this repository.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
PAGES = (
    "general/ENGINEERING_PRINCIPLES.md",
    "general/DECISIONS.md",
    "general/OPERATING_MODEL.md",
    "domains/science/SCIENCE_PRINCIPLES.md",
    "domains/science/SCIENCE_DECISIONS.md",
)


def run(*args: str | Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True, text=True)


class StampedCopy(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.source = self.tmp / "agent-guidance"
        (self.source / "tools").mkdir(parents=True)
        for name in ("stamp.py", "copy_check.py"):
            shutil.copy(TOOLS / name, self.source / "tools" / name)
        for page in PAGES:
            path = self.source / page
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {path.stem}\n\n- A rule.\n", encoding="utf-8")
        for args in (("init", "-q"), ("add", "."), ("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "source")):
            self.assertEqual(run("git", "-C", self.source, *args).returncode, 0)
        self.dest = self.tmp / "project" / "docs" / "principles"
        self.dest.mkdir(parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def stamp(self, verb: str = "into") -> subprocess.CompletedProcess[str]:
        return run(sys.executable, self.source / "tools" / "stamp.py", verb, self.dest, "--with", "science")

    def project_check(self, folder: Path | None = None) -> subprocess.CompletedProcess[str]:
        folder = folder or self.dest
        return run(sys.executable, folder / "copy_check.py", folder)

    def test_a_fresh_copy_checks_intact_with_no_source_repository(self) -> None:
        self.assertEqual(self.stamp().returncode, 0)
        moved = self.tmp / "elsewhere"
        shutil.copytree(self.dest, moved)
        shutil.rmtree(self.source)
        result = self.project_check(moved)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.count("INTACT"), len(PAGES) + 1)

    def test_each_stamp_is_one_line_followed_by_a_blank_line(self) -> None:
        self.stamp()
        for path in self.dest.iterdir():
            lines = path.read_text(encoding="utf-8").split("\n")
            self.assertRegex(lines[0], r"^(# )?Copied from agent-guidance \S+ at [0-9a-f]{12} \(\d{4}-\d{2}-\d{2}; sha256 [0-9a-f]{64}\)\. Do not edit here")
            self.assertEqual(lines[1], "")

    def test_an_edit_below_the_stamp_is_caught_by_both_checks(self) -> None:
        self.stamp()
        page = self.dest / "DECISIONS.md"
        page.write_text(page.read_text(encoding="utf-8").replace("A rule.", "A rule, edited."), encoding="utf-8")
        project = self.project_check()
        self.assertEqual(project.returncode, 1)
        self.assertIn(f"EDITED IN PLACE {page}", project.stdout)
        source = self.stamp("check")
        self.assertEqual(source.returncode, 1)
        self.assertIn(f"EDITED IN PLACE {page}", source.stdout)

    def test_an_edited_hash_in_the_stamp_line_is_caught_by_both_checks(self) -> None:
        self.stamp()
        page = self.dest / "OPERATING_MODEL.md"
        text = page.read_text(encoding="utf-8")
        at = text.index("sha256 ") + len("sha256 ")
        page.write_text(text[:at] + ("0" if text[at] != "0" else "1") + text[at + 1 :], encoding="utf-8")
        self.assertIn(f"EDITED IN PLACE {page}", self.project_check().stdout)
        self.assertIn(f"EDITED IN PLACE {page}", self.stamp("check").stdout)

    def test_an_edited_checker_reports_itself_and_is_caught_by_the_source_check(self) -> None:
        self.stamp()
        checker = self.dest / "copy_check.py"
        checker.write_text(checker.read_text(encoding="utf-8") + "\n# an added line\n", encoding="utf-8")
        self.assertIn(f"EDITED IN PLACE {checker}", self.project_check().stdout)
        self.assertIn(f"EDITED IN PLACE {checker}", self.stamp("check").stdout)

    def test_project_header_lines_are_kept_and_not_hashed(self) -> None:
        self.stamp()
        page = self.dest / "ENGINEERING_PRINCIPLES.md"
        page.write_text("State: LOCKED\n" + page.read_text(encoding="utf-8"), encoding="utf-8")
        self.assertEqual(self.project_check().returncode, 0)
        self.assertEqual(self.stamp().returncode, 0)
        self.assertTrue(page.read_text(encoding="utf-8").startswith("State: LOCKED\nCopied from agent-guidance "))
        self.assertEqual(self.project_check().returncode, 0)

    def test_a_copy_stamped_in_the_old_form_still_checks_until_restamped(self) -> None:
        for page in PAGES:
            sha = run("git", "-C", self.source, "log", "-1", "--format=%H", "--", page).stdout.strip()
            date = run("git", "-C", self.source, "log", "-1", "--format=%cs", sha).stdout.strip()
            body = (self.source / page).read_text(encoding="utf-8")
            old = f"Copied from agent-guidance {page} at {sha[:12]} ({date}). Do not edit here; propose changes to that repository."
            (self.dest / Path(page).name).write_text(f"{old}\n\n{body}", encoding="utf-8")
        source = self.stamp("check")
        self.assertEqual(source.returncode, 2, source.stdout)
        self.assertEqual(source.stdout.count("CURRENT"), len(PAGES))
        self.assertIn("BEHIND", source.stdout)
        shutil.copy(self.source / "tools" / "copy_check.py", self.dest / "copy_check.py.unstamped")
        project = run(sys.executable, self.dest / "copy_check.py.unstamped", self.dest)
        self.assertEqual(project.returncode, 1)
        self.assertEqual(project.stdout.count("NO DIGEST"), len(PAGES))
        (self.dest / "copy_check.py.unstamped").unlink()
        self.assertEqual(self.stamp().returncode, 0)
        self.assertEqual(self.project_check().returncode, 0)
        self.assertEqual(self.stamp("check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
