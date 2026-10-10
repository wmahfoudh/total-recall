---
name: total-recall
description: Sets up a persistent memory for a project in an internal folder, checks an existing one and brings it to the current form. Each Claude Code session then knows what was done and what comes next. Use when the user types /total-recall, or asks to set up, install, check, repair or update the project memory, the internal folder or total recall on a repository.
disable-model-invocation: true
---

# Total recall

The user works on a project with Claude Code over many sessions, and
each session needs to know what was done before and what comes next.
This skill installs a memory for that inside the project: a folder of
plain documents that a session reads at its start and updates at its
close.

Run the steps below in order. Each one says what to do, what to show the
user, and where to stop. The user runs every command that writes to git
or outside the project.

## What it installs

`internal-<folder>/`, where `<folder>` is the name of the project's
folder:

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines. Its first line imports `rules.md` |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents, the internal folder |
| `state.md` | The snapshot: position, done this session, next, waiting on the user |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps. Phase 01 is written at the install |
| `history.md` | The session log, newest first |
| `story.md` | The diary in the user's voice, appended at the end |
| `decisions.md` | Dated decisions, appended at the end |
| `close.md` | The close routine |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records, listed in its README |
| `tools/` | `doc-check.py`, which checks the documents, and `machine-check.py`, which reports the guardrails of the machine, with a README |
| `memory/` | The memory notes of the project and their index |

## 1. The ground

Check that the working directory is the root of a git repository:

```
test -d .git && echo repository || echo "no .git here"
```

When there is no `.git`, stop. Tell the user to run `git init` in the
project folder first, and that nothing was written.

The folder name is the last part of the working directory
(`basename "$PWD"`). The internal folder is `internal-<folder>`, with
the name kept as it is, spaces and capitals included.

## 2. The mode

When `internal-<folder>/` exists, check it and stop:

1. List the files of `${CLAUDE_SKILL_DIR}/templates/` against the
   internal folder, and name each one that is missing.
2. Read `.git/info/exclude` and say whether the line
   `/internal-<folder>/` is there, as information.
3. Run `python3 "internal-<folder>/tools/machine-check.py"`, or the
   copy in `${CLAUDE_SKILL_DIR}/templates/tools/` when the folder has
   none, and show its table.
4. Offer the repair, and run it on the user's word only:

   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --repair --target "internal-<folder>"
   ```

   It adds the files that need no answer (the rules, the routines, the
   tools, the code map, the records README) where they are missing,
   keeps every existing file, and prints `needs answers:` for each
   missing file that the install writes from the user's answers (the
   project file, the snapshot, the plan, a phase file, the history, the
   story, the decisions, the memory note, the tools README). Those are
   written by hand from what the folder already holds, never a second
   phase file: the existing phase files keep their numbers.

Then stop. The steps that follow are for a fresh install.

## 3. The questions

Ask these in one message, numbered. Say that short answers are enough
and that everything can be changed later.

1. What is the project: what does it do, and for whom?
2. What is it made of: the language or the stack, where the code or the
   documents live, and the command that checks it, if any?
3. How is it delivered: a public repository, releases, pages? What must
   stay internal?
4. What is the first phase: what does it deliver, and what is its first
   task?
5. What must a session know before touching the project: rules,
   constraints, things not to do?

## 4. The description

From the answers, write:

- the description of the project, about 100 words, in the user's voice:
  what it is, for whom, what it is made of, how it is delivered;
- the constraints as a list, one line each: the kind of project, the
  check command, what stays internal, each rule the user gave;
- the first phase: its name, its goal in a sentence, and the name of its
  first task. The slug of the phase is its name in lowercase with
  hyphens, for the file name.

Show all of it and ask the user to approve or correct it. Nothing is
written before the approval. Apply each correction and show the result
again, until the user says it is right.

## 5. The list and the go

Show the files that will be written: the table above with the folder
name filled in. Then ask one question:
"Keep the folder out of git, yes or no?" On a yes, show the line that
step 7 hands over. The answer is not written in any file. Wait for the
go.

## 6. The folder

Write the answers as JSON in the session scratchpad, with these keys:
`project` (the folder name), `internal` (`internal-<folder>`), `date`
(today as DD/MM/YYYY, from `date +%d/%m/%Y`), `description`,
`constraints` (the list as Markdown lines, joined with newlines),
`phase1_name`, `phase1_slug`, `phase1_goal`, `task1_name`.

Then run:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --answers "<scratchpad>/answers.json" --target "internal-<folder>"
```

The script writes each file that does not exist and keeps each one that
does, and prints a `wrote` or a `kept` line per file. Read the lines and
show them. It refuses to run, and writes nothing, when a placeholder has
no answer. Nothing is overwritten, because git cannot bring a file of
this folder back.

Then run the check and show its last line:

```
python3 "internal-<folder>/tools/doc-check.py" "internal-<folder>"
```

A fresh install reads `clean`.

## 7. The exclusion

Only when the user answered yes in step 5. On a no, go to step 8.

The line that keeps the folder out of git goes in `.git/info/exclude`,
a file git never commits. A write into `.git` is the user's. Hand them
the command:

```
printf '/internal-<folder>/\n' >> .git/info/exclude
```

When they say it is done, read the file (`cat .git/info/exclude`) and
confirm the line. Then ask them to run `git status` and to confirm that
nothing of the folder shows. Run no git command.

## 8. The machine

Run `python3 "internal-<folder>/tools/machine-check.py"` and show the
table. Each row reads `present` or `missing`:

| Row | What it is |
|---|---|
| global rules file | `~/.claude/CLAUDE.md`, the user's rules for every project. The internal folder carries its own copy in `rules.md`. This row is information |
| deny list: git writes, sudo, destructive tools | permission patterns that refuse those commands to a session |
| guard hooks on Bash | scripts that read each command before it runs and refuse git writes, recursive deletes and writes into `.git` |
| jq | needed by the guard scripts |
| sandbox | a setting of the machine, left to the user |

For each missing row among the deny lists and the hooks, propose the fix
in one line. On the user's word, give the lines, and the user runs them.

When `~/.claude/settings.json` does not exist:

```
cp "${CLAUDE_SKILL_DIR}/machine/settings-guardrails.json" ~/.claude/settings.json
```

When it exists, print the `permissions` block and the `hooks` block of
`${CLAUDE_SKILL_DIR}/machine/settings-guardrails.json` and ask the user
to add them to their file. A `permissions.deny` list that exists gets
the patterns appended.

The scripts:

```
mkdir -p ~/.claude/hooks && cp "${CLAUDE_SKILL_DIR}/machine/hooks/"*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh
```

The guard scripts need `jq`. Without it they refuse every command, so
when `jq` is missing, the user installs it first with their package
manager, before the hooks.

After the user has run the lines, run the check again and show the
table.

## 9. The scenario and the next step

End with the scenario, numbered, for the user to try:

1. On a yes in step 5, `git status` shows nothing from
   `internal-<folder>/`.
2. A new session, opened with "read internal-<folder>/CLAUDE.md" (or
   with "let's start" where a global file maps it), gives the briefing:
   Phase 01 open, Task 1 next.
3. "let's close" rewrites `state.md` and adds the entry at the top of
   `history.md`.

Then the next step in one line: open the first session with "let's
start" and design Task 1 with the user.

## What this skill never does

- Run a git command that writes. The exclusion line and every commit
  are the user's.
- Write under `.claude/`, of the project or of the home.
- Write outside the project, apart from the answers file in the session
  scratchpad. The machine lines are handed over, not run.
- Overwrite an existing file. The render keeps what exists.
