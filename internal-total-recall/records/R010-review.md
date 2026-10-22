# Review of the memory, 11/10/2026

The review run at the close of Phase 04, on the user's word.

**Size before:** 5,450 words read at each start, limit 8,000. The check
reads `clean`.

**The rule of the memory note `reference-system-read-only`:** checked
by the hash of the package test over the 73 tracked files and the files
of this folder, paths only printed. No hit in the files, their paths or
the commit messages. The two records that hold `/home/` hold it as a
test pattern, not as a path of this machine.

## From this session

**A.** `state.md`, "Position" and "Waiting on the user".

- Current: "committed up to `e01301f`, the close not yet", and "The
  commit of this close."
- Proposed: "committed up to the close of Phase 04", and the line
  removed from "Waiting on the user".
- Reason: the user committed the close after it was written.

**B.** Two empty folders, `.claude/.cc-writes/` at the root of this
folder (07/10/2026) and `phases/.claude/.cc-writes/` (10/10/2026).

- Current: untracked, empty, written by Claude Code when the working
  directory of a session was inside this folder.
- Proposed: removed by the user, with
  `rmdir internal-total-recall/.claude/.cc-writes internal-total-recall/.claude internal-total-recall/phases/.claude/.cc-writes internal-total-recall/phases/.claude`.
  No document changes: the rule of `rules.md`, "The internal folder",
  already says the working directory stays the repository.
- Reason: `CLAUDE.md` says nothing is written under `.claude/`.

## Contradictions

**1.** When an item leaves the Roadmap.

- `lifecycle.md`, "The Roadmap", and the header of the Roadmap in
  `plan.md`, 07/10/2026: "An item becomes a phase or a task when it
  opens, and leaves the Roadmap when it is delivered in full." Step 4
  of `close.md` says the same.
- D32 and D34, 11/10/2026: the minors and the second real project left
  the Roadmap when their phase opened, before they were delivered.
- Proposed, the newer practice wins: "An item leaves the Roadmap when
  it opens as a phase or a task: the phase file holds it from then on."
  In `lifecycle.md` and `plan.md`, and step 4 of `close.md` becomes
  "Clear the Roadmap in `plan.md`: an item that opened as a phase or a
  task leaves it, and the rest is renumbered." The same text in the
  templates of the skill is a change to the package, made under a task
  of Phase 05.
- The other choice: the second real project goes back to the Roadmap
  as item 1 until it is delivered, and the text stays.

**2.** Where a replaced decision goes in `obsolete.md`.

- `review.md`, step 6: "A replaced decision moves whole to the top of
  `obsolete.md`".
- The header of `obsolete.md` and `doc-check.py`: the most recently
  replaced first, by the date of the "Replaced by" line.
- Proposed: "A replaced decision moves whole to `obsolete.md`, at its
  place by the date it was replaced, the top for a decision replaced
  today". Needed by item 5, whose decision was replaced on 07/10/2026.

## Out of date

**3.** `tools/README.md`, the line of `machine-check.py`.

- Current: "reports the guardrails of the machine: the global rules
  file, the permission deny list, the guard hooks, `jq`, the sandbox."
- Proposed: "reports the guardrails of the machine: the global rules
  file, the start phrases line, the permission deny list, the guard
  hooks, `jq`, the sandbox."
- Reason: the row "start phrases" was added in Task 40 (D29). The
  template `skill/templates/tools/README.md` has the same line, a
  change to the package under a task of Phase 05.

**4.** The memory note `reference-system-read-only`, "How to apply".

- Current: "a `grep -ri` of the name over this folder is part of the
  close until a check tool does it."
- Proposed: "the review runs the same hash check over the tracked
  files and this folder, and prints only the paths, until item 3 of
  the Roadmap brings this folder into the package test."
- Reason: no step of `close.md` runs the grep, and a session cannot run
  it without the name, which it must not know or write. The hash check
  ran in this review. About the same size, in a note read at each
  start.

## Replaced decisions

**5.** D5, 07/10/2026, "the rules file".

- Current: in `decisions.md`, it says the user's seventeen writing
  rules are merged into the writing section of `rules.md`.
- Proposed: moved whole to the end of `obsolete.md` with "Replaced by
  D9 on 07/10/2026.", and D9 adds: "It replaces D5, and restates what
  holds: the rules travel with the project in `rules.md`, from the
  global file and the memory notes of the reference, and the user's
  own rules win where they differ from the global file."
- Reason: D9 put the user's style in the note `user-writing-style`, now
  eighteen rules, and D23 removed the repeats between the two.

**6.** D8, 07/10/2026, "the minors of the review".

- Current: in `decisions.md`, the thirteen minors are item 2 of the
  Roadmap.
- Proposed: moved whole to the top of `obsolete.md` with "Replaced by
  D33 on 11/10/2026.", and D33 adds: "It replaces D8, the minors as a
  Roadmap item."
- Reason: the minors were fixed in Phase 04, `e01301f`.

## The memory notes

The two notes match the decisions in force and the tree, apart from
item 4. The index has a line per note.
