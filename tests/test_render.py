import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDER = ROOT / "skill" / "scripts" / "render.py"

ANSWERS = {
    "project": "My Project", "internal": "internal-My Project", "date": "07/10/2026",
    "description": "A project.", "constraints": "- One.\n- Two.",
    "phase1_name": "The start", "phase1_slug": "the-start", "phase1_goal": "Get going.",
    "task1_name": "The first task",
}

TEMPLATES = {
    "CLAUDE.md": "# {{project}}\n\n{{description}}\n\n{{constraints}}\n",
    "phases/phase-01-{{phase1_slug}}.md": "# Phase 01: {{phase1_name}}\n\n{{phase1_goal}}\n",
    "tools/x.py": "print('{{not_a_placeholder}}')\n",
    "memory/MEMORY.md": "- note\n",
}


def make(root, files):
    for name, text in files.items():
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class Render(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.templates = Path(self.tmp.name) / "templates"
        self.target = Path(self.tmp.name) / "internal-My Project"
        make(self.templates, TEMPLATES)
        self.answers = Path(self.tmp.name) / "answers.json"
        self.answers.write_text(json.dumps(ANSWERS), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_render(self, answers=None):
        return subprocess.run([sys.executable, "-I", str(RENDER), "--answers", str(answers or self.answers),
                               "--target", str(self.target), "--templates", str(self.templates)],
                              capture_output=True, text=True)

    def test_the_folder_is_written_with_the_answers_filled_in(self):
        result = self.run_render()
        self.assertEqual(result.returncode, 0, result.stderr)
        claude = (self.target / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertEqual(claude, "# My Project\n\nA project.\n\n- One.\n- Two.\n")
        phase = self.target / "phases" / "phase-01-the-start.md"
        self.assertEqual(phase.read_text(encoding="utf-8"), "# Phase 01: The start\n\nGet going.\n")
        self.assertIn("wrote ", result.stdout)

    def test_a_script_is_copied_as_it_is_and_made_executable(self):
        self.run_render()
        script = self.target / "tools" / "x.py"
        self.assertEqual(script.read_text(encoding="utf-8"), TEMPLATES["tools/x.py"])
        self.assertTrue(os.access(script, os.X_OK))

    def test_a_second_run_keeps_every_existing_file(self):
        self.run_render()
        (self.target / "CLAUDE.md").write_text("edited\n", encoding="utf-8")
        (self.target / "memory" / "MEMORY.md").unlink()
        result = self.run_render()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / "CLAUDE.md").read_text(encoding="utf-8"), "edited\n")
        self.assertTrue((self.target / "memory" / "MEMORY.md").exists())
        self.assertIn("kept ", result.stdout)
        self.assertEqual(result.stdout.count("wrote "), 1)

    def test_a_cache_folder_of_the_templates_is_not_copied(self):
        make(self.templates, {"tools/__pycache__/x.cpython-314.pyc": "", "tools/.hidden": ""})
        result = self.run_render()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / "tools" / "__pycache__").exists())
        self.assertFalse((self.target / "tools" / ".hidden").exists())

    def test_an_unknown_placeholder_in_a_template_stops_the_run(self):
        make(self.templates, {"bad.md": "{{nope}}\n"})
        result = self.run_render()
        self.assertEqual(result.returncode, 2)
        self.assertIn("bad.md: nope", result.stderr)
        self.assertFalse(self.target.exists())

    def test_a_missing_answer_stops_the_run(self):
        short = dict(ANSWERS)
        del short["task1_name"]
        answers = Path(self.tmp.name) / "short.json"
        answers.write_text(json.dumps(short), encoding="utf-8")
        result = self.run_render(answers)
        self.assertEqual(result.returncode, 2)
        self.assertIn("task1_name", result.stderr)
        self.assertFalse(self.target.exists())

    def test_a_repair_adds_only_the_files_that_need_no_answer(self):
        make(self.templates, {"close.md": "# The close\n", "tools/README.md": "{{internal}}\n"})
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--repair", "--target", str(self.target),
                                 "--templates", str(self.templates)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "close.md").exists())
        self.assertTrue((self.target / "tools" / "x.py").exists())
        self.assertFalse((self.target / "tools" / "README.md").exists())
        self.assertFalse((self.target / "phases").exists())
        self.assertEqual((self.target / "CLAUDE.md").read_text(encoding="utf-8"), "mine\n")
        self.assertIn("needs answers: tools/README.md", result.stdout)
        self.assertIn("needs answers: phases/phase-01-{{phase1_slug}}.md", result.stdout)
        self.assertNotIn("CLAUDE.md", result.stdout)

    def test_the_real_templates_are_the_default(self):
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--help"], capture_output=True, text=True)
        self.assertIn("templates", result.stdout)


