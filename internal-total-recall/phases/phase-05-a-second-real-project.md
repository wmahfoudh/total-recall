# Phase 05: A second real project

Opened 11/10/2026 at the close of Phase 04, named from the head of the
Roadmap. The phase tries the templates on an ordinary project of
another kind, from the install to a few sessions, and brings back here
what those sessions show. The user can rename it.

**The rules:**

- The work in the other project follows that project's own internal
  folder. This file records what comes back: the faults, the findings,
  the changes they lead to here.
- A change to a tool or to the render script starts with a failing
  test. A change to a template is checked by the sample render and
  `tools/doc-check.py`.
- The installed copies of the tools in this folder follow the
  templates: a changed tool is copied here in the same task.
- The rules of `lifecycle.md`, "The numbers", hold.

**The order:**

1. Task 47, the second project.
2. Task 48, the templates after the review of 11/10/2026.
3. Task 49, the review of the README.
4. The close of the phase, as its last task, numbered when it is
   written.

### The opening of the phase

No step: the project has no opening routine.

### Task 47: The second project

What it does and why: the skill installed on a project of another kind,
chosen by the user, and used for a few sessions at the user's pace, to
see how the templates hold outside this repository.

**The steps:**

- [ ] **Step 1: The choice** The user chooses the project, then the
  steps are written here in place of this one.

### Task 48: The templates after the review of 11/10/2026

What it does and why: items 1 and 3 of the review of 11/10/2026
(`records/2026-10-11-review.md`), applied to this folder, are carried
into the templates of the skill: a Roadmap item leaves the Roadmap when
it opens as a phase or a task, in `lifecycle.md`, `plan.md` and step 4
of `close.md`; the start phrases line in the `machine-check.py` line of
`tools/README.md`. Step 6 of `review.md`, item 2, too.

**The steps:**

- [x] **Step 1: The templates** The changes made, checked by the sample
  render and `tools/doc-check.py`, the suite green. Done 11/10/2026:
  `lifecycle.md`, `plan.md`, `close.md`, `review.md` and
  `tools/README.md` of the templates changed. `lifecycle.md`,
  `close.md`, `review.md` and the tools README now match this folder,
  and `update.py plan` reads `nothing to update`. The sample render
  reads `clean`. 153 tests green.

**Suggested git line:**

```
git add skill/templates internal-total-recall
git commit -m "doc: templates updated with the changes of the memory review"
```

### Task 49: The review of the README

What it does and why: the user asked for a full review of `README.md`
for errors and incoherences, in the user's voice and rules, so that it
describes the project well.

**The steps:**

- [x] **Step 1: The review** The README read against `SKILL.md`, the
  tools, the guard scripts and the decisions. Done 11/10/2026: fifteen
  items, all approved by the user: the template name
  `CLAUDE.template.md`, the commands, the rows of the machine check,
  what the guardrails refuse, the size of the folder in words in place
  of a token count never measured, the root of the repository at the
  install, the first person of line 34, the link command, the close
  list, a paragraph split, a typo.
- [x] **Step 2: The changes** Done 11/10/2026: applied, no dash, no
  list break, 153 tests green. The paragraph of "The review of the
  memory" holds 112 words, over the rule of about 100, not in the
  approved items.

**Suggested git line:**

```
git add README.md internal-total-recall
git commit -m "doc: readme fixed after a full review"
```

**Checkpoint for the phase:** written when the tasks are known.
