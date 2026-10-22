import datetime
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from forms import for_each_form, load, make

NOW = datetime.datetime(2026, 11, 30, 20, 33)


def templates_of(form):
    return {
        form.project_file: "@rules.md\n\n# {{project}}\n",
        "rules.md": "# Rules\n\nNew rules.\n",
        "close.md": "# The close\n\nNew close.\n",
        "review.md": "# The review\n",
        "obsolete.md": "# Obsolete decisions\n",
        "decisions.md": "# Decisions\n\nNew header.\n\n## D1, {{date}}: x\n\ny\n",
        "phases/P01-{{phase1_slug}}.md": "# Phase 01: {{phase1_name}}\n",
        "tools/doc-check.py": "print('new')\n",
    }


def folder_of(form):
    """An older folder of the form, with its own content and old routine files."""
    return {
        form.project_file: "@rules.md\n\n# My project\n\nMine.\n",
        "rules.md": "# Rules\n\nOld rules.\n",
        "close.md": "# The close\n\nNew close.\n",
        "state.md": "# State\n\nMine.\n",
        "decisions.md": "# Decisions\n\nOld header.\n\n## 07/10/2026: the first\n\nText.\n",
        "phases/P01-the-start.md": "# Phase 01: The start\n",
        "tools/doc-check.py": "print('old')\n",
    }


class Backup:
    def setUp(self):
        self.update = load(self.form.scripts / "update.py", "update")
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name) / "internal-my-project"
        make(self.target, folder_of(self.form))

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
        self.assertIn("internal-my-project/phases/P01-the-start.md", names)
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


class Update:
    def setUp(self):
        self.update = load(self.form.scripts / "update.py", "update")
        self.project_file = self.form.project_file
        self.folder = folder_of(self.form)
        self.tmp = tempfile.TemporaryDirectory()
        self.templates = Path(self.tmp.name) / "templates"
        self.target = Path(self.tmp.name) / "internal-my-project"
        make(self.templates, templates_of(self.form))
        make(self.target, self.folder)

    def tearDown(self):
        self.tmp.cleanup()

    def run_update(self, *args):
        return subprocess.run([sys.executable, "-I", str(self.form.scripts / "update.py"), *args,
                               "--target", str(self.target), "--templates", str(self.templates)],
                              capture_output=True, text=True)

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
        self.assertEqual(old, self.folder["rules.md"])
        self.assertEqual((self.target / "rules.md").read_text(encoding="utf-8"),
                         templates_of(self.form)["rules.md"])
        self.assertTrue((self.target / "review.md").exists())
        self.assertTrue((self.target / "obsolete.md").exists())
        decisions = (self.target / "decisions.md").read_text(encoding="utf-8")
        self.assertTrue(decisions.startswith("# Decisions\n\nNew header.\n\n## D1, 07/10/2026: the first\n"))

    def test_the_project_content_is_not_touched(self):
        self.run_update("apply")
        for name in (self.project_file, "state.md", "phases/P01-the-start.md"):
            self.assertEqual((self.target / name).read_text(encoding="utf-8"), self.folder[name], name)
        self.assertFalse((self.target / "phases" / "P01-{{phase1_slug}}.md").exists())

    def test_the_plan_lists_the_phase_files_of_the_old_form_to_rename(self):
        make(self.target, {"phases/phase-02-old.md": "# Phase 02: Old\n"})
        plan = self.update.plan_update(self.templates, self.target)
        self.assertEqual(plan["rename"], [("phases/phase-02-old.md", "phases/P02-old.md")])
        result = self.run_update("plan")
        self.assertIn("rename phases/phase-02-old.md phases/P02-old.md", result.stdout)

    def test_the_apply_renames_the_phase_files_of_the_old_form(self):
        make(self.target, {"phases/phase-02-old.md": "# Phase 02: Old\n"})
        result = self.run_update("apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / "phases" / "phase-02-old.md").exists())
        self.assertEqual((self.target / "phases" / "P02-old.md").read_text(encoding="utf-8"), "# Phase 02: Old\n")
        self.assertIn("nothing to update", self.run_update("apply").stdout)

    def test_the_records_of_the_old_form_are_listed_for_the_hand(self):
        make(self.target, {"records/2026-10-07-design.md": "# Spec\n", "records/README.md": "# Records\n",
                           "records/R000-plan.md": "# Plan\n"})
        plan = self.update.plan_update(self.templates, self.target)
        self.assertEqual(plan["by_hand"], ["records/2026-10-07-design.md"])
        result = self.run_update("plan")
        self.assertIn("by hand: records/2026-10-07-design.md", result.stdout)
        self.run_update("apply")
        self.assertTrue((self.target / "records" / "2026-10-07-design.md").exists())

    def test_a_second_apply_finds_nothing_and_makes_no_backup(self):
        self.run_update("apply")
        result = self.run_update("apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("nothing to update", result.stdout)
        self.assertEqual(len(list((self.target / "backup").glob("*.tar.gz"))), 1)

    def test_a_folder_the_skill_did_not_write_is_refused(self):
        (self.target / self.project_file).write_text("# My notes\n", encoding="utf-8")
        result = self.run_update("apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("does not look like a total-recall folder", result.stderr)
        self.assertFalse((self.target / "backup").exists())
        self.assertEqual((self.target / "rules.md").read_text(encoding="utf-8"), self.folder["rules.md"])

    def test_the_backup_command_makes_a_manual_archive(self):
        result = self.run_update("backup")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list((self.target / "backup").glob("internal-my-project-*-manual.tar.gz"))), 1)
        self.assertIn("backup ", result.stdout)


for_each_form(globals(), Backup, Update)
