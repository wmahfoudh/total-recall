#!/usr/bin/env python3
"""Writes the internal folder of a project from the templates.

Usage: python3 render.py --answers FILE --target DIR [--templates DIR]
       python3 render.py --repair --target DIR [--templates DIR]

The answers file is JSON with one value per placeholder. Placeholders
are written {{name}} in the templates, in file names and in text. A
file that already exists in the target is kept and reported; nothing
is overwritten. Scripts are copied as they are and made executable.

With --repair no answers are read: only the templates that carry no
placeholder are added where they are missing, and each missing file
that needs answers is named for the session to write by hand.

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
    """The files of the templates folder, without caches and hidden files."""
    templates = Path(templates)
    files = []
    for path in sorted(templates.rglob("*")):
        parts = path.relative_to(templates).parts
        if not path.is_file() or any(p == "__pycache__" or p.startswith(".") for p in parts):
            continue
        files.append(path)
    return files


def needs_of(source, templates):
    """The placeholders a template uses, in its path and in its text."""
    names = placeholders_in(str(source.relative_to(templates)))
    if source.suffix in RENDERED_SUFFIXES:
        names |= placeholders_in(source.read_text(encoding="utf-8"))
    return names


def check_templates(templates):
    """Raises ValueError when a template names a placeholder that is not known."""
    unknown = {}
    for source in template_files(templates):
        bad = sorted(needs_of(source, templates) - set(PLACEHOLDERS))
        if bad:
            unknown[str(source.relative_to(templates))] = bad
    if unknown:
        detail = "; ".join(f"{name}: {', '.join(bad)}" for name, bad in unknown.items())
        raise ValueError(f"unknown placeholders in the templates: {detail}")


def plan(templates, target, answers):
    """The (source, destination) pairs, once the templates and the answers are checked."""
    templates = Path(templates)
    check_templates(templates)
    missing = [name for name in PLACEHOLDERS if name not in answers]
    if missing:
        raise ValueError("missing answers: " + ", ".join(missing))
    pairs = []
    for source in template_files(templates):
        relative = render_text(str(source.relative_to(templates)), answers)
        pairs.append((source, Path(target) / relative))
    return pairs


def plan_repair(templates, target):
    """The pairs that need no answer, and the names of the templates that do."""
    templates = Path(templates)
    check_templates(templates)
    pairs, by_hand = [], []
    for source in template_files(templates):
        relative = str(source.relative_to(templates))
        if needs_of(source, templates):
            by_hand.append(relative)
        else:
            pairs.append((source, Path(target) / relative))
    return pairs, by_hand


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
    parser.add_argument("--answers", help="the JSON file with one value per placeholder")
    parser.add_argument("--repair", action="store_true",
                        help="add only the files that need no answer, and name the others")
    parser.add_argument("--target", required=True, help="the internal folder to write")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES), help="the templates folder")
    args = parser.parse_args(argv)
    if not args.repair and not args.answers:
        parser.error("--answers is needed, or --repair")
    by_hand = []
    answers = {}
    try:
        if args.repair:
            pairs, by_hand = plan_repair(args.templates, args.target)
        else:
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
    for name in by_hand:
        if not (Path(args.target) / name).exists():
            print(f"needs answers: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
