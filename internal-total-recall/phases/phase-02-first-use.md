# Phase 02: First use

Opened 07/10/2026 at the close of Phase 01, named from the head of the
Roadmap. The phase takes the feedback of the first trials of the skill,
on a scratch repository and on real projects, and improves the skill
from it. The user tries, takes notes, and brings them to a session.

**The rules:**

- A list of notes is summarized one item at a time and discussed before
  any analysis. Each item that leads to a change becomes a task with
  its test, by `rules.md`, "Reports and issues".
- A change to a tool or to the render script starts with a failing
  test. A change to a template is checked by the sample render and
  `tools/doc-check.py`.
- The installed copies of the tools in this folder follow the
  templates: a changed tool is copied here in the same task.
- The rules of `lifecycle.md`, "The numbers", hold.

**The order:**

1. Task 15, the feedback of the first trial.
2. Task 16, the name of the reference project removed from this folder.
3. Task 17, the user's style as a memory note.
4. Tasks 18 to 25, the memory used with care: the spec
   `records/2026-10-10-design.md` and the plan
   `records/2026-10-10-plan.md`, approved 10/10/2026, run in this
   session by the session itself, a task at a time on the user's word.
5. The review of this project's folder with the new command, on the
   user's word after the delivery.
6. The close of the phase, as its last task.

### The opening of the phase

No step: the project has no opening routine.

### Task 15: The feedback of the first trial

What it does and why: the user tries the skill on a scratch repository
with the scenario of `SKILL.md`, and on a real project, and notes what
goes wrong, what is missing and what could be better. The session reads
the notes one at a time, discusses each, and turns the agreed ones into
tasks of this phase.

**The steps:**

- [x] **Step 1: The notes** The user's notes, read one item at a time,
  with the session's view on each: a fault to reproduce, a change to
  design, or a note for the Roadmap. The first two came on 07/10/2026,
  from the user's read of this folder right after the close: the
  reference project named in the folder (Task 16, done), and the
  user's style not found under `memory/` (Task 17, done on the user's
  word). Done 10/10/2026: three notes from the trials (the git
  question, the memory used with care with a review command, the
  README), and two ideas of the user (decisions newest first,
  `obsolete.md`), discussed one at a time and written as a spec,
  `records/2026-10-10-design.md`, waiting on the user's review.
- [x] **Step 2: The tasks** Each agreed item written as a task of this
  phase, in the task form, numbered from 18. Done 10/10/2026: the plan
  `records/2026-10-10-plan.md`, approved by the user, written below as
  Tasks 18 to 25. The full steps, the code and the tests are in the
  plan.

### Task 16: The name of the reference project removed from this folder

What it does and why: the user found the name of the reference project
and the path of its folder in this internal folder, in seven files.
The rule of Phase 01 had allowed it in the folder, which the user did
not want: the name is not written anywhere, the user gives the path
when a session needs it.

**The steps:**

- [x] **Step 1: The prose files** The history, this phase file's rules,
  the memory note and its index line, rewritten without the name or
  the path. Done 07/10/2026: four files rewritten.
- [x] **Step 2: The records** The spec, the plan, the review and the
  ledger: the name, the path of the folder, the path of this machine
  and the session scratchpad replaced by placeholders, with a line in
  `records/README.md`. Done 07/10/2026: zero mentions left over the
  folder (`grep -ri`), the check tool clean.

### Task 17: The user's style as a memory note

What it does and why: the user's style lived in `rules.md`, "The user's
style", by the consolidation of the spec, and the user looked for it
under `memory/`. Their word: "in memory is stronger and less prone to
be forgotten, that is the purpose". The style becomes a memory note
shipped in every project, read whole at the start and before writing
any text, and `rules.md` points to it.

**The steps:**

- [x] **Step 1: The test** The expected files of the package gain the
  note; a test checks the index line, the pointer in `rules.md` and the
  eighteen rules of the note. Done 07/10/2026: red on both.
- [x] **Step 2: The note and the pointer**
  `templates/memory/user-writing-style.md` (the eighteen rules, where
  each applies, the rule of a reply, the why and the how), its line in
  `templates/memory/MEMORY.md`, and the section of `templates/rules.md`
  replaced by a pointer. Done 07/10/2026: 58 tests green, the sample
  render writes eighteen files and reads clean, `rules.md` is 280
  lines.
- [x] **Step 3: The install here** The note, the index line and the
  rules copied into this folder. Done 07/10/2026: copies identical to
  the templates, three notes in `memory/`, the check tool clean.

