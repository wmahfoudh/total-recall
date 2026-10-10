# Decisions

The decisions in force, the newest first. Each entry gives its number,
the date, what was decided, on whose word and why. A decision on the
Roadmap, on a rule or on the design goes at the top when it is taken,
with the next number. A decision replaced by a newer one moves whole to
`obsolete.md`, and the new decision names it and restates the part that
still holds.

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
spec `records/2026-10-10-design.md`.

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

## D8, 07/10/2026: the minors of the review

The thirteen Minor findings of the fresh review are not fixed in the
build session: they are item 2 of the Roadmap, candidates for the
tasks of Phase 02 with the user's own notes. The rule of the executing
skill: minors never enter the fix pass, the user decides.

## D7, 07/10/2026: the repair mode

On an existing folder, the render adds only the templates that carry
no placeholder (the rules, the routines, the tools, the code map, the
records README) and names each missing file that needs answers, for
the session to write by hand from what the folder holds. It never
writes a second phase file. The session's ruling on the reviewer's
first Important finding, with a failing test first.

## D5, 07/10/2026: the rules file

The rules travel with the project in `rules.md`: the global file, the
user's seventeen writing rules merged into the writing section, and the
rules taken from the memory notes of the reference. Where the global
file and the user's own rules differ, the user's own rules win. The
user's word: "most important is human style and my own writing style".

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