OLD_DECISIONS = (
    "# Decisions\n\nOne entry per decision, appended at the end.\n\n"
    "## 07/10/2026: the first\n\nFirst text.\n\n"
    "## 07/10/2026: the second\n\nSecond text.\n\n```\n## inside a block\n```\n\n"
    "## the third, without a date\n\nThird text.\n"
)


class MigrateDecisions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.templates = root / "templates"
        make(self.templates, {"decisions.md": "# Decisions\n\nNew header.\n\n## D1, {{date}}: x\n\ny\n"})
        self.source = root / "decisions.md"
        self.source.write_text(OLD_DECISIONS, encoding="utf-8")
        self.out = root / "copy.md"

    def tearDown(self):
        self.tmp.cleanup()

    def run_migrate(self):
        return subprocess.run([sys.executable, "-I", str(RENDER), "--migrate-decisions", str(self.source),
                               "--out", str(self.out), "--templates", str(self.templates)],
                              capture_output=True, text=True)

    def test_the_decisions_are_numbered_and_newest_first(self):
        result = self.run_migrate()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Decisions\n\nNew header.\n\n## D3, the third, without a date\n"), text)
        titles = re.findall(r"^## .*$", text, re.MULTILINE)
        self.assertEqual(titles, ["## D3, the third, without a date", "## D2, 07/10/2026: the second",
                                  "## inside a block", "## D1, 07/10/2026: the first"])
        for body in ("First text.", "Second text.", "Third text.", "```\n## inside a block\n```"):
            self.assertIn(body, text)
        self.assertIn(f"wrote {self.out}", result.stdout)

    def test_a_title_without_a_date_is_warned(self):
        result = self.run_migrate()
        self.assertIn("warning: D3 has no date in its title: the third, without a date", result.stdout)

    def test_the_original_is_left_as_it_was(self):
        self.run_migrate()
        self.assertEqual(self.source.read_text(encoding="utf-8"), OLD_DECISIONS)

    def test_an_existing_output_is_not_replaced(self):
        self.out.write_text("mine\n", encoding="utf-8")
        result = self.run_migrate()
        self.assertEqual(result.returncode, 2)
        self.assertIn("exists", result.stderr)
        self.assertEqual(self.out.read_text(encoding="utf-8"), "mine\n")

    def test_numbered_decisions_are_refused(self):
        self.source.write_text("# Decisions\n\n## D1, 07/10/2026: a\n\nText.\n", encoding="utf-8")
        result = self.run_migrate()
        self.assertEqual(result.returncode, 2)
        self.assertIn("already numbered", result.stderr)
        self.assertFalse(self.out.exists())

    def test_a_file_that_is_not_utf8_is_refused(self):
        self.source.write_bytes("## 07/10/2026: caf\xe9\n".encode("latin-1"))
        result = self.run_migrate()
        self.assertEqual(result.returncode, 2)
        self.assertIn("not UTF-8", result.stderr)
        self.assertFalse(self.out.exists())



class RealTemplates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name) / "internal-My Project"

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_render_of_the_real_templates_reads_clean(self):
        answers = Path(self.tmp.name) / "answers.json"
        answers.write_text(json.dumps(ANSWERS), encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--answers", str(answers),
                                 "--target", str(self.target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        check = subprocess.run([sys.executable, "-I", str(self.target / "tools" / "doc-check.py"),
                                str(self.target)], capture_output=True, text=True)
        self.assertEqual(check.stdout.strip().splitlines()[-1], "clean", check.stdout)

    def test_a_repair_of_an_older_folder_adds_obsolete(self):
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--repair", "--target", str(self.target)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "obsolete.md").exists())

    def test_a_repair_of_an_older_folder_adds_the_review(self):
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
        subprocess.run([sys.executable, "-I", str(RENDER), "--repair", "--target", str(self.target)],
                       capture_output=True, text=True)
        self.assertTrue((self.target / "review.md").exists())

if __name__ == "__main__":
    unittest.main()
