---
name: total-recall
description: Sets up a persistent memory for a project in an internal folder, checks an existing one and brings it to the current form. Each Claude Code session then knows what was done and what comes next. Run it by typing /total-recall, to install the memory in a repository or to check and update an existing one.
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

`internal-<project-name>/`, where `<project-name>` is the name of the
project's folder:

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines. Its first line imports `rules.md` |
| `rules.md` | The rules for every project: writing, working with the user, verification, agents, the internal folder |
| `state.md` | The snapshot: position, done this session, next, waiting on the user |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase: the preamble, the order, the tasks with their steps. Phase 01 is written at the install |
| `history.md` | The session log, newest first |
| `story.md` | The diary in the user's voice, appended at the end |
| `decisions.md` | The decisions in force, numbered, newest first |
| `obsolete.md` | The decisions replaced by a newer one, with the number of the one that replaced them |
| `close.md` | The close routine |
| `review.md` | The review of the memory |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree |
| `records/` | One-off records, listed in its README |
| `tools/` | `start.py`, which prints what a session reads at its start, `doc-check.py`, which checks the documents, and `machine-check.py`, which reports the guardrails of the machine, with a README |
| `memory/` | The memory notes of the project and their index |
| `backup/` | The archives of the folder, made by `/total-recall backup` and before each update, listed in its README |

## The commands

The words after `/total-recall` choose what the skill does:

| Command | What it does |
|---|---|
| `/total-recall` | The install in a repository without the folder, steps 1 to 9. In a repository that has the folder, the check of step 2 |
| `/total-recall backup` | The backup below, then stop |
| `/total-recall update` | The update below, then stop |

**The backup.** Run step 1 and the check of the first line in step 2,
then:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/update.py" backup --target "internal-<project-name>"
```

Show the `backup` line. No question is asked: the archive adds a file
and changes nothing else.

**The update.** Run step 1 and the check of the first line in step 2,
then show the plan:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/update.py" plan --target "internal-<project-name>"
```

For each `replace` line, read the difference with the template and say
in one line what changed. Then ask one question: "Apply the update,
yes or no?" On a yes:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/update.py" apply --target "internal-<project-name>"
```

The script makes a backup ending in `-auto` first, then adds the
missing files, replaces the routine files and migrates the decisions.
Show its lines. A `needs answers:` line names a missing file of the
project's own content, which is written by hand from what the folder
holds. Then offer "review the memory".

## 1. The ground

Check that the working directory is the root of a git repository. In
a worktree or a submodule `.git` is a file, so the check asks git:

```
test "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" && echo repository || echo "not the root of a repository"
```

When the line reads `not the root of a repository`, stop. Tell the user
that nothing was written, and to open the session at the root of the
repository, or to run `git init` in the project folder when it has no
repository yet.

The folder name is the last part of the working directory
(`basename "$PWD"`). The internal folder is `internal-<project-name>`,
with the name kept as it is, spaces and capitals included.

Then look for another documentation system at the root of the project:

```
for f in CLAUDE.md CLAUDE.local.md AGENTS.md .claude/CLAUDE.md memory-bank; do test -e "$f" && echo "found: $f" || true; done
```

When a line reads `found:`, the project has another documentation
system, and the skill does not change it. Stop, and tell the user in
one message that nothing was written, which files were found, and the
way to move to total recall:

1. Move these files out of the project. Claude Code also loads a
   `CLAUDE.md` found in a subfolder, so a move inside the project keeps
   it in use.
2. Run `/total-recall` again to install the memory.
3. Open a session with "let's start", give Claude the path of the old
   files, and ask it to bring them in. Claude reads them, asks questions,
   and proposes where each item goes, by the rule "When to ask before a
   write" of `rules.md`.

## 2. The mode

When `internal-<project-name>/` exists, first read the first line of
its project file:

```
head -n 1 "internal-<project-name>/CLAUDE.md"
```

The skill always writes `@rules.md` there. When the file is missing or
its first line is another, the folder
does not look like a total-recall folder. Stop, and tell the user that
nothing was written and that the skill does not change a folder it did
not write.

Otherwise, check the folder and stop:

1. Read the exclusion file, `cat "$(git rev-parse --git-path info/exclude)"`,
   and say whether the line `/internal-<project-name>/` is there, as
   information.
2. Run `python3 "internal-<project-name>/tools/machine-check.py"`, or the
   copy in `${CLAUDE_SKILL_DIR}/templates/tools/` when the folder has
   none, and show its table.
3. Show what an update would change:

   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/update.py" plan --target "internal-<project-name>"
   ```

   When it prints more than `nothing to update`, say that
   `/total-recall update` applies it with one yes, after a backup.

