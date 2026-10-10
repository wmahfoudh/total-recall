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
- [ ] **Step 3: The code** `start.py` in the templates and the measure
  of `doc-check.py`, the suite green.
- [ ] **Step 4: The routine** The start routine and the size line of
  the template `CLAUDE.md`, the file lists of `SKILL.md` and the
  README; checked by the sample render.
- [ ] **Step 5: The install here** The script, the tool and the routine
  brought into this folder, and the measure run on it.
- [ ] **Step 6: The trial** The user opens a fresh session with
  "let's start": the briefing comes from the output of the script, and
  `CLAUDE.md` and `rules.md` are loaded once.

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

### Task 34: The compressed copy of the rules

What it does and why: `rules.md` and the style note are 3,742 words
read at each start in every project. A short copy for Claude to read,
written from the plain originals and checked by `doc-check.py`, the way
caveman-compress keeps an original and a compressed copy. The cost: two
copies to keep in step, and a style note that teaches plain English by
its own sentences.

### Task 35: The start levels

What it does and why: a light start that reads `state.md` and the
current task, and a full start that adds the rules, like the modes of
ponytail. The risk: a light session that misses the rules, the worry
behind the first item of Parked.

### Task 36: The short close entries

What it does and why: the history and the story are written by Claude
at each close, and output costs more than input. A line in `close.md`
for shorter entries. The tests of caveman found that a plain "be
concise" gives most of the gain.

### Task 37: The repeats of the templates

What it does and why: the templates write the description twice
(`CLAUDE.md` and the Goal of `plan.md`) and the constraints twice, and
the note `project-instruction-file` repeats `CLAUDE.md` and `rules.md`,
all read at each start. Item 6 of the Roadmap, moved here.

### Task 38: The phase file that grows

What it does and why: the file of Phase 02 reached 4,167 words with
seventeen tasks. The start reads only its preamble and current task,
but the close and the review read it whole, and their cost grows with
it.

### Task 39: The tests that pin the wording

What it does and why: many tests of `tests/test_package.py` check exact
sentences of `SKILL.md` and the templates. They keep the rules in the
text, and each change of wording becomes a change of a test too: Task
22 found two literals of its plan that did not match its own tests.

### Task 40: "let's start" for a new user

What it does and why: the phrase works on this machine because the
user's global rules file maps it to the project file. A new user has no
such file. A line handed over by the skill, tried on a machine without
the global file. Item 4 of the Roadmap, moved here.

### Task 41: A second real project

What it does and why: the only project that runs the skill is its own
repository, and most of the feedback of Phase 02 came from it. A
second, ordinary project tries the templates on work of another kind.

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
