import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from forms import CLAUDE, COMMON_FILES, FORMS, PI, ROOT, for_each_form, load

TEXT = (".md", ".py", ".sh", ".json", ".txt")
# The name of the reference project is written nowhere in the
# repository, so the test keeps its SHA-256 hash and hashes each word.
FORBIDDEN_HASHES = {"535609a8f9190ae30850b6c191e554c978db017302fbb285554d04519a5daa69"}
HOME_PATH = "/" + "home" + "/"
# Several tests below check a sentence of a rule in SKILL.md, the README
# or a template. They stop a rewrite from dropping the rule unnoticed.
# When a change of wording is meant, the test is changed in the same edit.


def forbidden_words(text, hashes):
    """The words of the text, lowercased, whose SHA-256 hash is in hashes."""
    words = sorted(set(re.findall(r"[a-z0-9]+", text.lower())))
    return [w for w in words if hashlib.sha256(w.encode()).hexdigest() in hashes]


def text_files():
    files = [ROOT / "README.md"]
    for form in FORMS:
        files += [p for p in form.folder.rglob("*") if p.is_file() and p.suffix in TEXT]
    files += [p for p in (ROOT / "tests").glob("*.py")]
    return [p for p in files if p.exists()]


def skill_steps(form):
    """The numbered steps of SKILL.md, by number: the title line, then the body."""
    text = form.skill_file.read_text(encoding="utf-8")
    parts = re.split(r"^## (\d+)\. ", text, flags=re.MULTILINE)
    return dict(zip(parts[1::2], parts[2::2]))


def read_template(form, name):
    return (form.templates / name).read_text(encoding="utf-8")


class WritingRules(unittest.TestCase):
    def setUp(self):
        self.doc = load(CLAUDE.tools / "doc-check.py", "doc_check")

    def test_no_dash_character_anywhere(self):
        for path in text_files():
            found = self.doc.find_dashes(path.read_text(encoding="utf-8"))
            self.assertEqual(found, [], f"{path.relative_to(ROOT)}: {found}")

    def test_a_blank_line_before_each_list_and_table(self):
        for path in text_files():
            if path.suffix != ".md":
                continue
            found = self.doc.find_list_breaks(path.read_text(encoding="utf-8"))
            self.assertEqual(found, [], f"{path.relative_to(ROOT)}: {found}")

    def test_nothing_names_the_origin_project_or_a_home_path(self):
        for path in text_files():
            text = path.read_text(encoding="utf-8").lower()
            self.assertEqual(forbidden_words(text, FORBIDDEN_HASHES), [],
                             f"{path.relative_to(ROOT)} names the reference project")
            self.assertNotIn(HOME_PATH, text, f"{path.relative_to(ROOT)} names a home path")

    def test_a_forbidden_word_is_found_by_its_hash(self):
        digest = hashlib.sha256(b"sample").hexdigest()
        self.assertEqual(forbidden_words("A Sample, then more.", {digest}), ["sample"])
        self.assertEqual(forbidden_words("Nothing here.", {digest}), [])


