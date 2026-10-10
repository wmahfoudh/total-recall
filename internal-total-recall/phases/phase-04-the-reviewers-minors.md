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

- [ ] **Step 1: The design** The findings read with the user's notes,
  one at a time, each kept, changed or dropped, then the steps written
  here in place of this one.

**Checkpoint for the phase:** written when the tasks are known.