4. Offer the review of the content, "review the memory", which follows
   `review.md` of the folder.

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
name filled in, and the name of the phase file,
`phases/P01-<slug>.md`. Then ask one question:
"Keep the folder out of git, yes or no?" On a yes, show the line that
step 7 hands over. The answer is not written in any file. Wait for the
go.

## 6. The folder

Write the answers as JSON in the session scratchpad, with these keys:
`project` (the folder name), `internal` (`internal-<project-name>`), `date`
(today as DD/MM/YYYY, from `date +%d/%m/%Y`), `description`,
`constraints` (the list as Markdown lines, joined with newlines),
`phase1_name`, `phase1_slug`, `phase1_goal`, `task1_name`.

Then run:

```
python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --answers "<scratchpad>/answers.json" --target "internal-<project-name>"
```

The script writes each file that does not exist and keeps each one that
does, and prints a `wrote` or a `kept` line per file. Read the lines and
show them. It refuses to run, and writes nothing, when a placeholder has
no answer.

Then run the check and show its last line:

```
python3 "internal-<project-name>/tools/doc-check.py" "internal-<project-name>"
```

A fresh install reads `clean`.

## 7. The exclusion

Only when the user answered yes in step 5. On a no, go to step 8.

The line that keeps the folder out of git goes in the exclusion file,
`.git/info/exclude`, a file git never commits. In a worktree, git keeps
the file in the main repository, so the command asks git for its path.
A write into `.git` is the user's. Hand them the command:

```
printf '/internal-<project-name>/\n' >> "$(git rev-parse --git-path info/exclude)"
```

When they say it is done, read the file
(`cat "$(git rev-parse --git-path info/exclude)"`) and confirm the
line. Then ask them to run `git status` and to confirm that
nothing of the folder shows. Run no git command.

## 8. The machine

Run `python3 "internal-<project-name>/tools/machine-check.py"` and show the
table. Each row reads `present` or `missing`:

| Row | What it is |
|---|---|
| global rules file | `~/.claude/CLAUDE.md`, the user's rules for every project. The internal folder carries its own copy in `rules.md`. This row is information |
| start phrases | the line of the global rules file that names the project file, so that "let's start" finds the folder |
| deny list: git writes, sudo, destructive tools | permission patterns that refuse those commands to a session |
| guard hooks on Bash | scripts that read each command before it runs and refuse git writes, recursive deletes and writes into `.git` |
| jq | needed by the guard scripts |
| sandbox | a setting of the machine, left to the user |

For each missing row among the deny lists and the hooks, propose the fix
in one line. On the user's word, give the lines, and the user runs them.

When the start phrases row reads `missing`, propose the line below for
the end of `~/.claude/CLAUDE.md`, a new file if there is none. The user
adds it. Without the line, a session opens with "read
`internal-<project-name>/CLAUDE.md`".

```
In a project with a folder `internal-<project-name>/` at its root, "let's start", "let's continue" and "let's resume" mean: read `internal-<project-name>/CLAUDE.md` and run its start routine.
```

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
   `internal-<project-name>/`.
2. A new session, opened with "read
   `internal-<project-name>/CLAUDE.md`" (or with "let's start" where the
   global file has the line of step 8), gives the briefing: Phase 01 open, Task 1
   next.
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
- Change the project's own content in an update: the project file, the
  state, the plan, the phases, the history, the story, the notes, the
  text of the decisions.
