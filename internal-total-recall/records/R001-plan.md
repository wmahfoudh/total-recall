# Total recall: the implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `/total-recall` skill: a package that installs a project memory system in `internal-<folder>/`, kept out of git, with the documents, the routines, two tools and the portable rules.

**Architecture:** The skill is a folder of templates, two Python tools and a render script, driven by `SKILL.md`. The tools and the render script are tested with `unittest`. The templates are tested by rendering them with sample answers and running the document check on the result.

**Tech Stack:** Markdown, Python 3 (standard library only), bash for the three guard scripts, Claude Code skills.

**Spec:** `<the session scratchpad>/2026-10-07-total-recall-design.md`

## Global Constraints

- No em dash and no en dash in any file of the repository. A hyphen is fine.
- A blank line before every list and every table, in every Markdown file.
- All the text follows the user's writing rules: plain English, the software as the actor, short sentences, modest claims, no slogan, no private vocabulary. The README and the templates are read by the user, so they follow the user's own style in full.
- No reference to the reference project, to this machine or to a home path anywhere in `skill/` and in `README.md`. `machine/` carries the guard scripts as they are.
- Python 3 with the standard library only, so the tools run anywhere.
- Dates are written `DD/MM/YYYY`.
- The session runs no git command that writes, writes nothing under `.claude/`, and writes nothing outside the project except in its scratchpad. Each task ends with the git line for the user.
- The skill never overwrites an existing file.
- `SKILL.md` stays under 500 lines, and its frontmatter has `name`, `description` (third person, under 1024 characters) and `disable-model-invocation: true`.
- The test command is `python3 -m unittest discover -s tests -v`, run from the repository root.

## Review Focus

1. A project folder with a space or capitals in its name (`My Project`): the render keeps the name verbatim in every placeholder, and the exclusion line printed by the skill carries it verbatim. Test in Task 5.
2. `### Task 10:` after `### Task 9:` in a phase file: the order is checked on integers, not on strings, so it is not reported. Test in Task 2.
3. A fenced code block that holds a line starting with `- ` or `|` right after a sentence: not a list, not reported. Test in Task 1.
4. A settings file that is absent or is not JSON: `machine-check.py` reports the guardrail as missing and does not crash. Test in Task 3.
5. A second run of the render on a folder that already has files: every existing file is kept byte for byte and only the missing files are added. Test in Task 5.

---

## File structure

```
total-recall/
  README.md                          what total recall is, the install, the use, the limits
  skill/
    SKILL.md                         the frontmatter and the nine steps of /total-recall
    scripts/
      render.py                      writes the internal folder from the templates
    templates/
      CLAUDE.md                      the project file
      rules.md                       the portable rules
      state.md
      plan.md
      phases/phase-01-{{phase1_slug}}.md
      history.md
      story.md
      decisions.md
      close.md
      lifecycle.md
      code-map.md
      records/README.md
      tools/README.md
      tools/doc-check.py             checks the documents of an internal folder
      tools/machine-check.py         reports the guardrails of the machine
      memory/MEMORY.md
      memory/project-instruction-file.md
    machine/
      settings-guardrails.json       the deny list and the hook entries for ~/.claude/settings.json
      hooks/bash-guard.sh
      hooks/git-guard.sh
      hooks/guard-lib.sh
  tests/
    test_doc_check.py
    test_machine_check.py
    test_render.py
    test_package.py                  the writing rules and the skill structure, over the whole package
```

Each file has one owner. The tools are standalone files, copied into each project by the render. The tests live outside `skill/`, so the installed skill stays lean.

The placeholders of the templates, written `{{name}}`, in file names and in text: `project`, `internal`, `date`, `description`, `constraints`, `phase1_name`, `phase1_slug`, `phase1_goal`, `task1_name`.

---

### Task 1: The document check, the text rules

**Files:**

- Create: `skill/templates/tools/doc-check.py`
- Test: `tests/test_doc_check.py`

**Interfaces:**

- Produces: in `doc-check.py`, `find_dashes(text) -> list[tuple[int, str]]`, `find_list_breaks(text) -> list[tuple[int, str]]`, `is_list(line) -> bool`, `is_table(line) -> bool`. Each tuple is the line number (from 1) and a message. Task 4 reuses these functions for the package test.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_doc_check.py
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and see them fail**

Run: `python3 -m unittest tests.test_doc_check -v`
Expected: every test errors with `FileNotFoundError` or `AttributeError`, since the tool does not exist.

- [ ] **Step 3: Write the tool with the two text checks**

```python
#!/usr/bin/env python3
"""Checks the documents of an internal folder.

Usage: python3 doc-check.py <internal folder>

Prints one line per finding, "path:line: message", then a count. Exits
with 1 when it found something, 0 when the documents are clean, 2 on a
usage error. Python 3 with the standard library only.

The records folder is skipped: a record is kept as it was received.
"""
import re
import sys
from pathlib import Path

DASHES = {chr(0x2014): "an em dash", chr(0x2013): "an en dash"}
LIST_RE = re.compile(r"^\s*([-*+]|\d+\.)\s")


def is_list(line):
    return bool(LIST_RE.match(line))


def is_table(line):
    return line.lstrip().startswith("|")


def find_dashes(text):
    """The line number and a message for each line that holds a dash."""
    found = []
    for number, line in enumerate(text.split("\n"), 1):
        for char, name in DASHES.items():
            if char in line:
                found.append((number, f"{name}, write a comma, a colon or a new sentence"))
    return found


def find_list_breaks(text):
    """A list line or a table line that follows a line of text.

    A blank line must come before a list or a table. An indented line
    after a list item belongs to the list. The lines of a fenced code
    block are skipped.
    """
    found = []
    lines = text.split("\n")
    in_block = False
    in_code = False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            in_block = False
            continue
        if in_code:
            continue
        if not line.strip():
            in_block = False
            continue
        continuation = in_block and line.startswith("  ")
        if is_list(line) or is_table(line):
            previous = lines[number - 2] if number > 1 else ""
            opens_block = previous.strip() and not in_block
            after_fence = previous.lstrip().startswith("```")
            if opens_block and not is_table(previous) and not after_fence:
                found.append((number, "a list or a table needs a blank line before it"))
            in_block = True
        elif not continuation:
            in_block = False
    return found


def main(argv):
    if len(argv) != 2 or not Path(argv[1]).is_dir():
        print("usage: doc-check.py <internal folder>", file=sys.stderr)
        return 2
    findings = check_folder(argv[1])
    for line in findings:
        print(line)
    if findings:
        print(f"{len(findings)} finding(s)")
        return 1
    print("clean")
    return 0


def check_folder(folder):
    """The findings of the folder, one string each. Filled in Task 2."""
    folder = Path(folder)
    findings = []
    for path in sorted(folder.rglob("*.md")):
        if "records" in path.relative_to(folder).parts:
            continue
        text = path.read_text(encoding="utf-8")
        for number, message in find_dashes(text) + find_list_breaks(text):
            findings.append(f"{path.relative_to(folder)}:{number}: {message}")
    return findings


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `python3 -m unittest tests.test_doc_check -v`
Expected: `OK`, 10 tests.

- [ ] **Step 5: The git line, for the user**

```
git add skill/templates/tools/doc-check.py tests/test_doc_check.py
git commit -m "feat: document check with the dash and the blank line rules"
```

### Task 2: The document check, the structure rules

**Files:**

