# Total Recall

**Total Recall** is a skill that initializes a living memory system for a project, new or existing. A session then starts without exploring the code again, and without you explaining where the project was, what was decided and how you like to work. It gives a project a folder of plain documents that a session selectively reads at its start and updates at its close with minimal cost.

The folder is named `internal-<project-name>`, after the project's folder. At the install, the skill asks whether git should ignore it.

## What it installs

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents, the internal folder |
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
| `tools/` | The script of the start, a check of the documents and a check of the machine |
| `memory/` | The memory notes of the project and their index |
| `backup/` | The archives of the folder, made by `/total-recall backup` and before each update, listed in its README |

## Adapt the templates

The templates in `skill/templates/` are a starting point, written for one way of working. Read them after the install of your first project, and change them if needed:

- `rules.md`: the rules on writing, working with the user, verification and agents.
- `memory/user-writing-style.md`: the author's style, as an example. Describe your own style here.
- `CLAUDE.template.md`: the project file, written as `CLAUDE.md` at the install, with the phrases of the sessions and the size read at each start.
- `close.md` and `review.md`: the close routine and the review of the memory.
- `lifecycle.md`: phases, tasks and steps, and their numbers.

A change in `skill/templates/` applies to the projects installed after it. A change in the internal folder of a project applies to that project only.

## How a session works

The session opens with "let's start". Claude runs a script that prints the snapshot, the memory notes, the head of the plan and the current task of the open phase, so that it does not read whole files. Claude Code loads the project file and the rules by itself. Then Claude gives a briefing: where the project is, what the last session did, what comes next, what waits on the user. Then it waits for the go.

During the session the work follows the open phase, a task at a time. Small facts with an obvious place are written as the work goes: a ticked step, a decision, a Roadmap item. A text that would go into a file read at each start, or that changes something already written, is proposed first, at a pause in the work.

"let's close" runs the close routine: the held proposals, the snapshot rewritten, the phase file checked, the code map updated, the Roadmap cleared, an entry in the history and in the story, the project file reread against the project, the check tool run on the documents, and the review suggested when a phase closes.

## The review of the memory

Requirements change. After a few months, the documents of a project can contradict each other. "review the memory" reads the whole folder and writes a report: contradictions, duplicates, text out of date, text in the wrong place, replaced decisions. Each item gives the current text, the proposed text and the reason. 

The review also takes in what was decided in the current session and is not written yet, such as a new rule or a correction. The memory notes are checked too, and a rule in a note is checked where it applies, across the repository for a rule about the repository. Nothing is applied before the user approves it by number.

A folder made by an older version of the skill is brought to the current form by `/total-recall update` in that project. The skill shows the plan and asks one yes, makes a backup, updates the routine files and numbers the decisions, then offers the review.

## The plan

Work is in phases, tasks and steps. Phases count from 01, tasks from 1 across phases, steps inside a task. A phase is a file. The project always has an open phase, so each piece of work has a home. The rules are in `lifecycle.md` of the folder.

## Install the skill

The skill is the `skill/` folder of this repository. Link it, or copy it, into the skills folder of Claude Code. From the root of this repository:

```
mkdir -p ~/.claude/skills && ln -s "$(pwd)/skill" ~/.claude/skills/total-recall
```

A copy (`cp -r skill ~/.claude/skills/total-recall`) is not updated when this repository changes.

## Use it on a project

1. In the project folder, run `git init` if the folder is not a repository yet.
2. Start Claude Code at the root of the repository and type `/total-recall`.
3. Answer the five questions, read the description it writes, and correct it until it is right.
4. Say whether git should ignore the folder, for example to keep the memory of the project out of a public repository. On a yes, run the line the skill hands over, then `git status` to see that nothing of the folder shows.
5. Read the machine table. When a guardrail is missing, the skill proposes the lines to run.
6. Open the first session with "let's start".

## Commands

The skill starts only by its command, `/total-recall`, with an optional word, `update` or `backup`. Claude does not start it on its own (`disable-model-invocation: true` in `SKILL.md`). A request in plain words, such as "set up the documentation", does not start it, so the skill does not change the documents of a project that keeps its documentation another way. The same setting keeps the description of the skill out of the context until you type the command, so the skill costs no tokens in a session that does not use it.

| Where you type it | What happens |
|---|---|
| `/total-recall` in a repository without an internal folder | The install: five questions, the description to approve, the folder written, the git question, the machine check |
| `/total-recall` in a repository with another documentation system, such as a root `CLAUDE.md` or `AGENTS.md`, or a `memory-bank/` folder | Nothing written: the files found are named, with the way to move to total recall: move them out of the project, install, then bring them in through a session of questions |
| `/total-recall` in a repository that has the folder | The check: the exclusion line, the machine, what an update would change, then the offer of the review |
| `/total-recall update` | The plan of the update, one yes, a backup ending in `-auto`, then the missing files added, the routine files replaced and the decisions numbered. The project's own content is not touched |
| `/total-recall backup` | An archive of the folder in `backup/`, ending in `-manual` |

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

Install the skill, open the project, and start the session with "let's start". The phrase works with a line in the global rules file, `~/.claude/CLAUDE.md`, that names `internal-<project-name>/CLAUDE.md`. The install proposes the line when it is missing. On a machine without the line, the first message of a session is "read `internal-<project-name>/CLAUDE.md`", and the phrases work from there. The rules are in the folder, and the session follows them without a global file.

The machine check, `tools/machine-check.py` of the folder, says which guardrails the machine has: the global rules file, the start phrases line, the permission deny list, the guard hooks, `jq`, the sandbox.

The skill ships the deny list and the three guard scripts under `skill/machine/`, and proposes them when they are missing.

## The guardrails

The guardrails keep a session from writing where it should not: a deny list of permissions (git writes, sudo, the destructive tools, the SSH keys and the shell startup files) and two hook scripts, with a library they share, that read each command before it runs and refuse git and GitHub writes, forced and recursive deletes, and writes into `.git`. Claude Code applies them from `~/.claude/settings.json`. The scripts need `jq`.

## Why does the skill use scripts?

The skill writes the folder, prints the start and checks the documents with small Python scripts, and Claude does the rest. The scripts give the same result at each run, and they cost few tokens. On the project used to build the skill, if Claude checked the documents itself, it would read the whole folder, more than 20,000 words. The script does the same check in one command, and prints one line when the folder is clean. The scripts also make a backup of the folder before they replace a file. They use the standard library only.

## Limits

- When git ignores the folder, the folder has no history. `/total-recall backup` writes an archive of it in `backup/`, and old archives are deleted by hand.
- The skill writes nothing under `.claude/` and nothing outside the project. The sandbox is a setting of the machine.
- The check tool reads Markdown in the form the templates use. A document in another form gets findings to read, not errors.
- Tested on Linux with Python 3 (for the moment). The tools use the standard library only.

## Tests

```
python3 -m unittest discover -s tests -v
```
