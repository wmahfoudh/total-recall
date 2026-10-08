# total-recall: the plan

## Goal

Total recall is a Claude Code skill that gives a project a memory: a folder of plain documents inside the project, kept out of git, that a session reads at its start and updates at its close. I made it from the memory system of an earlier project of mine, keeping what worked and changing what did not. The repository holds the skill (`skill/`), its tests (`tests/`) and the README. It is for my own projects, on any machine where Claude Code runs. The skill is installed by a link into `~/.claude/skills/`, and this project is the first one it runs on.

## Constraints

- Markdown templates, Python 3 with the standard library only, bash for the three guard scripts.
- The check command is `python3 -m unittest discover -s tests -v`, from the repository root, green before a hand-over.
- The repository may be shared: nothing in it names the reference project, this machine or another project's stack. The internal folder stays out of git.
- All the text follows `rules.md`: no dash character, a blank line before each list and table, the README in the user's voice.
- Git writes are the user's. Nothing is written under `.claude/`.
- The tests write no bytecode into the templates.

## Phases

One file per phase in `phases/`, named `phase-NN-<name>.md`. The open
phase is named in `state.md`. The rules of the numbers are in
`lifecycle.md`.

## Roadmap

Ordered. Each item is a few lines: what it is, why, its size in
sessions. An item becomes a phase or a task when it opens, and leaves
the Roadmap when it is delivered in full.

1. **The feedback of the first trials.** The user tries the skill on a
   scratch repository and on a real project, takes notes, and brings
   them: each item is summarized one at a time, then becomes a task.
   The first task of Phase 02. One session or more.
2. **The reviewer's minors.** The thirteen Minor findings of the fresh
   review of 07/10/2026, in `records/2026-10-07-review.md`: the machine
   check on a regex matcher, a quoted command and JSON of the wrong
   shape; an answer that is not a string in the render; a BOM and a
   table after a list item in the document check; the `.git` test in a
   worktree; the snapshot and history templates at render time; "two
   hook scripts" in the README; the description of the skill; the file
   list of step 5; the skill-creator checks named in the spec; a
   capital in the history qualifier. Half a session, with the user's
   own notes.
3. **The guardrails on another machine.** The machine check and the
   proposal of the deny list and the guard scripts, tried on a machine
   that has none. Half a session, on that machine.
4. **The fine tuning of the templates.** After a few sessions on real
   projects: the size of `state.md`, the number of memory notes, the
   close routine, the task form. What the sessions show. One session.

## Parked

Asks set aside, each with the condition for its return.

- A pointer note in Claude Code's own memory folder, and a session
  start hook that prints the snapshot: back if a session ever opens
  without the phrase or the file read, and misses the rules.
- The `autoMemoryDirectory` setting pointing Claude Code's memory at the
  folder: back only if the user accepts a file under `.claude/`.

## Blocked

What waits on something outside, with what it waits for. Nothing yet.

The decisions on the Roadmap and on the plan are in `decisions.md`.
