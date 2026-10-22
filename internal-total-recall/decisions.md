# Decisions

The decisions in force, the newest first. Each entry gives its number,
the date, what was decided, on whose word and why. A decision on the
Roadmap, on a rule or on the design goes at the top when it is taken,
with the next number. A decision replaced by a newer one moves whole to
`obsolete.md`, and the new decision names it and restates the part that
still holds.

## D37, 22/10/2026: a record and a phase file are named by a letter and a number

A record is named `RNNN-<name>.md` and a phase file `PNN-<name>.md`: a
letter for the kind, the number, then the name. The number of a record
counts from 000 in the order of creation, the number of a phase from 01,
as before. The date of a record stays in the README of the records and
in the record. The user's word, after the first round of the day.

It replaces D36, the running number without the letter. The number and
the date hold.

## D35, 22/10/2026: two forms of the skill, changed together

The skill has two forms: `skill-claude/` for Claude Code, named
`skill/` until 22/10/2026, and `skill-pi/` for Pi, written by the user
on 16/10/2026. A change to one form is made in the other in the same
task, and the tests run over both forms. D31 reads with
`skill-claude/machine/hooks/`. The user's word.

## D34, 11/10/2026: Phase 04 closed, Phase 05 A second real project opened

Phase 04 closes with its checkpoint met: the fifteen findings handled,
committed as `e01301f`, the suite green. Phase 05 opens with the head
of the Roadmap, the second real project, which the user set aside
until Phase 04 was done. The project is still to be chosen. The rule
of `lifecycle.md`, at the user's "let's close".

## D33, 11/10/2026: the minors fixed at once

The fifteen findings of Task 45 are fixed in one pass, by common sense,
with no reading one at a time: they are small and need only logic.
Finding 12, the skill-creator checks named in the spec, is dropped:
the spec is a record kept as received, and the package test covers the
frontmatter. The user's word.

It replaces D8, the minors as a Roadmap item.

## D32, 11/10/2026: Phase 03 closed, Phase 04 The reviewer's minors opened

Phase 03 closes with its checkpoint met: the benchmark recorded, each
task delivered or moved on the user's word, the suite green. Phase 04
takes item 2 of the Roadmap, the reviewer's minors, before the head,
the second real project, which waits for a project to be chosen. The
check's miss of a "Done" step not ticked joins the minors. The user's
word.

## D31, 11/10/2026: the guard scripts stay in the skill

The guard scripts stay in `skill/machine/hooks/`. Step 8 of the install
already proposes them only when the machine check reports them missing,
a session never reads them, and they enforce the rules of `rules.md` on
the user's own commands and removals. A repository of their own is
Parked, back if a second user installs the skill or if the copies fall
behind the scripts the machine runs. The user's word.

## D30, 11/10/2026: the second real project moves to the Roadmap

Task 41 leaves Phase 03 and becomes item 1 of the Roadmap. It is not an
optimization, its sessions run in another project at the user's pace,
and it tries the templates best once the changes of the phase are
committed. The project is still to be chosen. The user's word.

## D29, 11/10/2026: the start phrases in the global file

A line in the global rules file names
`internal-<project-name>/CLAUDE.md` for "let's start", "let's continue"
and "let's resume". `machine-check.py` reports the line as the row
"start phrases", and step 8 of the install proposes it when it is
missing. The repository keeps no root `CLAUDE.md`. The global file
stays whole, since it serves the projects without total recall. The
user's word.

## D28, 11/10/2026: the tests that pin the wording stay

The tests that check a sentence of a rule stay as they are. They stop a
rewrite from dropping a rule unnoticed, and a meant change of wording
changes the test in the same edit. A comment at the top of
`tests/test_package.py` gives this reason. The user's word.

## D27, 11/10/2026: the close reads the tasks of the session

Step 3 of the close reads only the tasks of the session, found by their
headings, and `doc-check.py` checks the form of the rest of the phase
file. A done step says what happened in a line or two. The review still
reads the whole file. The user's word.

## D26, 11/10/2026: the repeats of the templates removed

Task 37 removes four repeats of the templates:

- the Goal of `plan.md` points to the description of `CLAUDE.md`;
- the Constraints of `plan.md` point to "Engineering" of `CLAUDE.md`;
- the note `project-instruction-file` is deleted, since a session reads
  it after `CLAUDE.md` is loaded and it adds nothing to it;
- the template `CLAUDE.md` is named `CLAUDE.template.md`, and
  `render.py` writes it as `CLAUDE.md`, so that Claude Code does not
  load the templates as instructions in this repository.

The user's word.

## D25, 11/10/2026: no line for shorter close entries

Task 36 ends with no change to `close.md`. The reasons:

- the history entries went from 522 words to about 150 under the
  present routine, which already asks for short bullets and a story
  the size of a social media post;
- a start does not read `history.md` or `story.md`, so the cost is the
  writing, about 550 words a close with `state.md`;
- the story is the user's diary, and its length is the user's taste.

The user's word.

## D24, 11/10/2026: no start levels

Task 35 ends with no change: the start keeps a single level. The
reasons:

- Claude Code loads `CLAUDE.md` and `rules.md` when the session reads
  or writes a file in the folder, so a light start delays the rules and
  does not save them;
- the style note, the largest part left, is read before any text, the
  briefing included;
- the other notes, the plan part and the phase part are about 1,150
  words, and the notes include the one that keeps the name of the
  reference project out of the repository.

The user's word.

## D23, 11/10/2026: no compressed copy of the rules, the repeats removed

Task 34 makes no compressed copy of the rules. It removes the repeats
between `rules.md` and the style note, each rule written once in plain
English. The reasons:

- a copy in shorthand shows Claude the style the rules forbid;
- the pairs of wrong and right examples do not compress;
- two copies drift apart, and a check sees words, not meaning.

The global rules file of this machine, which repeats most of
`rules.md`, is weighed in Task 40 with the entry point. The user's
word.

## D22, 11/10/2026: the start script, and the rules loaded by Claude Code

The start routine runs `tools/start.py`, which prints the whole start
in one output: the snapshot, the memory notes, the goal and the head of
the Roadmap, the preamble and the current task of the open phase. The
routine relies on Claude Code to load `CLAUDE.md` and `rules.md` when
the session reads a file in the folder, and no longer reads them, which
stops a double read of about 3,500 words. When the script fails, the
routine reads the files as before. The user's word, the design under
Task 33.

## D21, 10/10/2026: Phase 02 closed, Phase 03 Optimization opened

Phase 02 closes with the trial of the update on a scratch repository
not run: the user's word that the backup is fine stands for it, and
the update was run for real on this folder in Task 30. Phase 03 takes
its name, Optimization, from the user and not from the head of the
Roadmap. It lowers the cost of a start, measured against
`records/R008-baseline.md`, and takes items 4 and 6 of the
Roadmap with the points of the exploration of 10/10/2026. The user's
word.

## D20, 10/10/2026: the README speaks to the reader

The README speaks to the reader with "you", with no first person, by
the user's own rewrites: the opening in the user's words, "let's start"
where the read phrase was, one line per paragraph, a section on the
templates to adapt and on a fork. Rule 16 of the style note changed to
match, in the note and its template, the user's word at the review. It
replaces D15, and restates what holds: the folder is named
`internal-<project-name>`, in backticks.

## D19, 10/10/2026: the skill starts by its command only

`disable-model-invocation: true` stays in `SKILL.md`: Claude does not
start the skill on its own, so a request in plain words does not start
it on a project documented another way, and the description of the
skill stays out of the context until the command. The user's word.

## D18, 10/10/2026: the review takes in the session and the notes

The review starts with what the session decided and the folder does
not hold yet, and checks the memory notes: a rule of a note is checked
where it applies, across the repository for a rule about the
repository. The user's word, after the first review missed the memory
folder: the causes are fixed in the skill, then the skill runs again.

## D17, 10/10/2026: the refusal of another documentation system

The skill writes nothing over another documentation system (a root
`CLAUDE.md`, `CLAUDE.local.md` or `AGENTS.md`, a `.claude/CLAUDE.md`, a
`memory-bank/` folder) or over a folder whose `CLAUDE.md` does not
start with `@rules.md`. It names what it found and recommends to move
it out of the project, install, then bring it in through a session of
questions. The user's word.

