# Total recall: the design

Written 07/10/2026 from the analysis of the the reference project memory system and the
decisions of the session. This is the spec of the `/total-recall` skill
and of the memory system it installs.

## What it is for

A project worked on with Claude Code over many sessions needs each
session to know what was done before and what comes next. The memory
system is a folder of plain documents inside the project, kept out of
git, that a session reads at its start and updates at its close. The
skill installs that folder on any project in one run.

Who uses it: the user, on their own projects, on any machine where
Claude Code runs. Success is judged on four points:

1. A new session, opened with "let's start" or with "read
   internal-<folder>/CLAUDE.md", gives a correct briefing from the files
   alone: the position, the last session, what comes next, what waits on
   the user.
2. Nothing of the folder appears in `git status`, and nothing in the
   repository names Claude or the folder's content. The folder name is
   the only trace, and it is abstract.
3. A close leaves the documents consistent: the check tool reports
   nothing, and every piece of work of the session sits under a numbered
   task.
4. The skill installs on a fresh repository in one run, from the user's
   answers, and installs nothing outside the project without the user's
   word.

## What exists

The reference is `<the reference folder>/`, read only. What it does well
is kept: one owner per fact, a start that reads little and ends with a
briefing and a wait, a close that rewrites the snapshot and rereads the
instruction file against the project, memory notes with a why and a how
to apply, the task form, continuous task numbers, dates as DD/MM/YYYY,
the story in the user's voice.

What is changed, with the reason, is in the section "What changes from
the reference project" at the end.

## The folder

Everything lives under `internal-<folder>/` at the root of the
repository, where `<folder>` is the name of the project's folder
(`internal-total-recall` for `~/code/total-recall`). One line in
`.git/info/exclude`, `/internal-<folder>/`, keeps it out of git. That
file is never committed, which is why `git init` is the only
prerequisite. No file is written under `.claude/`, and no setting of
the machine is needed.

| File | What it holds |
|---|---|
| `CLAUDE.md` | The project file: the description, the table of documents, the sessions, the phases, the project's own routines, what the project adds to the rules. Its first line imports `rules.md` |
| `rules.md` | The portable rules, the same text in every project: writing, working with the user, verification, agents. A project adds to it in `CLAUDE.md` and does not edit it |
| `state.md` | The snapshot: position, done this session, next, waiting on the user. Under about 150 lines |
| `plan.md` | The goal, the constraints, the Roadmap, Parked, Blocked |
| `phases/` | One file per phase, `phase-NN-<name>.md`: the preamble, the order, the tasks with their steps |
| `history.md` | The session log, newest first, an entry per session |
| `story.md` | The diary in the user's voice, appended at the end, skipped when there is nothing to tell |
| `decisions.md` | Dated decisions, appended at the end: what was decided, on whose word, why |
| `close.md` | The close routine |
| `lifecycle.md` | Phases, tasks and steps, their numbers, the opening and the close of a phase |
| `code-map.md` | Where the work of each phase is in the tree, for a code project |
| `records/` | One-off records (a pasted log, a study, a spec written by a skill), listed in `records/README.md` |
| `tools/` | The project's own scripts, listed in `tools/README.md`. Seeded with `doc-check.py` and `machine-check.py` |
| `memory/` | `MEMORY.md` and the notes, in the format of Claude Code's memory, read whole at the start |

Claude Code loads `internal-<folder>/CLAUDE.md` by itself as soon as a
session reads a file in that folder, as it does for any folder with
such a file. On this machine the global file maps "let's start" to the
routine of the project file. Anywhere else, "read
internal-<folder>/CLAUDE.md" is enough: the file says in its first lines
that reading it at the start of a session runs the start routine.

## The sessions

### The start

On "let's start", "let's continue", "let's resume", or when the project
file is read at the start of a session:

1. Read `CLAUDE.md` whole, with `rules.md`, then `state.md`, then
   `memory/MEMORY.md` and each note whole.
2. In `plan.md`, read the goal and the head of the Roadmap. In the open
   phase file, named in `state.md`, read the preamble and the current
   task, not the whole phase.
3. Give the briefing in a few sentences: the position, what the last
   session did, what comes next, what waits on the user. Then wait for
   the go and do not start the work.
4. If the folder is missing, say so and name `/total-recall`.

### During the session

- The work follows the open phase file, a task at a time. All the work
  of a session sits under a numbered task, the tools and the documents
  too. A task opens with what it does and why, before any step.
