# Phase 03: Optimization

Opened 10/10/2026 on the user's word, at the close of Phase 02, with the
name given by the user. The phase lowers the cost of a session start
and of the routines, measured against the baseline
`records/2026-10-10-baseline.md` at its end. It also takes the points
the session raised on 10/10/2026 when it explored the repository: the
phase file that grows, the tests that pin the wording, a single real
user, the global rules file, the guard hooks.

**The rules:**

- A change to a script or a tool starts with a failing test. A change
  to a template is checked by the sample render and
  `tools/doc-check.py`.
- The benchmark measures the same files the same way as the baseline,
  in words: `wc -w` and `doc-check.py --size`.
- Tasks 34 to 42 are discussed with the user when they open, before
  any change: each one may end as a change, a Roadmap item or nothing.
- The installed copies of the tools in this folder follow the
  templates: a changed tool is copied here in the same task.
- The rules of `lifecycle.md`, "The numbers", hold.

**The order:**

1. Task 32, the baseline.
2. Task 33, the start script.
3. Tasks 34 to 36, the other ideas on the cost: the compressed copy of
   the rules, the start levels, the short close entries.
4. Task 37, the repeats of the templates.
5. Tasks 38 to 42, the points of the exploration: the phase file that
   grows, the tests that pin the wording, "let's start" for a new user,
   a second real project, the guard hooks.
6. Task 43, the benchmark.
7. Task 44, the close of the phase.

### The opening of the phase

No step: the project has no opening routine.

### Task 32: The baseline

What it does and why: the cost of a start measured before any change,
so that the benchmark at the end of the phase has a figure to compare
with. The user's word, 10/10/2026.

**The steps:**

- [x] **Step 1: The words** The words read at each start, in the
  template and in this project, and the parts of the start read beyond
  them. Done 10/10/2026: `records/2026-10-10-baseline.md`, 6,207 words
  in this project, 4,854 in the template, about 8,300 with the global
  rules file of this machine.

The tokens are not measured, the user's word on 10/10/2026: the
phase limits its measure to words.

### Task 33: The start script

What it does and why: the start routine needs the goal and the head of
the Roadmap from `plan.md`, and the preamble and the current task from
the open phase file. Claude now reads the whole files and picks. A
script prints those parts alone, the way `doc-check.py` prints one line
in place of the documents it checks. The idea came from the tools that
filter the output of commands before it reaches the context.

**The steps:**

- [x] **Step 1: The design** What the script prints, how it finds the
  open phase and the current task, what the start routine says, how it
  is measured. Discussed with the user. Done 11/10/2026: the design
  below, the user's three answers (the whole start in one command,
  rely on Claude Code for the rules, the first Roadmap item in full),
  D22.
- [x] **Step 2: The tests** The tests of `start.py` and of the new
  measure of `doc-check.py --size`, seen red. Done 11/10/2026: 21 new
  tests, 18 red. `tests/test_start.py` (14, each an error on the missing
  script); `StartSize` in `tests/test_doc_check.py` (5, one red: the
  whole plan counted); the expected files and the start routine in
  `tests/test_package.py`; `ROUTINE_FILES` in `tests/test_update.py`.
  The four others of `StartSize` pass before the code: the rules, the
  state, the old count without the script and no bytecode hold today
  too. The suite: 134 tests, 4 failures, 14 errors.
- [x] **Step 3: The code** `start.py` in the templates and the measure
  of `doc-check.py`, the suite green. Done 11/10/2026: 133 of 134 tests
  green, the one red is the start routine of Step 4.
  `skill/templates/tools/start.py`, new; `start_script`, `words_of` and
  `start_size` in `doc-check.py`, which loads the script beside it with
  no bytecode; `tools/start.py` in `ROUTINE_FILES` of `update.py`. Run
  on this folder: exit 0, 3,189 words, the plan in 294 words (the file
  653), the phase in 1,012 (the file 1,697, Task 33 alone is long). The
  new measure reads 6,706 words where the old one read 6,046: the old
  one left the phase file out. The start as read before was 6,046 and
  the whole phase file, 7,743 words, and the rules read twice on top.
