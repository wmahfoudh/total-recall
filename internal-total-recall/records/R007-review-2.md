# The review of the memory, 10/10/2026, second run

The review by `review.md` after `/total-recall update`, with the
session's decisions taken in. It replaces the first report of the day,
`2026-10-10-review.md`, set aside when the review missed the memory
folder. Nothing is changed before the user answers.

Size read at each start, before: 6045 words, limit 8000. The check
reads `clean`.

## From this session

Decided or learned in this session and not written in the folder, apart
from the phase file:

1. **The backup and the update** (Task 29, the user's word): the rule
   "the skill never overwrites a file" is gone; `backup/` holds dated
   archives ending in `-manual` or `-auto`, with no special treatment
   for git, old ones deleted by hand; `/total-recall update` is one yes
   after an `-auto` backup. Proposed: decision D16, which replaces D6
   (item 19).
2. **The refusal of another documentation system** (Task 26, the user's
   word): the skill writes nothing over a root `CLAUDE.md`,
   `CLAUDE.local.md`, `AGENTS.md`, `.claude/CLAUDE.md`, `memory-bank/`,
   or a folder whose `CLAUDE.md` does not start with `@rules.md`, and
   recommends to move it out, install, then bring it in through a
   session of questions. Proposed: decision D17.
3. **The review takes in the session and checks the notes** (Task 27,
   the user's word): fix the causes in the skill, then run it again
   with the session's decisions. Proposed: decision D18.
4. **The skill is started by the command only** (the user's word):
   `disable-model-invocation: true` stays, it avoids an accidental start
   on a project documented another way and keeps the description out of
   the context. Proposed: decision D19.
5. **The README speaks to the reader** (the user's rewrites): the
   opening in the user's own words, "let's start" in place of the read
   phrase, one line per paragraph, no first person, a section on the
   templates to adapt and on a fork. This replaces part of D15 (item
   20) and touches the style note (item 9). Proposed: decision D20.
6. **The name of the reference project in the history.** Replaced by a
   hash in the tests (Task 28); the history from `aca0d06` still holds
   it in two commits. Proposed: an item under Blocked in `plan.md`,
   waiting on the user's decision on a rewrite of the history.
7. **Found on the way, for the Roadmap:** the line of a global rules
   file that maps "let's start" for a new user; the package test does
   not read the internal folder, which git now tracks; the check
   reports a list item after a paragraph inside the item before it.
   Proposed: in the Roadmap (item 16).

## Contradictions

8. **The folder in git.** D12: the folder is in git on purpose, and no
   document states the choice. Still stated in `CLAUDE.md`, "Working
   documents" ("Git does not track it: one line in `.git/info/exclude`
   keeps it out. A file replaced here does not come back from a
   commit."), in `CLAUDE.md`, "Engineering", and `plan.md`,
   "Constraints" ("The internal folder stays out of git."), in
   `memory/project-instruction-file.md` ("git does not track"), and in
   `state.md`. Proposed: the sentences removed, the note worded as its
   template; `state.md` at the close.
9. **The voice of the README and rule 16 of the style note.** Rule 16
   says prose for a product's readers speaks in the first person about
   why the project exists. The user's README speaks to the reader with
   "you" and has no first person, by the user's own rewrite. `CLAUDE.md`,
   "Engineering", says "the README in the user's voice". Your choice:
   - (a) rule 16 stays for other projects; this project's `CLAUDE.md`
     says the README speaks to the reader, neutral, no first person
     (recommended: the choice is about a public skill);
   - (b) rule 16 changes in the note and its template: prose for
     readers speaks to the reader, without the first person.
10. **The reason of D2.** D2 gives as its reason "the repository must
    not show that Claude is part of the stack", and the repository has
    held this folder since `1c64cda`. Your choice:
    - (a) the reason is dropped (recommended);
    - (b) the reason holds, and the folder leaves git again.
11. **The session rules of `CLAUDE.md`.** "A correction from the user
    becomes a memory note at once" and "A decision is appended to
    `decisions.md`" contradict D13, D14 and `rules.md`. Proposed: the
    two bullets of the template, and the paragraph of "review the
    memory" after the close.

## Duplicates

12. **The reference project.** The first bullet of "Writing" in
    `CLAUDE.md` repeats the note `reference-system-read-only`; both are
    read at each start. Proposed: the rule stays in the note, the
    bullet becomes "The reference project is never named, by the memory
    note `reference-system-read-only`."

## Out of date

13. **The table of `CLAUDE.md`.** The row of `decisions.md` reads
    "Dated decisions, appended at the end"; `obsolete.md`, `review.md`
    and `backup/` have no row; no line gives the size read at each
    start. Proposed: the rows and the line of the template.
14. **`code-map.md`.** Phase 01 says the fixes of the review are
    uncommitted (they are `3d49152` and `45ed75f`); Phase 02 names Task
    17 only. Proposed: the commits named, and the entries of the tasks
    that touched code: Task 18 `doc-check.py` (`d64cf13`), Task 19
    `render.py` migration (`9201de6`), Task 28 `tests/test_package.py`
    hash, Task 29 `update.py` and `render.present`, with their tests.
15. **`records/README.md`.** The row of `2026-10-07-design.md` ends
    "Names the reference project", where a placeholder replaced the
    name. Proposed: "Refers to the reference project by a placeholder",
    and a row for this report.
16. **The Roadmap of `plan.md`.** Item 1, the feedback of the first
    trials, is delivered for this round (Tasks 15 to 29). Proposed: it
    leaves; in come the three items of item 7, and two template items:
    the description and the constraints written twice (`CLAUDE.md` and
    `plan.md`, both read at each start), and the note
    `project-instruction-file` that repeats `CLAUDE.md` and `rules.md`.
17. **The order of the phase file.** The preamble of
    `phases/phase-02-first-use.md` lists Tasks 18 to 25; Tasks 26 to 29
    were added. Proposed: the order names Tasks 18 to 29.
18. **The tools README.** The line of `doc-check.py` in
    `tools/README.md` lacks the checks of the decisions and of the size.
    Proposed: the line of the template, with this folder's name.

## Replaced decisions

19. **D6, the skill is the installer.** "Installs the folder, or checks
    an existing one, and nothing more" and "hands over the exclusion
    line" are replaced by D12 and D16. D6 moves to `obsolete.md`,
    "Replaced by D16 on 10/10/2026", and D16 restates what holds: user
    invoked only, the questions, the description approved, the folder
    written, the machine reported.
20. **D15, the README for a public skill.** "In the user's voice" is
    replaced by D20 (item 5). D15 moves, "Replaced by D20 on
    10/10/2026", and D20 restates the name `internal-<project-name>`
    and the review of this project after delivery.
21. **D2, the folder and nothing else.** The exclusion line is replaced
    by D12. D2 moves, "Replaced by D12 on 10/10/2026", and D12 restates
    "nothing else is written outside the folder: no file under
    `.claude/`, no setting of the machine, no `CLAUDE.local.md` at the
    root", with the reason chosen in item 10.
22. **D4, the twelve changes from the reference.** "Corrections as
    memory notes at once" is replaced by D13. D4 moves, "Replaced by D13
    on 10/10/2026", and D13 restates the eleven other changes.

## The memory notes

23. **`project-instruction-file`**: the git clause (item 8), and a
    repeat of `CLAUDE.md` and `rules.md` (item 16, for the template).
24. **`reference-system-read-only`**: the rule holds in the tracked
    files (none names the project). Out of date: "The package test
    checks the word in `skill/` and `README.md`"; it now checks
    `skill/`, `tests/` and the README by a hash. Proposed: that
    sentence corrected. The history: item 6.
25. **`user-writing-style`**: identical to its template; rule 16, item
    9. The index has a line per note.

## The size after

About 6,000 words read at each start, by estimate: items 8 and 12
remove about 110 words, item 13 adds about 60.
