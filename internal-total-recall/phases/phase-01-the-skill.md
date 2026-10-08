# Phase 01: The skill

Opened 07/10/2026, the user's word, at the start of the project. The
phase builds the skill from the analysis of a reference memory system,
verifies it, and applies it to this project. The whole phase ran in one
session, with the superpowers skills as the process: brainstorming for
the design, a written spec, a written plan, test first for the tools,
and a fresh reviewer at the end.

**The rules:**

- The reference memory system is the user's production folder, read
  only. Nothing is written, moved or deleted there. Its name and its
  path are not written anywhere in this repository or in this folder:
  the user gives the path when a session needs it.
- Nothing in the repository or in this folder names the reference
  project or this machine.
- Every text follows `rules.md`. The tests check the dash characters and
  the blank lines over the whole package.
- The rules of `lifecycle.md`, "The numbers", hold.

**The order:**

1. Task 1, the analysis of the reference memory system.
2. Task 2, the design and the spec.
3. Task 3, the plan.
4. Task 4, the document check tool.
5. Task 5, the machine check tool.
6. Task 6, the package test and the render script.
7. Task 7, the rules file.
8. Task 8, the routines and the living documents.
9. Task 9, the machine folder.
10. Task 10, the skill file and the README.
11. Task 11, the verification of the package.
12. Task 12, the review.
13. Task 13, the install on this project.
14. Task 14, the close.

### The opening of the phase

- [x] **Step 1: The repository** `git init` by the user, before the
  session. Done 07/10/2026: `.git` present, no commit yet.

### Task 1: The analysis of the reference memory system

What it does and why: the user has a working memory system in another
project, with a start routine, a close routine, a plan of phases and
tasks, a snapshot, a history, a story and memory notes. The skill is
made from it, keeping what works and changing what does not, so the
first task reads it whole and judges it.

**The steps:**

- [x] **Step 1: The read** The instruction file, the routines, the
  snapshot, the structure of the plan and of the history, the eight
  memory notes, the settings that wire them, the machine-wide guards.
  Done 07/10/2026: read with `cat` and `sed`, nothing written there. The
  memory of the reference is wired by a `.claude/settings.local.json`
  that a machine-wide git ignore file keeps out of git, a dependency the
  user did not want.
- [x] **Step 2: The assessment** What works and stays, what changes,
  with the evidence (the sizes of the files, the growth of the
  guardrails and the open questions). Done 07/10/2026: twelve changes
  listed and approved, recorded in `decisions.md`.
- [x] **Step 3: The documentation check** The Claude Code pages on
  skills, instruction files, memory, hooks and git exclusions, read by
  a research agent. Done 07/10/2026: the facts that shaped the design
  are in the spec, "The folder".

### Task 2: The design and the spec

What it does and why: the design is agreed section by section in the
chat (the folder, the sessions, the plan and the numbers, the skill),
then written as a spec that the plan argues from.

**The steps:**

- [x] **Step 1: The sections** The folder and its files, the start and
  the close, the plan and the numbers, the skill. Done 07/10/2026: each
  approved by the user with corrections: no file under `.claude/`, no
  dependency on a setting or on the skill for the loading, a `tools/`
  folder, three to five questions at the install.
- [x] **Step 2: The spec** Written, checked for dash characters and
  blank lines, approved. Done 07/10/2026: `records/2026-10-07-design.md`.

### Task 3: The plan

What it does and why: the spec becomes a plan of tasks with tests first,
so that the package is built the same way whoever builds it.

**The steps:**

- [x] **Step 1: The plan** Thirteen tasks, each with its tests, its
  code or its sections, and the git line for the user. Done
  07/10/2026: `records/2026-10-07-plan.md`, approved; the user chose
  the native execution, in the session, with the user's voice on every
  text.

### Task 4: The document check tool

What it does and why: the close needs a check that the documents are
consistent, so that drift is caught the day it happens. The tool reads
an internal folder and reports what breaks the rules.

**The steps:**

- [x] **Step 1: The text rules** The dash characters and the blank line
  before a list or a table, tests first. Done 07/10/2026: ten tests
  red, then green.
- [x] **Step 2: The structure rules** The table of documents, the task
  numbers, the ticked steps, the length of `state.md`, the history
  titles, the memory index, tests first. Done 07/10/2026: twenty six
  tests green. A trial on the reference folder, read only, gave 695
  findings, five read and true. A history title may carry a word after
  the date, the user's habit for a second session of a day.

The git line: `feat: document check with the text and structure rules`.

### Task 5: The machine check tool

What it does and why: the guardrails live in the settings of a machine,
not in the project. The tool reports which ones a machine has, so that
the skill can propose the missing ones.

**The steps:**

- [x] **Step 1: The tool** Tests first on a fake home, then the tool.
  Done 07/10/2026: ten tests green; the table on this machine reads
  present on every row, matching the managed settings.

The git line: `feat: machine check reports the guardrails of a machine`.

### Task 6: The package test and the render script

What it does and why: the writing rules must hold over every file of
the package, and the internal folder must be written from the templates
without ever overwriting a file.

**The steps:**

- [x] **Step 1: The package test** The dash characters, the blank
  lines, the origin name and the home path over every file; the
  structure of the skill. Done 07/10/2026: the three writing tests
  green on the first run, the structure tests red until the files
  existed.
