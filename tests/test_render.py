import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from forms import for_each_form, make

ANSWERS = {
    "project": "My Project", "internal": "internal-My Project", "date": "07/10/2026",
    "description": "A project.", "constraints": "- One.\n- Two.",
    "phase1_name": "The start", "phase1_slug": "the-start", "phase1_goal": "Get going.",
    "task1_name": "The first task",
}


def templates_of(form):
    """A small set of templates, with the template of the project file of the form."""
    return {
        form.template: "# {{project}}\n\n{{description}}\n\n{{constraints}}\n",
        "phases/P01-{{phase1_slug}}.md": "# Phase 01: {{phase1_name}}\n\n{{phase1_goal}}\n",
        "tools/x.py": "print('{{not_a_placeholder}}')\n",
        "memory/MEMORY.md": "- note\n",
    }


class Render:
    def setUp(self):
        self.render = self.form.scripts / "render.py"
        self.project_file = self.form.project_file
        self.tmp = tempfile.TemporaryDirectory()
        self.templates = Path(self.tmp.name) / "templates"
        self.target = Path(self.tmp.name) / "internal-My Project"
        make(self.templates, templates_of(self.form))
        self.answers = Path(self.tmp.name) / "answers.json"
        self.answers.write_text(json.dumps(ANSWERS), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_render(self, answers=None):
        return subprocess.run([sys.executable, "-I", str(self.render), "--answers", str(answers or self.answers),
                               "--target", str(self.target), "--templates", str(self.templates)],
                              capture_output=True, text=True)

    def run_repair(self):
        return subprocess.run([sys.executable, "-I", str(self.render), "--repair", "--target", str(self.target),
                               "--templates", str(self.templates)], capture_output=True, text=True)

    def test_the_folder_is_written_with_the_answers_filled_in(self):
        result = self.run_render()
        self.assertEqual(result.returncode, 0, result.stderr)
        project = (self.target / self.project_file).read_text(encoding="utf-8")
        self.assertEqual(project, "# My Project\n\nA project.\n\n- One.\n- Two.\n")
        phase = self.target / "phases" / "P01-the-start.md"
        self.assertEqual(phase.read_text(encoding="utf-8"), "# Phase 01: The start\n\nGet going.\n")
        self.assertIn("wrote ", result.stdout)

    def test_a_script_is_copied_as_it_is_and_made_executable(self):
        self.run_render()
        script = self.target / "tools" / "x.py"
        self.assertEqual(script.read_text(encoding="utf-8"), templates_of(self.form)["tools/x.py"])
        self.assertTrue(os.access(script, os.X_OK))

    def test_a_second_run_keeps_every_existing_file(self):
        self.run_render()
        (self.target / self.project_file).write_text("edited\n", encoding="utf-8")
        (self.target / "memory" / "MEMORY.md").unlink()
        result = self.run_render()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / self.project_file).read_text(encoding="utf-8"), "edited\n")
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

    def test_an_answer_that_is_not_a_string_stops_the_run(self):
        odd = dict(ANSWERS, constraints=["One.", "Two."])
        answers = Path(self.tmp.name) / "odd.json"
        answers.write_text(json.dumps(odd), encoding="utf-8")
        result = self.run_render(answers)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("constraints", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.target.exists())

    def test_answers_that_are_not_an_object_stop_the_run(self):
        answers = Path(self.tmp.name) / "list.json"
        answers.write_text(json.dumps(list(ANSWERS)), encoding="utf-8")
        result = self.run_render(answers)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.target.exists())

    def test_a_repair_adds_only_the_files_that_need_no_answer(self):
        make(self.templates, {"close.md": "# The close\n", "tools/README.md": "{{internal}}\n"})
        self.target.mkdir()
        (self.target / self.project_file).write_text("mine\n", encoding="utf-8")
        result = self.run_repair()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "close.md").exists())
        self.assertTrue((self.target / "tools" / "x.py").exists())
        self.assertFalse((self.target / "tools" / "README.md").exists())
        self.assertFalse((self.target / "phases").exists())
        self.assertEqual((self.target / self.project_file).read_text(encoding="utf-8"), "mine\n")
        self.assertIn("needs answers: tools/README.md", result.stdout)
        self.assertIn("needs answers: phases/P01-{{phase1_slug}}.md", result.stdout)
        self.assertNotIn(self.project_file, result.stdout)

    def test_the_template_of_the_project_file_is_written_under_the_name_of_the_project_file(self):
        result = self.run_render()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / self.project_file).is_file())
        self.assertFalse((self.target / self.form.template).exists())

    def test_a_repair_names_a_missing_project_file_by_the_name_of_the_project_file(self):
        self.target.mkdir()
        result = self.run_repair()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"needs answers: {self.project_file}", result.stdout)
        self.assertNotIn(self.form.template, result.stdout)

    def test_a_repair_finds_a_first_phase_file_under_its_own_name(self):
        self.target.mkdir()
        make(self.target, {"phases/P01-my-own-name.md": "# Phase 01: Mine\n"})
        result = self.run_repair()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("P01-", result.stdout)

    def test_a_repair_finds_a_first_phase_file_under_the_old_form_of_its_name(self):
        self.target.mkdir()
        make(self.target, {"phases/phase-01-my-own-name.md": "# Phase 01: Mine\n"})
        result = self.run_repair()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("P01-", result.stdout)

    def test_the_real_templates_are_the_default(self):
        result = subprocess.run([sys.executable, "-I", str(self.render), "--help"], capture_output=True, text=True)
        self.assertIn("templates", result.stdout)


OLD_DECISIONS = (
    "# Decisions\n\nOne entry per decision, appended at the end.\n\n"
    "## 07/10/2026: the first\n\nFirst text.\n\n"
    "## 07/10/2026: the second\n\nSecond text.\n\n```\n## inside a block\n```\n\n"
    "## the third, without a date\n\nThird text.\n"
)


class MigrateDecisions:
    def setUp(self):
        self.render = self.form.scripts / "render.py"
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
        return subprocess.run([sys.executable, "-I", str(self.render), "--migrate-decisions", str(self.source),
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


class RealTemplates:
    def setUp(self):
        self.render = self.form.scripts / "render.py"
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name) / "internal-My Project"

    def tearDown(self):
        self.tmp.cleanup()

    def repair(self):
        return subprocess.run([sys.executable, "-I", str(self.render), "--repair", "--target", str(self.target)],
                              capture_output=True, text=True)

    def test_a_render_of_the_real_templates_reads_clean(self):
        answers = Path(self.tmp.name) / "answers.json"
        answers.write_text(json.dumps(ANSWERS), encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(self.render), "--answers", str(answers),
                                 "--target", str(self.target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        check = subprocess.run([sys.executable, "-I", str(self.target / "tools" / "doc-check.py"),
                                str(self.target)], capture_output=True, text=True)
        self.assertEqual(check.stdout.strip().splitlines()[-1], "clean", check.stdout)

    def test_a_repair_of_an_older_folder_adds_obsolete(self):
        self.target.mkdir()
        (self.target / self.form.project_file).write_text("mine\n", encoding="utf-8")
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "obsolete.md").exists())

    def test_a_repair_of_an_older_folder_adds_the_review(self):
        self.target.mkdir()
        (self.target / self.form.project_file).write_text("mine\n", encoding="utf-8")
        self.repair()
        self.assertTrue((self.target / "review.md").exists())


for_each_form(globals(), Render, MigrateDecisions, RealTemplates)
