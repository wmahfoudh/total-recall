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
- The skill has two forms, `skill-claude/` for Claude Code and
  `skill-pi/` for Pi. A change to one form is made in the other in the
  same task, and the tests run over both forms (D35).

**The order:**

1. Task 47, the second project.
2. Task 48, the templates after the review of 11/10/2026.
3. Task 49, the review of the README.
4. Task 50, the Pi form of the skill.
5. Task 51, the records and the phases numbered.
6. Task 52, the writing style note merged.
7. Task 53, the README rewritten.
8. The close of the phase, as its last task, numbered when it is
   written.

### The opening of the phase

No step: the project has no opening routine.

### Task 47: The second project

What it does and why: the skill installed on a project of another kind,
chosen by the user, and used for a few sessions at the user's pace, to
see how the templates hold outside this repository.

**The steps:**

- [x] **Step 1: The choice** The user chooses the project, then the
  steps are written here in place of this one. Done 22/10/2026: the
  skill in use on a project of the user's, at their pace, outside the
  sessions of this repository. What came back: the records named by
  the date are inefficient (D36, then D37), and the newer style note
  (Task 52). The user's word: the task is done, that feedback is the
  proof.

### Task 48: The templates after the review of 11/10/2026

What it does and why: items 1 and 3 of the review of 11/10/2026
(`records/R010-review.md`), applied to this folder, are carried
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
  list break, 153 tests green, committed as `cdf9d41`. The paragraph of
  "The review of the memory", 112 words, split by the user in
  `2f1e8a6`.

**Suggested git line:**

```
git add README.md internal-total-recall
git commit -m "doc: readme fixed after a full review"
```

### Task 50: The Pi form of the skill

What it does and why: the user wrote a Pi form of the skill on
16/10/2026, `skill-pi/` (26 files, `df99639`), outside a session, and
the memory has no record of it. The task records it, sets the rule that
the two forms change together (D35), renames `skill/` to
`skill-claude/` so that the two forms are named alike, and brings the
Pi form into the tests, so that a change to the Pi form starts with a
failing test like a change to the Claude Code form.

**The steps:**

- [x] **Step 1: The record** D35 written, this task written, the Pi
  form read file by file against the Claude Code form. Done
  22/10/2026: the Pi form differs in the project file (`AGENTS.md`),
  the command (`/skill:total-recall`), the global rules file
  (`~/.pi/agent/AGENTS.md`, or `AGENTS.override.md` or `CLAUDE.md`
  there), the machine check (three rows: no deny list, no hooks, no
  `jq`), the guardrails (the memory note `guardrails.md` in place of
  the settings and the hook scripts, no `machine/` folder), the answers
  file (the system temporary folder), and the Pi README. The style note
  of the Pi form has no frontmatter. The rest is the same text with
  `AGENTS.md` for `CLAUDE.md`.
- [x] **Step 2: The rename** `skill/` moved to `skill-claude/` by the
  user, with git, the link in `~/.claude/skills/` replaced by the
  user, then the references updated: the tests, `README.md`, the Pi
  README and this folder. Done 22/10/2026: the tests name the forms
  in `tests/forms.py`; `README.md` names `skill-claude/` in the
  install, the templates and the machine folder, with a line on the
  Pi form; the Pi README points to `../skill-claude`; `plan.md` and
  `code-map.md` of this folder updated. The project file of this
  folder and the note `reference-system-read-only` still say
  `skill/`: held for the close, as a proposal.
- [x] **Step 3: The Pi form in the tests** The tests run over both
  forms: the text rules (no dash, the blank lines, the reference name
  by hash, no home path) over `skill-pi/` too, the structure of the Pi
  skill file and its templates, the render, the update, the start
  script and the document check of the Pi form, and the Pi machine
  check with its own rows. The Pi facts the tests encode come from the
  Pi documentation, read online. Done 22/10/2026: `tests/forms.py`
  holds the two forms, and a test class written for both is made into
  a TestCase per form (`RenderClaude`, `RenderPi`). The document
  check, the render, the update and the start tests run over both
  forms. The Pi machine check has its own class: the five names of the
  rules file Pi reads, in order, and the agent directory from the
  flag, the environment, then the home. The package test has a Pi
  class: no machine folder, the guardrails note in the index and in
  the skill file, `<skill>` in the commands, the Pi README. 294 tests
  green, 153 before. One finding: the Pi skill file wraps a sentence
  of the check mode over two lines; the test now reads the step
  without its line breaks.

**Suggested git line:**

```
git add skill-claude skill-pi tests README.md internal-total-recall
git commit -m "chore: the pi form of the skill in the tests, the claude form renamed"
```

### Task 51: The records and the phases numbered

