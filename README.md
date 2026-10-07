# Total recall

I work on my projects with Claude Code over many sessions, and each
session starts from nothing. Total recall is a skill that gives a
project a memory: a folder of plain documents inside the project, kept
out of git, that a session reads at its start and updates at its close.
The next session knows what was done and what comes next.

The folder is named `internal-<folder>`, after the project's folder.
One line in `.git/info/exclude` keeps it out of git. Nothing of it
reaches the repository, and the folder name is the only trace.

## What it installs

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents |
| `state.md` | The snapshot: position, done this session, next, waiting on me |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps |
| `history.md` | The session log, newest first |
| `story.md` | The diary in my voice, appended at the end |
| `decisions.md` | Dated decisions, appended at the end |
| `close.md` | The close routine |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records: a pasted log, a study, a spec written by a skill |
| `tools/` | A check of the documents and a check of the machine |
| `memory/` | The memory notes of the project and their index |

## How a session works

The session opens with "let's start", or with "read
internal-<folder>/CLAUDE.md" on a machine that has no global rules
file. It reads the project file, the rules, the snapshot and the memory
notes, then the open phase, and gives a briefing: where the project is,
what the last session did, what comes next, what waits on me. Then it
waits for my go.

During the session the work follows the open phase, a task at a time. A
step is ticked with its date when it is done. A correction becomes a
memory note at once, and a decision goes to the decisions file.

"let's close" runs the close routine: the snapshot rewritten, the phase
file checked, the Roadmap cleared, an entry in the history, a story
entry in my voice, the project file reread against the project, and the
check tool run on the documents.

## The plan

Work is in phases, tasks and steps. Phases count from 01, tasks from 1
across phases, steps inside a task. A phase is a file. The project
always has an open phase: every piece of work has a home. The rules
are in `lifecycle.md` of the folder.

## Install the skill

The skill is the `skill/` folder of this repository. Link it, or copy
it, into the skills folder of Claude Code:

```
ln -s "$(pwd)/skill" ~/.claude/skills/total-recall
```

A copy (`cp -r skill ~/.claude/skills/total-recall`) does not follow
this repository when it changes.

## Use it on a project

1. In the project folder, run `git init` if the folder is not a
   repository yet.
2. Start Claude Code there and type `/total-recall`.
3. Answer the five questions, read the description it writes, and
   correct it until it is right.
4. Run the one line it hands you for `.git/info/exclude`, then
   `git status` to see that nothing of the folder shows.
5. Read the machine table. When a guardrail is missing, the skill
   proposes the lines, and you run them.
6. Open the first session with "let's start".

## Check it

1. `git status` shows nothing from the internal folder.
2. A new session opened with "read internal-<folder>/CLAUDE.md" gives
   the briefing, with Phase 01 open and Task 1 next.
3. "let's close" rewrites `state.md` and adds an entry at the top of
   `history.md`.

## On another machine

Install the skill, open the project, and start the session with "read
internal-<folder>/CLAUDE.md". The rules travel with the folder. The
session follows them without a global file. The machine check,
`tools/machine-check.py` of the folder, says which guardrails the
machine has: the permission deny list, the guard hooks, `jq`, the
sandbox. The skill ships the deny list and the three guard scripts under
`skill/machine/`, and proposes them when they are missing.

## The guardrails

The guardrails keep a session from writing where it should not: a deny
list of permissions (git writes, sudo, the destructive tools) and two
hook scripts that read each command before it runs and refuse git
writes, recursive deletes and writes into `.git`. Claude Code applies
them from `~/.claude/settings.json`. The scripts need `jq`.

## Limits

- The folder is not in git: it has no history and no backup. A copy
  of it is my own routine.
- The skill writes nothing under `.claude/` and nothing outside the
  project. The sandbox is a setting of the machine.
- The check tool reads Markdown in the form the templates use. A
  document in another form gets findings to read, not errors.
- Tried on Linux with Python 3. The tools use the standard library only.

## Tests

```
python3 -m unittest discover -s tests -v
```
