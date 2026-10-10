# The memory used with care: the implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The skill asks before the git exclusion, writes to the memory with judgment, ships a review of the memory that also brings an older folder to the current form, keeps the decisions numbered and newest first with `obsolete.md`, and has a README written for a public skill.

**Architecture:** Two scripts change: `skill/templates/tools/doc-check.py` gains the checks of the decisions and of the size read at each start, `skill/scripts/render.py` gains `--migrate-decisions`. The rest is Markdown: two new templates (`review.md`, `obsolete.md`), edits to `SKILL.md`, the templates and the README. Each change of behavior starts with a failing test.

**Tech Stack:** Python 3, standard library only; Markdown; `unittest`.

**Spec:** `internal-total-recall/records/2026-10-10-design.md`

The tasks are numbered as tasks of Phase 02, from 18, by `lifecycle.md`.

## Global Constraints

- Markdown templates, Python 3 with the standard library only, bash for the three guard scripts.
- The check command is `python3 -m unittest discover -s tests -v`, from the repository root, green before a hand-over.
- The repository may be shared: nothing in it names the reference project, this machine or another project's stack.
- All the text follows `rules.md` and `memory/user-writing-style.md`: no em dash and no en dash, a blank line before each list and table.
- Git writes are the user's: each task ends with the lines to copy, the user runs them. Nothing is written under `.claude/`.
- The tests write no bytecode into the templates.
- `SKILL.md` stays under 500 lines of body.
- The installed copies of the tools in `internal-total-recall/tools/` are not updated by this plan: the new check would report the old form of this folder's decisions. They are updated at the review of this project, on the user's word, after delivery.

## Review Focus

1. A `## ` line inside a fenced code block of `decisions.md`: the migration and the check must not read it as a title. Tested in Tasks 18 and 19.
2. A decision title with no date (an older hand written entry): the migration keeps its text, numbers it and warns, and the check reports it. Tested in Tasks 18 and 19.
3. A `decisions.md` that is not UTF-8, or an output file that exists: the migration writes nothing and says why. Tested in Task 19.
4. A size limit written `8,000` or `8000`: both read as the same number. Tested in Task 18.
5. A folder made by an older skill, with no `decisions.md` in the new form and no `obsolete.md`: the check does not crash, and the repair adds `obsolete.md` and `review.md`. Tested in Tasks 18, 20 and 23.

---

### Task 18: The check of the decisions and of the size

**Files:**

- Modify: `skill/templates/tools/doc-check.py`
- Modify: `skill/templates/tools/README.md` (the line of `doc-check.py`)
- Test: `tests/test_doc_check.py` (class `FolderRules`)

**Interfaces:**

- Produces: `check_decisions(text, obsolete=False) -> list[(line, message)]`, `start_size(folder) -> int`, `size_limit(claude_text) -> int`, `SIZE_LIMIT = 8000`, the option `--size`.

- [ ] **Step 1: Write the failing tests**

Add to `class FolderRules` in `tests/test_doc_check.py`:

