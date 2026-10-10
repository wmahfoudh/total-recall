# Total recall

**Total Recall** is a skill that initializes a living memory system for a project at creation. This avoids asking the expensive *explore the code* at each start of a session, explaining again where the project was, what was decided and how you like to work. It gives a project a folder of plain documents inside the project, which a session reads at its start and updates at its close with minimal cost.

The folder is named `internal-<project-name>`, after the project's folder. At the install, the skill asks whether git should ignore it.

## What it installs

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents |
| `state.md` | The snapshot: position, done this session, next, waiting on the user |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps |
| `history.md` | The session log, newest first |
| `story.md` | The diary of the project, a short story at each close |
| `decisions.md` | The decisions in force, numbered, newest first |
| `obsolete.md` | The decisions replaced by a newer one |
| `close.md` | The close routine |
| `review.md` | The review of the memory |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records: a pasted log, a study, a spec written by a skill |
| `tools/` | A check of the documents and a check of the machine |
| `memory/` | The memory notes of the project and their index |

## How a session works

The session opens with "let's start". It reads the project file, the rules, the snapshot and the memory notes, then the open phase, and gives a briefing: where the project is, what the last session did, what comes next, what waits on the user. Then it waits for the go.

During the session the work follows the open phase, a task at a time. Small facts with an obvious place are written as the work goes: a ticked step, a decision, a Roadmap item. A text that would go into a file read at each start, or that changes something already written, is proposed first, at a pause in the work.

"let's close" runs the close routine: the held proposals, the snapshot rewritten, the phase file checked, the Roadmap cleared, an entry in the history and in the story, the project file reread against the project, and the check tool run on the documents.

## The review of the memory

Requirements change. After a few months, the documents of a project can contradict each other. "review the memory" reads the whole folder and writes a report: contradictions, duplicates, text out of date, text in the wrong place, replaced decisions. Each item gives the current text, the proposed text and the reason. Nothing is applied before the user approves it by number.

A folder made by an older version of the skill is brought to the current form by `/total-recall` in that project. The skill shows what changed in the routine files, numbers the decisions, then offers the review.

## The plan

Work is in phases, tasks and steps. Phases count from 01, tasks from 1 across phases, steps inside a task. A phase is a file. The project always has an open phase, so each piece of work has a home. The rules are in `lifecycle.md` of the folder.

## Install the skill

The skill is the `skill/` folder of this repository. Link it, or copy it, into the skills folder of Claude Code:

```
ln -s "$(pwd)/skill" ~/.claude/skills/total-recall
```

A copy (`cp -r skill ~/.claude/skills/total-recall`) is not updated when this repository changes.

## Use it on a project

1. In the project folder, run `git init` if the folder is not a repository yet.
2. Start Claude Code there and type `/total-recall`.
3. Answer the five questions, read the description it writes, and correct it until it is right.
4. Say whether git should ignore the folder. On a yes, run the line the skill hands over, then `git status` to see that nothing of the folder shows.
5. Read the machine table. When a guardrail is missing, the skill proposes the lines to run.
6. Open the first session with "let's start".

## Commands

The skill has one command, and Claude does not start the skill on its own (`disable-model-invocation: true` in `SKILL.md`): you type `/total-recall`. A request in plain words, such as "set up the documentation", does not start it, so the skill does not change the documents of a project that keeps its documentation another way. The same setting keeps the description of the skill out of the context until you type the command, so the skill costs no tokens in a session that does not use it.

| Where you type it | What happens |
|---|---|
| `/total-recall` in a repository without an internal folder | The install: five questions, the description to approve, the folder written, the git question, the machine check |
| `/total-recall` in a repository that has the folder | The check and the update: the missing files named and the repair offered, the routine files compared with the templates, older decisions migrated in a copy, then the offer of the review |

The phrases are defined by the project file, so they work in a session that has read the folder, even with the skill uninstalled.

| Phrase | What happens |
|---|---|
| "let's start", "let's continue", "let's resume" | The start routine: the folder read, the briefing, then Claude waits for the go |
| "let's close", "docs routine", "documentation routine", "sync the docs" | The close routine: the proposals held during the session, the snapshot, the history, the story, the check |
| "review the memory" | The review: a report under `records/`, nothing changed before the answer by number |

## Check it

1. On a yes at step 4, `git status` shows nothing from the internal folder.
2. A new session opened with "let's start" gives the briefing, with Phase 01 open and Task 1 next.
3. "let's close" rewrites `state.md` and adds an entry at the top of `history.md`.

## On another machine

Install the skill, open the project, and start the session with "let's start". Claude Code knows the phrase from a global rules file, `~/.claude/CLAUDE.md`, that maps it to the project file. On a machine without that mapping, the first message of a session is "read `internal-<project-name>/CLAUDE.md`", and the phrases work from there. The rules are in the folder, and the session follows them without a global file. The machine check, `tools/machine-check.py` of the folder, says which guardrails the machine has: the permission deny list, the guard hooks, `jq`, the sandbox. The skill ships the deny list and the three guard scripts under `skill/machine/`, and proposes them when they are missing.

## The guardrails

The guardrails keep a session from writing where it should not: a deny list of permissions (git writes, sudo, the destructive tools) and two hook scripts, with a library they share, that read each command before it runs and refuse git writes, recursive deletes and writes into `.git`. Claude Code applies them from `~/.claude/settings.json`. The scripts need `jq`.

## Why does the skill use scripts?

The skill writes the folder and checks it with small Python scripts, and Claude does the rest. The scripts give the same result at each run, and they cost few tokens. On the project used to build the skill, if Claude checked the documents itself, it would read about 14,000 words, around 18,000 tokens. The script does the same check in one command, and prints one line when the folder is clean. The scripts also refuse to overwrite a file, which matters for an uncommitted folder. They use the standard library only.

## Limits

- When git ignores the folder, the folder has no history and no backup. Keep a copy of it yourself.
- The skill writes nothing under `.claude/` and nothing outside the project. The sandbox is a setting of the machine.
- The check tool reads Markdown in the form the templates use. A document in another form gets findings to read, not errors.
- Tested on Linux with Python 3 (for the moment). The tools use the standard library only.

## Tests

```
python3 -m unittest discover -s tests -v
```