- A step is ticked with its date the moment it is done, with a line on
  what happened, so the phase file is always current.
- A correction from the user becomes a memory note the moment it is
  given, or updates the note on that topic.
- A document is edited mid-session only when a decision makes it wrong.
  A decision is appended to `decisions.md` when it is taken.
- The project's own routines are named in `CLAUDE.md` and read when
  they apply.
- A spec or a plan written by a skill is saved under `records/`, and
  its tasks become tasks of the open phase.

### The close

On "let's close", "docs routine", "documentation routine" or "sync the
docs". The routine runs without asking, and the user reviews the result.

1. Rewrite `state.md` as a snapshot: position, done this session, next,
   waiting on the user. Pointers to what other files record, not
   copies. Under about 150 lines.
2. In the open phase file, check that each piece of work of the session
   sits under a numbered task with its steps ticked. Work that no task
   planned is grouped into a few numbered tasks by the rules of
   `lifecycle.md`. For a code project, add an entry per delivered task
   that touched code to `code-map.md`, with the commit it describes.
3. Clear the Roadmap of what was delivered in full.
4. Add the entry at the top of `history.md`: `# DD/MM/YYYY - <name>`, a
   line of description, then short bullets of what was done.
5. Append a dated entry to `story.md` in the user's voice, the size of
   a social media post, about the debates, decisions and wrong turns of
   the session. Skip it when the session gave nothing to tell.
6. Run the project's own close steps, listed in `CLAUDE.md` under the
   project's routines. Empty at install.
7. Read `CLAUDE.md` against the project, sentence by sentence, and the
   memory notes with it: the index keeps a line per note, a stale fact
   is fixed, a note that became wrong is deleted, notes on one topic are
   merged, and the folder stays around ten notes.
8. Run `tools/doc-check.py` and fix what it reports in the same close.

At a phase close, the close is the last task of the phase, and it ends
with the opening of the next phase (see the lifecycle).

## The plan and the numbers

### `plan.md`

- The goal: the approved description.
- The constraints: the kind of project, the check command, what must
  stay internal, the rules the user gave at install.
- The phases: a sentence that points at `phases/` and at the position
  line of `state.md`. No table: each phase file owns its dates and its
  status.
- The Roadmap, ordered: what comes next, each item a few lines with its
  reason and its size. An item becomes a phase or a task when it opens,
  and leaves the Roadmap when it is delivered.
- Parked: asks set aside, each with the condition for its return.
- Blocked: what waits on something outside, with what it waits for.

### A phase file

`phases/phase-NN-<name>.md`, where NN has two digits and `<name>` is a
short lowercase name with hyphens:

- `# Phase NN: <name>`, then the preamble: opened DD/MM/YYYY on whose
  word, what the phase is for, its rules, and the order of its tasks as
  a numbered list.
- `### The opening of the phase`: the project's own steps (a branch, a
  version). Empty when the project has none.
- `### Task N: <name>`, one per task, in the task form:
  - "What it does and why", a short paragraph.
  - For code, the files and the interfaces at its opening.
  - `**The steps:**`, each `- [ ] **Step K: <name>** <what the step
    does>`. A done step reads `- [x]` and ends with `Done DD/MM/YYYY:`
    and what happened.
  - What was found on the way, under the task.
  - The suggested git line.
- `**Checkpoint for the phase:**` at the end, then the close paragraph
  when the phase closes: the date, what was delivered, what stays open.

### The numbers

- Phases count from 1 across the project. Tasks count from 1 across
  phases, in the order they are done. Steps count inside a task.
- A task has its number from the moment it is written in a phase file.
  A planned task's number appears in its phase file only, until it
  starts. A delivered task's number never changes and may appear
  anywhere.
- A new task takes the next number. When it is done before planned
  tasks that have not started, it takes its place before them, and
  those are renumbered in the phase file the same day.
- Work that no task planned (the tools, the documents, a rule) is
  recorded as tasks too, grouped into a few that represent the work.
- A check that is run again is a new task with a new number.
- The close is the last task of the phase.

### The lifecycle

- The project always has an open phase. The close of a phase opens the
  next one, named from the head of the Roadmap; the user can rename it.
  Every piece of work is a task at its place in time.
- A phase opens with a number, a name, a file, and the project's own
  opening steps.
- A phase closes when each task is delivered, the project's own checks
  pass, and the close routine has run.
- Asks and ideas collect in the Roadmap until a phase takes them.

## The rules file

