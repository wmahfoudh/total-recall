# Phase 04: The reviewer's minors

Opened 11/10/2026 on the user's word, at the close of Phase 03, with
item 2 of the Roadmap taken before the head (D32). The phase fixes the
Minor findings of the fresh review of 07/10/2026 and the small faults
of the check found since, in this repository.

**The rules:**

- A change to a tool or to the render script starts with a failing
  test. A change to a template is checked by the sample render and
  `tools/doc-check.py`.
- The installed copies of the tools in this folder follow the
  templates: a changed tool is copied here in the same task.
- The user's own notes on the findings are discussed before any change.
- The rules of `lifecycle.md`, "The numbers", hold.

**The order:**

1. Task 45, the reviewer's minors.
2. The close of the phase, as its last task, numbered when it is
   written.

### The opening of the phase

No step: the project has no opening routine.

### Task 45: The reviewer's minors

What it does and why: the thirteen Minor findings of the fresh review
of 07/10/2026, in `records/2026-10-07-review.md`: the machine check on
a regex matcher, a quoted command and JSON of the wrong shape; an
answer that is not a string in the render; a BOM and a table after a
list item in the document check; the `.git` test in a worktree; the
snapshot and history templates at render time; "two hook scripts" in
the README; the description of the skill; the file list of step 5; the
skill-creator checks named in the spec; a capital in the history
qualifier. With them, two faults of the check found later:

- found 10/10/2026: the check reports a list item that follows a
  paragraph inside the item before it;
- found 11/10/2026, in Task 37: the check does not report a step with
  a "Done" line and a box not ticked, which `start.py` takes for the
  current task.

**The steps:**

- [x] **Step 1: The design** The fifteen findings listed with the
  user. Done 11/10/2026: the user asked for all of them fixed at once,
  by common sense, with no reading one at a time (D33).
- [x] **Step 2: The failing tests** Ten tests for findings 1 to 5, 13,
  14 and 15. Done 11/10/2026: nine failed as expected, the tenth (a
  hook on another tool) already passed.
- [x] **Step 3: The machine check** Findings 1 and 2. Done 11/10/2026:
  the matcher is read as a regular expression, `*` and an empty
  matcher as all tools; the command is split as a shell would, with a
  leading `bash`, `sh` or `zsh` skipped; each value is checked for its
  JSON type, so a file of the wrong shape reads as missing.
- [x] **Step 4: The render** Finding 3. Done 11/10/2026: answers that
  are not a JSON object, or an answer that is not a string, stop the
  run with exit 2 and a message, before anything is written.
- [x] **Step 5: The document check** Findings 4, 5, 13, 14 and 15.
  Done 11/10/2026: files are read with `utf-8-sig`; a table after a
  list item is reported; a capital is accepted in the history
  qualifier; an indented paragraph after a blank line belongs to the
  list item; an open step with a "Done" mark is reported. The tools
  README of the template and of this folder name the new check.
- [x] **Step 6: The templates and the skill** Findings 6, 7 and 11.
  Done 11/10/2026: step 1 asks git for the root of the repository, so
  a worktree, a submodule and a subfolder are told apart from a folder
  with no repository; steps 2 and 7 ask git for the path of the
  exclusion file; step 5 names the phase file; the state template
  gives Task 1 at step 1, the design.
- [x] **Step 7: The findings with no change** Findings 8, 9, 10 and 12.
  Done 11/10/2026: 8, 9 and 10 were fixed before this phase (the
  history template has no exclusion line, the README says "two hook
  scripts, with a library they share", the description names
  `/total-recall`). 12 is dropped: the spec is a record kept as
  received, and the package test covers the frontmatter of the skill.
- [x] **Step 8: The checks** Done 11/10/2026: 153 tests green, the
  sample render reads `clean` with the new state line, this folder
  reads `clean` at 5,637 words, the tools of this folder match the
  templates, `machine-check.py` reports this machine in full, no dash
  in the changed files.
- [ ] **Step 9: The user's trial** The user reads the changes and runs
  the suite.

**Suggested git line:**

```
git add skill/SKILL.md skill/scripts/render.py skill/templates/state.md skill/templates/tools tests internal-total-recall
git commit -m "fix: the reviewer's minors in the checks, the render and the install steps"
```

**Checkpoint for the phase:** written when the tasks are known.
