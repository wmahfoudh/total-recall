#!/usr/bin/env python3
"""Prints what a session reads at its start.

Usage: python3 start.py <internal folder>

Prints, each part headed with its file: state.md and the memory notes
whole; from plan.md the goal, the first Roadmap item in full, the
titles of the other items and the titles under Blocked; from the open
phase file the preamble and the current task. CLAUDE.md and rules.md
are left out: Claude Code loads them when the session reads a file in
the folder.

Exits with 1 when state.md cannot be read, so that the start routine
reads the files itself, and 2 on a usage error. Python 3 with the
standard library only.
"""
import re
import sys
from pathlib import Path

PHASE_RE = re.compile(r"^phase-(\d+)-.*\.md$")
STATE_PHASE_RE = re.compile(r"phases/phase-\d+-[^`\s]*\.md")
TASK_RE = re.compile(r"^### Task \d+:")
OPEN_STEP_RE = re.compile(r"^\s*- \[ \]")
DONE_STEP_RE = re.compile(r"^\s*- \[x\]", re.IGNORECASE)
ITEM_RE = re.compile(r"^\d+\.\s")
TITLE_RE = re.compile(r"\*\*(.+?)\*\*")
CHECKPOINT = "**Checkpoint for the phase:**"


class StartError(Exception):
    pass


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def open_phase(folder):
    """The phase file with the highest number, or None."""
    phases = Path(folder) / "phases"
    if not phases.is_dir():
        return None
    numbered = [(int(m.group(1)), path) for path in phases.iterdir()
                if path.is_file() and (m := PHASE_RE.match(path.name))]
    return max(numbered)[1] if numbered else None


def sections(text):
    """The '## ' sections of a text, by title."""
    found, title = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            found[title] = []
        elif title is not None:
            found[title].append(line)
    return found


def items(lines, pattern):
    """The list items of a section that match the pattern, each with its wrapped lines."""
    found = []
    for line in lines:
        if pattern.match(line):
            found.append([line])
        elif found and line.startswith((" ", "\t")) and line.strip():
            found[-1].append(line)
        elif not line.strip() and found:
            found.append(None)
    return [item for item in found if item]


def title_of(item, number=None):
    match = TITLE_RE.search(item[0])
    title = f"**{match.group(1)}**" if match else item[0].split(None, 1)[-1]
    return f"{number}. {title}" if number else f"- {title}"


def plan_head(text):
    """The goal, the first Roadmap item in full, the titles of the other items and of Blocked."""
    parts = sections(text)
    out = []
    if "Goal" in parts:
        out += ["## Goal", "", "\n".join(parts["Goal"]).strip(), ""]
    roadmap = items(parts.get("Roadmap", []), ITEM_RE)
    out += ["## Roadmap: the first item and the titles", ""]
    if roadmap:
        out += roadmap[0]
        out += [title_of(item, n) for n, item in enumerate(roadmap[1:], start=2)]
    else:
        out.append("No item.")
    blocked = items(parts.get("Blocked", []), re.compile(r"^- "))
    out += ["", "## Blocked: the titles", ""]
    out += [title_of(item) for item in blocked] or ["No item."]
    return "\n".join(out)


def tasks(text):
    """The tasks of a phase file, each a list of lines, up to the next heading or the checkpoint."""
    found, current = [], None
    for line in text.splitlines():
        if TASK_RE.match(line):
            current = [line]
            found.append(current)
        elif line.startswith("### ") or line.startswith(CHECKPOINT):
            current = None
        elif current is not None:
            current.append(line)
    return found


def current_task(text):
    """The first task with an open step, or the one after the last ticked task, or None."""
    found = tasks(text)
    for task in found:
        if any(OPEN_STEP_RE.match(line) for line in task):
            return task
    ticked = [n for n, task in enumerate(found) if any(DONE_STEP_RE.match(line) for line in task)]
    following = ticked[-1] + 1 if ticked else 0
    return found[following] if following < len(found) else None


def preamble(text):
    lines = []
    for line in text.splitlines():
        if line.startswith("### "):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def start_text(folder):
    """The whole start as one text. Raises StartError when state.md cannot be read."""
    folder = Path(folder)
    state = read(folder / "state.md")
    if state is None:
        raise StartError("state.md is missing or cannot be read")
    out = ["==> state.md <==", "", state.strip(), ""]

    memory = folder / "memory"
    if memory.is_dir():
        notes = sorted(memory.glob("*.md"), key=lambda path: (path.name != "MEMORY.md", path.name))
        for path in notes:
            text = read(path)
            if text is not None:
                out += [f"==> memory/{path.name} <==", "", text.strip(), ""]

    plan = read(folder / "plan.md")
    out.append("==> plan.md: the goal and the head of the Roadmap <==")
    out += ["", plan_head(plan) if plan is not None else "plan.md is missing.", ""]

    phase = open_phase(folder)
    if phase is None:
        out += ["==> phases/ <==", "", "No phase file.", ""]
    else:
        name = f"phases/{phase.name}"
        named = STATE_PHASE_RE.search(state)
        if named and named.group(0) != name:
            out += [f"warning: state.md names {named.group(0)}, the open phase is {name}", ""]
        text = read(phase) or ""
        task = current_task(text)
        label = task[0][4:].split(":")[0] if task else "no current task"
        out += [f"==> {name}: the preamble and {label} <==", "", preamble(text), ""]
        out += ["\n".join(task).strip() if task else "No current task.", ""]
    return "\n".join(out)


def main(argv):
    if len(argv) != 2 or not Path(argv[1]).is_dir():
        print("usage: start.py <internal folder>", file=sys.stderr)
        return 2
    try:
        print(start_text(argv[1]), end="")
    except StartError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