What it does and why: a record is named by a running number of three
digits in place of the date, which the user found inefficient
(22/10/2026, D36). After the first round the user asked for a letter
before the number, `R` for a record and `P` for a phase file, so that
the two kinds are told apart at a glance (D37): `records/RNNN-<name>.md`
and `phases/PNN-<name>.md`. The date of a record stays in the records
README and in the record. The change goes in both forms of the skill,
in the tests and in this folder, whose records are renamed in the
order of their creation, read from the git history.

**The steps:**

- [x] **Step 1: This folder** The records of this folder renamed, the
  README of the records and the paths in this folder updated. Done
  22/10/2026: eleven records, `R000-design.md` to `R010-review.md`,
  in the order of the git history, and of the README for the four of
  07/10/2026, committed together. The paths updated in the README of
  the records, the history, the decisions, the state and the phase
  files. The records themselves left as received.
- [x] **Step 2: The skill** The templates, the scripts, the skill
  files and the tests of both forms changed, test first: a record is
  `RNNN-<name>.md`, a phase file `PNN-<name>.md`. The tools read the
  old name of a phase file too, and the plan of the update lists the
  files of an older folder to rename. Done 22/10/2026: sixteen tests
  changed or added first, 36 failures and 6 errors, then 310 green. In
  both forms, `start.py`, `doc-check.py` and `render.py` read `PNN-`
  and the older `phase-NN-`; `update.py` plans and applies the rename
  of the older phase files (`rename old new`) and lists the records
  named by a date (`by hand: ...`), since their number needs the order
  of their creation; the template of the first phase file is
  `P01-{{phase1_slug}}.md`; `state.md`, `lifecycle.md`, `plan.md`,
  `review.md` (`records/RNNN-review.md`, with the next number), the
  records README (the naming rule) and the skill files changed.
- [x] **Step 3: This folder again** The records renamed `R000-` to
  `R010-`, the phase files `P01-` to `P05-`, the paths updated, the
  routine files and the tools of this folder copied from the
  templates. Done 22/10/2026: `R000-design.md` to `R010-review.md`,
  `P01-the-skill.md` to `P05-a-second-real-project.md`, the paths
  updated in nine files, the naming rule in the records README,
  `plan.md` reworded, `lifecycle.md`, `review.md` and the two tools
  copied. `update.py plan` reads `nothing to update`, the check reads
  `clean`, the start script names `P05`. A quote of the old template
  name in a finding of Phase 02 stays, as a record of the past.

Found on the way: six records name another record by its old date
name. Left as received, the user's word, 22/10/2026.

**Suggested git line**, with Task 50 in one commit:

```
git add -A skill-claude skill-pi tests README.md internal-total-recall
git commit -m "feat: the pi form in the tests, records and phase files named by a letter and a number"
```

### Task 52: The writing style note merged

What it does and why: the user keeps a newer version of the note
`user-writing-style` in the reference project, with a rule of
19/10/2026 and eleven rules of 21/10/2026 more than the note here, each
with a wrong and a right example. The newer note is merged into the
note of this folder and into the templates of both forms, without the
name of the reference project or its product.

**The steps:**

- [x] **Step 1: The merge proposed** The note is read at each start, so
  the merged text is proposed with its size before it is written. Done
  22/10/2026: a first draft put the eleven newer rules after the
  eighteen here, 29 rules and 2,070 words. The user refused it as a
  mathematical merge: each rule is to be read for what it is about,
  and the rules about the same thing merged, with a generic example
  where one is needed. The second draft has 14 rules, from the word to
  the sentence, then who acts, the tone, and the kinds of text, with
  the user's own examples where a rule needs one, 1,622 words. The user
  rewrote the Why line in the draft and approved it.
- [x] **Step 2: The three copies** The note of this folder and the two
  templates written, the tests updated (the count of the rules). Done
  22/10/2026: the note of this folder, the Claude Code template and
  the Pi template (a heading in place of the frontmatter,
  `/skill:total-recall` in rule 8), the three index lines, the test at
  14 rules. 310 tests green.

**Suggested git line:**

```
git add skill-claude/templates/memory skill-pi/templates/memory tests/test_package.py internal-total-recall
git commit -m "doc: the writing style note merged with the newer rules, fourteen rules"
```

### Task 53: The README rewritten

What it does and why: the user asked for the whole `README.md`
rewritten by the writing style rules merged in Task 52, so that the
public page reads in their plain style, each sentence read as a user
who never opened the repository. The review of the whole skill, the
first ask of the day, goes to the Roadmap in its place.

**The steps:**

- [ ] **Step 1: The rewrite** The README rewritten section by section
  by the merged note, the facts unchanged, and proposed to the user.
- [ ] **Step 2: The checks** The tests green (several hold a sentence
  of the README), the document check, no dash.

**Checkpoint for the phase:** written when the tasks are known.
