# The review of the memory, 10/10/2026

The first review of this folder, on the user's word, after the delivery
of Tasks 18 to 26. It has two parts: the form, as `/total-recall` step
2 brings an older folder to the current form, and the content, by
`review.md` of the skill. Nothing is changed before the user answers.

Size read at each start, before: 5803 words, limit 8000 (the default,
`CLAUDE.md` names no limit yet). The new check reports 15 findings, the
15 old titles of `decisions.md`.

## The form

1. **The missing files.** The repair adds `obsolete.md` and
   `review.md` from the templates. Nothing else is written.
2. **`rules.md`.** Replaced whole by the template. The differences are
   the template's own: the sentence "Git does not track it, and nothing
   in it can be brought back from a commit" removed, "not under a
   folder git tracks" removed, the section "When to ask before a write"
   added. No edit of this project in the file.
3. **`close.md`.** Replaced whole by the template: step 1 asks the held
   proposals, step 10 suggests the review, "Nothing of the folder goes
   through git" becomes "The close runs no git command". No edit of
   this project in the file.
4. **`lifecycle.md`.** Replaced whole by the template: the last
   sentence names `obsolete.md`.
5. **`tools/doc-check.py`.** Replaced by the template: the checks of
   the decisions, of `obsolete.md` and of the size.
6. **`tools/README.md`.** The line of `doc-check.py` takes the text of
   the template, with this folder's name in the commands.
7. **`decisions.md`.** Migrated by `render.py --migrate-decisions`:
   numbered D1 to D15 in the order they were taken, newest first, the
   header of the template. The text of each entry is kept.

## Contradictions

8. **The folder in git.** D12 (10/10/2026): the folder is in git on
   purpose, and no document states the choice. These places state the
   old exclusion:
   - `CLAUDE.md`, "Working documents": "Git does not track it: one line
     in `.git/info/exclude` keeps it out. A file replaced here does not
     come back from a commit."
   - `CLAUDE.md`, "Engineering", and `plan.md`, "Constraints": "The
     internal folder stays out of git."
   - `memory/project-instruction-file.md`: "and git does not track
     `internal-total-recall/`", and the why, "out of the repository".
   - `state.md`, "Position": "The exclusion line is in
     `.git/info/exclude`, and git ignores this folder."

   Proposed: the sentences removed, the note worded as its template
   ("in one folder of the project"). `state.md` is rewritten at the
   close.
9. **The reason of D2.** D2 (07/10/2026) gives as its reason "the
   repository must not show that Claude is part of the stack". Since
   `1c64cda` the repository holds this folder, its `CLAUDE.md` and its
   memory notes. The two cannot both hold. Your choice:
   - (a) the reason is dropped: the repository may show that Claude is
     part of the stack (recommended, since the folder is in git on
     purpose);
   - (b) the reason holds, and the folder leaves git again.
