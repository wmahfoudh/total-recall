import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "skill" / "templates" / "tools" / "doc-check.py"
EM = chr(0x2014)
EN = chr(0x2013)


def load(path, name):
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TextRules(unittest.TestCase):
    def setUp(self):
        self.tool = load(TOOL, "doc_check")

    def test_a_dash_is_reported_with_its_line(self):
        found = self.tool.find_dashes(f"fine\nbad {EM} here\nalso {EN} bad\n")
        self.assertEqual([n for n, _ in found], [2, 3])

    def test_a_hyphen_is_not_a_dash(self):
        self.assertEqual(self.tool.find_dashes("a well-known case, 2 - 1\n"), [])

    def test_a_list_after_text_is_reported(self):
        found = self.tool.find_list_breaks("Some text\n- item\n")
        self.assertEqual([n for n, _ in found], [2])

    def test_a_list_after_a_heading_is_reported(self):
        found = self.tool.find_list_breaks("## Title\n1. item\n")
        self.assertEqual([n for n, _ in found], [2])

    def test_a_list_after_a_blank_line_is_fine(self):
        self.assertEqual(self.tool.find_list_breaks("Text\n\n- a\n- b\n"), [])

    def test_a_wrapped_list_item_belongs_to_the_list(self):
        text = "Text\n\n1. one that\n   wraps\n2. two\n"
        self.assertEqual(self.tool.find_list_breaks(text), [])

    def test_a_nested_list_belongs_to_the_list(self):
        text = "Text\n\n- a\n  - inside a\n- b\n"
        self.assertEqual(self.tool.find_list_breaks(text), [])

    def test_lines_inside_a_code_block_are_skipped(self):
        text = "Text\n```\nnot a list\n- looks like one\n| a | table |\n```\n"
        self.assertEqual(self.tool.find_list_breaks(text), [])

    def test_a_table_after_text_is_reported(self):
        found = self.tool.find_list_breaks("Text\n| a | b |\n|---|---|\n")
        self.assertEqual([n for n, _ in found], [2])

    def test_a_table_after_a_blank_line_is_fine(self):
        self.assertEqual(self.tool.find_list_breaks("Text\n\n| a |\n|---|\n| 1 |\n"), [])


MINIMAL = {
    "CLAUDE.md": "# P\n\n| File | What it holds |\n|---|---|\n| `state.md` | x |\n| `phases/` | y |\n",
    "state.md": "# State\n",
    "phases/phase-01-start.md": "# Phase 01: start\n\n### Task 1: first\n\n- [ ] **Step 1: a** b\n",
    "history.md": "# 07/10/2026 - The install\n\nA line.\n\n- a bullet\n",
    "memory/MEMORY.md": "- [Note](note.md): a note\n",
    "memory/note.md": "---\nname: note\n---\n\nText\n",
}


def make_folder(root, files):
    for name, text in files.items():
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def run_tool(folder):
    return subprocess.run([sys.executable, "-I", str(TOOL), str(folder)],
                          capture_output=True, text=True)


