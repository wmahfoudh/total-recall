"""The two forms of the skill, and the helper that runs a test class over both.

A test class written for both forms is a plain class with test methods
that read `self.form`. `for_each_form` makes a TestCase per form from
it, named after the form, as in `RenderClaude` and `RenderPi`.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Form:
    def __init__(self, name, folder, project_file, template, command, readme,
                 other_systems, note_head, own_files):
        self.name = name
        self.folder = ROOT / folder
        self.project_file = project_file
        self.template = template
        self.command = command
        self.readme = ROOT / readme
        self.other_systems = other_systems
        self.note_head = note_head
        self.own_files = own_files
        self.skill_file = self.folder / "SKILL.md"
        self.scripts = self.folder / "scripts"
        self.templates = self.folder / "templates"
        self.tools = self.templates / "tools"

    def __repr__(self):
        return self.name


# The files both forms carry, relative to the folder of the form.
COMMON_FILES = [
    "SKILL.md", "scripts/render.py", "scripts/update.py", "templates/rules.md",
    "templates/state.md", "templates/plan.md", "templates/phases/P01-{{phase1_slug}}.md",
    "templates/history.md", "templates/story.md", "templates/decisions.md",
    "templates/close.md", "templates/lifecycle.md", "templates/code-map.md",
    "templates/records/README.md", "templates/tools/README.md",
    "templates/tools/doc-check.py", "templates/tools/machine-check.py",
    "templates/tools/start.py", "templates/memory/MEMORY.md",
    "templates/memory/user-writing-style.md", "templates/obsolete.md",
    "templates/review.md", "templates/backup/README.md",
]

CLAUDE = Form(
    "claude", "skill-claude", "CLAUDE.md", "CLAUDE.template.md", "/total-recall", "README.md",
    ("CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", ".claude/CLAUDE.md", "memory-bank"),
    "---\nname: user-writing-style\n",
    ["templates/CLAUDE.template.md", "machine/settings-guardrails.json",
     "machine/hooks/bash-guard.sh", "machine/hooks/git-guard.sh", "machine/hooks/guard-lib.sh"],
)
PI = Form(
    "pi", "skill-pi", "AGENTS.md", "AGENTS.template.md", "/skill:total-recall", "skill-pi/README.md",
    ("AGENTS.md", "AGENTS.override.md", "CLAUDE.md", ".pi/APPEND_SYSTEM.md", "memory-bank"),
    "# The user's writing style\n",
    ["README.md", "templates/AGENTS.template.md", "templates/memory/guardrails.md"],
)
FORMS = (CLAUDE, PI)


def load(path, name):
    """The script at path as a module, without bytecode beside it.

    update.py imports render from its own folder. The render of the form
    loaded before is dropped from the cache, so that each form gets its
    own.
    """
    sys.dont_write_bytecode = True
    sys.modules.pop("render", None)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def for_each_form(namespace, *bases):
    """Adds to the namespace of a test module a TestCase per form for each base."""
    for base in bases:
        for form in FORMS:
            name = f"{base.__name__}{form.name.capitalize()}"
            namespace[name] = type(name, (base, unittest.TestCase), {"form": form})


def make(root, files):
    """Writes the files, relative path to text, under root."""
    for name, text in files.items():
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