## D16, 10/10/2026: the backup and the update

The rule "the skill never overwrites a file" is gone. `backup/` holds
dated archives of the folder, named
`internal-<project-name>-YYYY-MM-DD-HH-MM-manual.tar.gz` or `-auto`,
with no special treatment for git, old ones deleted by the user.
`/total-recall backup` writes a manual archive; `/total-recall update`
shows its plan, asks one yes, writes an auto archive, then adds the
missing files, replaces the routine files and migrates the decisions,
never the project's own content. The user's word. It replaces D6, and
restates what holds: `/total-recall` is user invoked only; at the
install it asks the questions, writes a description the user approves,
writes the folder, reports the machine and proposes the missing
guardrails.

## D14, 10/10/2026: the decisions newest first, and obsolete.md

The decisions are numbered and kept newest first, and a replaced
decision moves whole to `obsolete.md` with the number and the date of
the one that replaces it. The user's idea and the name `obsolete.md`.
`story.md` stays oldest first.

## D13, 10/10/2026: the memory used with care

The skill writes to the memory without asking when the place is
obvious and the cost small, and asks first when the text goes into a
file read at each start, changes something written, has no clear place
or is large. The questions wait for a pause, except a correction. A
review of the memory, "review the memory", proposes its changes in a
report and applies only the approved ones. `/total-recall` on an
existing folder brings it to the current form. The user's notes, the
spec `records/R004-design.md`.

It replaces D4 for the corrections, and restates the rest of D4's
changes from the reference: always an open phase; a decisions file; the
snapshot kept to four sections; no phase index table; planned task
numbers in the phase file only; steps ticked at the moment; records in
a folder with their own list; skill output under `records/`; reading
the file starts the routine; the code map carries its commit; a memory
note per topic; the rules loaded twice on this machine, accepted.

## D12, 10/10/2026: the internal folder in git, the user's choice

The skill asks the user at the install whether the internal folder
stays out of git, and writes the exclusion line only on a yes. No
document, README or memory note states the choice. This project's
folder is in git since `1c64cda`, on purpose: the user's word. It
replaces D2, and restates what holds: nothing else is written outside
the folder, no file under `.claude/`, no setting of the machine, no
`CLAUDE.local.md` at the root. The reason of D2, that the repository
must not show Claude in the stack, is dropped: the user's word at the
review of the memory.

## D11, 07/10/2026: the history title

A history title may carry a word after the date, `# DD/MM/YYYY, later -
<name>`, for a second session of a day: the user's habit, seen in the
reference history. The session's ruling during Task 4.

## D10, 07/10/2026: the reference project is named nowhere

The name of the reference project and the path of its folder are not
written anywhere, in the package or in this internal folder, its
records included. The user gives the path when a session needs it. The
user's word, after finding the name in seven files of this folder.

## D9, 07/10/2026: the user's style is a memory note

The user's own style is shipped as the memory note `user-writing-style`
in every project, read whole at the start and before writing any text,
and `rules.md` points to it. This replaces the consolidation of the
spec, which had put the style in `rules.md` and shipped one note. The
user's word: "in memory is stronger and less prone to be forgotten,
that is the purpose". A correction on the text updates the note.

It replaces D5, and restates what holds: the rules travel with the
project in `rules.md`, from the global file and the memory notes of
the reference, and the user's own rules win where they differ from the
global file.

## D7, 07/10/2026: the repair mode

On an existing folder, the render adds only the templates that carry
no placeholder (the rules, the routines, the tools, the code map, the
records README) and names each missing file that needs answers, for
the session to write by hand from what the folder holds. It never
writes a second phase file. The session's ruling on the reviewer's
first Important finding, with a failing test first.

## D3, 07/10/2026: the loading

The project file loads by itself when a session reads a file of the
folder, and says in its first lines that reading it at the start of a
session runs the start routine. "let's start" works on this machine
through the global file; "read internal-<folder>/CLAUDE.md" works
anywhere. The skill is not relied on for the loading: it can be
uninstalled. The user's word.

## D1, 07/10/2026: the memory system

The project keeps its memory in `internal-total-recall/`, installed by
`/total-recall`, the user's word. Phase 01 is The skill.