class FolderRules(unittest.TestCase):
    def check(self, extra=None, drop=()):
        files = dict(MINIMAL)
        files.update(extra or {})
        for name in drop:
            files.pop(name)
        with tempfile.TemporaryDirectory() as root:
            make_folder(root, files)
            result = run_tool(root)
        return result.returncode, result.stdout

    def test_a_clean_folder_is_clean(self):
        code, out = self.check()
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_missing_file_of_the_table_is_reported(self):
        code, out = self.check({"CLAUDE.md": MINIMAL["CLAUDE.md"] + "| `gone.md` | z |\n"})
        self.assertEqual(code, 1)
        self.assertIn("CLAUDE.md:7: gone.md is named in the table and does not exist", out)

    def test_a_file_of_the_table_may_live_at_the_repository_root(self):
        with tempfile.TemporaryDirectory() as repo:
            internal = Path(repo) / "internal-p"
            make_folder(internal, {"CLAUDE.md": MINIMAL["CLAUDE.md"] + "| `CHANGELOG.md` | z |\n"})
            make_folder(internal, {k: v for k, v in MINIMAL.items() if k != "CLAUDE.md"})
            (Path(repo) / "CHANGELOG.md").write_text("# Log\n", encoding="utf-8")
            result = run_tool(internal)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_task_number_used_twice_is_reported(self):
        code, out = self.check({"phases/phase-02-next.md": "# Phase 02: next\n\n### Task 1: again\n"})
        self.assertEqual(code, 1)
        self.assertIn("phases/phase-02-next.md:3: Task 1 is already in phase-01-start.md", out)

    def test_task_numbers_must_grow_inside_a_file(self):
        text = "# Phase 01: start\n\n### Task 5: a\n\n### Task 3: b\n"
        code, out = self.check({"phases/phase-01-start.md": text})
        self.assertIn("phases/phase-01-start.md:5: Task 3 does not follow Task 5", out)

    def test_task_numbers_are_compared_as_numbers(self):
        text = "# Phase 01: start\n\n### Task 9: a\n\n### Task 10: b\n"
        code, out = self.check({"phases/phase-01-start.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_task_named_in_prose_is_not_counted(self):
        text = "# Phase 01: start\n\n### Task 2: a\n\nAs Task 1 showed, and Task 7 will.\n"
        code, out = self.check({"phases/phase-01-start.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_ticked_step_needs_its_done_mark(self):
        text = "# Phase 01: start\n\n### Task 1: a\n\n- [x] **Step 1: a** b\n"
        code, out = self.check({"phases/phase-01-start.md": text})
        self.assertIn("phases/phase-01-start.md:5: a ticked step needs 'Done DD/MM/YYYY:' and what happened", out)

    def test_a_done_mark_on_a_wrapped_line_counts(self):
        text = "# Phase 01: start\n\n### Task 1: a\n\n- [x] **Step 1: a** b\n  Done 07/10/2026: it worked.\n"
        code, out = self.check({"phases/phase-01-start.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_done_mark_wrapped_at_the_line_break_counts(self):
        text = "# Phase 01: start\n\n### Task 1: a\n\n- [x] **Step 1: a** b. Done\n  07/10/2026: it worked.\n"
        code, out = self.check({"phases/phase-01-start.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_long_state_file_is_reported(self):
        code, out = self.check({"state.md": "# State\n" + "line\n" * 150})
        self.assertIn("state.md:151: state.md has 151 lines, over 150", out)

    def test_a_history_title_in_another_form_is_reported(self):
        for title in ("# 2026-10-07 - x", "# 7/10/2026 - x", "# The install"):
            code, out = self.check({"history.md": title + "\n"})
            self.assertIn("history.md:1: a history entry starts with '# DD/MM/YYYY - <name>'", out, title)

    def test_a_history_title_with_a_qualifier_after_the_date_is_fine(self):
        code, out = self.check({"history.md": "# 07/10/2026, later - The second session\n"})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_note_missing_from_the_index_is_reported(self):
        code, out = self.check({"memory/other.md": "---\nname: other\n---\n\nText\n"})
        self.assertIn("memory/MEMORY.md:0: the note other.md is not in the index", out)

    def test_an_index_line_without_its_note_is_reported(self):
        code, out = self.check(drop=("memory/note.md",))
        self.assertIn("memory/MEMORY.md:0: the index names note.md, which does not exist", out)

    def test_a_file_that_is_not_utf8_is_reported_by_name(self):
        with tempfile.TemporaryDirectory() as root:
            make_folder(root, MINIMAL)
            (Path(root) / "story.md").write_bytes("caf\xe9\n".encode("latin-1"))
            result = run_tool(root)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("story.md:0: not UTF-8", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_only_the_table_of_documents_is_checked_for_files(self):
        routines = "\n## The project's own routines\n\n| Routine | File | When |\n|---|---|---|\n| `release` | `records/release.md` | before a tag |\n"
        code, out = self.check({"CLAUDE.md": MINIMAL["CLAUDE.md"] + routines})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_the_records_folder_is_skipped(self):
        code, out = self.check({"records/log.md": f"pasted {EM} as is\nText\n- list\n"})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_decision_title_in_another_form_is_reported(self):
        code, out = self.check({"decisions.md": "# Decisions\n\n## 07/10/2026: old form\n\nText.\n"})
        self.assertEqual(code, 1)
        self.assertIn("decisions.md:3: a decision starts with '## Dn, DD/MM/YYYY: <name>'", out)

    def test_decisions_must_come_newest_first(self):
        text = "# Decisions\n\n## D1, 07/10/2026: a\n\nText.\n\n## D2, 08/10/2026: b\n\nText.\n"
        code, out = self.check({"decisions.md": text})
        self.assertIn("decisions.md:7: D2 is below D1: the newest decision comes first", out)

    def test_decisions_newest_first_are_clean(self):
        text = "# Decisions\n\n## D2, 08/10/2026: b\n\nText.\n\n## D1, 07/10/2026: a\n\nText.\n"
        code, out = self.check({"decisions.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_title_inside_a_code_block_is_not_a_decision(self):
        text = "# Decisions\n\n## D1, 07/10/2026: a\n\n```\n## not a title\n```\n"
        code, out = self.check({"decisions.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_an_obsolete_decision_needs_its_replaced_line(self):
        text = "# Obsolete decisions\n\n## D1, 07/10/2026: a\n\nText.\n"
        code, out = self.check({"obsolete.md": text})
        self.assertIn("obsolete.md:3: an obsolete decision needs 'Replaced by Dn on DD/MM/YYYY.' under its title", out)

    def test_obsolete_decisions_most_recently_replaced_first_are_clean_with_any_numbers(self):
        text = ("# Obsolete decisions\n\n## D1, 07/10/2026: a\n\nReplaced by D4 on 10/10/2026.\n\nText.\n\n"
                "## D3, 08/10/2026: b\n\nReplaced by D5 on 09/10/2026.\n\nText.\n")
        code, out = self.check({"obsolete.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_obsolete_decisions_must_come_most_recently_replaced_first(self):
        text = ("# Obsolete decisions\n\n## D3, 08/10/2026: b\n\nReplaced by D5 on 09/10/2026.\n\nText.\n\n"
                "## D1, 07/10/2026: a\n\nReplaced by D4 on 10/10/2026.\n\nText.\n")
        code, out = self.check({"obsolete.md": text})
        self.assertIn("obsolete.md:9: this decision was replaced after the one above it: "
                      "the most recently replaced comes first", out)

    def test_a_size_over_the_limit_is_reported(self):
        claude = MINIMAL["CLAUDE.md"] + "\nThe size read at each start: 60 words at most.\n"
        code, out = self.check({"CLAUDE.md": claude, "state.md": "# State\n\n" + "word " * 60 + "\n"})
        self.assertEqual(code, 1)
        self.assertRegex(out, r"CLAUDE\.md:0: the files read at each start hold \d+ words, over the limit of 60")

    def test_the_limit_may_be_written_with_a_comma(self):
        claude = MINIMAL["CLAUDE.md"] + "\nThe size read at each start: 1,000 words at most.\n"
        code, out = self.check({"CLAUDE.md": claude, "state.md": "# State\n\n" + "word " * 900 + "\n"})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_the_default_limit_is_8000_words(self):
        code, out = self.check({"state.md": "# State\n\n" + "word " * 8001 + "\n"})
        self.assertRegex(out, r"over the limit of 8000")

    def test_the_size_option_prints_the_size_before_the_findings(self):
        with tempfile.TemporaryDirectory() as root:
            make_folder(root, MINIMAL)
            result = subprocess.run([sys.executable, "-I", str(TOOL), "--size", root],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"^read at each start: \d+ words, limit 8000\n")
        self.assertEqual(result.stdout.strip().splitlines()[-1], "clean")

    def test_a_missing_folder_is_a_usage_error(self):
        result = run_tool("/nonexistent/folder")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