- [x] **Step 4: The routine** The start routine and the size line of
  the template `CLAUDE.md`, the file lists of `SKILL.md` and the
  README; checked by the sample render. Done 11/10/2026: 134 tests
  green. The routine runs the script, does not read `CLAUDE.md` and
  `rules.md` again, and reads the files when the script fails. The
  line of `start.py` in `templates/tools/README.md`, the `tools/` rows
  of `SKILL.md` and the README, the paragraph of the README on a
  session. Found by the sample render: the template note
  `project-instruction-file` and its index line said to read both
  files whole at the start, the double read again; both now say that
  Claude Code loads them. A sample render: the script exits 0, the
  check reads `clean`, 4,990 words read at each start.
- [x] **Step 5: The install here** The script, the tool and the routine
  brought into this folder, and the measure run on it. Done 11/10/2026:
  `tools/start.py` added and `tools/doc-check.py` replaced, copied from
  the templates (the plan of `update.py` named these two; its backup
  was refused the day before, and the folder is in git). By hand, the
  project's own files: the routine and the size line of `CLAUDE.md`,
  the line of `tools/README.md`, the note `project-instruction-file`
  and its index line, the same as the templates. The update plan now
  reads `nothing to update`, the check `clean`. The measure, on the
  files of today: 7,022 words read at each start with the script (the
  phase part 1,256, Task 33 being long). The old routine on the same
  files: 8,059 words, and 11,621 with the rules read twice. The
  shell's `cp` asks before an overwrite: a copy is made by Python.
- [x] **Step 6: The trial** The user opens a fresh session with
  "let's start": the briefing comes from the output of the script, and
  `CLAUDE.md` and `rules.md` are loaded once. Done 11/10/2026: passed on
  the user's word: `CLAUDE.md` read once with the Read tool, `rules.md`
  loaded once by its import, the script exit 0. Whether the script
  alone makes Claude Code load `CLAUDE.md` stays unknown, since the
  file was loaded before it ran. The entry point went to Task 40.

**The design**, agreed 11/10/2026:

- `tools/start.py`, standard library only, run as
  `python3 <folder>/tools/start.py <folder>`. Shipped in the templates
  like `doc-check.py`, added to an older folder by the update.
- It prints the whole start, each part headed with its file:
  `state.md` whole; the memory index and each note whole; from
  `plan.md` the goal, the first Roadmap item in full, the titles of
  the other items and the titles under Blocked; from the open phase
  file the preamble and the current task.
- It leaves out `CLAUDE.md` and `rules.md`: Claude Code loads them when
  the session reads a file in the folder, and the start routine no
  longer reads them.
- The open phase is the phase file with the highest number. When
  `state.md` names another file, the script prints a warning line.
- The current task is the first task with a step not ticked. When no
  task has one, it is the task after the last ticked one.
- When the script fails, the start routine reads the files as before.
- `doc-check.py --size` counts `CLAUDE.md`, `rules.md` and the output
  of the script, in place of `state.md`, `plan.md` and the notes.
- Not known yet: whether running the script counts as a read of a file
  in the folder, which makes Claude Code load `CLAUDE.md`. Reading
  `state.md` with `cat` counts. If the script does not, the routine
  opens with a read of `state.md`, then runs the script.

The estimate on this folder, 11/10/2026, in words:

| Part | Today | With the script |
|---|---|---|
| `CLAUDE.md` and `rules.md` | 3,517, read twice | 3,517, once |
| `state.md` and the notes | 1,948 | 1,948 |
| `plan.md` | 742 | about 130 |
| The phase file | 1,159 (Phase 02: 4,167) | 466 |

What was found on the way: the start reads `CLAUDE.md` and `rules.md`
twice. Claude Code's documentation of memory: a `CLAUDE.md` in a
subfolder loads "once Claude reads, writes, or edits another file in
that subdirectory", with its imports, and step 1 of the start routine
reads both files too. Seen in the session of 10/10/2026: `CLAUDE.md`
read with `cat`, then both files added again by Claude Code at the read
of `close.md`. About 3,500 words a start, not counted in the baseline.

The same load happens in this repository for the templates: the write
of `skill/templates/tools/start.py` on 11/10/2026 made Claude Code load
`skill/templates/CLAUDE.md` and `skill/templates/rules.md` as
instructions, about 3,300 words, each time a session works in
`skill/templates/`. A candidate for Task 37.

### Task 34: The compressed copy of the rules

What it does and why: `rules.md` and the style note are 3,742 words
read at each start in every project. A short copy for Claude to read,
written from the plain originals and checked by `doc-check.py`, the way
caveman-compress keeps an original and a compressed copy. The cost: two
copies to keep in step, and a style note that teaches plain English by
its own sentences.

