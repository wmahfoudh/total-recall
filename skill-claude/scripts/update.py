#!/usr/bin/env python3
"""Backs up the internal folder of a project, and updates it to the current templates.

Usage: python3 update.py backup --target DIR
       python3 update.py plan --target DIR [--templates DIR]
       python3 update.py apply --target DIR [--templates DIR]

backup writes one archive of the folder, without its backup/ folder, to
backup/<folder>-YYYY-MM-DD-HH-MM-manual.tar.gz. plan prints what an
update would do and changes nothing. apply makes an archive of the kind
auto, then adds the missing templates that need no answer, replaces the
routine files that differ from their templates, migrates the decisions
to numbered entries, and renames the phase files of the older form,
phase-NN-<name>.md, to PNN-<name>.md. The records of the older form,
named by a date, are listed to number by hand. The project's own
content (the project file, the state, the plan, the phases, the
history, the story, the notes, the text of the decisions) is not
changed: a phase file of the older form is only renamed.

Exits 0 when done, 2 when the folder does not look like a total-recall
folder (its CLAUDE.md does not start with @rules.md) or on an error.
"""
import argparse
import datetime
import re
import shutil
import sys
import tarfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render  # noqa: E402

ROUTINE_FILES = ("rules.md", "close.md", "lifecycle.md", "review.md",
                 "tools/doc-check.py", "tools/machine-check.py", "tools/start.py")
KINDS = ("manual", "auto")
SIGNATURE = "@rules.md"
OLD_PHASE_RE = re.compile(r"^phase-(\d+)-(.+\.md)$")
OLD_RECORD_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")


def is_total_recall(target):
    """The skill always writes @rules.md as the first line of the project file."""
    try:
        text = (Path(target) / "CLAUDE.md").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return text.split("\n", 1)[0].strip() == SIGNATURE


def backup(target, kind, now=None):
    """Writes the archive of the folder and returns its path.

    The kind is manual when the user asks for the backup, auto when the
    skill makes it before an update. A second archive in the same minute
    takes -2, -3, so that no archive replaces another.
    """
    if kind not in KINDS:
        raise ValueError(f"the kind of a backup is manual or auto, not {kind}")
    target = Path(target)
    now = now or datetime.datetime.now()
    folder = target / "backup"
    folder.mkdir(exist_ok=True)
    stem = f"{target.resolve().name}-{now:%Y-%m-%d-%H-%M}-{kind}"
    path = folder / f"{stem}.tar.gz"
    count = 2
    while path.exists():
        path = folder / f"{stem}-{count}.tar.gz"
        count += 1
    with tarfile.open(path, "w:gz") as archive:
        for item in sorted(target.rglob("*")):
            relative = item.relative_to(target)
            if relative.parts[0] == "backup" or not item.is_file():
                continue
            archive.add(item, arcname=str(Path(target.resolve().name) / relative))
    return path


def decisions_to_migrate(target):
    path = Path(target) / "decisions.md"
    if not path.exists():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ValueError(f"{path} is not UTF-8, nothing was written")
    _, entries = render.split_decisions(text)
    return bool(entries) and not any(render.NUMBERED_RE.match(entry) for entry in entries)


def renames(target):
    """The phase files of the older form, with the name each takes: (old, new), relative to the target."""
    phases = Path(target) / "phases"
    if not phases.is_dir():
        return []
    found = []
    for path in sorted(phases.iterdir()):
        match = OLD_PHASE_RE.match(path.name)
        if path.is_file() and match:
            found.append((f"phases/{path.name}", f"phases/P{match.group(1)}-{match.group(2)}"))
    return found


def records_by_hand(target):
    """The records of the older form, named by a date: their number needs the order of their creation."""
    records = Path(target) / "records"
    if not records.is_dir():
        return []
    return [f"records/{p.name}" for p in sorted(records.iterdir()) if p.is_file() and OLD_RECORD_RE.match(p.name)]


def plan_update(templates, target):
    """What an update would do: the files to add, the files to replace, the decisions to migrate."""
    templates, target = Path(templates), Path(target)
    pairs, by_hand = render.plan_repair(templates, target)
    add = sorted(str(destination.relative_to(target)) for _, destination in pairs if not destination.exists())
    replace = [name for name in ROUTINE_FILES
               if (target / name).exists() and (templates / name).exists()
               and (target / name).read_bytes() != (templates / name).read_bytes()]
    needs = [name for name in by_hand if not render.present(target, name)]
    return {"add": add, "replace": replace, "migrate": decisions_to_migrate(target), "needs_answers": needs,
            "rename": renames(target), "by_hand": records_by_hand(target)}


def apply_update(templates, target, now=None):
    """Makes the auto backup, then applies the plan. Returns (archive or None, plan, warnings)."""
    templates, target = Path(templates), Path(target)
    plan = plan_update(templates, target)
    if not (plan["add"] or plan["replace"] or plan["migrate"] or plan["rename"]):
        return None, plan, []
    archive = backup(target, "auto", now)
    pairs, _ = render.plan_repair(templates, target)
    render.write(pairs, {})
    for name in plan["replace"]:
        shutil.copyfile(templates / name, target / name)
    warnings = []
    for old, new in plan["rename"]:
        if (target / new).exists():
            warnings.append(f"{new} exists, {old} was left as it is")
        else:
            (target / old).rename(target / new)
    if plan["migrate"]:
        decisions = target / "decisions.md"
        header = render.split_decisions((templates / "decisions.md").read_text(encoding="utf-8"))[0]
        text, warnings = render.migrate_decisions(decisions.read_text(encoding="utf-8"), header)
        decisions.write_text(text, encoding="utf-8")
    return archive, plan, warnings


def print_plan(plan):
    lines = [f"add {name}" for name in plan["add"]]
    lines += [f"replace {name}" for name in plan["replace"]]
    if plan["migrate"]:
        lines.append("migrate decisions.md")
    lines += [f"rename {old} {new}" for old, new in plan["rename"]]
    for line in lines or ["nothing to update"]:
        print(line)
    for name in plan["needs_answers"]:
        print(f"needs answers: {name}")
    for name in plan["by_hand"]:
        print(f"by hand: {name}, to number in the order of its creation")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Backs up the internal folder, and updates it to the current templates.")
    parser.add_argument("command", choices=("backup", "plan", "apply"))
    parser.add_argument("--target", required=True, help="the internal folder")
    parser.add_argument("--templates", default=str(render.DEFAULT_TEMPLATES), help="the templates folder")
    args = parser.parse_args(argv)
    target = Path(args.target)
    if not is_total_recall(target):
        print(f"{target} does not look like a total-recall folder: its CLAUDE.md does not start "
              f"with {SIGNATURE}. Nothing was written.", file=sys.stderr)
        return 2
    try:
        if args.command == "backup":
            print(f"backup {backup(target, 'manual')}")
            return 0
        if args.command == "plan":
            print_plan(plan_update(args.templates, target))
            return 0
        archive, plan, warnings = apply_update(args.templates, target)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    if archive is not None:
        print(f"backup {archive}")
    print_plan(plan)
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