class SkillStructure:
    def frontmatter(self):
        text = self.form.skill_file.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        head, body = text[4:].split("\n---\n", 1)
        fields = dict(line.split(":", 1) for line in head.splitlines() if ":" in line)
        return {k.strip(): v.strip() for k, v in fields.items()}, body

    def test_the_frontmatter_has_the_required_fields(self):
        fields, _ = self.frontmatter()
        self.assertEqual(fields["name"], "total-recall")
        self.assertEqual(fields["disable-model-invocation"], "true")
        self.assertLess(len(fields["description"]), 1024)
        self.assertNotIn(" I ", " " + fields["description"] + " ")
        self.assertIn(self.form.command, fields["description"])

    def test_the_body_stays_under_500_lines(self):
        _, body = self.frontmatter()
        self.assertLess(len(body.splitlines()), 500)

    def test_every_placeholder_of_the_templates_is_known(self):
        render = load(self.form.scripts / "render.py", "render")
        pattern = re.compile(r"\{\{(\w+)\}\}")
        for path in self.form.templates.rglob("*"):
            if not path.is_file():
                continue
            names = set(pattern.findall(str(path.relative_to(self.form.templates))))
            if path.suffix in (".md", ".json", ".txt"):
                names |= set(pattern.findall(path.read_text(encoding="utf-8")))
            self.assertTrue(names <= set(render.PLACEHOLDERS), f"{path}: {names}")

    def test_the_expected_files_exist(self):
        missing = [name for name in COMMON_FILES + self.form.own_files if not (self.form.folder / name).is_file()]
        self.assertEqual(missing, [])
        self.assertTrue(self.form.readme.is_file())

    def test_no_template_is_named_like_a_context_file(self):
        # Claude Code loads a CLAUDE.md found in a subfolder, and Pi an AGENTS.md
        # of the working directory: a template under either name would be read
        # as instructions in this repository.
        for name in ("CLAUDE.md", "AGENTS.md"):
            found = [str(p.relative_to(self.form.folder)) for p in self.form.templates.rglob(name)]
            self.assertEqual(found, [])

    def test_the_note_on_the_project_file_is_gone(self):
        self.assertFalse((self.form.templates / "memory" / "project-instruction-file.md").exists())
        index = read_template(self.form, "memory/MEMORY.md")
        self.assertNotIn("project-instruction-file", index)

    def test_the_plan_points_to_the_project_file_for_the_goal_and_the_constraints(self):
        plan = read_template(self.form, "plan.md")
        self.assertNotIn("{{description}}", plan)
        self.assertNotIn("{{constraints}}", plan)
        goal = plan.split("## Goal", 1)[1].split("\n## ", 1)[0]
        constraints = plan.split("## Constraints", 1)[1].split("\n## ", 1)[0]
        self.assertIn(f"`{self.form.project_file}`", goal)
        self.assertIn(f"`{self.form.project_file}`", constraints)

    def test_the_start_routine_runs_the_start_script(self):
        project = read_template(self.form, self.form.template)
        routine = project[project.index("runs the start routine"):project.index("During the session")]
        self.assertIn("tools/start.py", routine)

    def test_the_style_note_is_in_the_index_and_pointed_to_by_the_rules(self):
        index = read_template(self.form, "memory/MEMORY.md")
        self.assertIn("(user-writing-style.md)", index)
        rules = read_template(self.form, "rules.md")
        self.assertIn("memory/user-writing-style.md", rules)
        note = read_template(self.form, "memory/user-writing-style.md")
        self.assertTrue(note.startswith(self.form.note_head), note[:40])
        self.assertEqual(len(re.findall(r"^\d+\. ", note, re.MULTILINE)), 14)

    def test_the_decisions_are_numbered_and_obsolete_is_in_the_table(self):
        decisions = read_template(self.form, "decisions.md")
        self.assertIn("\n## D1, {{date}}: ", decisions)
        self.assertNotIn("{{", decisions.split("\n## ", 1)[0])
        project = read_template(self.form, self.form.template)
        self.assertIn("| `obsolete.md` |", project)

    def test_the_project_file_names_the_command_of_the_form(self):
        project = read_template(self.form, self.form.template)
        self.assertIn(f"{self.form.command} backup", project)
        for form in FORMS:
            if form is not self.form:
                self.assertNotIn(form.command + " ", project)

    def test_the_names_of_the_phase_files_and_the_records_are_documented(self):
        self.assertIn("`phases/PNN-<name>.md`", read_template(self.form, "lifecycle.md"))
        self.assertIn("`PNN-<name>.md`", read_template(self.form, "plan.md"))
        self.assertIn("`RNNN-<name>.md`", read_template(self.form, "records/README.md"))
        self.assertIn("phases/P01-<slug>.md", skill_steps(self.form)["5"])
        self.assertIn("phases/P01-{{phase1_slug}}.md", read_template(self.form, "state.md"))
        for name in ("lifecycle.md", "plan.md", "state.md", "review.md"):
            self.assertNotIn("phase-NN", read_template(self.form, name), name)
            self.assertNotIn("phase-01", read_template(self.form, name), name)