Discussed with the user 11/10/2026, D23: no compressed copy. A copy in
shorthand shows Claude the style the rules forbid, the pairs of
examples do not compress, and two copies drift apart. The task removes
the repeats between `rules.md` and the style note instead, each rule
written once in plain English. The kept copy is by default the one in
the style note.

**The steps:**

- [x] **Step 1: The comparison** Each rule found in both `rules.md` and
  the style note, with the copy to keep. Approved by the user before
  any edit. Done 11/10/2026: six repeats, approved as listed. The use
  of the note, the ", and" clause, "Headings are plain nouns" (which
  disagreed with rule 13) and the product text kept in the note, the
  example of a notice moved into rule 11. The jargon sentence and the
  comments and git messages kept in `rules.md`. The prose tics and the
  opening paragraph of `rules.md` left as they are.
- [x] **Step 2: The edit** The repeats removed from the template
  `rules.md` and the style note and from the copies in this folder,
  checked by the sample render, `doc-check.py` and the suite. Done
  11/10/2026: both templates edited, copied here by Python. The suite
  caught the pointer to the note without its path; the path is back.
  134 tests green, the check `clean` here and on a sample render.
- [x] **Step 3: The measure** `doc-check.py --size` before and after,
  written here. Done 11/10/2026: 6,305 words read at each start before,
  6,128 after, 177 words fewer. `rules.md` and the note went from 3,742
  words to 3,565. The sample render reads 4,812.

### Task 35: The start levels

What it does and why: a light start that reads `state.md` and the
current task, and a full start that adds the rules, like the modes of
ponytail. The risk: a light session that misses the rules, the worry
behind the first item of Parked.

**The steps:**

- [x] **Step 1: The discussion** Whether the task ends as a change, a
  Roadmap item or nothing. Done 11/10/2026: nothing, on the user's
  word, D24. The start read 6,128 words: `CLAUDE.md` and `rules.md`
  3,403, the style note 1,139, the rest 1,586.

### Task 36: The short close entries

What it does and why: the history and the story are written by Claude
at each close, and output costs more than input. A line in `close.md`
for shorter entries. The tests of caveman found that a plain "be
concise" gives most of the gain.

**The steps:**

- [x] **Step 1: The discussion** Whether the task ends as a change, a
  Roadmap item or nothing. Done 11/10/2026: nothing, on the user's
  word, D25. The history entries, newest first: 156, 142, 232, 269 and
  522 words; the story entries: 142, 159, 172 and 365.

### Task 37: The repeats of the templates

What it does and why: the templates write the description twice
(`CLAUDE.md` and the Goal of `plan.md`) and the constraints twice, and
the note `project-instruction-file` repeats `CLAUDE.md` and `rules.md`,
all read at each start. Item 6 of the Roadmap, moved here.

Discussed with the user 11/10/2026, D26: four changes. The Goal and the
Constraints of `plan.md` point to `CLAUDE.md`. The note
`project-instruction-file` is deleted, since a session reads it only
after `CLAUDE.md` is loaded. The template `CLAUDE.md` is renamed
`CLAUDE.template.md`, and `render.py` writes it as `CLAUDE.md`: a
`CLAUDE.md` in `skill/templates/` makes Claude Code load it with the
template rules, about 3,200 words, in each session here that touches
the templates.

**The steps:**

- [x] **Step 1: The tests** The rename in the render tests and the
  package test, the note gone from the expected files and the index,
  no `{{description}}` or `{{constraints}}` in the template plan. Seen
  red. Done 11/10/2026: five new tests and the template paths of
  `test_package.py` changed; 139 tests, 6 failures and 6 errors, each
  on the old name or the old file.
- [x] **Step 2: The code and the templates** The rename in `render.py`,
  the template `CLAUDE.template.md`, the pointers of the template
  plan, the index line of the note removed. The old files removed by
  the user. The suite green, the sample render clean. Done 11/10/2026:
  `destination_of` and `TEMPLATE_NAMES` in `render.py`; the three old
  files removed by the user. 139 tests green; the sample render has a
  `CLAUDE.md`, no `CLAUDE.template.md`, no placeholder, the check
  `clean`.
