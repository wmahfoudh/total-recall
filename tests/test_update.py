import datetime
import importlib.util
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATE = ROOT / "skill" / "scripts" / "update.py"
NOW = datetime.datetime(2026, 11, 30, 20, 33)

TEMPLATES = {
    "CLAUDE.md": "@rules.md\n\n# {{project}}\n",
    "rules.md": "# Rules\n\nNew rules.\n",
    "close.md": "# The close\n\nNew close.\n",
    "review.md": "# The review\n",
    "obsolete.md": "# Obsolete decisions\n",
    "decisions.md": "# Decisions\n\nNew header.\n\n## D1, {{date}}: x\n\ny\n",
    "phases/phase-01-{{phase1_slug}}.md": "# Phase 01: {{phase1_name}}\n",
    "tools/doc-check.py": "print('new')\n",
}

FOLDER = {
    "CLAUDE.md": "@rules.md\n\n# My project\n\nMine.\n",
    "rules.md": "# Rules\n\nOld rules.\n",
    "close.md": "# The close\n\nNew close.\n",
    "state.md": "# State\n\nMine.\n",
    "decisions.md": "# Decisions\n\nOld header.\n\n## 07/10/2026: the first\n\nText.\n",
    "phases/phase-01-the-start.md": "# Phase 01: The start\n",
    "tools/doc-check.py": "print('old')\n",
}


def load():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("update", UPDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make(root, files):
    for name, text in files.items():
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class Backup(unittest.TestCase):
    def setUp(self):
        self.update = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name) / "internal-my-project"
        make(self.target, FOLDER)

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_name_gives_the_folder_the_time_and_the_kind(self):
        path = self.update.backup(self.target, "manual", NOW)
        self.assertEqual(path, self.target / "backup" / "internal-my-project-2026-11-30-20-33-manual.tar.gz")
        auto = self.update.backup(self.target, "auto", NOW)
        self.assertEqual(auto.name, "internal-my-project-2026-11-30-20-33-auto.tar.gz")

    def test_the_archive_holds_the_folder_without_the_backups(self):
        self.update.backup(self.target, "manual", NOW)
        path = self.update.backup(self.target, "auto", NOW)
        with tarfile.open(path) as archive:
            names = archive.getnames()
        self.assertIn("internal-my-project/state.md", names)
        self.assertIn("internal-my-project/phases/phase-01-the-start.md", names)
        self.assertFalse(any("/backup" in name for name in names), names)

    def test_a_second_archive_in_the_same_minute_is_kept_apart(self):
        first = self.update.backup(self.target, "manual", NOW)
        second = self.update.backup(self.target, "manual", NOW)
        self.assertNotEqual(first, second)
        self.assertEqual(second.name, "internal-my-project-2026-11-30-20-33-manual-2.tar.gz")
        self.assertTrue(first.exists() and second.exists())

    def test_an_unknown_kind_is_refused(self):
        with self.assertRaises(ValueError):
            self.update.backup(self.target, "weekly", NOW)


class Update(unittest.TestCase):
    def setUp(self):
        self.update = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.templates = Path(self.tmp.name) / "templates"
        self.target = Path(self.tmp.name) / "internal-my-project"
        make(self.templates, TEMPLATES)
        make(self.target, FOLDER)

    def tearDown(self):
        self.tmp.cleanup()

    def run_update(self, *args):
        return subprocess.run([sys.executable, "-I", str(UPDATE), *args, "--target", str(self.target),
                               "--templates", str(self.templates)], capture_output=True, text=True)

    def test_the_plan_names_what_the_update_would_do(self):
        plan = self.update.plan_update(self.templates, self.target)
        self.assertEqual(plan["add"], ["obsolete.md", "review.md"])
        self.assertEqual(plan["replace"], ["rules.md", "tools/doc-check.py"])
        self.assertTrue(plan["migrate"])

    def test_the_start_script_is_a_routine_file(self):
        self.assertIn("tools/start.py", self.update.ROUTINE_FILES)

    def test_the_plan_changes_nothing(self):
        before = {p: p.read_bytes() for p in self.target.rglob("*") if p.is_file()}
        result = self.run_update("plan")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("add obsolete.md", result.stdout)
        self.assertIn("replace rules.md", result.stdout)
        self.assertIn("migrate decisions.md", result.stdout)
        after = {p: p.read_bytes() for p in self.target.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_the_apply_makes_a_backup_first_and_applies_the_plan(self):
        result = self.run_update("apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        archives = list((self.target / "backup").glob("*-auto.tar.gz"))
        self.assertEqual(len(archives), 1)
        with tarfile.open(archives[0]) as archive:
            old = archive.extractfile("internal-my-project/rules.md").read().decode()
        self.assertEqual(old, FOLDER["rules.md"])
        self.assertEqual((self.target / "rules.md").read_text(encoding="utf-8"), TEMPLATES["rules.md"])
        self.assertTrue((self.target / "review.md").exists())
        self.assertTrue((self.target / "obsolete.md").exists())
        decisions = (self.target / "decisions.md").read_text(encoding="utf-8")
        self.assertTrue(decisions.startswith("# Decisions\n\nNew header.\n\n## D1, 07/10/2026: the first\n"))

    def test_the_project_content_is_not_touched(self):
        self.run_update("apply")
        for name in ("CLAUDE.md", "state.md", "phases/phase-01-the-start.md"):
            self.assertEqual((self.target / name).read_text(encoding="utf-8"), FOLDER[name], name)
        self.assertFalse((self.target / "phases" / "phase-01-{{phase1_slug}}.md").exists())

    def test_a_second_apply_finds_nothing_and_makes_no_backup(self):
        self.run_update("apply")
        result = self.run_update("apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("nothing to update", result.stdout)
        self.assertEqual(len(list((self.target / "backup").glob("*.tar.gz"))), 1)

    def test_a_folder_the_skill_did_not_write_is_refused(self):
        (self.target / "CLAUDE.md").write_text("# My notes\n", encoding="utf-8")
        result = self.run_update("apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("does not look like a total-recall folder", result.stderr)
        self.assertFalse((self.target / "backup").exists())
        self.assertEqual((self.target / "rules.md").read_text(encoding="utf-8"), FOLDER["rules.md"])

    def test_the_backup_command_makes_a_manual_archive(self):
        result = self.run_update("backup")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list((self.target / "backup").glob("internal-my-project-*-manual.tar.gz"))), 1)
        self.assertIn("backup ", result.stdout)


if __name__ == "__main__":
    unittest.main()
