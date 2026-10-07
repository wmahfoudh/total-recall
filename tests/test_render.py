import json
import os
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

    def test_the_real_templates_are_the_default(self):
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--help"], capture_output=True, text=True)
        self.assertIn("templates", result.stdout)


if __name__ == "__main__":
    unittest.main()