- Modify: `skill/templates/tools/doc-check.py` (add the functions below and extend `check_folder`)
- Test: `tests/test_doc_check.py` (add the class `FolderRules`)

**Interfaces:**

- Consumes: `is_list`, `is_table` from Task 1.
- Produces: `check_folder(folder) -> list[str]` complete, each string `path:line: message` with the path relative to the folder; the command line `python3 doc-check.py <folder>` with exit codes 0, 1 and 2. `DATE_RE`, the pattern of a date `DD/MM/YYYY`. Task 5 and Task 12 run the command on rendered folders.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_doc_check.py`:

```python
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
        self.assertIn("CLAUDE.md:6: gone.md is named in the table and does not exist", out)

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

    def test_a_long_state_file_is_reported(self):
        code, out = self.check({"state.md": "# State\n" + "line\n" * 150})
        self.assertIn("state.md:151: state.md has 151 lines, over 150", out)

    def test_a_history_title_in_another_form_is_reported(self):
        for title in ("# 2026-10-07 - x", "# 7/10/2026 - x", "# The install"):
            code, out = self.check({"history.md": title + "\n"})
            self.assertIn("history.md:1: a history entry starts with '# DD/MM/YYYY - <name>'", out, title)

    def test_a_note_missing_from_the_index_is_reported(self):
        code, out = self.check({"memory/other.md": "---\nname: other\n---\n\nText\n"})
        self.assertIn("memory/MEMORY.md:0: the note other.md is not in the index", out)

    def test_an_index_line_without_its_note_is_reported(self):
        code, out = self.check(drop=("memory/note.md",))
        self.assertIn("memory/MEMORY.md:0: the index names note.md, which does not exist", out)

    def test_the_records_folder_is_skipped(self):
        code, out = self.check({"records/log.md": f"pasted {EM} as is\nText\n- list\n"})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_missing_folder_is_a_usage_error(self):
        result = run_tool("/nonexistent/folder")
        self.assertEqual(result.returncode, 2)
```

- [ ] **Step 2: Run the tests and see them fail**

Run: `python3 -m unittest tests.test_doc_check -v`
Expected: the `FolderRules` tests fail: the clean folder passes by chance, the others report nothing where a finding is expected.

- [ ] **Step 3: Write the structure checks**

Add to `doc-check.py`, above `main`, and replace `check_folder`:

```python
DATE_RE = r"\d{2}/\d{2}/\d{4}"
TASK_RE = re.compile(r"^### Task (\d+):")
DONE_STEP_RE = re.compile(r"^\s*- \[x\]", re.IGNORECASE)
DONE_MARK_RE = re.compile(r"Done " + DATE_RE + ":")
HISTORY_TITLE_RE = re.compile(r"^# " + DATE_RE + r" - \S")
STATE_MAX_LINES = 150