- [x] **Step 3: The install here** The pointers of `plan.md` and the
  index line of the note in this folder, the note removed by the user.
  Done 11/10/2026: the old Constraints matched "Engineering" of
  `CLAUDE.md` line for line before they were replaced. The check
  `clean`.
- [x] **Step 4: The measure** `doc-check.py --size` before and after,
  here and on the sample render. Done 11/10/2026: here 6,158 words
  before, 5,887 after; the sample render 4,812 before, 4,613 after.
  The load of the template `CLAUDE.md` in this repository is not
  measured: the next session that edits a template shows it.

### Task 38: The phase file that grows

What it does and why: the file of Phase 02 reached 4,167 words with
seventeen tasks. The start reads only its preamble and current task,
but the close and the review read it whole, and their cost grows with
it.

Discussed with the user 11/10/2026, D27: the review keeps reading the
whole file, since it is rare and looks across the folder. The close
reads only the tasks of the session, and a done step says what
happened in a line or two, as `CLAUDE.md` already asks.

**The steps:**

- [x] **Step 1: The close and the form** Step 3 of `close.md` and the
  form of a phase file in `lifecycle.md`, in the templates and here.
  Done 11/10/2026: both edited and copied, the check `clean`.

### Task 39: The tests that pin the wording

What it does and why: many tests of `tests/test_package.py` check exact
sentences of `SKILL.md` and the templates. They keep the rules in the
text, and each change of wording becomes a change of a test too: Task
22 found two literals of its plan that did not match its own tests.

Discussed with the user 11/10/2026, D28: of the 51 checks of text, about
a dozen pin a sentence of a rule, and they stay. The others check
names, text that a tool reads, or old wording kept out.

**The steps:**

- [x] **Step 1: The comment** The reason of the wording checks at the
  top of `tests/test_package.py`. Done 11/10/2026: three lines, suite green.

### Task 40: "let's start" for a new user

What it does and why: the phrase works on this machine because the
user's global rules file maps it to the project file. A new user has no
such file. A line handed over by the skill, tried on a machine without
the global file. Item 4 of the Roadmap, moved here.

Seen at the trial of Task 33, 11/10/2026: even on this machine, a plain
"let's start" had nothing at the root of the repository or in Claude
Code's memory folder that named `internal-total-recall/`. The session
found the folder by listing the tree. "read
internal-total-recall/CLAUDE.md" is the sure way in, by `rules.md`.

The global rules file of this machine, 2,052 words, repeats most of
`rules.md`, and both load at each start in this project. Whether it
shrinks to the start phrases and a pointer is decided here, with the
entry point (D23).

Found 11/10/2026: the global file says the phrases run "the routine the
project's instruction file defines" and names no folder.

Discussed with the user 11/10/2026, D29: a line in the global file
names `internal-<project-name>/CLAUDE.md`, the machine check reports
it, and the install proposes it. The global file stays whole.

**The steps:**

- [x] **Step 1: The tests** The row of the machine check, the line in
  step 8 of `SKILL.md`, the README. Done 11/10/2026: 4 new tests, 5 red.
- [x] **Step 2: The code** `START_LINE` and the row in
  `machine-check.py`, step 8 and 9 of `SKILL.md`, the README, the copy
  here. Done 11/10/2026: 143 tests green; here the row reads `missing`.
- [x] **Step 3: The line on this machine** The user adds the line to
  the global file; the machine check reads `present`. Done 11/10/2026:
  the row reads `present`. The trial of a plain "let's start" is next.

### Task 41: A second real project

What it does and why: the only project that runs the skill is its own
repository, and most of the feedback of Phase 02 came from it. A
second, ordinary project tries the templates on work of another kind.

**The steps:**

- [x] **Step 1: The discussion** Whether the task ends as a change, a
  Roadmap item or nothing. Done 11/10/2026: item 1 of the Roadmap, on
  the user's word, D30. The project is still to be chosen.

### Task 42: The guard hooks

What it does and why: the three guard scripts are 543 lines of bash for
the whole machine, and the rest of the skill is for a project. Whether
they stay in the skill, become an option, or move to a repository of
their own.

### Task 43: The benchmark

What it does and why: the cost of a start measured again by the method
of the baseline, and compared with it in a record.

### Task 44: The close

What it does and why: the close routine of `close.md`, the last task of
the phase.

**Checkpoint for the phase:** the benchmark recorded and compared with
the baseline, each task delivered or moved to the Roadmap on the user's
word, the suite green.