The git line: `feat: the user's writing style shipped as a memory note`.

### Task 18: The check of the decisions and of the size

What it does and why: `doc-check.py` checks that the decisions are
numbered and newest first, that each obsolete decision has its
"Replaced by" line with the most recently replaced first, and that the
size read at each start stays under the limit of `CLAUDE.md`. The
review and the close rely on these checks. Plan, Task 18.

The files: `skill/templates/tools/doc-check.py`,
`skill/templates/tools/README.md`, `tests/test_doc_check.py`. The
copy in this folder's `tools/` waits for the review of this project.

**The steps:**

- [x] **Step 1: The tests** Eleven tests in `FolderRules`, seen red.
  Done 10/10/2026: seven red. The four others check a clean folder and
  passed before the code, since the old tool reports nothing there: the
  plan's "eleven red" was a miscount.
- [x] **Step 2: The code** `check_decisions`, `start_size`,
  `size_limit`, the option `--size`, the README line; the suite green.
  Done 10/10/2026: 69 tests green. The new tool run on this folder
  prints `read at each start: 5780 words, limit 8000` and 15 findings,
  the 15 old titles of `decisions.md`, expected until the review.

The git line: `feat: check the order of the decisions and the size read at each start`.

### Task 19: The migration of the decisions

What it does and why: `render.py --migrate-decisions` writes the
decisions of an older folder in the new form, in a copy, so that an
older project can be brought up to date without losing a word. Plan,
Task 19.

**The steps:**

- [x] **Step 1: The tests** Six tests in `MigrateDecisions`, seen red.
  Done 10/10/2026: five red. The sixth checks that the source is left
  as it was, which holds before the code too.
- [x] **Step 2: The code** The migration and its options; the suite
  green. Done 10/10/2026: 75 tests green. On a copy of this folder's
  decisions: 15 entries, D15 on top, 15 words more (one `Dn,` each),
  the original's checksum unchanged, a second run refused with exit 2,
  and the new check reads `clean` on a scratch copy of the folder with
  the migrated file.

The git line: `feat: migrate an older decisions file to numbered entries, newest first`.

### Task 20: The decisions newest first and obsolete.md

What it does and why: the templates write the decisions numbered and
newest first, and ship `obsolete.md`. Plan, Task 20.

**The steps:**

- [x] **Step 1: The tests** The package and the real render, seen red.
  Done 10/10/2026: four red, the real render with one finding, the old
  decision title.
- [x] **Step 2: The templates** `decisions.md`, `obsolete.md`, the
  table of `CLAUDE.md`, `lifecycle.md`; the suite green. Done
  10/10/2026: 78 tests green. A sample render writes 19 files, `## D1`
  in its decisions, reads `clean` with 4532 words read at each start.
  The migration of a copy of this folder's decisions now takes the new
  header.

The git line: `feat: decisions numbered and newest first, replaced ones in obsolete.md`.

### Task 21: The git question

What it does and why: the skill asks whether the internal folder stays
out of git, and no template states the answer. The user's note. Plan,
Task 21.

**The steps:**

- [x] **Step 1: The tests** `GitQuestion`, seen red. Done 10/10/2026:
  both red, `templates/rules.md` said "does not track" and step 5 had
  no question.
- [x] **Step 2: The text** `SKILL.md` and the templates; the suite
  green. Done 10/10/2026: 80 tests green. A sample render reads
  `clean`, and none of its sentences says how git treats the folder.
  `SKILL.md` keeps the exclusion in step 2 (reported as information),
  step 5 (the question) and step 7 (on a yes only). The README is Task
  24.

The git line: `feat: ask whether git should ignore the internal folder`.

### Task 22: When to ask before a write

What it does and why: the rules say when a write to the memory needs
the user's judgment and when it does not, so that the documents follow
the work without stopping it. The user's note. Plan, Task 22.

**The steps:**

- [x] **Step 1: The tests** `WhenToAsk`, seen red. Done 10/10/2026:
  three red.
- [x] **Step 2: The text** `rules.md`, `CLAUDE.md`, `close.md`; the
  suite green. Done 10/10/2026: 83 tests green. Two literals of the
  plan's text did not match its tests (`**When to ask:**` with the
  colon inside the bold, the quoted heading wrapped over two lines),
  fixed in the text: the colon outside the bold like the other labels,
  the quote on one line. A sample render reads `clean`, 4762 words read
  at each start. The close now has nine steps: the new step 1, the old
  ones renumbered 2 to 9.

