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
- The benchmark measures the same files the same way as the baseline:
  `wc -w`, `doc-check.py --size`, and `/context` after "let's start".
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
- [ ] **Step 2: The tokens** The user opens a fresh session with
  "let's start", runs `/context`, and the figure goes into the record
  with the word counts of the files that changed since `b315d2c`.

### Task 33: The start script

What it does and why: the start routine needs the goal and the head of
the Roadmap from `plan.md`, and the preamble and the current task from
the open phase file. Claude now reads the whole files and picks. A
script prints those parts alone, the way `doc-check.py` prints one line
in place of the documents it checks. The idea came from the tools that
filter the output of commands before it reaches the context.

**The steps:**

- [ ] **Step 1: The design** What the script prints, how it finds the
  open phase and the current task, what the start routine says, how it
  is measured. Discussed with the user.
- [ ] **Step 2: The tests** The tests of the script, seen red.
- [ ] **Step 3: The script** The script in the templates, the suite
  green.
- [ ] **Step 4: The routine** The start routine of the template
  `CLAUDE.md` runs the script, checked by the sample render.
- [ ] **Step 5: The install here** The script and the routine copied
  into this folder.

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
