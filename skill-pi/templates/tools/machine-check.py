#!/usr/bin/env python3
"""Reports the guardrails of this machine for Pi sessions.

Usage: python3 machine-check.py [--home DIR] [--agent-dir DIR]

Prints a table with a row per guardrail: present or missing, and where
it was found. Reads the global rules file in the agent directory.
Changes nothing. Exits 0.

The agent directory is `PI_CODING_AGENT_DIR` when it is set, and
`~/.pi/agent` otherwise.
"""
import argparse
import os
from pathlib import Path

# Pi reads the first of these that exists in the agent directory.
RULES_CANDIDATES = ("AGENTS.override.md", "AGENTS.md", "AGENTS.MD",
                    "CLAUDE.md", "CLAUDE.MD")
# The line the install proposes for the global rules file. Without it, a
# session opened with "let's start" has nothing that names the folder.
START_LINE = ('In a project with a folder `internal-<project-name>/` at its root, '
              '"let\'s start", "let\'s continue" and "let\'s resume" mean: read '
              '`internal-<project-name>/AGENTS.md` and '
              '`internal-<project-name>/rules.md`, and run the start routine of '
              '`AGENTS.md`.')
START_MARKER = "internal-<project-name>/AGENTS.md"


def agent_dir(home, given):
    """The agent directory: the flag, then the environment, then ~/.pi/agent."""
    if given:
        return Path(given)
    from_env = os.environ.get("PI_CODING_AGENT_DIR")
    if from_env:
        return Path(from_env)
    return Path(home) / ".pi" / "agent"


def rules_file(directory):
    """The global rules file Pi would read, or None."""
    for name in RULES_CANDIDATES:
        path = Path(directory) / name
        if path.is_file():
            return path
    return None


def report(home, given):
    directory = agent_dir(home, given)
    rows = []
    rules = rules_file(directory)
    rows.append(("global rules file", "present" if rules else "missing",
                 str(rules) if rules else f"none in {directory}"))
    try:
        mapped = rules is not None and START_MARKER in rules.read_text(encoding="utf-8")
    except (OSError, ValueError):
        mapped = False
    rows.append(("start phrases", "present" if mapped else "missing",
                 str(rules) if mapped else ""))
    rows.append(("sandbox", "not built in",
                 "Pi has no built in sandbox; run Pi in a container to isolate a session"))
    return rows


def render_table(rows):
    lines = ["| Guardrail | Status | Where |", "|---|---|---|"]
    for name, status, where in rows:
        lines.append(f"| {name} | {status} | {where} |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Reports the guardrails of this machine.")
    parser.add_argument("--home", default=os.path.expanduser("~"))
    parser.add_argument("--agent-dir", help="the Pi agent directory; overrides PI_CODING_AGENT_DIR")
    args = parser.parse_args(argv)
    print(render_table(report(args.home, args.agent_dir)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