- [x] **Step 2: The render script** Tests first, then the script. Done
  07/10/2026: seven tests green, one added after a stray cache file was
  copied into a sample: the render skips cache and hidden files, and
  the test loaders write no bytecode.

The git line: `feat: render script writes the internal folder from the templates`.

### Task 7: The rules file

What it does and why: the user's global rules and their writing style
must travel with the project, so that a session on any machine follows
them. The file consolidates the global file and the memory notes of the
reference, decoupled from it.

**The steps:**

- [x] **Step 1: The file** The seventeen rules of the user's style
  merged with the global writing rules into one list of eighteen, the
  replies rule, the other sections of the global file, and the rules
  taken from the notes. Done 07/10/2026: 358 lines, the writing tests
  green.

The git line: `feat: the portable rules`.

### Task 8: The routines and the living documents

What it does and why: the templates are what every project gets. The
routines (close, lifecycle) and the living documents (the project file,
the snapshot, the plan, the first phase, the history, the story, the
decisions, the code map, the records and tools READMEs, the memory).

**The steps:**

- [x] **Step 1: The routines** `close.md` and `lifecycle.md` from the
  spec. Done 07/10/2026: the writing tests green.
- [x] **Step 2: The documents** The twelve other templates with their
  placeholders. Done 07/10/2026: the sample render writes seventeen
  files, the check reads clean, no placeholder left.

The git line: `feat: the templates of the memory system`.

### Task 9: The machine folder

What it does and why: the guard scripts and the deny list of this
machine, made portable so that the skill can propose them elsewhere.

**The steps:**

- [x] **Step 1: The folder** The three scripts copied byte for byte,
  the settings snippet built from the managed settings (35 deny
  patterns and the two hooks). Done 07/10/2026: three tests green.

The git line: `feat: the guardrails as a settings snippet and the guard scripts`.

### Task 10: The skill file and the README

What it does and why: `SKILL.md` is what the session runs at
`/total-recall`; the README is what a reader opens first.

**The steps:**

- [x] **Step 1: SKILL.md** The nine steps, user invoked only. Done
  07/10/2026: 214 lines, the six commands parse.
- [x] **Step 2: The README** In the user's voice. Done 07/10/2026: the
  package test green.
- [x] **Step 3: The reread** The ", so " chains of both files split into
  two sentences, the tic rule. Done 07/10/2026: seven chains split,
  the suite green.

The git line: `feat: the total-recall skill and its readme`.

### Task 11: The verification of the package

What it does and why: the five checks of the spec, run on the finished
package, with their outputs shown.

**The steps:**

- [x] **Step 1: The checks** Done 07/10/2026: 53 tests green; the dry
  run writes seventeen files, clean, no placeholder; no dash character
  and no origin name in the package; the machine table present on every
  row; `SKILL.md` under 500 lines with its three fields.

### Task 12: The review

What it does and why: a fresh reviewer reads the package against the
spec, the plan and the rulings, the one fresh context of the build. The
user allowed the agent.

**The steps:**

- [x] **Step 1: The reviewer** Launched, read only, on the most capable
  model, with the spec, the plan, the ledger and the five review focus
  items. Done 07/10/2026: the report is awaited.
- [x] **Step 2: The findings** Critical and Important fixed with a test
  first, Minor to the Roadmap, the report saved under `records/`. Done
  07/10/2026: no Critical; four Important fixed in one pass, each with
  a failing test first (the repair mode of the render adds only the
  files that need no answer; the tools README quotes its commands; the
  check tool names a file that is not UTF-8 and reads the table of
  documents only); 57 tests green; thirteen Minor findings in
  `records/2026-10-07-review.md`, item 2 of the Roadmap.

### Task 13: The install on this project

What it does and why: the skill runs on this project first, so that the
next session opens on a briefing and nothing of this session is lost.

**The steps:**

- [x] **Step 1: The skill's steps** The ground, the description approved
  by the user, the render, the check. Done 07/10/2026: seventeen files
  written, clean.
- [x] **Step 2: The content** This phase written from the session, the
  records copied, the decisions, the history, the story, the code map,
  one memory note. Done 07/10/2026: the check reads clean after the
  slips of this file were corrected.
- [x] **Step 3: The exclusion** The line `/internal-total-recall/` in
  `.git/info/exclude`, run by the user, then `git status` clean of the
  folder. Done 07/10/2026: the line is there (twice, harmless), and
  `git check-ignore` reads the folder as ignored.
- [x] **Step 4: The machine** The table read. Done 07/10/2026: present
  on every row, matching the managed settings.

### Task 14: The close

What it does and why: the close routine of `close.md`, the last task of
the phase, which opens Phase 02.

**The steps:**

- [x] **Step 1: The routine** The snapshot, the check of this file, the
  Roadmap, the history, the story, the decisions, the memory, the check
  tool, then the close paragraph and Phase 02. Done 07/10/2026: each
  document brought to the end of the session, the check tool clean,
  Phase 02 opened.

**Checkpoint for the phase:** the next session, opened with "let's
start", gives the briefing from the files alone; `git status` shows
nothing of the folder; the skill installs on a scratch repository in one
run.

Closed 07/10/2026: the skill, its tests and its README built in one
session, reviewed by a fresh reviewer, and applied to this project.
Tasks 1 to 14, three commits by the user (`aca0d06`, then `3d49152`
and `45ed75f` with the fixes of the review). Open at the close: the
trial on a scratch repository, which is the first task of Phase 02.
