@rules.md

# {{project}}

{{description}}

This file read at the start of a session runs the start routine below,
with no need for the phrase.

## Working documents

`{{internal}}/` is the memory of the project. Claude Code loads this
file when a session reads a file in the folder.

The size read at each start (this file, `rules.md` and the output of
`tools/start.py`): 8,000 words at most. `tools/doc-check.py` reports
it.

| File | What it holds |
|---|---|
| `rules.md` | The rules for every project: writing, working with the user, verification. Imported above |
| `state.md` | The snapshot: position, done this session, next, waiting on the user |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps |
| `history.md` | The session log, newest first |
| `story.md` | The diary in the user's voice, appended at the end |
| `decisions.md` | The decisions in force, numbered, newest first |
| `obsolete.md` | The decisions replaced by a newer one, with the number of the one that replaced them |
| `close.md` | The close routine |
| `review.md` | The review of the memory |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records, listed in its README |
| `tools/` | The scripts of the project, listed in its README |
| `memory/` | The memory notes of the project and their index |
| `backup/` | The archives of the folder, made by `/total-recall backup` and before each update, listed in its README |

## Sessions

"let's start", "let's continue" or "let's resume" runs the start routine:

1. Run `python3 "{{internal}}/tools/start.py" "{{internal}}"` and read
   its output: `state.md` and the memory notes whole, the goal and the
   head of the Roadmap, the preamble and the current task of the open
   phase. Claude Code loads this file and `rules.md` when the session
   reads a file in the folder: do not read them again.
2. When the script fails, read `state.md`, then `memory/MEMORY.md` and
   each note whole, the goal and the head of the Roadmap in `plan.md`,
   and the preamble and the current task of the open phase file named
   in `state.md`.
3. Give the briefing in a few sentences: the position, what the last
   session did, what comes next, what waits on the user. Then wait for
   the go, and do not start the work.

During the session:

- The work follows the open phase file, a task at a time. All the work
  of a session is under a numbered task of the open phase, the tools and
  the documents too. A task opens with what it does and why.
- A step is ticked with its date the moment it is done, with a line on
  what happened.
- What the session learns is written by the rule of `rules.md`,
  "When to ask before a write": a correction from the user is proposed
  at once, the rest waits for a pause.
- A decision goes at the top of `decisions.md` with the next number,
  and a decision it replaces moves to `obsolete.md`. A document is
  edited mid-session only when a decision makes it wrong.
- A spec or a plan written by a skill is saved under `records/`, and its
  tasks become tasks of the open phase.

"let's close", "docs routine", "documentation routine" or "sync the
docs" runs the close routine: read `close.md` and follow it. It runs
without asking permission. The user reads the result.

"review the memory" runs the review: read `review.md` and follow it.
It changes nothing before the user approves its report.

## Phases

The work is in phases, tasks and steps, one file per phase in
`phases/`. The project always has an open phase, named in `state.md`.
Read `lifecycle.md` when a phase opens or closes, and for the numbers.

## The project's own routines

Read when they apply. The table starts empty, and the project fills it:
a check before a hand-over, a gate, a release, a close step.

| Routine | File | When |
|---|---|---|

## Engineering

{{constraints}}

## Writing

The rules of `rules.md` hold for all the text. What the project adds:
nothing yet.
