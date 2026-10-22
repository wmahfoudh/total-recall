# Total Recall

**Total Recall** is a skill that gives a project a memory: a folder of plain documents inside the project, read by a session at its start and updated at its close. A session opens with where the project is, what was decided and how you like to work, read from the folder, not from the code or from you.

The folder is named `internal-<project-name>`, after the project's folder. At the install, the skill asks whether git should ignore it.

This project uses `/total-recall`, the `internal-total-recall/` folder is left public on purpose as a demo of how a real implementation looks like.

## What it installs

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents, the internal folder |
| `state.md` | The snapshot: the position, what was done this session, what comes next, what waits on the user |
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
| `records/` | One-off records, numbered: a pasted log, a study, a spec written by a skill |
| `tools/` | Three scripts: the start, the check of the documents, the check of the machine |
| `memory/` | The memory notes of the project and their index |
| `backup/` | The archives of the folder, made by `/total-recall backup` and before each update, listed in its README |

## Adapt the templates

The templates in `skill-claude/templates/` are written for one way of working. Read them after your first install, and change what does not fit:

- `rules.md`: the rules on writing, working with the user, verification and agents.
- `memory/user-writing-style.md`: the author's style, as an example. Describe your own here.
- `CLAUDE.template.md`: the project file, written as `CLAUDE.md` at the install, with the phrases of the sessions and the size read at each start.
- `close.md` and `review.md`: the close routine and the review of the memory.
- `lifecycle.md`: phases, tasks and steps, and their numbers.

A change in `skill-claude/templates/` applies to the projects installed after it. A change in the internal folder of a project applies to that project only.

## How a session works

You open the session with "let's start". Claude reads the snapshot, the memory notes, the head of the plan and the current task of the open phase, not the whole files. Claude Code loads the project file and the rules by itself. Then Claude gives a briefing: where the project is, what the last session did, what comes next, what waits on you. Then it waits for your go.

During the session, the work follows the open phase, a task at a time. A small fact with an obvious place is written as the work goes: a ticked step, a decision, a Roadmap item. A text for a file read at each start, or a change to something already written, is proposed to you first, at a pause in the work.

"let's close" runs the close routine:

- the proposals held during the session are asked;
- the snapshot is rewritten, the phase file checked, the code map updated, the Roadmap cleared of the items that opened;
- an entry goes in the history and in the story;
- the project file is reread against the project, and the documents are checked by the tool;
- the review is suggested when a phase closes.

## The review of the memory

Requirements change. After a few months, the documents of a project can contradict each other. "review the memory" reads the whole folder and writes a report: contradictions, duplicates, text out of date, text in the wrong place, replaced decisions. Each item gives the current text, the proposed text and the reason.

The review also takes in what was decided in the current session and is not written yet, such as a new rule or a correction. The memory notes are checked too: a rule in a note is checked where it applies, across the repository for a rule about the repository. Nothing is applied before you approve it by number.

`/total-recall update` brings a folder made by an older version of the skill to the current form. The skill shows the plan and asks one yes, makes a backup, replaces the routine files, numbers the decisions and renames the phase files of the older form, then offers the review.

## The plan

The work is in phases, tasks and steps. Phases count from 01, tasks from 1 across the phases, steps inside a task. A phase is a file, `phases/P01-<name>.md`. The project always has an open phase: each piece of work has its place in one. The rules are in `lifecycle.md` of the folder.

## Install the skill

The skill has two forms: `skill-claude/` for Claude Code, and `skill-pi/` for Pi, with its own README. Link the Claude Code form into the skills folder of Claude Code, from the root of this repository:

```
mkdir -p ~/.claude/skills && ln -s "$(pwd)/skill-claude" ~/.claude/skills/total-recall
```

A copy (`cp -r skill-claude ~/.claude/skills/total-recall`) works too. It is not updated when this repository changes.

## Use it on a project