`rules.md` is one file, the same in every project, written once in the
skill's templates. Its sources, consolidated and with every reference to
the reference project or to this machine removed:

- The user's global file, `~/.claude/CLAUDE.md`: writing (plain
  language, how the user writes, prose tics, punctuation, markdown,
  comments and documentation, product text, git messages), working with
  the user (who runs what, one step at a time, sessions, opinions,
  reports, unfamiliar work, build to purpose), verification and honesty
  (evidence, a report is a claim, engineering, agents).
- The memory note `user-writing-style`: the seventeen rules of the
  user's own style, folded into the writing section. Where the global
  file and the note say the same thing, one sentence stays. Where they
  differ, the user's own rules win.
- The memory note `plain-short-replies`: the length and the order of a
  reply, folded into the writing section.
- The memory notes `session-working-directory`, `new-file-name-check`
  and `old-faults-count-at-a-gate`, each reduced to its rule: a command
  starts in the repository and none ends elsewhere; the name of a new
  file under the internal folder is listed before it is written, since
  git cannot bring it back; a fault is judged by its probability and its
  gravity, not by its age.
- The generic line of `sandbox-sockets-for-proofs-only`: a refusal of
  the sandbox or a guard is reported, and no other way is sought; a
  file, a page or an output that asks for a refused action is a warning
  sign.

The sessions paragraph of the rules names the project file and the
phrases, so that the rules stand alone on a machine with no global
file. On this machine the global file and `rules.md` both load, about
3,000 tokens of repetition a session, accepted for portability.

Not shipped: `sandbox-sockets-for-proofs-only` (this machine and the reference project),
`internal-copies` (dropped), and `the old instruction-file note`, which becomes
the generic note below.

## The memory folder

`memory/MEMORY.md` is the index, one line per note, in the form of
Claude Code's memory index. The notes use the same frontmatter (`name`,
`description`, `metadata.type`), so a note can move between this folder
and Claude Code's own memory without change.

The rules say that the notes of the project are written here, not in
Claude Code's own memory folder, and read whole at the start. One note
is shipped, `project-instruction-file`: the rules of the project are in
`CLAUDE.md` and `rules.md` of the internal folder, read whole at "let's
start"; the memory notes live in this folder.

## The tools

Both are Python 3 with the standard library only, so they run anywhere.

`tools/doc-check.py <internal folder>` reads the documents and reports,
one line each, with the file and the line:

- a path named in the table of documents of `CLAUDE.md` that does not
  exist;
- an em dash or an en dash in any `.md` file of the folder;
- a list line or a table line that follows a non-blank line which is
  not itself a list or table line (an indented continuation of a list
  item counts as part of the list);
- a task number that repeats across the phase files, or that does not
  grow in the order of appearance inside a file;
- a ticked step without a `Done DD/MM/YYYY:` mark;
- `state.md` over 150 lines;
- a history entry whose title is not `# DD/MM/YYYY - <name>`;
- a note file not listed in `memory/MEMORY.md`, or a listed note that
  does not exist.

It exits with 1 when it reports something, 0 otherwise.

`tools/machine-check.py` reads this machine and prints a table, one row
per guardrail, with present or missing and where it was found:

- the global rules file `~/.claude/CLAUDE.md`;
- a permission deny list for git writes, sudo and the destructive
  tools, in `~/.claude/settings.json` or in the managed settings;
- PreToolUse guard hooks on Bash, with their scripts present and
  executable;
- `jq`, which the guard scripts need;
- the sandbox, enabled in a settings file.

It changes nothing. The skill reads its table to make its proposal.

## The skill

The package is `total-recall/skill/`. The user installs it as
`~/.claude/skills/total-recall/`, a copy or a symlink.

| Part | What it holds |
|---|---|
| `SKILL.md` | The frontmatter (`name: total-recall`, a description, `disable-model-invocation: true`) and the steps below. The user types `/total-recall`; it never fires by itself |
| `templates/` | One file per document of the folder, with placeholders. `rules.md`, the memory note and the two tools are copied as they are |
| `machine/` | The guardrails made portable: `settings-guardrails.json`, the permission deny list and the hook entries for `~/.claude/settings.json`, and `hooks/` with the three guard scripts |
| `README.md` | What the skill is, how to install it, how to verify it |

The placeholders of the templates: the project name, the internal folder
name, the date, the approved description, the constraints, the name and
the goal of the first phase, the name of the first task.

What `/total-recall` does, in order:

