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
    """The files of the templates folder, without caches and hidden files."""
    templates = Path(templates)
    files = []
    for path in sorted(templates.rglob("*")):
        parts = path.relative_to(templates).parts
        if not path.is_file() or any(p == "__pycache__" or p.startswith(".") for p in parts):
            continue
        files.append(path)
    return files


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
