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
# The line the install proposes for the global rules file. Without it, a
# session opened with "let's start" has nothing that names the folder.
START_LINE = ('In a project with a folder `internal-<project-name>/` at its root, '
              '"let\'s start", "let\'s continue" and "let\'s resume" mean: read '
              '`internal-<project-name>/CLAUDE.md` and run its start routine.')
START_MARKER = "internal-<project-name>/CLAUDE.md"


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
    try:
        mapped = START_MARKER in rules.read_text(encoding="utf-8")
    except (OSError, ValueError):
        mapped = False
    rows.append(("start phrases", "present" if mapped else "missing", str(rules) if mapped else ""))
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