10. **The session rules of `CLAUDE.md`.** "A correction from the user
    becomes a memory note at once" and "A decision is appended to
    `decisions.md`" contradict D13 and D14 and the new `rules.md`.
    Proposed: the two bullets of the template ("What the session learns
    is written by the rule of `rules.md`, ..." and "A decision goes at
    the top of `decisions.md` with the next number, ..."), and the
    paragraph of "review the memory" after the close.

## Duplicates

11. **The reference project.** The first bullet of "Writing" in
    `CLAUDE.md` (about 75 words) repeats the memory note
    `reference-system-read-only`, the search of the name at the close
    included. Both are read at each start. Proposed: the rule stays in
    the note, and the bullet becomes "The reference project is never
    named, by the memory note `reference-system-read-only`."

## Out of date

12. **The table of `CLAUDE.md`.** The row of `decisions.md` reads
    "Dated decisions, appended at the end", and `obsolete.md` and
    `review.md` have no row. Proposed: the rows of the template, and
    the line of the size under "Working documents": "The size read at
    each start (this file, `rules.md`, `state.md`, `plan.md` and the
    memory notes): 8,000 words at most."
13. **`code-map.md`.** Phase 01 says the fixes of the review are
    uncommitted; they are `3d49152` and `45ed75f`. Phase 02 names Task
    17 only. Proposed: the commits named, and the entries of Tasks 18
    to 26 that touched code: `doc-check.py` (`check_decisions`,
    `start_size`, `size_limit`, `--size`, `d64cf13`), `render.py`
    (`split_decisions`, `migrate_decisions`, `run_migration`,
    `--migrate-decisions`, `9201de6`), the new tests (`MigrateDecisions`,
    `RealTemplates`, `GitQuestion`, `WhenToAsk`, `Review`, `Readme`,
    `AnotherSystem`), `SKILL.md` steps 1, 2, 5, 7 and 9.
14. **`records/README.md`.** The row of `2026-10-07-design.md` ends
    "Names the reference project", but the name was replaced by a
    placeholder on 07/10/2026. Proposed: "Refers to the reference
    project by a placeholder".
15. **The Roadmap of `plan.md`.** Item 1, the feedback of the first
    trials, is delivered for this round (Tasks 15 to 26). Proposed: it
    leaves, and three items found today come in:
    - the repair prints `needs answers:` for a first phase file that
      exists under its own name (Task 23);
    - a line for a global rules file that maps "let's start" for a new
      user, to try on a machine without the user's file (Task 24);
    - the templates write the description twice (`CLAUDE.md` and the
      Goal of `plan.md`) and the constraints twice, both read at each
      start.

    Item 2, the reviewer's minors, stays, with the list item after a
    paragraph that the check reports (Task 23).
16. **`state.md`.** Dated 07/10/2026, Task 15 open. Proposed: no change
    now, the close rewrites it.

## Replaced decisions

After the migration of item 7.

17. **D2, the folder and nothing else.** Replaced by D12 on
    10/10/2026: the exclusion line. D2 moves whole to `obsolete.md`,
    and D12 restates what still holds: "Nothing else is written outside
    the folder: no file under `.claude/`, no setting of the machine, no
    `CLAUDE.local.md` at the root", with the reason chosen in item 9.
18. **D4, the twelve changes from the reference.** "Corrections as
    memory notes at once" is replaced by D13 on 10/10/2026. D4 moves
    whole, and D13 restates the eleven others.
19. **D6, the skill is the installer.** "Hands over the exclusion line"
    is replaced by D12, and the check of an existing folder by D13 (the
    update to the current form). D6 moves whole, and D13 restates what
    holds: `/total-recall` is user invoked only, asks the questions,
    writes a description the user approves, writes the folder, reports
    the machine and proposes the missing guardrails.

## The memory folder

20. **The name of the reference project in the repository.** D10 and
    the note `reference-system-read-only` say the name is written
    nowhere in the repository. The list of forbidden words of
    `tests/test_package.py` holds it, since `aca0d06`, and the test
    skips the `tests/` folder in its own check. Proposed, as a task with
    its test: the test keeps the SHA-256 hash of the name and compares
    the hash of each word of the files, so the name is written nowhere.
    The name stays in the git history from `aca0d06`: removing it from
    there is a rewrite of the history and a forced push, the user's
    decision.
21. **`memory/project-instruction-file.md` repeats other files.** Its
    content (where the rules are, read whole at the start, the notes in
    this folder) is in `CLAUDE.md`, "Sessions", and in `rules.md`, "The
    internal folder", all read at each start (150 words). The note is a
    template. Proposed: a Roadmap item for the template, this copy left
    as it is (apart from item 8).

The other notes need nothing: `user-writing-style` is identical to its
template and holds the correction of the day, and the index has a line
per note.

## The size after

About 6,050 words read at each start, by estimate: `rules.md` grows by
about 280 words, `CLAUDE.md` by about 60, and items 8 and 11 remove
about 110.
