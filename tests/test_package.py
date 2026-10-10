import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill"
TEXT = (".md", ".py", ".sh", ".json", ".txt")
FORBIDDEN = ("oryx", "/home/")


def load(path, name):
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def text_files():
    files = [ROOT / "README.md"]
    files += [p for p in SKILL.rglob("*") if p.is_file() and p.suffix in TEXT]
    files += [p for p in (ROOT / "tests").glob("*.py")]
    return [p for p in files if p.exists()]



def skill_steps():
    """The numbered steps of SKILL.md, by number: the title line, then the body."""
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    parts = re.split(r"^## (\d+)\. ", text, flags=re.MULTILINE)
    return dict(zip(parts[1::2], parts[2::2]))

class WritingRules(unittest.TestCase):
    def setUp(self):
        self.doc = load(SKILL / "templates" / "tools" / "doc-check.py", "doc_check")

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
            if path.parent.name == "tests":
                continue
            text = path.read_text(encoding="utf-8").lower()
            for word in FORBIDDEN:
                self.assertNotIn(word, text, f"{path.relative_to(ROOT)} names {word!r}")


class SkillStructure(unittest.TestCase):
    def frontmatter(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
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

    def test_the_body_stays_under_500_lines(self):
        _, body = self.frontmatter()
        self.assertLess(len(body.splitlines()), 500)

    def test_every_placeholder_of_the_templates_is_known(self):
        render = load(SKILL / "scripts" / "render.py", "render")
        pattern = re.compile(r"\{\{(\w+)\}\}")
        for path in (SKILL / "templates").rglob("*"):
            if not path.is_file():
                continue
            names = set(pattern.findall(str(path.relative_to(SKILL / "templates"))))
            if path.suffix in (".md", ".json", ".txt"):
                names |= set(pattern.findall(path.read_text(encoding="utf-8")))
            self.assertTrue(names <= set(render.PLACEHOLDERS), f"{path}: {names}")

    def test_the_expected_files_exist(self):
        expected = ["SKILL.md", "scripts/render.py", "templates/CLAUDE.md", "templates/rules.md",
                    "templates/state.md", "templates/plan.md", "templates/phases/phase-01-{{phase1_slug}}.md",
                    "templates/history.md", "templates/story.md", "templates/decisions.md",
                    "templates/close.md", "templates/lifecycle.md", "templates/code-map.md",
                    "templates/records/README.md", "templates/tools/README.md",
                    "templates/tools/doc-check.py", "templates/tools/machine-check.py",
                    "templates/memory/MEMORY.md", "templates/memory/project-instruction-file.md",
                    "templates/memory/user-writing-style.md", "templates/obsolete.md",
                    "templates/review.md",
                    "machine/settings-guardrails.json", "machine/hooks/bash-guard.sh",
                    "machine/hooks/git-guard.sh", "machine/hooks/guard-lib.sh"]
        missing = [name for name in expected if not (SKILL / name).is_file()]
        self.assertEqual(missing, [])
        self.assertTrue((ROOT / "README.md").is_file())

    def test_the_style_note_is_in_the_index_and_pointed_to_by_the_rules(self):
        index = (SKILL / "templates" / "memory" / "MEMORY.md").read_text(encoding="utf-8")
        self.assertIn("(user-writing-style.md)", index)
        rules = (SKILL / "templates" / "rules.md").read_text(encoding="utf-8")
        self.assertIn("memory/user-writing-style.md", rules)
        note = (SKILL / "templates" / "memory" / "user-writing-style.md").read_text(encoding="utf-8")
        self.assertTrue(note.startswith("---\nname: user-writing-style\n"))
        self.assertEqual(len(re.findall(r"^\d+\. ", note, re.MULTILINE)), 18)


    def test_the_decisions_are_numbered_and_obsolete_is_in_the_table(self):
        decisions = (SKILL / "templates" / "decisions.md").read_text(encoding="utf-8")
        self.assertIn("\n## D1, {{date}}: ", decisions)
        self.assertNotIn("{{", decisions.split("\n## ", 1)[0])
        claude = (SKILL / "templates" / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("| `obsolete.md` |", claude)

class MachineFolder(unittest.TestCase):
    def test_the_snippet_is_json_with_the_deny_list_and_the_hooks(self):
        data = json.loads((SKILL / "machine" / "settings-guardrails.json").read_text(encoding="utf-8"))
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
                target.write_bytes((SKILL / "machine" / "hooks" / name).read_bytes())
                target.chmod(0o755)
            (home / ".claude" / "settings.json").write_bytes(
                (SKILL / "machine" / "settings-guardrails.json").read_bytes())
            result = subprocess.run([sys.executable, "-I", str(SKILL / "templates" / "tools" / "machine-check.py"),
                                     "--home", root, "--managed", str(home / "none.json")],
                                    capture_output=True, text=True, env={"PATH": "", "HOME": root})
        for row in ("deny list: git writes", "deny list: sudo", "deny list: destructive tools",
                    "guard hooks on Bash"):
            self.assertIn(f"| {row} | present |", result.stdout)

    def test_the_scripts_have_a_shebang_and_run_their_help_path(self):
        for name in ("bash-guard.sh", "git-guard.sh"):
            script = SKILL / "machine" / "hooks" / name
            self.assertTrue(script.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash"))
            self.assertTrue(os.access(script, os.X_OK), name)



class GitQuestion(unittest.TestCase):
    def test_the_skill_asks_before_the_exclusion(self):
        steps = skill_steps()
        self.assertIn("Keep the folder out of git, yes or no?", steps["5"])
        self.assertTrue(steps["7"].split("\n", 1)[1].strip().startswith("Only when the user answered yes"))

    def test_no_template_states_how_git_treats_the_folder(self):
        for path in (SKILL / "templates").rglob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in ("out of git", "does not track", "info/exclude", "not in git", "goes through git"):
                self.assertFalse(phrase in text, f"{path.relative_to(SKILL)} says {phrase!r}")


class WhenToAsk(unittest.TestCase):
    def read(self, name):
        return (SKILL / "templates" / name).read_text(encoding="utf-8")

    def test_the_rules_say_when_to_ask_before_a_write(self):
        rules = self.read("rules.md")
        self.assertIn("### When to ask before a write", rules)
        for label in ("**Written without asking**", "**Asked first**", "**When to ask**", "**A proposal**"):
            self.assertIn(label, rules)

    def test_the_project_file_points_to_the_rule_and_sets_the_size(self):
        claude = self.read("CLAUDE.md")
        self.assertIn('"When to ask before a write"', claude)
        self.assertNotIn("becomes a memory note at once", claude)
        self.assertIn("The size read at each start", claude)
        self.assertIn("8,000 words", claude)

    def test_the_close_asks_the_held_proposals_first(self):
        steps = re.findall(r"^(\d+)\. (.*)$", self.read("close.md"), re.MULTILINE)
        self.assertEqual(steps[0][0], "1")
        self.assertTrue(steps[0][1].startswith("Ask the proposals held"), steps[0])


class Review(unittest.TestCase):
    def read(self, name):
        return (SKILL / "templates" / name).read_text(encoding="utf-8")

    def test_the_review_is_named_in_the_project_file_and_the_skill(self):
        claude = self.read("CLAUDE.md")
        self.assertIn("| `review.md` |", claude)
        self.assertIn('"review the memory"', claude)
        self.assertIn("| `review.md` |", (SKILL / "SKILL.md").read_text(encoding="utf-8"))

    def test_the_review_writes_a_report_before_any_change(self):
        review = self.read("review.md")
        self.assertIn("records/YYYY-MM-DD-review.md", review)
        self.assertIn("Nothing is changed before the user approves", review)
        self.assertIn("doc-check.py\" --size", review)

    def test_the_check_mode_brings_an_older_folder_to_the_current_form(self):
        step = skill_steps()["2"]
        for needle in ("--migrate-decisions", "diff -u", "review the memory"):
            self.assertIn(needle, step)

    def test_the_close_suggests_the_review_without_starting_it(self):
        self.assertIn("Suggest the review", self.read("close.md"))


def prose(text):
    """The text without its fenced code blocks and its inline code."""
    text = re.sub(r"^\s*```.*?^\s*```", "", text, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


class Readme(unittest.TestCase):
    def test_a_path_is_written_in_backticks(self):
        for path in (ROOT / "README.md", SKILL / "SKILL.md"):
            found = re.findall(r"<[A-Za-z][^>\n]*>", prose(path.read_text(encoding="utf-8")))
            self.assertEqual(found, [], f"{path.name}: GitHub drops these as HTML tags")

    def test_the_folder_is_named_after_the_project(self):
        for path in (ROOT / "README.md", SKILL / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("<folder>", text, path.name)
        self.assertIn("internal-<project-name>", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_the_readme_does_not_talk_about_its_voice_or_state_the_git_choice(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        for phrase in ("voice", "does not track", "not in git", "keeps it out of git"):
            self.assertFalse(phrase in text, phrase)

if __name__ == "__main__":
    unittest.main()
