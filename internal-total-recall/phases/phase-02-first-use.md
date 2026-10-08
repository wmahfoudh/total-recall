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
4. The tasks the feedback gives, numbered when they are written.
5. The close of the phase, as its last task.

### The opening of the phase

No step: the project has no opening routine.

### Task 15: The feedback of the first trial

What it does and why: the user tries the skill on a scratch repository
with the scenario of `SKILL.md`, and on a real project, and notes what
goes wrong, what is missing and what could be better. The session reads
the notes one at a time, discusses each, and turns the agreed ones into
tasks of this phase.

**The steps:**

- [ ] **Step 1: The notes** The user's notes, read one item at a time,
  with the session's view on each: a fault to reproduce, a change to
  design, or a note for the Roadmap. The first two came on 07/10/2026,
  from the user's read of this folder right after the close: the
  reference project named in the folder (Task 16, done), and the
  user's style not found under `memory/` (Task 17, done on the user's
  word). The notes of the trials on other repositories are still to
  come.
- [ ] **Step 2: The tasks** Each agreed item written as a task of this
  phase, in the task form, numbered from 18.

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

**Checkpoint for the phase:** written when the tasks are known.