def check_documents_table(folder, text):
    """Each file named in the table of documents of CLAUDE.md exists.

    A name is looked for in the folder, then at the root of the
    repository, for a public file that a project's own routine names.
    """
    found = []
    for number, line in enumerate(text.split("\n"), 1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or not cells[0].startswith("`"):
            continue
        name = cells[0].strip("`")
        if not (folder / name).exists() and not (folder.parent / name).exists():
            found.append((number, f"{name} is named in the table and does not exist"))
    return found


def check_tasks(phase_files):
    """Task numbers are unique across the phase files and grow inside each."""
    found = []
    seen = {}
    for path in phase_files:
        last = 0
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            match = TASK_RE.match(line)
            if not match:
                continue
            task = int(match.group(1))
            if task in seen:
                found.append((path, number, f"Task {task} is already in {seen[task]}"))
            else:
                seen[task] = path.name
            if task <= last:
                found.append((path, number, f"Task {task} does not follow Task {last}"))
            last = max(last, task)
    return found


def check_done_steps(text):
    """A ticked step carries 'Done DD/MM/YYYY:' on its line or its continuation."""
    found = []
    lines = text.split("\n")
    for number, line in enumerate(lines, 1):
        if not DONE_STEP_RE.match(line):
            continue
        block = [line]
        for following in lines[number:]:
            if following.startswith("  ") and not is_list(following):
                block.append(following)
            else:
                break
        if not DONE_MARK_RE.search(" ".join(block)):
            found.append((number, "a ticked step needs 'Done DD/MM/YYYY:' and what happened"))
    return found


def check_state(text):
    count = len(text.rstrip("\n").split("\n"))
    if count > STATE_MAX_LINES:
        return [(count, f"state.md has {count} lines, over {STATE_MAX_LINES}")]
    return []


def check_history(text):
    found = []
    for number, line in enumerate(text.split("\n"), 1):
        if line.startswith("# ") and not HISTORY_TITLE_RE.match(line):
            found.append((number, "a history entry starts with '# DD/MM/YYYY - <name>'"))
    return found


def check_memory(folder):
    """Each note is in the index, and each index line names a note."""
    memory = folder / "memory"
    index = memory / "MEMORY.md"
    if not index.exists():
        return [(index, 0, "memory/MEMORY.md is missing")]
    listed = set(re.findall(r"\]\(([^)]+\.md)\)", index.read_text(encoding="utf-8")))
    notes = {path.name for path in memory.glob("*.md")} - {"MEMORY.md"}
    found = []
    for name in sorted(notes - listed):
        found.append((index, 0, f"the note {name} is not in the index"))
    for name in sorted(listed - notes):
        found.append((index, 0, f"the index names {name}, which does not exist"))
    return found


def check_folder(folder):
    """The findings of the folder, one string each: path:line: message."""
    folder = Path(folder)
    findings = []

    def add(path, number, message):
        findings.append(f"{path.relative_to(folder)}:{number}: {message}")

    for path in sorted(folder.rglob("*.md")):
        if "records" in path.relative_to(folder).parts:
            continue
        text = path.read_text(encoding="utf-8")
        for number, message in find_dashes(text) + find_list_breaks(text):
            add(path, number, message)
    claude = folder / "CLAUDE.md"
    if claude.exists():
        for number, message in check_documents_table(folder, claude.read_text(encoding="utf-8")):
            add(claude, number, message)
    else:
        findings.append("CLAUDE.md:0: CLAUDE.md is missing")
    phases_dir = folder / "phases"
    phases = sorted(phases_dir.glob("phase-*.md")) if phases_dir.is_dir() else []
    for path in phases:
        for number, message in check_done_steps(path.read_text(encoding="utf-8")):
            add(path, number, message)
    for path, number, message in check_tasks(phases):
        add(path, number, message)
    state = folder / "state.md"
    if state.exists():
        for number, message in check_state(state.read_text(encoding="utf-8")):
            add(state, number, message)
    history = folder / "history.md"
    if history.exists():
        for number, message in check_history(history.read_text(encoding="utf-8")):
            add(history, number, message)
    for path, number, message in check_memory(folder):
        add(path, number, message)
    return findings
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `python3 -m unittest tests.test_doc_check -v`
Expected: `OK`, 25 tests.

- [ ] **Step 5: Run the tool on the the reference project folder, read only, as a trial**

Run: `python3 -I skill/templates/tools/doc-check.py <the reference folder> | tail -5`
Expected: findings (the the reference project documents follow other conventions: a table of documents that names files at its root, no `Done` marks, a long state file). Read five of them to check that each is true. Nothing is written there.

- [ ] **Step 6: The git line, for the user**

```
git add skill/templates/tools/doc-check.py tests/test_doc_check.py
git commit -m "feat: document check with the table, the numbers, the steps and the memory index"
```

### Task 3: The machine check

**Files:**

- Create: `skill/templates/tools/machine-check.py`
- Test: `tests/test_machine_check.py`

**Interfaces:**

- Produces: `report(home, managed) -> list[tuple[str, str, str]]`, rows of (guardrail, "present" or "missing", where); `render_table(rows) -> str`; the command line `python3 machine-check.py [--home DIR] [--managed FILE]`, exit 0 always. The rows, in order: `global rules file`, `deny list: git writes`, `deny list: sudo`, `deny list: destructive tools`, `guard hooks on Bash`, `jq`, `sandbox`. Task 10 (SKILL.md) reads this table.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_machine_check.py
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "skill" / "templates" / "tools" / "machine-check.py"

DENY = ["Bash(sudo *)", "Bash(sudo)", "Bash(git commit*)", "Bash(git push*)",
        "Bash(dd *)", "Bash(mkfs*)", "Bash(shred *)"]


def run_tool(home, managed, path=""):
    env = {"PATH": path, "HOME": str(home)}
    return subprocess.run([sys.executable, "-I", str(TOOL), "--home", str(home),
                           "--managed", str(managed)], capture_output=True, text=True, env=env)


def rows_of(output):
    rows = {}
    for line in output.splitlines()[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[cells[0]] = (cells[1], cells[2])
    return rows


class MachineCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        (self.home / ".claude").mkdir(parents=True)
        self.managed = Path(self.tmp.name) / "managed.json"

    def tearDown(self):
        self.tmp.cleanup()

    def write_settings(self, data):
        (self.home / ".claude" / "settings.json").write_text(json.dumps(data), encoding="utf-8")

    def test_an_empty_machine_reports_everything_missing(self):
        result = run_tool(self.home, self.managed)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = rows_of(result.stdout)
        self.assertEqual(set(rows), {"global rules file", "deny list: git writes", "deny list: sudo",
                                     "deny list: destructive tools", "guard hooks on Bash", "jq", "sandbox"})
        self.assertTrue(all(status == "missing" for status, _ in rows.values()), rows)

    def test_a_settings_file_that_is_not_json_is_missing_not_a_crash(self):
        (self.home / ".claude" / "settings.json").write_text("{not json", encoding="utf-8")
        self.managed.write_text("", encoding="utf-8")
        result = run_tool(self.home, self.managed)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows_of(result.stdout)["deny list: sudo"][0], "missing")

    def test_the_deny_list_is_found_in_the_managed_settings(self):
        self.managed.write_text(json.dumps({"permissions": {"deny": DENY}}), encoding="utf-8")
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["deny list: git writes"], ("present", "managed settings"))
        self.assertEqual(rows["deny list: sudo"], ("present", "managed settings"))
        self.assertEqual(rows["deny list: destructive tools"], ("present", "managed settings"))

    def test_the_deny_list_is_found_in_the_user_settings(self):
        self.write_settings({"permissions": {"deny": DENY}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["deny list: git writes"], ("present", "~/.claude/settings.json"))

    def test_a_partial_deny_list_reports_what_is_missing(self):
        self.write_settings({"permissions": {"deny": ["Bash(git commit*)", "Bash(git push*)"]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["deny list: git writes"][0], "present")
        self.assertEqual(rows["deny list: sudo"][0], "missing")

    def test_the_rules_file_is_found(self):
        (self.home / ".claude" / "CLAUDE.md").write_text("# Rules\n", encoding="utf-8")
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["global rules file"][0], "present")

    def test_a_hook_counts_when_its_script_exists_and_runs(self):
        hooks = self.home / ".claude" / "hooks"
        hooks.mkdir()
        script = hooks / "git-guard.sh"
        script.write_text("#!/bin/sh\n", encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        self.write_settings({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": "$HOME/.claude/hooks/git-guard.sh"}]}]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["guard hooks on Bash"], ("present", "~/.claude/settings.json: git-guard.sh"))

    def test_a_hook_whose_script_is_not_executable_is_missing(self):
        hooks = self.home / ".claude" / "hooks"
        hooks.mkdir()
        (hooks / "git-guard.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        self.write_settings({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": "~/.claude/hooks/git-guard.sh"}]}]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["guard hooks on Bash"][0], "missing")

    def test_jq_is_looked_up_on_the_path(self):
        bin_dir = Path(self.tmp.name) / "bin"
        bin_dir.mkdir()
        jq = bin_dir / "jq"
        jq.write_text("#!/bin/sh\n", encoding="utf-8")
        jq.chmod(jq.stat().st_mode | stat.S_IXUSR)
        rows = rows_of(run_tool(self.home, self.managed, path=str(bin_dir)).stdout)
        self.assertEqual(rows["jq"], ("present", str(jq)))

    def test_the_sandbox_is_read_from_either_file(self):
        self.managed.write_text(json.dumps({"sandbox": {"enabled": True}}), encoding="utf-8")
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["sandbox"], ("present", "managed settings"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and see them fail**

Run: `python3 -m unittest tests.test_machine_check -v`
Expected: every test errors, the tool does not exist.

- [ ] **Step 3: Write the tool**

```python
#!/usr/bin/env python3
"""Reports the guardrails of this machine for Claude Code sessions.

Usage: python3 machine-check.py [--home DIR] [--managed FILE]

Prints a table with a row per guardrail: present or missing, and where
it was found. Reads the user settings, the managed settings, the hook
scripts and the PATH. Changes nothing. Exits 0.
"""
import argparse
import json
import os
import shutil
from pathlib import Path

GIT_WRITE_PATTERNS = {"Bash(git commit*)", "Bash(git push*)"}
SUDO_PATTERNS = {"Bash(sudo *)", "Bash(sudo)"}
DESTRUCTIVE_PATTERNS = {"Bash(dd *)", "Bash(mkfs*)", "Bash(shred *)"}
MANAGED_DEFAULT = "/etc/claude-code/managed-settings.json"


def read_json(path):
    """The parsed file, or None when it is absent or is not JSON."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def deny_list(settings):
    return list(((settings or {}).get("permissions") or {}).get("deny") or [])


def bash_hooks(settings):
    """The commands of the PreToolUse hooks that match the Bash tool."""
    commands = []
    for entry in ((settings or {}).get("hooks") or {}).get("PreToolUse") or []:
        if entry.get("matcher") not in ("Bash", "", None):
            continue
        for hook in entry.get("hooks") or []:
            if hook.get("type") == "command" and hook.get("command"):
                commands.append(hook["command"])
    return commands


def script_of(command, home):
    """The path of the script a hook command runs, with ~ and $HOME expanded."""
    first = command.split()[0]
    first = first.replace("$HOME", str(home)).replace("${HOME}", str(home))
    if first.startswith("~"):
        first = str(home) + first[1:]
    return Path(first)


def report(home, managed):
    home = Path(home)
    sources = [("~/.claude/settings.json", read_json(home / ".claude" / "settings.json")),
               ("managed settings", read_json(managed))]
    rows = []
    rules = home / ".claude" / "CLAUDE.md"
    rows.append(("global rules file", "present" if rules.is_file() else "missing",
                 str(rules) if rules.is_file() else ""))
    denies = [(name, pattern) for name, settings in sources for pattern in deny_list(settings)]
    for label, patterns in (("deny list: git writes", GIT_WRITE_PATTERNS),
                            ("deny list: sudo", SUDO_PATTERNS),
                            ("deny list: destructive tools", DESTRUCTIVE_PATTERNS)):
        where = sorted({name for name, pattern in denies if pattern in patterns})
        rows.append((label, "present" if where else "missing", ", ".join(where)))
    good = []
    for name, settings in sources:
        for command in bash_hooks(settings):
            script = script_of(command, home)
            if script.is_file() and os.access(script, os.X_OK):
                good.append(f"{name}: {script.name}")
    rows.append(("guard hooks on Bash", "present" if good else "missing", ", ".join(good)))
    jq = shutil.which("jq")
    rows.append(("jq", "present" if jq else "missing", jq or ""))
    sandbox = [name for name, settings in sources if ((settings or {}).get("sandbox") or {}).get("enabled")]
    rows.append(("sandbox", "present" if sandbox else "missing", ", ".join(sandbox)))
    return rows


def render_table(rows):
    lines = ["| Guardrail | Status | Where |", "|---|---|---|"]
    for name, status, where in rows:
        lines.append(f"| {name} | {status} | {where} |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reports the guardrails of this machine.")
    parser.add_argument("--home", default=os.path.expanduser("~"))
    parser.add_argument("--managed", default=MANAGED_DEFAULT)
    args = parser.parse_args(argv)
    print(render_table(report(args.home, args.managed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `python3 -m unittest tests.test_machine_check -v`
Expected: `OK`, 10 tests.

- [ ] **Step 5: Run the tool on this machine**

Run: `python3 -I skill/templates/tools/machine-check.py`
Expected: seven rows. On this machine the three deny rows, the hooks row and the sandbox row read `present` with `managed settings`, the rules file row reads `present`, and `jq` reads `present` with its path. Compare with `/etc/claude-code/managed-settings.json` by eye.

- [ ] **Step 6: The git line, for the user**

```
git add skill/templates/tools/machine-check.py tests/test_machine_check.py
git commit -m "feat: machine check reports the guardrails of a machine"
```

### Task 4: The package test, the writing rules over the whole package

**Files:**

- Create: `tests/test_package.py`

**Interfaces:**

- Consumes: `find_dashes`, `find_list_breaks` from `doc-check.py` (loaded by path), `PLACEHOLDERS` from `render.py` (Task 5; until then the placeholder test fails, which is expected).
- Produces: the test that every later task runs after writing a file.

- [ ] **Step 1: Write the tests**

```python
# tests/test_package.py
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skill"
TEXT = (".md", ".py", ".sh", ".json", ".txt")
FORBIDDEN = ("the reference project", "/home/")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def text_files():
    files = [ROOT / "README.md"]
    files += [p for p in SKILL.rglob("*") if p.is_file() and p.suffix in TEXT]
    files += [p for p in (ROOT / "tests").glob("*.py")]
    return [p for p in files if p.exists()]


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
                    "machine/settings-guardrails.json", "machine/hooks/bash-guard.sh",
                    "machine/hooks/git-guard.sh", "machine/hooks/guard-lib.sh"]
        missing = [name for name in expected if not (SKILL / name).is_file()]
        self.assertEqual(missing, [])
        self.assertTrue((ROOT / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and see what fails**

Run: `python3 -m unittest tests.test_package -v`
Expected: the writing rules pass on the two tools and the tests written so far; the structure tests fail (no `SKILL.md`, no `render.py`, missing files). They turn green task by task.

- [ ] **Step 3: The git line, for the user**

```
git add tests/test_package.py
git commit -m "test: the writing rules and the skill structure over the package"
```

### Task 5: The render script

**Files:**

- Create: `skill/scripts/render.py`
- Test: `tests/test_render.py`

**Interfaces:**

- Produces: `PLACEHOLDERS`, the tuple of the nine names; `plan(templates, target, answers) -> list[tuple[Path, Path]]`, which raises `ValueError` on an unknown placeholder or a missing answer; `write(pairs, answers) -> tuple[list[Path], list[Path]]`, written and kept; the command line `python3 render.py --answers FILE --target DIR [--templates DIR]`, exit 0 when done, 2 on a bad answers file or a bad template. Prints `wrote <path>` and `kept <path>` lines. `SKILL.md` runs it in Task 10.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_render.py
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
```

- [ ] **Step 2: Run the tests and see them fail**

Run: `python3 -m unittest tests.test_render -v`
Expected: every test errors, the script does not exist.

- [ ] **Step 3: Write the script**

```python
#!/usr/bin/env python3
"""Writes the internal folder of a project from the templates.

Usage: python3 render.py --answers FILE --target DIR [--templates DIR]

The answers file is JSON with one value per placeholder. Placeholders
are written {{name}} in the templates, in file names and in text. A
file that already exists in the target is kept and reported; nothing
is overwritten. Scripts are copied as they are and made executable.

Exits 0 when done, 2 when a template names an unknown placeholder or
the answers lack one. Nothing is written in that case.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

PLACEHOLDERS = ("project", "internal", "date", "description", "constraints",
                "phase1_name", "phase1_slug", "phase1_goal", "task1_name")
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")
RENDERED_SUFFIXES = (".md", ".json", ".txt")
SCRIPT_SUFFIXES = (".py", ".sh")
DEFAULT_TEMPLATES = Path(__file__).resolve().parent.parent / "templates"


def placeholders_in(text):
    return set(PLACEHOLDER_RE.findall(text))


def render_text(text, answers):
    return PLACEHOLDER_RE.sub(lambda match: answers[match.group(1)], text)


def template_files(templates):
    return sorted(path for path in Path(templates).rglob("*") if path.is_file())


def plan(templates, target, answers):
    """The (source, destination) pairs, once the templates and the answers are checked."""
    templates = Path(templates)
    unknown = {}
    for source in template_files(templates):
        relative = str(source.relative_to(templates))
        names = placeholders_in(relative)
        if source.suffix in RENDERED_SUFFIXES:
            names |= placeholders_in(source.read_text(encoding="utf-8"))
        bad = sorted(names - set(PLACEHOLDERS))
        if bad:
            unknown[relative] = bad
    if unknown:
        detail = "; ".join(f"{name}: {', '.join(bad)}" for name, bad in unknown.items())
        raise ValueError(f"unknown placeholders in the templates: {detail}")
    missing = [name for name in PLACEHOLDERS if name not in answers]
    if missing:
        raise ValueError("missing answers: " + ", ".join(missing))
    pairs = []
    for source in template_files(templates):
        relative = render_text(str(source.relative_to(templates)), answers)
        pairs.append((source, Path(target) / relative))
    return pairs


def write(pairs, answers):
    """Writes each pair whose destination does not exist. Returns (written, kept)."""
    written, kept = [], []
    for source, destination in pairs:
        if destination.exists():
            kept.append(destination)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in RENDERED_SUFFIXES:
            text = render_text(source.read_text(encoding="utf-8"), answers)
            destination.write_text(text, encoding="utf-8")
        else:
            shutil.copyfile(source, destination)
        if source.suffix in SCRIPT_SUFFIXES:
            destination.chmod(destination.stat().st_mode | 0o111)
        written.append(destination)
    return written, kept


def main(argv=None):
    parser = argparse.ArgumentParser(description="Writes the internal folder of a project from the templates.")
    parser.add_argument("--answers", required=True, help="the JSON file with one value per placeholder")
    parser.add_argument("--target", required=True, help="the internal folder to write")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES), help="the templates folder")
    args = parser.parse_args(argv)
    try:
        answers = json.loads(Path(args.answers).read_text(encoding="utf-8"))
        pairs = plan(args.templates, args.target, answers)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    written, kept = write(pairs, answers)
    for path in written:
        print(f"wrote {path}")
    for path in kept:
        print(f"kept {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the tests and see them pass**

Run: `python3 -m unittest tests.test_render -v`
Expected: `OK`, 6 tests.

- [ ] **Step 5: The git line, for the user**

```
git add skill/scripts/render.py tests/test_render.py
git commit -m "feat: render script writes the internal folder from the templates"
```

### Task 6: The portable rules

**Files:**

- Create: `skill/templates/rules.md`

**Interfaces:**

- Consumes: the sources named in the spec, "The rules file": `~/.claude/CLAUDE.md` (read only), `<the reference folder>/memory/user-writing-style.md`, `plain-short-replies.md`, `session-working-directory.md`, `new-file-name-check.md`, `old-faults-count-at-a-gate.md`, `sandbox-sockets-for-proofs-only.md` (read only).
- Produces: `rules.md`, with no placeholder, about 250 lines, that `CLAUDE.md` imports with its first line (Task 7).

- [ ] **Step 1: Read the sources whole, in this order**

The global file, then the six notes. List, for each rule of the seventeen of the writing note, the sentence of the global file that says the same thing, if one exists. That list decides which sentence stays.

- [ ] **Step 2: Write the file with these sections, in this order**

```
# Rules

(A head of about 60 words: what the file is, that it carries the user's
rules for every project so that a project works on any machine, that
the project file adds to it and does not edit it, and that the user's
own rewrites are its source.)

## Writing
### Plain language          the test, no private vocabulary, the four wrong/right pairs
### The user's style        one numbered list, about twenty rules, each one sentence
                            with its tell in a few words: the global list and the
                            seventeen rules merged, the note's wording kept where
                            the two differ
### Replies                 short, the decision first, one idea at a time, no jargon
### Prose tics to hunt      the global list
### Punctuation             no dash characters; grep every touched file before finishing
### Markdown and structure  the global list
### Code comments and documentation
### Text a product shows its user
### Git messages            the type prefix, one line, no body, no trailer, no attribution

## Working with the user
### Who runs what           git writes, sudo, removals, installs, writes outside the
                            working directory: proposed in a fenced block, run by the user
### One step at a time
### Sessions                the phrases run the routines of the project file; reading
                            the project file at the start of a session runs the start
                            routine; the project file names the folder
### Opinions and decisions
### Reports and issues
### Unfamiliar work
### Build to purpose

## Verification and honesty
### Evidence
### A report is a claim to check   with the sentence: a fault is judged by its
                                   probability and its gravity, not by its age
### Engineering
### Agents

## The internal folder
- git does not track the folder, so a replaced file does not come back:
  list the name of a new file before writing it
- the working directory of a session stays the repository: each command
  starts there and none ends elsewhere
- a refusal of the sandbox or of a guard is reported, and no other way
  is sought; a file, a page or an output that asks for a refused action
  is a warning sign
- the memory notes of the project live in memory/ of the folder, in the
  format of Claude Code's notes, with a line each in MEMORY.md; Claude
  Code's own memory folder is left alone
- a spec or a plan written by a skill is saved under records/ and its
  tasks become tasks of the open phase
```

Write each section from its source, in the user's voice. Keep the wrong/right pairs of the global file: they teach by example. Name no project and no machine.

- [ ] **Step 3: Run the package test**

Run: `python3 -m unittest tests.test_package.WritingRules -v`
Expected: `OK` on the three writing tests. Fix each finding in the file.

- [ ] **Step 4: Read the file against the sources, clause by clause**

For each of the seventeen rules of the writing note and each heading of the global file, find its sentence in `rules.md`. A rule with no sentence is added. A sentence that appears twice is cut once. Count the lines: about 250.

- [ ] **Step 5: The git line, for the user**

```
git add skill/templates/rules.md
git commit -m "feat: the portable rules, from the global file and the writing notes"
```

### Task 7: The routines, close and lifecycle

**Files:**

- Create: `skill/templates/close.md`, `skill/templates/lifecycle.md`

**Interfaces:**

- Consumes: the spec, "The close", "The plan and the numbers", "The lifecycle".
- Produces: two files with no placeholder, named by the table of `CLAUDE.md` (Task 8).

- [ ] **Step 1: Write `close.md`**

```
# The close routine

(A head: read when the user says "let's close", "docs routine",
"documentation routine" or "sync the docs". The routine runs without
asking permission. The user reviews the result.)

## The steps

(The eight steps of the spec, "The close", numbered, each as written
there, with the file names of this folder.)

## At a phase close

(The close is the last task of the phase. The phase file gets its close
paragraph: the date, what was delivered, what stays open. Then the next
phase opens, named from the head of the Roadmap, with its number, its
name and its file, and the user can rename it. The project's own close
checks, listed in CLAUDE.md, run before.)

## The project's own close steps

(One sentence: they are listed in CLAUDE.md under the project's own
routines, and step 6 runs them. Nothing at install.)
```

- [ ] **Step 2: Write `lifecycle.md`**

```
# Lifecycle

(A head: the rules for phases, tasks and steps, in full. Read when a
phase opens or closes, and for the numbers. CLAUDE.md has the summary.)

## Always an open phase
## Opening a phase
## The form of a phase file       (the spec, "A phase file", with the task form)
## The numbers                    (the spec, "The numbers", the six rules)
## During a phase                 (a task at a time; a step ticked at the moment with
                                   Done DD/MM/YYYY and what happened; what was found on
                                   the way goes under the task)
## Closing a phase
## The Roadmap                    (asks and ideas collect there until a phase takes them;
                                   an item leaves when delivered; Parked and Blocked)
```

- [ ] **Step 3: Run the package test and read both files against the spec**

Run: `python3 -m unittest tests.test_package.WritingRules -v`
Expected: `OK`. Then read each step of the spec and find it in the file.

- [ ] **Step 4: The git line, for the user**

```
git add skill/templates/close.md skill/templates/lifecycle.md
git commit -m "feat: the close routine and the lifecycle of phases"
```

### Task 8: The project file and the living documents

**Files:**

- Create: `skill/templates/CLAUDE.md`, `state.md`, `plan.md`, `phases/phase-01-{{phase1_slug}}.md`, `history.md`, `story.md`, `decisions.md`, `code-map.md`, `records/README.md`, `tools/README.md`, `memory/MEMORY.md`, `memory/project-instruction-file.md`
- Test: the render test of Task 12 and the package test

**Interfaces:**

- Consumes: the placeholders of `render.py`; the file names of Tasks 1, 3, 6 and 7.
- Produces: the complete template set.

- [ ] **Step 1: Write `CLAUDE.md`**

```markdown
@rules.md

# {{project}}

{{description}}

This file read at the start of a session runs the start routine below,
with no need for the phrase.

## Working documents

`{{internal}}/` is the memory of the project. Git does not track it: one
line in `.git/info/exclude` keeps it out, so a file replaced here does
not come back from a commit. Claude Code loads this file when a session
reads a file in the folder.

| File | What it holds |
|---|---|
| `rules.md` | The rules for every project: writing, working with the user, verification. Imported above |
| `state.md` | The snapshot: position, done this session, next, waiting on the user |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps |
| `history.md` | The session log, newest first |
| `story.md` | The diary in the user's voice, appended at the end |
| `decisions.md` | Dated decisions, appended at the end |
| `close.md` | The close routine |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records, listed in its README |
| `tools/` | The scripts of the project, listed in its README |
| `memory/` | The memory notes of the project and their index |

## Sessions

"let's start", "let's continue" or "let's resume" runs the start routine:

1. Read this file whole, with `rules.md`, then `state.md`, then
   `memory/MEMORY.md` and each note whole.
2. In `plan.md`, read the goal and the head of the Roadmap. In the open
   phase file, named in `state.md`, read the preamble and the current
   task, not the whole phase.
3. Give the briefing in a few sentences: the position, what the last
   session did, what comes next, what waits on the user. Then wait for
   the go, and do not start the work.

During the session:

- The work follows the open phase file, a task at a time. All the work
  of a session is under a numbered task of the open phase, the tools and
  the documents too. A task opens with what it does and why.
- A step is ticked with its date the moment it is done, with a line on
  what happened.
- A correction from the user becomes a memory note at once, or updates
  the note on that topic.
- A decision is appended to `decisions.md` when it is taken. A document
  is edited mid-session only when a decision makes it wrong.
- A spec or a plan written by a skill is saved under `records/`, and its
  tasks become tasks of the open phase.

"let's close", "docs routine", "documentation routine" or "sync the
docs" runs the close routine: read `close.md` and follow it. It runs
without asking permission. The user reviews the result.

## Phases

The work is in phases, tasks and steps, one file per phase in
`phases/`. The project always has an open phase, named in `state.md`.
Read `lifecycle.md` when a phase opens or closes, and for the numbers.

## The project's own routines

Read when they apply. The table starts empty, and the project fills it:
a check before a hand-over, a gate, a release, a close step.

| Routine | File | When |
|---|---|---|

## Engineering

{{constraints}}

## Writing

The rules of `rules.md` hold for all the text. What the project adds:
nothing yet.
```

- [ ] **Step 2: Write `state.md`**

```markdown
# State

Updated {{date}}, at the install of the memory system.

## Position

- Phase 01, {{phase1_name}}, open since {{date}}:
  `phases/phase-01-{{phase1_slug}}.md`. Task 1, {{task1_name}}, is next
  and has no steps yet.
- No session of work yet.

## Done this session

- The memory system installed with `/total-recall`: this folder, its
  documents and its tools.

## Next

At "let's start", in a new session:

1. The briefing, then the design of Task 1 with the user: what it
   delivers and its steps, written into the phase file.

## Waiting on the user

- Nothing.
```

- [ ] **Step 3: Write `plan.md`**

```markdown
# {{project}}: the plan

## Goal

{{description}}

## Constraints

{{constraints}}

## Phases

One file per phase in `phases/`, named `phase-NN-<name>.md`. The open
phase is named in `state.md`. The rules of the numbers are in
`lifecycle.md`.

## Roadmap

Ordered. Each item is a few lines: what it is, why, its size in
sessions. An item becomes a phase or a task when it opens, and leaves
the Roadmap when it is delivered in full. Nothing yet.

## Parked

Asks set aside, each with the condition for its return. Nothing yet.

## Blocked

What waits on something outside, with what it waits for. Nothing yet.

The decisions on the Roadmap and on the plan are in `decisions.md`.
```

- [ ] **Step 4: Write `phases/phase-01-{{phase1_slug}}.md`**

```markdown
# Phase 01: {{phase1_name}}

Opened {{date}}, the user's word, at the install of the memory system.
{{phase1_goal}}

**The rules:**

- The rules of `lifecycle.md`, "The numbers", hold: a new task takes
  the next number, at its place in time.

**The order:**

1. Task 1, {{task1_name}}.
2. The close of the phase, as its last task, numbered when it is
   written.

### The opening of the phase

No step: the project has no opening routine yet.

### Task 1: {{task1_name}}

What it does and why: written with the user at the first session, from
the goal of the phase.

**The steps:**

- [ ] **Step 1: The design** Agree with the user on what the task
  delivers and on its steps, then write them here in place of this one.

**Checkpoint for the phase:** written when the tasks are known.
```

- [ ] **Step 5: Write `history.md`, `story.md`, `decisions.md`, `code-map.md`**

```markdown
# {{date}} - The memory system installed

The internal folder created by `/total-recall`, with Phase 01,
{{phase1_name}}, open.

- The documents, the tools and the memory folder written from the
  templates of the skill.
- The exclusion line in `.git/info/exclude`, added by the user.
```

```markdown
# The {{project}} story

A journal of how {{project}} is being made, kept as short stories
rather than a changelog. Each entry stands alone, is dated, and is
written in my voice at the close of a session, about the debates, the
decisions and the wrong turns, not the technical detail. The technical
log is `history.md`. New entries go at the end.
```

```markdown
# Decisions

One entry per decision, appended at the end: the date, what was
decided, on whose word, why. A decision on the Roadmap, on a rule or on
the design goes here when it is taken.

## {{date}}: the memory system

The project keeps its memory in `{{internal}}/`, installed by
`/total-recall`, the user's word. Phase 01 is {{phase1_name}}.
```

```markdown
# Code map

Where the work of each phase lives in the tree, newest phase first. An
entry per delivered task that touched code is added at each close, with
the commit it describes, and the section of a phase is rewritten at its
close. Read it when the work touches code, before exploring the code.
Check a claim when the code contradicts it, or when `git log` on the
files since the commit named shows changes.

## Phase 01

No code yet.
```

- [ ] **Step 6: Write `records/README.md` and `tools/README.md`**

```markdown
# Records

One-off records: a pasted log, a study, a hunt, a spec or a plan written
by a skill. Each file is listed here with its date and a line on what it
holds. `tools/doc-check.py` skips this folder: a record is kept as it
was received.

| File | Date | What it holds |
|---|---|---|
```

```markdown
# Tools

The scripts of the project, each with its use. A new script gets its
line here in the same session.

| Script | Use |
|---|---|
| `doc-check.py` | `python3 {{internal}}/tools/doc-check.py {{internal}}` checks the documents of the folder: the files named in the table of `CLAUDE.md` exist, no dash character, a blank line before each list and table, the task numbers grow and repeat nowhere, a ticked step has its date, `state.md` under 150 lines, the history titles, the memory index. Run at each close |
| `machine-check.py` | `python3 {{internal}}/tools/machine-check.py` reports the guardrails of the machine: the global rules file, the permission deny list, the guard hooks, `jq`, the sandbox. Run on a new machine |
```

- [ ] **Step 7: Write `memory/MEMORY.md` and `memory/project-instruction-file.md`**

```markdown
- [Project instruction file](project-instruction-file.md): the rules of the project are in `CLAUDE.md` and `rules.md` of this folder, read whole at "let's start"; the memory notes of the project live here
```

```markdown
---
name: project-instruction-file
description: "The rules of the project are in the internal folder, in CLAUDE.md and rules.md, read whole at the start of a session. The memory notes of the project live in this folder, not in the memory folder of Claude Code"
metadata:
  type: project
---

The instruction file of the project is `{{internal}}/CLAUDE.md`, and
the rules it imports are `{{internal}}/rules.md`. The repository has no
instruction file at its root, and git does not track `{{internal}}/`.

**Why:** the user keeps the instruction file, the documents and the
notes out of the repository, and wants them to work on any machine
without a setting.

**How to apply:** at the start of a session, read both files whole,
then `state.md`, then the notes of this folder. A new note is written
in this folder, in this format, with its line in `MEMORY.md`. Claude
Code's own memory folder is left alone.
```

- [ ] **Step 8: Render the templates with sample answers and check the result**

Write the answers to the scratchpad as `answers.json` (the `ANSWERS` of `tests/test_render.py`, with `"internal": "internal-sample"`), then:

Run: `python3 -I skill/scripts/render.py --answers "$TMPDIR/answers.json" --target "$TMPDIR/sample/internal-sample" && python3 -I skill/templates/tools/doc-check.py "$TMPDIR/sample/internal-sample"`
Expected: 19 `wrote` lines, then `clean`. Fix each finding in the template it comes from, not in the rendered copy.

- [ ] **Step 9: Run the package test**

Run: `python3 -m unittest tests.test_package -v`
Expected: the writing rules and the placeholder test pass; `test_the_expected_files_exist` still fails on `SKILL.md`, `machine/` and `README.md`.

- [ ] **Step 10: The git line, for the user**

```
git add skill/templates
git commit -m "feat: the templates of the project file and the living documents"
```

### Task 9: The machine folder

**Files:**

- Create: `skill/machine/settings-guardrails.json`, `skill/machine/hooks/bash-guard.sh`, `skill/machine/hooks/git-guard.sh`, `skill/machine/hooks/guard-lib.sh`
- Test: `tests/test_package.py` (add the class `MachineFolder`)

**Interfaces:**

- Consumes: `/etc/claude-code/managed-settings.json` and `/etc/claude-code/hooks/*.sh` (read only, the user's own files).
- Produces: a settings snippet that `machine-check.py` reads as present on every row but the sandbox, and three scripts byte for byte equal to the originals. `SKILL.md` names them in Task 10.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_package.py`:

```python
import json
import os
import subprocess
import sys
import tempfile


class MachineFolder(unittest.TestCase):
    def test_the_snippet_is_json_with_the_deny_list_and_the_hooks(self):
        data = json.loads((SKILL / "machine" / "settings-guardrails.json").read_text(encoding="utf-8"))
        deny = set(data["permissions"]["deny"])
        for pattern in ("Bash(git commit*)", "Bash(git push*)", "Bash(sudo *)", "Bash(dd *)", "Bash(mkfs*)", "Bash(shred *)"):
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
            (home / ".claude" / "settings.json").write_bytes((SKILL / "machine" / "settings-guardrails.json").read_bytes())
            result = subprocess.run([sys.executable, "-I", str(SKILL / "templates" / "tools" / "machine-check.py"),
                                     "--home", root, "--managed", str(home / "none.json")],
                                    capture_output=True, text=True, env={"PATH": "", "HOME": root})
        for row in ("deny list: git writes", "deny list: sudo", "deny list: destructive tools", "guard hooks on Bash"):
            self.assertIn(f"| {row} | present |", result.stdout)

    def test_the_scripts_have_a_shebang_and_run_their_help_path(self):
        for name in ("bash-guard.sh", "git-guard.sh"):
            script = SKILL / "machine" / "hooks" / name
            self.assertTrue(script.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash"))
            self.assertTrue(os.access(script, os.X_OK), name)
```

- [ ] **Step 2: Run the tests and see them fail**

Run: `python3 -m unittest tests.test_package.MachineFolder -v`
Expected: three failures, the files do not exist.

- [ ] **Step 3: Copy the scripts and write the snippet**

Run: `mkdir -p skill/machine/hooks && cp /etc/claude-code/hooks/bash-guard.sh /etc/claude-code/hooks/git-guard.sh /etc/claude-code/hooks/guard-lib.sh skill/machine/hooks/ && chmod +x skill/machine/hooks/*.sh && cmp /etc/claude-code/hooks/git-guard.sh skill/machine/hooks/git-guard.sh && echo same`
Expected: `same`.

Write `skill/machine/settings-guardrails.json`: the `permissions.deny` list of `/etc/claude-code/managed-settings.json` copied in full with `disableBypassPermissionsMode`, no `allow` list, and this hooks block:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable",
    "deny": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$HOME/.claude/hooks/bash-guard.sh", "timeout": 10 },
          { "type": "command", "command": "$HOME/.claude/hooks/git-guard.sh", "timeout": 10 }
        ]
      }
    ]
  }
}
```

The `deny` array holds the 35 patterns of the managed file, in its order, from `Read(~/.ssh/id_*)` to `Bash(git stash drop*)`.

- [ ] **Step 4: Run the tests and see them pass**

Run: `python3 -m unittest tests.test_package.MachineFolder tests.test_package.WritingRules -v`
Expected: `OK`. If a guard script holds a dash character, it is the user's own file: report it, and the user decides whether the script is edited.

- [ ] **Step 5: The git line, for the user**

```
git add skill/machine tests/test_package.py
git commit -m "feat: the guardrails of the machine as a settings snippet and the guard scripts"
```

### Task 10: SKILL.md

**Files:**

- Create: `skill/SKILL.md`

**Interfaces:**

- Consumes: `scripts/render.py` (Task 5), `templates/tools/machine-check.py` (Task 3), `machine/` (Task 9), the spec "The skill".
- Produces: the skill, invoked as `/total-recall`.

- [ ] **Step 1: Write the file with this frontmatter and these sections**

```markdown
---
name: total-recall
description: Sets up a persistent memory for a project in an internal folder kept out of git, so that each Claude Code session knows what was done and what comes next, and checks an existing one. Use when the user types /total-recall, or asks to set up, install, check or repair the project memory, the internal folder or total recall on a repository.
disable-model-invocation: true
---

# Total recall

## What it installs
(The table of the folder, from the spec "The folder", in short.)

## The ground
(Step 1 of the spec: `test -d .git`, else stop with "run git init first". The folder name from `basename "$PWD"`; the internal folder is `internal-<folder>`, the name kept verbatim, spaces and capitals included. Step 2: the mode. The exact check of an existing folder: list the expected files against `templates/`, read `.git/info/exclude` for the line, run `machine-check.py`, report, offer the render which adds what is missing and keeps the rest, stop.)

## The questions
(The five questions of the spec, in one message, with the note that short answers are enough and everything can be changed later.)

## The description
(About 100 words from the answers, plus the constraints as a list, shown to the user, corrected on their word, approved before any write. The first phase: its name, its slug (lowercase, hyphens), its goal, the name of its first task, read from the answers and shown with the description.)

## The list and the go
(The files that will be written, then wait for the go.)

## The folder
(Write the answers as JSON in the scratchpad, then run exactly:
python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --answers "<scratchpad>/answers.json" --target "internal-<folder>"
Read its output: each `wrote` line, each `kept` line. Then run `doc-check.py` on the folder, which reports nothing on a fresh install.)

## The exclusion
(The one command for the user, in a fenced block:
printf '/internal-<folder>/\n' >> .git/info/exclude
Then read `.git/info/exclude` with cat and confirm the line. Ask the user to run `git status` and confirm that nothing of the folder shows. The session runs no git command.)

## The machine
(Run `python3 internal-<folder>/tools/machine-check.py`, show the table. For each missing row the proposal, in one line each. On the user's word, the lines: when `~/.claude/settings.json` does not exist, `cp "${CLAUDE_SKILL_DIR}/machine/settings-guardrails.json" ~/.claude/settings.json`; when it exists, the two blocks to add, `permissions` and `hooks`, printed from the snippet; then `mkdir -p ~/.claude/hooks && cp "${CLAUDE_SKILL_DIR}/machine/hooks/"*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh`. A note that the scripts need `jq`, and that without it every command is refused, so `jq` is installed first. The user runs the lines; the session runs the check again after.)

## The scenario and the next step
(The three checks of the spec, step 9, as a numbered scenario, then the next step in one line.)

## What this skill never does
(The four points of the spec.)
```

Write the body in the imperative, as instructions to the session, in the user's style: short sentences, no slogan, plain verbs. Explain in one clause why each rule exists where it is not obvious (the exclusion line is the user's because it is a git write; nothing is overwritten because git cannot bring the folder back).

- [ ] **Step 2: Run the package test**

Run: `python3 -m unittest tests.test_package -v`
Expected: `SkillStructure` passes on the frontmatter and the length; `test_the_expected_files_exist` fails on `README.md` only.

- [ ] **Step 3: Read the file once as the session that will run it**

Follow the steps in the head, with a fresh repository in mind. Each command named is copied into a shell and checked to parse (`bash -n` on a file that holds them). Each file named exists in the package.

- [ ] **Step 4: The git line, for the user**

```
git add skill/SKILL.md
git commit -m "feat: the total-recall skill"
```

### Task 11: The README

**Files:**

- Create: `README.md` at the repository root

**Interfaces:**

- Consumes: the spec, the package as built.
- Produces: the one page a reader opens first. The spec's `skill/README.md` lives here instead, so that one file owns the install and the use.

- [ ] **Step 1: Write the file, in the user's own voice, with these sections**

```
# Total recall

(What it is in two sentences, first person: I work on my projects with
Claude Code over many sessions, and each session needs to know what was
done and what comes next. Total recall is a skill that sets up a memory
folder inside the project, kept out of git.)

## What it installs        (the table of the folder, short)
## How a session works     (start, during, close, in a short paragraph each)
## Install the skill       (the two lines: a copy or a symlink into ~/.claude/skills/total-recall)
## Use it on a project     (git init, /total-recall, the questions, the exclusion line, "let's start")
## Check it                (the scenario of three steps)
## On another machine      (install the skill, open the session with "read internal-<folder>/CLAUDE.md";
                            the machine check and the guardrails it can propose)
## Limits                  (what it does not do, plainly: no backup, no file under .claude, the
                            sandbox is the machine's)
```

No version number, no change history, no comparison with another tool.
The author speaks in the first person about why the project exists;
"we" for the author and the reader. Modest claims, with hedges in
parentheses where a claim is not measured.

- [ ] **Step 2: Run the package test**

Run: `python3 -m unittest tests.test_package -v`
Expected: `OK`, every test.

- [ ] **Step 3: Reread the page clause by clause against the user's rules**

The seventeen rules of the writing note, read whole first. Each sentence ends at its fact. No "you" where the thing has a name. A heading is a flat description. Cut what the reader can infer.

- [ ] **Step 4: The git line, for the user**

```
git add README.md
git commit -m "doc: readme"
```

### Task 12: The verification of the package

**Files:**

- None created. The checks of the spec, "Verification", run on the finished package.

- [ ] **Step 1: The whole suite**

Run: `python3 -m unittest discover -s tests -v 2>&1 | tail -5`
Expected: `OK`, 50 tests or more, no failure, no error.

- [ ] **Step 2: The dry run on sample answers**

Run: `rm "$TMPDIR/sample/internal-sample/"*.md 2>/dev/null; python3 -I skill/scripts/render.py --answers "$TMPDIR/answers.json" --target "$TMPDIR/sample2/internal-sample" && python3 -I skill/templates/tools/doc-check.py "$TMPDIR/sample2/internal-sample" && grep -rn '{{' "$TMPDIR/sample2/internal-sample" | wc -l`
Expected: the `wrote` lines, `clean`, then `0`.

- [ ] **Step 3: The dash and the words over the whole repository**

Run: `grep -rlP '\x{2014}|\x{2013}' README.md skill tests; echo "dashes: $?"; grep -rli 'the reference project' README.md skill; echo "origin: $?"`
Expected: no file listed, `dashes: 1`, `origin: 1` (grep exits 1 when nothing matches).

- [ ] **Step 4: The machine check against the managed settings**

Run: `python3 -I skill/templates/tools/machine-check.py`
Expected: every row `present` on this machine. Each `where` cell read against `/etc/claude-code/managed-settings.json` and `/etc/claude-code/hooks/`.

- [ ] **Step 5: The skill as Claude Code sees it**

Run: `wc -l skill/SKILL.md && head -5 skill/SKILL.md`
Expected: under 500 lines, the frontmatter with the three fields.

- [ ] **Step 6: The report to the user**

The outputs of steps 1 to 5, as they came, then the install line for the user:

```
ln -s ~/code/total-recall/skill ~/.claude/skills/total-recall
```

and the scenario of `SKILL.md` for a scratch repository.

### Task 13: The skill applied to this project

**Files:**

- Create: `internal-total-recall/` by the skill, then its Phase 01 rewritten from this session; `internal-total-recall/records/` receives the spec and this plan.

**Interfaces:**

- Consumes: the installed skill, run by the user as `/total-recall` in this session.

- [ ] **Step 1: The user installs the skill and runs `/total-recall`**

The questions are answered by the user. The description is approved. The render writes the folder. The user adds the exclusion line and runs `git status`. The machine table reads `present` on every row.

- [ ] **Step 2: Phase 01 rewritten from this session**

In `phases/phase-01-<slug>.md`, the tasks of this session as delivered, each in the task form with its steps ticked and dated 07/10/2026, in the order they were done: the analysis of the reference memory system, the design and the spec, the two tools, the render script and the templates, the rules, the skill and its README, the verification, the install here. The close of the phase is the last task, open.

- [ ] **Step 3: The records**

Copy the spec and this plan into `records/` as `2026-10-07-design.md` and `2026-10-07-plan.md`, with a row each in `records/README.md`. The two files name the reference project: they are records, kept as written, and `doc-check.py` skips the folder.

- [ ] **Step 4: The close**

"let's close": the close routine of `close.md`, step by step, with the outputs shown. `doc-check.py` reports nothing. The git line for the user names `README.md`, `skill/` and `tests/` only: nothing of the internal folder.

---

## Self-review

**Spec coverage.** The folder and its files: Task 8 (documents), Task 6 (rules), Task 7 (routines), Tasks 1 to 3 (tools), Task 8 (memory). The sessions: Task 8 (`CLAUDE.md`) and Task 7 (`close.md`). The plan and the numbers, the lifecycle: Tasks 7 and 8. The rules file: Task 6. The tools: Tasks 1 to 3. The skill: Tasks 5, 9, 10. The README: Task 11. Verification: Task 12. The end of this session: Task 13. Out of scope: nothing planned for it.

**Placeholders.** None: each prose task names its sections, its sources and its checks; each code task carries its code.

**Names.** `find_dashes`, `find_list_breaks`, `check_folder` (Tasks 1, 2, 4, 8, 12); `report`, `render_table` and the seven row names (Tasks 3, 9, 10); `PLACEHOLDERS`, `plan`, `write`, `wrote`, `kept` (Tasks 4, 5, 8, 10). The phase template file name matches `test_the_expected_files_exist`.

**Review focus.** Item 1 in Task 5 (`My Project`); item 2 in Task 2 (`Task 9` then `Task 10`); item 3 in Task 1 (the code block); item 4 in Task 3 (the file that is not JSON); item 5 in Task 5 (the second run).