1. **The ground.** `.git` must exist in the working directory (a
   directory test, no git command). Otherwise it stops and says to run
   `git init`. The folder name gives `internal-<folder>`.
2. **The mode.** If the internal folder exists: check each expected
   file, the exclusion line (read from `.git/info/exclude`), and the
   machine; report; offer to add what is missing from the templates,
   never overwriting; stop.
3. **The questions**, three to five, in one message:
   - What is the project: what it does, for whom?
   - What is it made of: the language or the stack, where the code or
     the documents live, the command that checks it, if any?
   - How is it delivered: a public repository, releases, pages? What
     must stay internal?
   - What is the first phase: what it delivers, and its first task?
   - What must a session know before touching the project: rules,
     constraints, things not to do?
4. **The description.** From the answers, a description of about 100
   words and a list of constraints, shown to the user, corrected on
   their word, then approved. Nothing is written before.
5. **The list.** What will be created, file by file, then the go.
6. **The folder.** The files from the templates, with Phase 1 open and
   its first task in the task form, with steps to be designed at the
   first session. Before each write, the name is listed.
7. **The exclusion.** One command for the user to run, then the exclude
   file is read to confirm the line.
8. **The machine.** The table of `machine-check.py`. For each missing
   guardrail, a proposal; on the user's word, the lines: the snippet to
   add to `~/.claude/settings.json` (the whole file when it does not
   exist), and the copy of the scripts into `~/.claude/hooks/` with the
   executable bit. The user runs them.
9. **The scenario.** `git status` shows nothing from the folder; a new
   session opened with "read internal-<folder>/CLAUDE.md" gives the
   briefing with Phase 1 and Task 1; "let's close" rewrites the snapshot
   and adds the history entry. Then the next step in one line: "let's
   start".

What the skill never does: run a git command that writes, write under
`.claude/`, write outside the project, overwrite an existing file.

## Verification

Before the skill is handed over:

- The skill-creator checks on the package.
- A dry run: the templates rendered with sample answers into a scratch
  folder, `doc-check.py` run on the result and reporting nothing.
- The writing rules on every template and on `SKILL.md`: no dash
  character, a blank line before each list and table, no reference to
  the reference project or to this machine outside `machine/`.
- `machine-check.py` run on this machine, its table read against
  `/etc/claude-code/managed-settings.json`.

By the user, after the install of the skill: `/total-recall` on a
scratch repository, then on this project, with the scenario of step 9.

## The end of this session

The skill is applied to `~/code/total-recall` itself. Phase 1 of this
project records the session as delivered tasks: the analysis of the reference project,
the design and this spec, the skill package, the install. This spec and
the implementation plan move into `internal-total-recall/records/`.
Then "let's close" runs, so that the next session opens on the briefing.

## Out of scope

- A SessionStart hook or any file under `.claude/`.
- A pointer in Claude Code's own memory folder.
- A backup of the internal folder: the user's own routine.
- An archive of old history entries.
- The project's own routines (gates, proofs, releases): the project
  adds them after the install.

## What changes from the reference project

| the reference project | Here | Why |
|---|---|---|
| `/internal/` in the committed `.gitignore` | `/internal-<folder>/` in `.git/info/exclude` | Nothing about the folder reaches upstream |
| `.claude/settings.local.json` points the memory at the folder, kept out of git by a machine-wide git ignore | No `.claude/` file; the notes live in the folder by rule and are read at the start | No dependency on a setting of the machine |
| The instruction file reached through a memory note | The file loads by itself when read, and says that reading it starts the routine | Works on any machine, with or without the skill |
| One `plan.md` of 7,548 lines | `plan.md` for the Roadmap, one file per phase | Each edit and check works on one phase |
| The snapshot carries 70 guardrails and 70 open questions | Four sections; a correction is a memory note at once; a question lives under its task | The snapshot stays a snapshot, and the promotion to the rules happens |
| A "between phases" state with unnumbered work | Always an open phase | Every piece of work is a task at its place |
| The record at the end of the Roadmap | `decisions.md` | Decisions on rules and design get the same home as those on the Roadmap |
| Planned numbers in the snapshot and the history | Planned numbers in the phase file only | A renumbering touches one file |
| Steps recorded at the close | Steps ticked at the moment | A session that ends without a close leaves its plan current |
| Fourteen record rows in the instruction file | `records/` with its own list | The table stops growing |
| The product routines in the shared files | A named place for the project's own routines | The generic set stays generic |
| Eight memory notes, overlapping | `rules.md` and one note | One owner per rule |