class MachineFolder(unittest.TestCase):
    """The Claude Code form ships the settings snippet and the guard scripts."""

    def test_the_snippet_is_json_with_the_deny_list_and_the_hooks(self):
        data = json.loads((CLAUDE.folder / "machine" / "settings-guardrails.json").read_text(encoding="utf-8"))
        deny = set(data["permissions"]["deny"])
        for pattern in ("Bash(git commit*)", "Bash(git push*)", "Bash(sudo *)", "Bash(dd *)",
                        "Bash(mkfs*)", "Bash(shred *)"):
            self.assertIn(pattern, deny)
        commands = [h["command"] for e in data["hooks"]["PreToolUse"] for h in e["hooks"]]
        self.assertEqual(commands, ["$HOME/.claude/hooks/bash-guard.sh", "$HOME/.claude/hooks/git-guard.sh"])
        self.assertEqual(data["permissions"]["disableBypassPermissionsMode"], "disable")

    def test_the_snippet_reads_as_present_on_a_machine_that_has_it(self):
        with tempfile.TemporaryDirectory() as root:
            home = Path(root)
            (home / ".claude" / "hooks").mkdir(parents=True)
            for name in ("bash-guard.sh", "git-guard.sh", "guard-lib.sh"):
                target = home / ".claude" / "hooks" / name
                target.write_bytes((CLAUDE.folder / "machine" / "hooks" / name).read_bytes())
                target.chmod(0o755)
            (home / ".claude" / "settings.json").write_bytes(
                (CLAUDE.folder / "machine" / "settings-guardrails.json").read_bytes())
            result = subprocess.run([sys.executable, "-I", str(CLAUDE.tools / "machine-check.py"),
                                     "--home", root, "--managed", str(home / "none.json")],
                                    capture_output=True, text=True, env={"PATH": "", "HOME": root})
        for row in ("deny list: git writes", "deny list: sudo", "deny list: destructive tools",
                    "guard hooks on Bash"):
            self.assertIn(f"| {row} | present |", result.stdout)

    def test_the_scripts_have_a_shebang_and_run_their_help_path(self):
        for name in ("bash-guard.sh", "git-guard.sh"):
            script = CLAUDE.folder / "machine" / "hooks" / name
            self.assertTrue(script.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash"))
            self.assertTrue(os.access(script, os.X_OK), name)


class PiGuardrails(unittest.TestCase):
    """The Pi form has no machine folder: the guardrails are a memory note."""

    def test_the_pi_form_has_no_machine_folder(self):
        self.assertFalse((PI.folder / "machine").exists())

    def test_the_guardrails_note_is_in_the_index_and_named_by_the_skill(self):
        index = read_template(PI, "memory/MEMORY.md")
        self.assertIn("(guardrails.md)", index)
        note = read_template(PI, "memory/guardrails.md")
        for word in ("sudo", "push", ".git", "rm"):
            self.assertIn(word, note)
        self.assertIn("memory/guardrails.md", skill_steps(PI)["8"])
        self.assertIn("memory/guardrails.md", read_template(PI, "rules.md"))

    def test_the_pi_skill_writes_its_folder_as_skill_and_never_the_claude_variable(self):
        text = PI.skill_file.read_text(encoding="utf-8")
        self.assertIn("## How to read the commands", text)
        self.assertNotIn("CLAUDE_SKILL_DIR", text)
        self.assertGreaterEqual(text.count('"<skill>/'), 4)

    def test_the_pi_readme_installs_the_pi_folder(self):
        readme = PI.readme.read_text(encoding="utf-8")
        self.assertIn('ln -s "$(pwd)/skill-pi"', readme)
        self.assertIn("/skill:total-recall", readme)


class GitQuestion:
    def test_the_skill_asks_before_the_exclusion(self):
        steps = skill_steps(self.form)
        self.assertIn("Keep the folder out of git, yes or no?", steps["5"])
        self.assertTrue(steps["7"].split("\n", 1)[1].strip().startswith("Only when the user answered yes"))

    def test_no_template_states_how_git_treats_the_folder(self):
        for path in self.form.templates.rglob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in ("out of git", "does not track", "info/exclude", "not in git", "goes through git"):
                self.assertFalse(phrase in text, f"{path.relative_to(self.form.folder)} says {phrase!r}")


class WhenToAsk:
    def test_the_rules_say_when_to_ask_before_a_write(self):
        rules = read_template(self.form, "rules.md")
        self.assertIn("### When to ask before a write", rules)
        for label in ("**Written without asking**", "**Asked first**", "**When to ask**", "**A proposal**"):
            self.assertIn(label, rules)

    def test_the_project_file_points_to_the_rule_and_sets_the_size(self):
        project = read_template(self.form, self.form.template)
        self.assertIn('"When to ask before a write"', project)
        self.assertNotIn("becomes a memory note at once", project)
        self.assertIn("The size read at each start", project)
        self.assertIn("8,000 words", project)

    def test_the_close_asks_the_held_proposals_first(self):
        steps = re.findall(r"^(\d+)\. (.*)$", read_template(self.form, "close.md"), re.MULTILINE)
        self.assertEqual(steps[0][0], "1")
        self.assertTrue(steps[0][1].startswith("Ask the proposals held"), steps[0])


class Review:
    def test_the_review_is_named_in_the_project_file_and_the_skill(self):
        project = read_template(self.form, self.form.template)
        self.assertIn("| `review.md` |", project)
        self.assertIn('"review the memory"', project)
        self.assertIn("| `review.md` |", self.form.skill_file.read_text(encoding="utf-8"))

    def test_the_review_writes_a_report_before_any_change(self):
        review = read_template(self.form, "review.md")
        self.assertIn("records/RNNN-review.md", review)
        self.assertIn("Nothing is changed before the user approves", review)
        self.assertIn("doc-check.py\" --size", review)

    def test_the_check_mode_shows_the_plan_of_the_update(self):
        step = skill_steps(self.form)["2"]
        for needle in ('update.py" plan', f"{self.form.command} update", "review the memory"):
            self.assertIn(needle, step)
        for gone in ("--migrate-decisions", "diff -u", "cp "):
            self.assertNotIn(gone, step)

    def test_the_review_starts_with_what_the_session_holds(self):
        review = read_template(self.form, "review.md")
        self.assertIn("From this session", review)
        self.assertLess(review.index("From this session"), review.index("Read the whole folder"))

    def test_the_review_checks_the_memory_notes_where_their_rules_apply(self):
        review = read_template(self.form, "review.md")
        self.assertIn("The memory notes", review)
        self.assertIn("across the repository", review)

    def test_the_close_suggests_the_review_without_starting_it(self):
        self.assertIn("Suggest the review", read_template(self.form, "close.md"))


def prose(text):
    """The text without its fenced code blocks and its inline code."""
    text = re.sub(r"^\s*```.*?^\s*```", "", text, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


class Readme(unittest.TestCase):
    """The README of the repository, which describes the Claude Code form."""

    def readme(self):
        return (ROOT / "README.md").read_text(encoding="utf-8")

    def test_a_path_is_written_in_backticks(self):
        for path in (ROOT / "README.md", CLAUDE.skill_file, PI.skill_file, PI.readme):
            found = re.findall(r"<[A-Za-z][^>\n]*>", prose(path.read_text(encoding="utf-8")))
            self.assertEqual(found, [], f"{path.relative_to(ROOT)}: GitHub drops these as HTML tags")

    def test_the_folder_is_named_after_the_project(self):
        for path in (ROOT / "README.md", CLAUDE.skill_file, PI.skill_file, PI.readme):
            self.assertNotIn("<folder>", path.read_text(encoding="utf-8"), path.name)
        self.assertIn("internal-<project-name>", self.readme())

    def test_the_readme_does_not_talk_about_its_voice_or_state_the_git_choice(self):
        text = self.readme().lower()
        for phrase in ("voice", "does not track", "not in git", "keeps it out of git"):
            self.assertFalse(phrase in text, phrase)

    def test_the_readme_says_the_review_takes_in_the_session(self):
        self.assertIn("decided in the current session", self.readme())

    def test_the_readme_names_the_refusal(self):
        self.assertIn("another documentation system", self.readme())

    def test_the_readme_names_both_forms(self):
        text = self.readme()
        self.assertIn("skill-claude", text)
        self.assertIn("skill-pi", text)
        self.assertNotIn("`skill/`", text)

    def test_the_backup_folder_is_in_the_readme(self):
        text = self.readme()
        self.assertIn("| `backup/` |", text)
        self.assertNotIn("refuse to overwrite", text)


class StartPhrases:
    def setUp(self):
        self.check = load(self.form.tools / "machine-check.py", "machine_check")

    def test_the_machine_step_hands_over_the_line_the_check_looks_for(self):
        step = skill_steps(self.form)["8"]
        self.assertIn(self.check.START_LINE, step)
        self.assertIn(self.check.START_MARKER, self.check.START_LINE)
        self.assertIn("| start phrases |", step)

    def test_the_readme_names_the_line_and_not_a_mapping_that_does_not_exist(self):
        readme = self.form.readme.read_text(encoding="utf-8")
        self.assertNotIn("that maps it to the project file", readme)
        self.assertIn(self.check.START_MARKER, readme)


class AnotherSystem:
    def test_the_install_stops_on_another_documentation_system(self):
        step = skill_steps(self.form)["1"]
        for name in self.form.other_systems:
            self.assertIn(name, step)
        self.assertIn("another documentation system", step)
        self.assertIn("Move these files out of the project", step)

    def test_the_check_mode_stops_on_a_folder_the_skill_did_not_write(self):
        # The step is read without its line breaks: the two forms wrap it differently.
        step = " ".join(skill_steps(self.form)["2"].split())
        self.assertIn("head -n 1", step)
        self.assertIn("does not look like a total-recall folder", step)
        self.assertLess(step.index("does not look like a total-recall folder"), step.index("Otherwise, check the folder"))


class BackupAndUpdate:
    def skill(self):
        return self.form.skill_file.read_text(encoding="utf-8")

    def test_the_skill_has_the_two_commands(self):
        text = self.skill()
        for needle in (f"{self.form.command} backup", f"{self.form.command} update",
                       'update.py" backup', 'update.py" apply'):
            self.assertIn(needle, text)

    def test_the_skill_no_longer_refuses_to_overwrite(self):
        never = self.skill().split("## What this skill never does", 1)[1]
        self.assertNotIn("Overwrite an existing file", never)

    def test_the_backup_folder_is_in_the_tables(self):
        project = read_template(self.form, self.form.template)
        self.assertIn("| `backup/` |", project)
        self.assertIn("| `backup/` |", self.skill())
        readme = self.form.readme.read_text(encoding="utf-8")
        self.assertIn(f"{self.form.command} backup", readme)
        self.assertIn(f"{self.form.command} update", readme)


for_each_form(globals(), SkillStructure, GitQuestion, WhenToAsk, Review, StartPhrases,
              AnotherSystem, BackupAndUpdate)

if __name__ == "__main__":
    unittest.main()
