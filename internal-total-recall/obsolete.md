# Obsolete decisions

The decisions replaced by a newer one, the most recently replaced
first. Each entry is moved whole from `decisions.md`, with one line
under its title: `Replaced by Dn on DD/MM/YYYY.`

## D8, 07/10/2026: the minors of the review

Replaced by D33 on 11/10/2026.

The thirteen Minor findings of the fresh review are not fixed in the
build session: they are item 2 of the Roadmap, candidates for the
tasks of Phase 02 with the user's own notes. The rule of the executing
skill: minors never enter the fix pass, the user decides.

## D15, 10/10/2026: the README for a public skill

Replaced by D20 on 10/10/2026.

The README is written in the user's voice and by the user's rules,
without saying so, and names the folder `internal-<project-name>`. The
review of this project waits for the final skill and the user's word.

## D6, 07/10/2026: the skill is the installer

Replaced by D16 on 10/10/2026.

`/total-recall` installs the folder, or checks an existing one, and
nothing more. It is user invoked only. It asks three to five questions,
writes a description the user approves, then writes the folder, hands
over the exclusion line, reports the machine, and proposes the missing
guardrails with the lines for the user to run.

## D4, 07/10/2026: the twelve changes from the reference

Replaced by D13 on 10/10/2026.

Approved by the user, each with its reason in the spec, "What changes":
always an open phase; a decisions file; the snapshot kept to four
sections, with corrections as memory notes at once; no phase index
table; planned task numbers in the phase file only; steps ticked at the
moment; records in a folder with their own list; skill output under
`records/`; reading the file starts the routine; the code map carries
its commit; a memory note per topic; the rules loaded twice on this
machine, accepted.

## D2, 07/10/2026: the folder and nothing else

Replaced by D12 on 10/10/2026.

The memory lives in `internal-<folder>/` at the root of the project,
and nothing else is written: no file under `.claude/`, no setting of
the machine, no `CLAUDE.local.md` at the root. The user's word: the
repository must not show that Claude is part of the stack, and the
system must not depend on a setting of a machine. The exclusion is one
line in `.git/info/exclude`, which git never commits.

## D5, 07/10/2026: the rules file

Replaced by D9 on 07/10/2026.

The rules travel with the project in `rules.md`: the global file, the
user's seventeen writing rules merged into the writing section, and the
rules taken from the memory notes of the reference. Where the global
file and the user's own rules differ, the user's own rules win. The
user's word: "most important is human style and my own writing style".
