#!/usr/bin/env python3
"""Checks the documents of an internal folder.

Usage: python3 doc-check.py [--size] <internal folder>

Prints one line per finding, "path:line: message", then a count. Exits
with 1 when it found something, 0 when the documents are clean, 2 on a
usage error. With --size, the first line gives the words read at each
start and the limit of CLAUDE.md. Python 3 with the standard library
only.

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
DECISION_TITLE_RE = re.compile(r"^## D(\d+), " + DATE_RE + r": \S")
REPLACED_RE = re.compile(r"^Replaced by D\d+ on (\d{2})/(\d{2})/(\d{4})\.$")
START_FILES = ("CLAUDE.md", "rules.md", "state.md", "plan.md")
SIZE_LIMIT = 8000
SIZE_RE = re.compile(r"The size read at each start[^0-9]*([0-9][0-9,]*) words")


def check_documents_table(folder, text):
    """Each file named in the table of documents of CLAUDE.md exists.

    The table of documents is the one whose first header cell is
    "File". The other tables of the file, such as the project's own
    routines, are left alone. A name is looked for in the folder, then
    at the root of the repository, for a public file that a project's
    own routine names.
    """
    found = []
    lines = text.split("\n")
    checking = False
    for number, line in enumerate(lines, 1):
        if not line.startswith("|"):
            checking = False
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        previous = lines[number - 2] if number > 1 else ""
        if not previous.startswith("|"):
            checking = bool(cells) and cells[0] == "File"
            continue
        if not checking or not cells or not cells[0].startswith("`"):
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
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.split("\n"), 1):
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
        block = [line.strip()]
        for following in lines[number:]:
            if following.startswith("  ") and not is_list(following):
                block.append(following.strip())
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


def check_decisions(text, obsolete=False):
    """Each entry of decisions.md or obsolete.md is titled '## Dn, DD/MM/YYYY: <name>'.

    In decisions.md the numbers fall from the top: the newest decision
    comes first. In obsolete.md the first line of text under a title is
    'Replaced by Dn on DD/MM/YYYY.', and those dates fall from the top:
    the most recently replaced decision comes first, whatever its
    number. The lines of a fenced code block are skipped.
    """
    found = []
    lines = text.split("\n")
    previous = None
    in_code = False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.startswith("## "):
            continue
        match = DECISION_TITLE_RE.match(line)
        if not match:
            found.append((number, "a decision starts with '## Dn, DD/MM/YYYY: <name>'"))
            continue
        if obsolete:
            following = next((later.strip() for later in lines[number:] if later.strip()), "")
            replaced = REPLACED_RE.match(following)
            if not replaced:
                found.append((number, "an obsolete decision needs 'Replaced by Dn on DD/MM/YYYY.' under its title"))
                continue
            day, month, year = replaced.groups()
            current = (int(year), int(month), int(day))
            if previous is not None and current > previous:
                found.append((number, "this decision was replaced after the one above it: "
                                      "the most recently replaced comes first"))
        else:
            current = int(match.group(1))
            if previous is not None and current >= previous:
                found.append((number, f"D{current} is below D{previous}: the newest decision comes first"))
        previous = current
    return found


def start_size(folder):
    """The words of the files read at each start: CLAUDE.md, rules.md, state.md, plan.md and the memory notes.

    plan.md is counted whole, although a session reads its head: the
    count errs on the high side.
    """
    folder = Path(folder)
    paths = [folder / name for name in START_FILES]
    memory = folder / "memory"
    if memory.is_dir():
        paths += sorted(memory.glob("*.md"))
    words = 0
    for path in paths:
        if not path.is_file():
            continue
        try:
            words += len(path.read_text(encoding="utf-8").split())
        except UnicodeDecodeError:
            continue
    return words


def size_limit(claude_text):
    """The limit written in CLAUDE.md, 'The size read at each start: N words', or the default."""
    match = SIZE_RE.search(claude_text)
    return int(match.group(1).replace(",", "")) if match else SIZE_LIMIT


def check_memory(folder):
    """Each note is in the index, and each index line names a note."""
    memory = folder / "memory"
    index = memory / "MEMORY.md"
    if not index.exists():
        return [(index, 0, "memory/MEMORY.md is missing")]
    try:
        index_text = index.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [(index, 0, "not UTF-8, the index cannot be read")]
    listed = set(re.findall(r"\]\(([^)]+\.md)\)", index_text))
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
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            add(path, 0, "not UTF-8, the document cannot be read")
            continue
        for number, message in find_dashes(text) + find_list_breaks(text):
            add(path, number, message)
    def text_of(path):
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return ""

    claude = folder / "CLAUDE.md"
    if claude.exists():
        for number, message in check_documents_table(folder, text_of(claude)):
            add(claude, number, message)
    else:
        findings.append("CLAUDE.md:0: CLAUDE.md is missing")
    phases_dir = folder / "phases"
    phases = sorted(phases_dir.glob("phase-*.md")) if phases_dir.is_dir() else []
    for path in phases:
        for number, message in check_done_steps(text_of(path)):
            add(path, number, message)
    for path, number, message in check_tasks(phases):
        add(path, number, message)
    state = folder / "state.md"
    if state.exists():
        for number, message in check_state(text_of(state)):
            add(state, number, message)
    history = folder / "history.md"
    if history.exists():
        for number, message in check_history(text_of(history)):
            add(history, number, message)
    for name, obsolete in (("decisions.md", False), ("obsolete.md", True)):
        path = folder / name
        if path.exists():
            for number, message in check_decisions(text_of(path), obsolete):
                add(path, number, message)
    limit = size_limit(text_of(claude)) if claude.exists() else SIZE_LIMIT
    words = start_size(folder)
    if words > limit:
        findings.append(f"CLAUDE.md:0: the files read at each start hold {words} words, over the limit of {limit}")
    for path, number, message in check_memory(folder):
        add(path, number, message)
    return findings


def main(argv):
    args = argv[1:]
    show_size = "--size" in args
    args = [arg for arg in args if arg != "--size"]
    if len(args) != 1 or not Path(args[0]).is_dir():
        print("usage: doc-check.py [--size] <internal folder>", file=sys.stderr)
        return 2
    folder = Path(args[0])
    if show_size:
        claude = folder / "CLAUDE.md"
        try:
            limit = size_limit(claude.read_text(encoding="utf-8")) if claude.exists() else SIZE_LIMIT
        except UnicodeDecodeError:
            limit = SIZE_LIMIT
        print(f"read at each start: {start_size(folder)} words, limit {limit}")
    findings = check_folder(folder)
    for line in findings:
        print(line)
    if findings:
        print(f"{len(findings)} finding(s)")
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
