# Decisions

One entry per decision, appended at the end: the date, what was
decided, on whose word, why. A decision on the Roadmap, on a rule or on
the design goes here when it is taken.

## 07/10/2026: the memory system

The project keeps its memory in `internal-total-recall/`, installed by
`/total-recall`, the user's word. Phase 01 is The skill.

## 07/10/2026: the folder and nothing else

The memory lives in `internal-<folder>/` at the root of the project,
and nothing else is written: no file under `.claude/`, no setting of
the machine, no `CLAUDE.local.md` at the root. The user's word: the
repository must not show that Claude is part of the stack, and the
system must not depend on a setting of a machine. The exclusion is one
line in `.git/info/exclude`, which git never commits.

## 07/10/2026: the loading

The project file loads by itself when a session reads a file of the
folder, and says in its first lines that reading it at the start of a
session runs the start routine. "let's start" works on this machine
through the global file; "read internal-<folder>/CLAUDE.md" works
anywhere. The skill is not relied on for the loading: it can be
uninstalled. The user's word.

## 07/10/2026: the twelve changes from the reference

Approved by the user, each with its reason in the spec, "What changes":
always an open phase; a decisions file; the snapshot kept to four
sections, with corrections as memory notes at once; no phase index
table; planned task numbers in the phase file only; steps ticked at the
moment; records in a folder with their own list; skill output under
`records/`; reading the file starts the routine; the code map carries
its commit; a memory note per topic; the rules loaded twice on this
machine, accepted.

## 07/10/2026: the rules file

The rules travel with the project in `rules.md`: the global file, the
user's seventeen writing rules merged into the writing section, and the
rules taken from the memory notes of the reference. Where the global
file and the user's own rules differ, the user's own rules win. The
user's word: "most important is human style and my own writing style".

## 07/10/2026: the skill is the installer

`/total-recall` installs the folder, or checks an existing one, and
nothing more. It is user invoked only. It asks three to five questions,
writes a description the user approves, then writes the folder, hands
over the exclusion line, reports the machine, and proposes the missing
guardrails with the lines for the user to run.

## 07/10/2026: the repair mode

On an existing folder, the render adds only the templates that carry
no placeholder (the rules, the routines, the tools, the code map, the
records README) and names each missing file that needs answers, for
the session to write by hand from what the folder holds. It never
writes a second phase file. The session's ruling on the reviewer's
first Important finding, with a failing test first.

## 07/10/2026: the minors of the review

The thirteen Minor findings of the fresh review are not fixed in the
build session: they are item 2 of the Roadmap, candidates for the
tasks of Phase 02 with the user's own notes. The rule of the executing
skill: minors never enter the fix pass, the user decides.

## 07/10/2026: the user's style is a memory note

The user's own style is shipped as the memory note `user-writing-style`
in every project, read whole at the start and before writing any text,
and `rules.md` points to it. This replaces the consolidation of the
spec, which had put the style in `rules.md` and shipped one note. The
user's word: "in memory is stronger and less prone to be forgotten,
that is the purpose". A correction on the text updates the note.

## 07/10/2026: the reference project is named nowhere

The name of the reference project and the path of its folder are not
written anywhere, in the package or in this internal folder, its
records included. The user gives the path when a session needs it. The
user's word, after finding the name in seven files of this folder.

## 07/10/2026: the history title

A history title may carry a word after the date, `# DD/MM/YYYY, later -
<name>`, for a second session of a day: the user's habit, seen in the
reference history. The session's ruling during Task 4.