```python
    def test_a_decision_title_in_another_form_is_reported(self):
        code, out = self.check({"decisions.md": "# Decisions\n\n## 07/10/2026: old form\n\nText.\n"})
        self.assertEqual(code, 1)
        self.assertIn("decisions.md:3: a decision starts with '## Dn, DD/MM/YYYY: <name>'", out)

    def test_decisions_must_come_newest_first(self):
        text = "# Decisions\n\n## D1, 07/10/2026: a\n\nText.\n\n## D2, 08/10/2026: b\n\nText.\n"
        code, out = self.check({"decisions.md": text})
        self.assertIn("decisions.md:7: D2 is below D1: the newest decision comes first", out)

    def test_decisions_newest_first_are_clean(self):
        text = "# Decisions\n\n## D2, 08/10/2026: b\n\nText.\n\n## D1, 07/10/2026: a\n\nText.\n"
        code, out = self.check({"decisions.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_a_title_inside_a_code_block_is_not_a_decision(self):
        text = "# Decisions\n\n## D1, 07/10/2026: a\n\n```\n## not a title\n```\n"
        code, out = self.check({"decisions.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_an_obsolete_decision_needs_its_replaced_line(self):
        text = "# Obsolete decisions\n\n## D1, 07/10/2026: a\n\nText.\n"
        code, out = self.check({"obsolete.md": text})
        self.assertIn("obsolete.md:3: an obsolete decision needs 'Replaced by Dn on DD/MM/YYYY.' under its title", out)

    def test_obsolete_decisions_most_recently_replaced_first_are_clean_with_any_numbers(self):
        text = ("# Obsolete decisions\n\n## D1, 07/10/2026: a\n\nReplaced by D4 on 10/10/2026.\n\nText.\n\n"
                "## D3, 08/10/2026: b\n\nReplaced by D5 on 09/10/2026.\n\nText.\n")
        code, out = self.check({"obsolete.md": text})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_obsolete_decisions_must_come_most_recently_replaced_first(self):
        text = ("# Obsolete decisions\n\n## D3, 08/10/2026: b\n\nReplaced by D5 on 09/10/2026.\n\nText.\n\n"
                "## D1, 07/10/2026: a\n\nReplaced by D4 on 10/10/2026.\n\nText.\n")
        code, out = self.check({"obsolete.md": text})
        self.assertIn("obsolete.md:9: this decision was replaced after the one above it: "
                      "the most recently replaced comes first", out)

    def test_a_size_over_the_limit_is_reported(self):
        claude = MINIMAL["CLAUDE.md"] + "\nThe size read at each start: 60 words at most.\n"
        code, out = self.check({"CLAUDE.md": claude, "state.md": "# State\n\n" + "word " * 60 + "\n"})
        self.assertEqual(code, 1)
        self.assertRegex(out, r"CLAUDE\.md:0: the files read at each start hold \d+ words, over the limit of 60")

    def test_the_limit_may_be_written_with_a_comma(self):
        claude = MINIMAL["CLAUDE.md"] + "\nThe size read at each start: 1,000 words at most.\n"
        code, out = self.check({"CLAUDE.md": claude, "state.md": "# State\n\n" + "word " * 900 + "\n"})
        self.assertEqual((code, out.strip()), (0, "clean"))

    def test_the_default_limit_is_8000_words(self):
        code, out = self.check({"state.md": "# State\n\n" + "word " * 8001 + "\n"})
        self.assertRegex(out, r"over the limit of 8000")

    def test_the_size_option_prints_the_size_before_the_findings(self):
        with tempfile.TemporaryDirectory() as root:
            make_folder(root, MINIMAL)
            result = subprocess.run([sys.executable, "-I", str(TOOL), "--size", root],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"^read at each start: \d+ words, limit 8000\n")
        self.assertEqual(result.stdout.strip().splitlines()[-1], "clean")
```

A folder with no `decisions.md` and no `obsolete.md` is the existing `test_a_clean_folder_is_clean`: `MINIMAL` has neither.

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_doc_check -v`
Expected: the eleven new tests FAIL (no finding printed, `--size` is a usage error), the others pass.

- [ ] **Step 3: Write the code**

In `skill/templates/tools/doc-check.py`, after `STATE_MAX_LINES = 150`:

```python
DECISION_TITLE_RE = re.compile(r"^## D(\d+), " + DATE_RE + r": \S")
REPLACED_RE = re.compile(r"^Replaced by D\d+ on (\d{2})/(\d{2})/(\d{4})\.$")
START_FILES = ("CLAUDE.md", "rules.md", "state.md", "plan.md")
SIZE_LIMIT = 8000
SIZE_RE = re.compile(r"The size read at each start[^0-9]*([0-9][0-9,]*) words")
```

After `check_history`:

```python
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
```

In `check_folder`, before `for path, number, message in check_memory(folder):`:

```python
    for name, obsolete in (("decisions.md", False), ("obsolete.md", True)):
        path = folder / name
        if path.exists():
            for number, message in check_decisions(text_of(path), obsolete):
                add(path, number, message)
    limit = size_limit(text_of(claude)) if claude.exists() else SIZE_LIMIT
    words = start_size(folder)
    if words > limit:
        findings.append(f"CLAUDE.md:0: the files read at each start hold {words} words, over the limit of {limit}")
```

Replace `main` and the usage line of the docstring:

```python
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
```

The docstring usage becomes `Usage: python3 doc-check.py [--size] <internal folder>`, with one more sentence: `With --size, the first line gives the words read at each start and the limit of CLAUDE.md.`

In `skill/templates/tools/README.md`, the line of `doc-check.py` gains, before "Run at each close": `the decisions numbered and newest first, each obsolete decision with its "Replaced by" line and the most recently replaced first, the size read at each start under the limit of CLAUDE.md (`--size` prints it).`

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: The git lines, for the user**

```
git add skill/templates/tools/doc-check.py skill/templates/tools/README.md tests/test_doc_check.py
git commit -m "feat: check the order of the decisions and the size read at each start"
```

### Task 19: The migration of the decisions

**Files:**

- Modify: `skill/scripts/render.py`
- Test: `tests/test_render.py` (new class `MigrateDecisions`)

**Interfaces:**

- Consumes: the header of `templates/decisions.md` (the text before its first `## ` line), written in Task 20. The tests use their own templates folder, so this task does not wait for Task 20.
- Produces: `split_decisions(text) -> (header, [entry])`, `migrate_decisions(text, header) -> (text, [warning])`, the options `--migrate-decisions FILE --out FILE`. `--target` is no longer required by argparse; `main` asks for it in the two other modes.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_render.py` (and `import re` at the top):

```python
OLD_DECISIONS = (
    "# Decisions\n\nOne entry per decision, appended at the end.\n\n"
    "## 07/10/2026: the first\n\nFirst text.\n\n"
    "## 07/10/2026: the second\n\nSecond text.\n\n```\n## inside a block\n```\n\n"
    "## the third, without a date\n\nThird text.\n"
)


class MigrateDecisions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.templates = root / "templates"
        make(self.templates, {"decisions.md": "# Decisions\n\nNew header.\n\n## D1, {{date}}: x\n\ny\n"})
        self.source = root / "decisions.md"
        self.source.write_text(OLD_DECISIONS, encoding="utf-8")
        self.out = root / "copy.md"

    def tearDown(self):
        self.tmp.cleanup()

    def run_migrate(self):
        return subprocess.run([sys.executable, "-I", str(RENDER), "--migrate-decisions", str(self.source),
                               "--out", str(self.out), "--templates", str(self.templates)],
                              capture_output=True, text=True)

    def test_the_decisions_are_numbered_and_newest_first(self):
        result = self.run_migrate()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.out.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Decisions\n\nNew header.\n\n## D3, the third, without a date\n"), text)
        titles = re.findall(r"^## .*$", text, re.MULTILINE)
        self.assertEqual(titles, ["## D3, the third, without a date", "## D2, 07/10/2026: the second",
                                  "## inside a block", "## D1, 07/10/2026: the first"])
        for body in ("First text.", "Second text.", "Third text.", "```\n## inside a block\n```"):
            self.assertIn(body, text)
        self.assertIn(f"wrote {self.out}", result.stdout)

    def test_a_title_without_a_date_is_warned(self):
        result = self.run_migrate()
        self.assertIn("warning: D3 has no date in its title: the third, without a date", result.stdout)

    def test_the_original_is_left_as_it_was(self):
        self.run_migrate()
        self.assertEqual(self.source.read_text(encoding="utf-8"), OLD_DECISIONS)

    def test_an_existing_output_is_not_replaced(self):
        self.out.write_text("mine\n", encoding="utf-8")
        result = self.run_migrate()
        self.assertEqual(result.returncode, 2)
        self.assertIn("exists", result.stderr)
        self.assertEqual(self.out.read_text(encoding="utf-8"), "mine\n")

    def test_numbered_decisions_are_refused(self):
        self.source.write_text("# Decisions\n\n## D1, 07/10/2026: a\n\nText.\n", encoding="utf-8")
        result = self.run_migrate()
        self.assertEqual(result.returncode, 2)
        self.assertIn("already numbered", result.stderr)
        self.assertFalse(self.out.exists())

    def test_a_file_that_is_not_utf8_is_refused(self):
        self.source.write_bytes("## 07/10/2026: caf\xe9\n".encode("latin-1"))
        result = self.run_migrate()
        self.assertEqual(result.returncode, 2)
        self.assertIn("not UTF-8", result.stderr)
        self.assertFalse(self.out.exists())
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_render -v`
Expected: the six new tests FAIL with "unrecognized arguments: --migrate-decisions" (exit 2 from argparse), the others pass.

- [ ] **Step 3: Write the code**

In `skill/scripts/render.py`, the docstring gains the usage line `python3 render.py --migrate-decisions FILE --out FILE [--templates DIR]` and a paragraph:

```
With --migrate-decisions the decisions file of an older folder is
written in the current form to the --out file: the entries numbered D1
to Dn in the order they were taken, the newest first, under the header
of the template. The source is not changed, and an --out file that
exists is not replaced.
```

After `DEFAULT_TEMPLATES`:

```python
NUMBERED_RE = re.compile(r"^## D\d+, ")
TITLE_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}: ")
```

After `write`:

```python
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
```

`UnicodeDecodeError` is a subclass of `ValueError`, so its `except` comes first.

In `main`: the `--target` argument loses `required=True`; two arguments are added, `--migrate-decisions` (help: "the decisions file of an older folder, written in the current form to --out") and `--out` (help: "the file the migrated decisions are written to"). After `args = parser.parse_args(argv)`:

```python
    if args.migrate_decisions:
        if not args.out:
            parser.error("--out is needed with --migrate-decisions")
        return run_migration(args.migrate_decisions, args.out, args.templates)
    if not args.target:
        parser.error("--target is needed")
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: The git lines, for the user**

```
git add skill/scripts/render.py tests/test_render.py
git commit -m "feat: migrate an older decisions file to numbered entries, newest first"
```

### Task 20: The decisions newest first and obsolete.md

**Files:**

- Modify: `skill/templates/decisions.md`, `skill/templates/CLAUDE.md` (the table), `skill/templates/lifecycle.md` (the last sentence)
- Create: `skill/templates/obsolete.md`
- Test: `tests/test_package.py`, `tests/test_render.py`

**Interfaces:**

- Consumes: `check_decisions` of Task 18, the header read by `run_migration` of Task 19.
- Produces: the header of `templates/decisions.md` (text before its first `## `), with no placeholder.

- [ ] **Step 1: Write the failing tests**

In `tests/test_package.py`, add `"templates/obsolete.md"` to the `expected` list of `test_the_expected_files_exist`, and to `class SkillStructure`:

```python
    def test_the_decisions_are_numbered_and_obsolete_is_in_the_table(self):
        decisions = (SKILL / "templates" / "decisions.md").read_text(encoding="utf-8")
        self.assertIn("\n## D1, {{date}}: ", decisions)
        self.assertNotIn("{{", decisions.split("\n## ", 1)[0])
        claude = (SKILL / "templates" / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("| `obsolete.md` |", claude)
```

In `tests/test_render.py`, add:

```python
class RealTemplates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.target = Path(self.tmp.name) / "internal-My Project"

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_render_of_the_real_templates_reads_clean(self):
        answers = Path(self.tmp.name) / "answers.json"
        answers.write_text(json.dumps(ANSWERS), encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--answers", str(answers),
                                 "--target", str(self.target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        check = subprocess.run([sys.executable, "-I", str(self.target / "tools" / "doc-check.py"),
                                str(self.target)], capture_output=True, text=True)
        self.assertEqual(check.stdout.strip().splitlines()[-1], "clean", check.stdout)

    def test_a_repair_of_an_older_folder_adds_obsolete(self):
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(RENDER), "--repair", "--target", str(self.target)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / "obsolete.md").exists())
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_package tests.test_render -v`
Expected: FAIL on the missing `templates/obsolete.md`, the `## D1` title, the table row; the real render reports the old decision title.

- [ ] **Step 3: Write the templates**

`skill/templates/decisions.md`, whole:

```markdown
# Decisions

The decisions in force, the newest first. Each entry gives its number,
the date, what was decided, on whose word and why. A decision on the
Roadmap, on a rule or on the design goes at the top when it is taken,
with the next number. A decision replaced by a newer one moves whole to
`obsolete.md`, and the new decision names it and restates the part that
still holds.

## D1, {{date}}: the memory system

The project keeps its memory in `{{internal}}/`, installed by
`/total-recall`, the user's word. Phase 01 is {{phase1_name}}.
```

`skill/templates/obsolete.md`, whole:

```markdown
# Obsolete decisions

The decisions replaced by a newer one, the most recently replaced
first. Each entry is moved whole from `decisions.md`, with one line
under its title: `Replaced by Dn on DD/MM/YYYY.`
```

In `skill/templates/CLAUDE.md`, the row of `decisions.md` becomes `| `decisions.md` | The decisions in force, numbered, newest first |`, and a row follows it: `| `obsolete.md` | The decisions replaced by a newer one, with the number of the one that replaced them |`.

In `skill/templates/lifecycle.md`, the last sentence becomes: "The decisions on the Roadmap are in `decisions.md`, and the replaced ones in `obsolete.md`."

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: The git lines, for the user**

```
git add skill/templates/decisions.md skill/templates/obsolete.md skill/templates/CLAUDE.md skill/templates/lifecycle.md tests/test_package.py tests/test_render.py
git commit -m "feat: decisions numbered and newest first, replaced ones in obsolete.md"
```

### Task 21: The git question

**Files:**

- Modify: `skill/SKILL.md` (the description, the opening, steps 2, 5, 7, 9)
- Modify: `skill/templates/CLAUDE.md` ("Working documents"), `skill/templates/rules.md` ("The internal folder"), `skill/templates/memory/project-instruction-file.md`, `skill/templates/history.md`, `skill/templates/close.md` (the last line)
- Test: `tests/test_package.py` (new class `GitQuestion`)

**Interfaces:**

- Produces: the literal question `Keep the folder out of git, yes or no?` in step 5, the opening `Only when the user answered yes` of step 7.

- [ ] **Step 1: Write the failing tests**

```python
def skill_steps():
    """The numbered steps of SKILL.md, by number: the title line, then the body."""
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    parts = re.split(r"^## (\d+)\. ", text, flags=re.MULTILINE)
    return dict(zip(parts[1::2], parts[2::2]))


class GitQuestion(unittest.TestCase):
    def test_the_skill_asks_before_the_exclusion(self):
        steps = skill_steps()
        self.assertIn("Keep the folder out of git, yes or no?", steps["5"])
        self.assertTrue(steps["7"].split("\n", 1)[1].strip().startswith("Only when the user answered yes"))

    def test_no_template_states_how_git_treats_the_folder(self):
        for path in (SKILL / "templates").rglob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in ("out of git", "does not track", "info/exclude", "not in git", "goes through git"):
                self.assertNotIn(phrase, text, f"{path.relative_to(SKILL)} says {phrase!r}")
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_package -v`
Expected: both new tests FAIL (`templates/CLAUDE.md says 'does not track'`).

- [ ] **Step 3: Write the text**

`SKILL.md`:

- The description: `Sets up a persistent memory for a project in an internal folder, checks an existing one and brings it to the current form. Each Claude Code session then knows what was done and what comes next. Use when the user types /total-recall, or asks to set up, install, check, repair or update the project memory, the internal folder or total recall on a repository.`
- The opening paragraph ends at "updates at its close." The two sentences on `.git/info/exclude` and on the folder name as the only trace are removed.
- Step 2, item 2: `Read .git/info/exclude and say whether the line ... is there, as information.`
- Step 5, after "Show the one line that will be handed over for `.git/info/exclude`": replaced by:

  ```
  Ask one question: "Keep the folder out of git, yes or no?" On a yes,
  show the line that step 7 hands over. The answer is not written in
  any file. Wait for the go.
  ```

- Step 7 starts with: `Only when the user answered yes in step 5. On a no, go to step 8.`
- Step 9, item 1: `On a yes in step 5, git status shows nothing from the internal folder.`

`skill/templates/CLAUDE.md`, "Working documents", the paragraph becomes:

```
`{{internal}}/` is the memory of the project. Claude Code loads this
file when a session reads a file in the folder.
```

`skill/templates/rules.md`, "The internal folder": the first paragraph becomes `The memory of the project is the internal folder named in the project file.` The first bullet keeps its text. The last bullet becomes: `A spec or a plan written by a skill is saved under records/ of the folder, and its tasks become tasks of the open phase.`

`skill/templates/memory/project-instruction-file.md`: the first paragraph ends at "The repository has no instruction file at its root." The why becomes: `the user keeps the instruction file, the documents and the notes in one folder of the project, and wants them to work on any machine without a setting.`

`skill/templates/history.md`: the bullet on the exclusion line is removed.

`skill/templates/close.md`, the last line of "The reply" becomes: `The close runs no git command.`

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: The git lines, for the user**

```
git add skill/SKILL.md skill/templates/CLAUDE.md skill/templates/rules.md skill/templates/memory/project-instruction-file.md skill/templates/history.md skill/templates/close.md tests/test_package.py
git commit -m "feat: ask whether git should ignore the internal folder"
```

### Task 22: When to ask before a write

**Files:**

- Modify: `skill/templates/rules.md` (a subsection at the end of "The internal folder")
- Modify: `skill/templates/CLAUDE.md` ("Working documents", "Sessions")
- Modify: `skill/templates/close.md` (a first step, the opening sentence)
- Test: `tests/test_package.py` (new class `WhenToAsk`)

**Interfaces:**

- Consumes: `size_limit` of Task 18 reads `The size read at each start: 8,000 words at most.`
- Produces: the heading `### When to ask before a write` of `rules.md`, which Tasks 23 and 24 name.

- [ ] **Step 1: Write the failing tests**

```python
class WhenToAsk(unittest.TestCase):
    def read(self, name):
        return (SKILL / "templates" / name).read_text(encoding="utf-8")

    def test_the_rules_say_when_to_ask_before_a_write(self):
        rules = self.read("rules.md")
        self.assertIn("### When to ask before a write", rules)
        for label in ("**Written without asking**", "**Asked first**", "**When to ask**", "**A proposal**"):
            self.assertIn(label, rules)

    def test_the_project_file_points_to_the_rule_and_sets_the_size(self):
        claude = self.read("CLAUDE.md")
        self.assertIn('"When to ask before a write"', claude)
        self.assertNotIn("becomes a memory note at once", claude)
        self.assertIn("The size read at each start", claude)
        self.assertIn("8,000 words", claude)

    def test_the_close_asks_the_held_proposals_first(self):
        steps = re.findall(r"^(\d+)\. (.*)$", self.read("close.md"), re.MULTILINE)
        self.assertEqual(steps[0][0], "1")
        self.assertTrue(steps[0][1].startswith("Ask the proposals held"), steps[0])
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_package -v`
Expected: the three new tests FAIL.

- [ ] **Step 3: Write the text**

`skill/templates/rules.md`, at the end of "The internal folder":

```markdown
### When to ask before a write

The memory is read again in each session, so what goes in it costs
tokens and attention. The session decides when the user's judgment is
needed, and the user keeps working on the project in the meantime.

**Written without asking**, when the place is obvious and the cost is
small:

- a ticked step, a history entry, a decision, a Roadmap item;
- a fact in the file that owns it, when that file is not read at each
  start: a phase file, a record, the code map.

**Asked first**, when the user's judgment matters:

- the text goes into a file read at each start (`CLAUDE.md`,
  `rules.md`, a memory note), and each line there is read in every
  session;
- the text changes, weakens or contradicts something written;
- the place is unclear, or between two files;
- the text is large: a new file, a new note, a section rewritten.

**When to ask:** the questions are held for a pause in the work, the
end of a task or the close, and asked together in one message. A
correction from the user is proposed at once, since it changes the
work of the same session.

**A proposal** gives what would be written, where, its size when the
file is read at each start, and two or three options: this place, a
cheaper place, nothing.
```

`skill/templates/CLAUDE.md`, "Working documents", after the paragraph of Task 21:

```
The size read at each start (this file, `rules.md`, `state.md`,
`plan.md` and the memory notes): 8,000 words at most.
`tools/doc-check.py` reports it.
```

`skill/templates/CLAUDE.md`, "Sessions", "During the session": the bullet "A correction from the user becomes a memory note at once, or updates the note on that topic." becomes:

```
- What the session learns is written by `rules.md`, "When to ask
  before a write": a correction from the user is proposed at once, the
  rest waits for a pause.
```

The bullet "A decision is appended to `decisions.md` when it is taken. A document is edited mid-session only when a decision makes it wrong." becomes:

```
- A decision goes at the top of `decisions.md` with the next number,
  and a decision it replaces moves to `obsolete.md`. A document is
  edited mid-session only when a decision makes it wrong.
```

`skill/templates/close.md`: the opening sentence "The routine runs without asking permission." becomes "The routine runs without asking permission, apart from the proposals of step 1." A first step is added and the others are renumbered 2 to 9:

```
1. Ask the proposals held during the session in one message, by
   `rules.md`, "When to ask before a write", and write the approved
   ones. With no proposal held, go to step 2.
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS, the real render of Task 20 reads clean (its size is under 8,000 words).

- [ ] **Step 5: The git lines, for the user**

```
git add skill/templates/rules.md skill/templates/CLAUDE.md skill/templates/close.md tests/test_package.py
git commit -m "feat: ask before a write only when the user's judgment matters"
```

### Task 23: The review of the memory

**Files:**

- Create: `skill/templates/review.md`
- Modify: `skill/templates/CLAUDE.md` (the table, "Sessions"), `skill/templates/close.md` (a last step), `skill/SKILL.md` (the table, step 2)
- Test: `tests/test_package.py` (new class `Review`), `tests/test_render.py`

**Interfaces:**

- Consumes: `doc-check.py --size` (Task 18), `render.py --migrate-decisions` (Task 19), `obsolete.md` (Task 20), the rule of Task 22.
- Produces: the phrase "review the memory", the report `records/YYYY-MM-DD-review.md`.

- [ ] **Step 1: Write the failing tests**

In `tests/test_package.py`, add `"templates/review.md"` to the `expected` list, and:

```python
class Review(unittest.TestCase):
    def read(self, name):
        return (SKILL / "templates" / name).read_text(encoding="utf-8")

    def test_the_review_is_named_in_the_project_file_and_the_skill(self):
        claude = self.read("CLAUDE.md")
        self.assertIn("| `review.md` |", claude)
        self.assertIn('"review the memory"', claude)
        self.assertIn("| `review.md` |", (SKILL / "SKILL.md").read_text(encoding="utf-8"))

    def test_the_review_writes_a_report_before_any_change(self):
        review = self.read("review.md")
        self.assertIn("records/YYYY-MM-DD-review.md", review)
        self.assertIn("Nothing is changed before the user approves", review)
        self.assertIn("doc-check.py\" --size", review)

    def test_the_check_mode_brings_an_older_folder_to_the_current_form(self):
        step = skill_steps()["2"]
        for needle in ("--migrate-decisions", "diff -u", "review the memory"):
            self.assertIn(needle, step)

    def test_the_close_suggests_the_review_without_starting_it(self):
        self.assertIn("Suggest the review", self.read("close.md"))
```

In `tests/test_render.py`, `class RealTemplates`:

```python
    def test_a_repair_of_an_older_folder_adds_the_review(self):
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
        subprocess.run([sys.executable, "-I", str(RENDER), "--repair", "--target", str(self.target)],
                       capture_output=True, text=True)
        self.assertTrue((self.target / "review.md").exists())
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_package tests.test_render -v`
Expected: the five new tests FAIL.

- [ ] **Step 3: Write the text**

`skill/templates/review.md`, whole:

````markdown
# The review of the memory

Read when the user says "review the memory". The review reads the whole
folder, writes a report of the changes it proposes, and applies the
ones the user approves. Nothing is changed before the user approves the
report.

## What it reads

- Living documents, which the review may rewrite: `CLAUDE.md`,
  `rules.md`, the memory notes, `plan.md`, `state.md`, `decisions.md`,
  `lifecycle.md`, `close.md`, `review.md`, `code-map.md` and the open
  phase file.
- Records, which the review does not rewrite: `history.md`, `story.md`,
  `obsolete.md`, the closed phase files and `records/`. They are read
  for the dates and the facts.

## The steps

1. Run the check with the size:

   ```
   python3 "<internal folder>/tools/doc-check.py" --size "<internal folder>"
   ```

   Note the size read at each start and the findings.
2. Read the whole folder and look for five kinds of items:
   1. Contradictions: two statements that disagree. Give both, with
      their dates and their places, and propose the one that wins,
      usually the newer.
   2. Duplicates: the same fact in two places. The fact stays in the
      file that owns it, and the other place links to it.
   3. Out of date: a file, a task or a state named that no longer
      exists. Check it against the tree before the item is written.
   4. Misplaced: text read at each start that a session needs rarely.
      Propose the file read when it applies.
   5. Replaced decisions: a decision of `decisions.md` that a newer one
      replaces.
3. Write the report in `records/YYYY-MM-DD-review.md`. List the name
   first, and add `-2` for a second review on the same day. The report
   gives the size before, then the items numbered from 1, grouped by
   kind. Each item gives the file and the heading, the current text,
   the proposed text and the reason.
4. Show the report in the reply, a line per item, and ask the user to
   answer by number: "all", "all but 3", "1 and 4". A contradiction is
   settled only by the user's choice. The other items can be approved
   together.
5. Apply the approved items. A replaced decision moves whole to the top
   of `obsolete.md`, with the line `Replaced by Dn on DD/MM/YYYY.`
   under its title, and the newer decision names it.
6. Add the report to `records/README.md`, run the check with the size
   again, and fix what it reports.

## The reply

The items applied and the items left, a line each, the size before and
after, and the last line of the check.
````

`skill/templates/CLAUDE.md`: the table gains `| `review.md` | The review of the memory |` after the row of `close.md`. "Sessions" gains, after the paragraph of the close:

```
"review the memory" runs the review: read `review.md` and follow it.
It changes nothing before the user approves its report.
```

`skill/templates/close.md`: a last step, 10:

```
10. Suggest the review in one line when a reason exists: the check
    reports the size over the limit, a contradiction was found in the
    session, or a phase closes. The close does not start it.
```

`SKILL.md`: the table of "What it installs" gains the rows of `obsolete.md` and `review.md` as in `templates/CLAUDE.md`, and the row of `decisions.md` reads "The decisions in force, numbered, newest first". The opening line of step 2 becomes "When `internal-<project-name>/` exists, check it, bring it to the current form, and stop:", items 1 to 4 are kept, and three items follow them, before "Then stop.":

````markdown
5. Compare the routine files with the current templates: `rules.md`,
   `close.md`, `lifecycle.md`, `review.md`, `tools/doc-check.py`,
   `tools/machine-check.py`. For each one that differs, run

   ```
   diff -u "internal-<project-name>/<file>" "${CLAUDE_SKILL_DIR}/templates/<file>"
   ```

   and say in a few lines what changed. `rules.md` is replaced whole,
   since the project file adds to it and does not edit it. `close.md`
   and `lifecycle.md` may hold the project's own edits: the user
   chooses for each file. Hand the `cp` lines of the chosen files to
   the user in one block. The user runs them.
6. When the titles of `decisions.md` have no number, write the current
   form in a copy:

   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --migrate-decisions "internal-<project-name>/decisions.md" --out "<scratchpad>/decisions.md"
   ```

   Show the head of the copy and each `warning:` line, then hand over
   the line that replaces the file:

   ```
   cp "<scratchpad>/decisions.md" "internal-<project-name>/decisions.md"
   ```

7. Offer the review of the content, "review the memory", which follows
   `review.md` of the folder.
````

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS. `SKILL.md` body under 500 lines.

- [ ] **Step 5: The git lines, for the user**

```
git add skill/templates/review.md skill/templates/CLAUDE.md skill/templates/close.md skill/SKILL.md tests/test_package.py tests/test_render.py
git commit -m "feat: review of the memory, and the update of an older folder"
```

### Task 24: The README for a public skill

**Files:**

- Modify: `README.md` (rewritten whole), `skill/SKILL.md` (`<folder>` becomes `<project-name>`)
- Test: `tests/test_package.py` (new class `Readme`)

**Interfaces:**

- Consumes: the behavior of Tasks 18 to 23, which the README describes.

- [ ] **Step 1: Write the failing tests**

```python
def prose(text):
    """The text without its fenced code blocks and its inline code."""
    text = re.sub(r"^\s*```.*?^\s*```", "", text, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


class Readme(unittest.TestCase):
    def test_a_path_is_written_in_backticks(self):
        for path in (ROOT / "README.md", SKILL / "SKILL.md"):
            found = re.findall(r"<[A-Za-z][^>\n]*>", prose(path.read_text(encoding="utf-8")))
            self.assertEqual(found, [], f"{path.name}: GitHub drops these as HTML tags")

    def test_the_folder_is_named_after_the_project(self):
        for path in (ROOT / "README.md", SKILL / "SKILL.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("<folder>", text, path.name)
        self.assertIn("internal-<project-name>", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_the_readme_does_not_talk_about_its_voice_or_state_the_git_choice(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        for phrase in ("voice", "does not track", "not in git", "keeps it out of git"):
            self.assertNotIn(phrase, text)
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest tests.test_package -v`
Expected: the three new tests FAIL (`<folder>` in prose, "my voice").

- [ ] **Step 3: Write the README and rename the placeholder**

In `SKILL.md`, replace each `<folder>` with `<project-name>` (`sed -i 's/<folder>/<project-name>/g' skill/SKILL.md`), and fix any `<...>` left outside backticks.

`README.md`, whole. This draft is shown to the user before the tests run, and the user's corrections go in before Step 4:

````markdown
# Total recall

I work on my projects with Claude Code over many sessions, and each
session started from nothing. I had to explain again where the project
was, what was decided and how I like to work. Total recall is the skill
I made for that. It gives a project a memory: a folder of plain
documents inside the project, which a session reads at its start and
updates at its close.

The folder is named `internal-<project-name>`, after the project's
folder. At the install, the skill asks whether git should ignore it.

## What it installs

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents |
| `state.md` | The snapshot: position, done this session, next, waiting on the user |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps |
| `history.md` | The session log, newest first |
| `story.md` | The diary of the project, a short story at each close |
| `decisions.md` | The decisions in force, numbered, newest first |
| `obsolete.md` | The decisions replaced by a newer one |
| `close.md` | The close routine |
| `review.md` | The review of the memory |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records: a pasted log, a study, a spec written by a skill |
| `tools/` | A check of the documents and a check of the machine |
| `memory/` | The memory notes of the project and their index |

## How a session works

The session opens with "let's start", or with "read
`internal-<project-name>/CLAUDE.md`" on a machine that has no global
rules file. It reads the project file, the rules, the snapshot and the
memory notes, then the open phase, and gives a briefing: where the
project is, what the last session did, what comes next, what waits on
the user. Then it waits for the go.

During the session the work follows the open phase, a task at a time.
Small facts with an obvious place are written as the work goes: a
ticked step, a decision, a Roadmap item. A text that would go into a
file read at each start, or that changes something already written, is
proposed first, at a pause in the work. I did not want to stop my
project to look after its documents.

"let's close" runs the close routine: the held proposals, the snapshot
rewritten, the phase file checked, the Roadmap cleared, an entry in the
history and in the story, the project file reread against the project,
and the check tool run on the documents.

## The review of the memory

Requirements change, and after a few months the documents of a project
contradicted each other. "review the memory" reads the whole folder and
writes a report: contradictions, duplicates, text out of date, text in
the wrong place, replaced decisions. Each item gives the current text,
the proposed text and the reason. Nothing is applied before the user
approves it by number.

A folder made by an older version of the skill is brought to the
current form by `/total-recall` in that project. The skill shows what
changed in the routine files, numbers the decisions, then offers the
review.

## The plan

Work is in phases, tasks and steps. Phases count from 01, tasks from 1
across phases, steps inside a task. A phase is a file. The project
always has an open phase, so each piece of work has a home. The rules
are in `lifecycle.md` of the folder.

## Install the skill

The skill is the `skill/` folder of this repository. Link it, or copy
it, into the skills folder of Claude Code:

```
ln -s "$(pwd)/skill" ~/.claude/skills/total-recall
```

A copy (`cp -r skill ~/.claude/skills/total-recall`) does not follow
this repository when it changes.

## Use it on a project

1. In the project folder, run `git init` if the folder is not a
   repository yet.
2. Start Claude Code there and type `/total-recall`.
3. Answer the five questions, read the description it writes, and
   correct it until it is right.
4. Say whether git should ignore the folder. On a yes, run the line the
   skill hands over, then `git status` to see that nothing of the
   folder shows.
5. Read the machine table. When a guardrail is missing, the skill
   proposes the lines to run.
6. Open the first session with "let's start".

## Check it

1. On a yes at step 4, `git status` shows nothing from the internal
   folder.
2. A new session opened with "read `internal-<project-name>/CLAUDE.md`"
   gives the briefing, with Phase 01 open and Task 1 next.
3. "let's close" rewrites `state.md` and adds an entry at the top of
   `history.md`.

## On another machine

Install the skill, open the project, and start the session with "read
`internal-<project-name>/CLAUDE.md`". The rules travel with the folder,
and the session follows them without a global file. The machine check,
`tools/machine-check.py` of the folder, says which guardrails the
machine has: the permission deny list, the guard hooks, `jq`, the
sandbox. The skill ships the deny list and the three guard scripts
under `skill/machine/`, and proposes them when they are missing.

## The guardrails

The guardrails keep a session from writing where it should not: a deny
list of permissions (git writes, sudo, the destructive tools) and two
hook scripts, with a library they share, that read each command before
it runs and refuse git writes, recursive deletes and writes into
`.git`. Claude Code applies them from `~/.claude/settings.json`. The
scripts need `jq`.

## Limits

- When git ignores the folder, the folder has no history and no backup.
  I keep a copy of it myself.
- The skill writes nothing under `.claude/` and nothing outside the
  project. The sandbox is a setting of the machine.
- The check tool reads Markdown in the form the templates use. A
  document in another form gets findings to read, not errors.
- I tried it on Linux with Python 3 (for the moment). The tools use
  the standard library only.

## Tests

```
python3 -m unittest discover -s tests -v
```
````

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS.

- [ ] **Step 5: The git lines, for the user**

```
git add README.md skill/SKILL.md tests/test_package.py
git commit -m "doc: readme rewritten for a public skill, folder named after the project"
```

### Task 25: The final check

**Files:** none changed, unless a check fails.

- [ ] **Step 1: The suite**

Run: `python3 -m unittest discover -s tests -v`
Expected: all tests PASS, the count above 58.

- [ ] **Step 2: The sample render**

Render the real templates into `<the session scratchpad>/sample/internal-sample` with the answers of `tests/test_render.py`, then run its `tools/doc-check.py --size`. Expected: the size line, then `clean`.

- [ ] **Step 3: The migration on a copy of this project's decisions**

Copy `internal-total-recall/decisions.md` to the scratchpad, run `render.py --migrate-decisions` on the copy, and show the head of the result and the warnings. This folder is not changed: its review waits for the user's word.

- [ ] **Step 4: The dashes and the blank lines**

Run `python3 skill/templates/tools/doc-check.py internal-total-recall` for this folder's own text (it reports the old form of the decisions, expected until the review), and the package test for the dashes.

- [ ] **Step 5: The scenario for the user**

1. A scratch repository: `/total-recall`, answer "no" to the git question. Expected: no exclusion line handed over, `git status` shows the folder (correct on a no).
2. The same with "yes". Expected: the line handed over, `git status` clean.
3. `/total-recall` again on the folder of step 1. Expected: the check, no routine file differs, the decisions already numbered, the offer of the review.
4. "review the memory" on that folder. Expected: a report under `records/` with few or no items (a fresh folder), nothing changed before the answer.
5. The README on GitHub after the push: `internal-<project-name>` shows whole.