1. In the project folder, run `git init` if the folder is not a repository yet.
2. Start Claude Code at the root of the repository and type `/total-recall`.
3. Answer the five questions. Read the description the skill writes, and correct it until it is right.
4. Say whether git should ignore the folder, for example when the repository is public. On a yes, run the line the skill hands over, then `git status`: nothing of the folder shows.
5. Read the machine table. When a guardrail is missing, the skill proposes the lines to run.
6. Open the first session with "let's start".

## Commands

The skill starts only when you type `/total-recall`, with `update` or `backup` after it when needed. Claude does not start it on its own (`disable-model-invocation: true` in `SKILL.md`). A request in plain words, such as "set up the documentation", does nothing, and the documents of a project kept another way are left alone. With the same setting, the description of the skill enters the context only when you type the command. The skill costs no tokens in a session that does not use it.

| Where you type it | What happens |
|---|---|
| `/total-recall` in a repository without an internal folder | The install: five questions, the description to approve, the folder written, the git question, the machine check |
| `/total-recall` in a repository with another documentation system, such as a root `CLAUDE.md` or `AGENTS.md`, or a `memory-bank/` folder | Nothing is written. The skill names the files it found and the way to move to total recall: move them out of the project, install, then bring them in through a session of questions |
| `/total-recall` in a repository that has the folder | The check: the exclusion line, the machine, what an update would change, then the offer of the review |
| `/total-recall update` | The plan of the update, one yes, a backup ending in `-auto`, then the missing files added, the routine files replaced, the decisions numbered and the phase files of the older form renamed. The project's own content is not changed |
| `/total-recall backup` | An archive of the folder in `backup/`, ending in `-manual` |

The phrases below are defined by the project file. They work in a session that has read the folder, with or without the skill installed.

| Phrase | What happens |
|---|---|
| "let's start", "let's continue", "let's resume" | The start routine: the folder read, the briefing, then Claude waits for your go |
| "let's close", "docs routine", "documentation routine", "sync the docs" | The close routine: the proposals held during the session, the snapshot, the history, the story, the check |
| "review the memory" | The review: a report under `records/`, nothing changed before your answer by number |

## Check it

1. On a yes at step 4, `git status` shows nothing from the internal folder.
2. A new session opened with "let's start" gives the briefing, with Phase 01 open and Task 1 next.
3. "let's close" rewrites `state.md` and adds an entry at the top of `history.md`.

## On another machine

Install the skill, open the project, and start the session with "let's start". The phrase works through a line in the global rules file, `~/.claude/CLAUDE.md`, that names `internal-<project-name>/CLAUDE.md`. The install proposes the line when it is missing. Without the line, the first message of a session is "read `internal-<project-name>/CLAUDE.md`", and the phrases work from there. The rules are in the folder: the session follows them with or without a global file.

The machine check, `tools/machine-check.py` of the folder, says which guardrails the machine has: the global rules file, the start phrases line, the permission deny list, the guard hooks, `jq`, the sandbox.

The deny list and the three guard scripts are under `skill-claude/machine/`. The skill proposes them when they are missing.

## The guardrails

The guardrails stop a session from writing where it should not. A deny list of permissions refuses git writes, sudo, the destructive tools, the SSH keys and the shell startup files. Two hook scripts, with a library they share, read each command before it runs and refuse git and GitHub writes, forced and recursive deletes, and writes into `.git`. Claude Code applies them from `~/.claude/settings.json`. The scripts need `jq`.

## Why does the skill use scripts?

Small Python scripts write the folder, print the start and check the documents. Claude does the rest. A script gives the same result at each run and costs few tokens. On the project I built the skill on, a check of the documents by Claude would read the whole folder, more than 20,000 words. The script does the same check in one command, and prints one line when the folder is clean. The scripts make a backup of the folder before they replace a file. They use the standard library of Python only.

## Limits

- When git ignores the folder, the folder has no history. `/total-recall backup` writes an archive of it in `backup/`. Old archives are deleted by hand.
- The skill writes nothing under `.claude/` and nothing outside the project. The sandbox is a setting of the machine.
- The check tool reads Markdown in the form the templates use. A document in another form gets findings to read, not errors.
- Tested on Linux with Python 3 (for the moment).

## Tests

```
python3 -m unittest discover -s tests -v
```
