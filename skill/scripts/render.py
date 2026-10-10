#!/usr/bin/env python3
"""Writes the internal folder of a project from the templates.

Usage: python3 render.py --answers FILE --target DIR [--templates DIR]
       python3 render.py --repair --target DIR [--templates DIR]
       python3 render.py --migrate-decisions FILE --out FILE [--templates DIR]

The answers file is JSON with one value per placeholder. Placeholders
are written {{name}} in the templates, in file names and in text. A
file that already exists in the target is kept and reported; nothing
is overwritten. Scripts are copied as they are and made executable.

With --repair no answers are read: only the templates that carry no
placeholder are added where they are missing, and each missing file
that needs answers is named for the session to write by hand.

With --migrate-decisions the decisions file of an older folder is
written in the current form to the --out file: the entries numbered D1
to Dn in the order they were taken, the newest first, under the header
of the template. The source is not changed, and an --out file that
exists is not replaced.

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
NUMBERED_RE = re.compile(r"^## D\d+, ")
TITLE_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}: ")


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


def split_decisions(text):
    """The header and the entries of a decisions file, in file order.

    An entry starts at a '## ' line outside a fenced code block.
    """
    header, entries = [], []
    in_code = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            entries.append([line])
        elif entries:
            entries[-1].append(line)
        else:
            header.append(line)
    return "\n".join(header), ["\n".join(entry) for entry in entries]


def migrate_decisions(text, header):
    """The decisions numbered in file order, the newest first, under the header.

    An older file adds its entries at the end, so the file order is the
    order in which they were taken. Returns (text, warnings). Raises
    ValueError when the file holds no entry or is already numbered.
    """
    _, entries = split_decisions(text)
    if not entries:
        raise ValueError("no decision found: an entry starts with '## '")
    if any(NUMBERED_RE.match(entry) for entry in entries):
        raise ValueError("the decisions are already numbered, nothing was written")
    numbered, warnings = [], []
    for number, entry in enumerate(entries, 1):
        title, _, body = entry.partition("\n")
        name = title[3:]
        if not TITLE_DATE_RE.match(name):
            warnings.append(f"D{number} has no date in its title: {name}")
        numbered.append(f"## D{number}, {name}\n{body}".rstrip("\n"))
    return header.rstrip("\n") + "\n\n" + "\n\n".join(reversed(numbered)) + "\n", warnings


def run_migration(source, out, templates):
    """Writes the migrated copy. Returns the exit code."""
    out = Path(out)
    if out.exists():
        print(f"{out} exists, nothing was written", file=sys.stderr)
        return 2
    try:
        text = Path(source).read_text(encoding="utf-8")
        template = (Path(templates) / "decisions.md").read_text(encoding="utf-8")
        new_text, warnings = migrate_decisions(text, split_decisions(template)[0])
    except UnicodeDecodeError:
        # A subclass of ValueError, so it is caught first.
        print(f"{source} is not UTF-8, nothing was written", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    out.write_text(new_text, encoding="utf-8")
    for warning in warnings:
        print(f"warning: {warning}")
    print(f"wrote {out}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Writes the internal folder of a project from the templates.")
    parser.add_argument("--answers", help="the JSON file with one value per placeholder")
    parser.add_argument("--repair", action="store_true",
                        help="add only the files that need no answer, and name the others")
    parser.add_argument("--target", help="the internal folder to write")
    parser.add_argument("--migrate-decisions",
                        help="the decisions file of an older folder, written in the current form to --out")
    parser.add_argument("--out", help="the file the migrated decisions are written to")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES), help="the templates folder")
    args = parser.parse_args(argv)
    if args.migrate_decisions:
        if not args.out:
            parser.error("--out is needed with --migrate-decisions")
        return run_migration(args.migrate_decisions, args.out, args.templates)
    if not args.target:
        parser.error("--target is needed")
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
