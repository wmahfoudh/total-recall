# Total recall for Pi

This folder is the Pi form of the total-recall skill. It installs a
memory for a project: a folder of plain documents that a session reads
at its start and updates at its close, so the next session knows what
was done and what comes next.

The skill is the same idea as the Claude Code form in `../skill-claude`, with
the parts that belong to Pi:

- the command is `/skill:total-recall`, and the words after it choose
  the mode;
- the global rules file is `~/.pi/agent/AGENTS.md`;
- the project file of the memory is `AGENTS.md`, Pi's own context file
  name;
- the guardrails are memory notes, read at the start of every session,
  in place of the settings deny list and the three shell hooks.

## The one difference to know

Claude Code loads a `CLAUDE.md` found in a subfolder when a session
reads a file in that folder. Pi loads context files only from the agent
directory and the ancestors of the working directory, never from a
subfolder. The memory therefore opens in one of two ways:

1. The phrase "let's start" works through a line in
   `~/.pi/agent/AGENTS.md` that the install proposes.
2. Without that line, the session opens with "read
   `internal-<project-name>/AGENTS.md` and
   `internal-<project-name>/rules.md`".

Both are described in `SKILL.md`, step 8.

## Install the skill

Link it, or copy it, into the skills folder of Pi:

```
mkdir -p ~/.pi/agent/skills && ln -s "$(pwd)/skill-pi" ~/.pi/agent/skills/total-recall
```

A copy is not updated when this repository changes.

## Use it

1. In the project folder, run `git init` if it is not a repository yet.
2. Start Pi at the root of the repository and type
   `/skill:total-recall`.
3. Answer the five questions, read the description it writes, and
   correct it until it is right.
4. Say whether git should ignore the folder.
5. Read the machine table. The skill proposes the line for
   `~/.pi/agent/AGENTS.md` when the start phrases are missing.
6. Open the first session with "let's start".

## Commands

| Command | What happens |
|---|---|
| `/skill:total-recall` | The install in a repository without the internal folder. In one that has it, the check |
| `/skill:total-recall update` | The plan of the update, one yes, a backup, then the routine files replaced and the decisions numbered |
| `/skill:total-recall backup` | An archive of the folder in `backup/`, ending in `-manual` |

The phrases below are defined by the project file, so they work in a
session that has read the folder, even with the skill uninstalled.

| Phrase | What happens |
|---|---|
| "let's start", "let's continue", "let's resume" | The start routine: the folder read, the briefing, then Pi waits for the go |
| "let's close", "docs routine", "documentation routine", "sync the docs" | The close routine |
| "review the memory" | A report under `records/`, nothing changed before the answer by number |

## The guardrails are memory notes

`memory/guardrails.md` ships in `templates/`, is written into every
folder, and is read whole at the start of every session. It lists the
commands a session never runs: git and GitHub writes, `sudo`, recursive
or forced deletes, block devices, and the paths kept out (`.git`,
`/etc`, `~/.ssh`, `~/.gnupg`, shell startup files and the Pi credential
store). The full rules are in `rules.md`, "Who runs what" and "The
internal folder".

Pi has no settings deny list and the skill installs no extension, so
these are instructions the session follows, not a program that stops a
command. The sandbox row of the machine table stays information: run Pi
in a container when a session needs isolation.

## The scripts

- `scripts/render.py` writes the folder from the templates of
  `templates/`.
- `scripts/update.py` backs up the folder and brings an older one to
  the current form.
- The folder it writes carries `tools/start.py`, which prints what a
  session reads at its start, `tools/doc-check.py`, which checks the
  documents, and `tools/machine-check.py`, which reports the guardrails
  of the machine.

They use the standard library of Python 3 only.

## Limits

- Pi has no built in sandbox. The machine check reports this as
  information; run Pi in a container when a session needs isolation.
- The skill writes nothing under `.pi/`, of the project or of the agent
  directory.
- `tools/doc-check.py` reads Markdown in the form the templates use. A
  document in another form gets findings to read, not errors.
