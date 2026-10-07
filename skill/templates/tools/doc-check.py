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


DATE_RE = r"\d{2}/\d{2}/\d{4}"
TASK_RE = re.compile(r"^### Task (\d+):")
DONE_STEP_RE = re.compile(r"^\s*- \[x\]", re.IGNORECASE)
DONE_MARK_RE = re.compile(r"Done " + DATE_RE + ":")
HISTORY_TITLE_RE = re.compile(r"^# " + DATE_RE + r"(, [a-z ]+)? - \S")
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


if __name__ == "__main__":
    sys.exit(main(sys.argv))