The git line: `feat: ask before a write only when the user's judgment matters`.

### Task 23: The review of the memory

What it does and why: "review the memory" proposes the cleanup of the
folder in a report and applies the approved items, and `/total-recall`
brings an older folder to the current form. The user's note. Plan,
Task 23.

**The steps:**

- [x] **Step 1: The tests** `Review` and the repair, seen red. Done
  10/10/2026: six red, one of them an error on the missing
  `review.md`.
- [x] **Step 2: The text** `review.md`, `CLAUDE.md`, `close.md`,
  `SKILL.md`; the suite green. Done 10/10/2026: 88 tests green,
  `SKILL.md` 263 lines. The new items of step 2 write `<folder>` like
  the rest of `SKILL.md`, renamed with the rest in Task 24. Three blank
  lines added before a list item that follows a paragraph inside the
  item before it (`review.md` step 2, `SKILL.md` items 5 and 6): the
  check reports that form, a limit already among the review's minors.
  On a scratch copy of this folder, the repair writes `obsolete.md` and
  `review.md` and keeps the rest. Four routine files differ from the
  templates (lines changed: `rules.md` 23, `close.md` 27,
  `lifecycle.md` 2, `tools/doc-check.py` 99). A sample render reads
  `clean`, 4791 words read at each start.

What was found on the way: the repair prints `needs answers:
phases/phase-01-{{phase1_slug}}.md` on a folder whose first phase file
has its own name (`phase-01-the-skill.md` here). The file exists, and
the hint is wrong. The behavior predates this plan. A candidate for the
Roadmap, with the review's minors.

The git line: `feat: review of the memory, and the update of an older folder`.

### Task 24: The README for a public skill

What it does and why: the README is written for readers who do not
know the project, in the user's voice, and names the folder
`internal-<project-name>` in backticks. The user's note. Plan, Task 24.

**The steps:**

- [x] **Step 1: The tests** `Readme`, seen red. Done 10/10/2026:
  three red, among them three `<folder>` outside backticks in the
  README, the cause of the `internal-/` the user saw on GitHub.
- [x] **Step 2: The draft** Shown to the user and corrected. Done
  10/10/2026: three sentences of the plan's draft fixed by the style
  rules before showing it (two images, a paragraph in mixed tenses);
  the user's word: "it's fine".
- [x] **Step 3: The README and the placeholder** The suite green. Done
  10/10/2026: 91 tests green. `SKILL.md`: 16 `<folder>` renamed to
  `<project-name>`, one path of step 9 put in backticks, two lines
  rewrapped.
- [x] **Step 4: Why scripts?** A section of the README on the user's
  question, why the skill uses Python. Done 10/10/2026: the user's
  corrections ("by hand" replaced by Claude as the actor, a rough
  comparison of the cost) applied; about 14,000 words of this folder
  without its records, around 18,000 tokens at about 1.3 tokens a
  word, against one command; 91 tests green.
- [x] **Step 5: The phrase and the lines** "let's start" in the README
  in place of "read `internal-<project-name>/CLAUDE.md`", and the
  wrapped lines joined, after the user's own edits (`7e49fdc` and
  before). Done 10/10/2026: the read phrase kept once, under "On
  another machine", for a machine whose global rules file does not map
  "let's start"; 149 lines down to 94, the words identical apart from
  the three changed sentences; 91 tests green.

The git line: `doc: readme rewritten for a public skill, folder named after the project`.

### Task 25: The final check

What it does and why: the suite, the sample render, the migration on a
copy of this folder's decisions, and the scenario for the user. Plan,
Task 25.

**The steps:**

- [x] **Step 1: The checks** The suite, the sample render, the
  migration on a copy. Done 10/10/2026: 91 tests green; a sample render
  writes 20 files and reads `clean`, 4791 words read at each start; the
  migration of a copy of this folder's decisions puts D15 on top; this
  folder reads `clean` with its own tool and 15 findings with the new
  one (the old decision titles, for the review); no bytecode in
  `skill/`.
- [x] **Step 2: The scenario** Given to the user. Done 10/10/2026: five
  checks on a scratch repository, in the reply of the session.

The user's correction of the day on the text, "a folder that may have
no copy elsewhere" for "an uncommitted folder", added to rule 4 of
`memory/user-writing-style.md` on the user's word, then to the
template `skill/templates/memory/user-writing-style.md`: the two
copies identical, the suite green.

**Checkpoint for the phase:** Tasks 18 to 25 delivered and tried by the user, the suite green, then the review of this folder on the user's word.
