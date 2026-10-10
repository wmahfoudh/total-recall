# total-recall: the plan

## Goal

The goal is the description at the top of `CLAUDE.md`.

## Constraints

The constraints are under "Engineering" in `CLAUDE.md`.

## Phases

One file per phase in `phases/`, named `phase-NN-<name>.md`. The open
phase is named in `state.md`. The rules of the numbers are in
`lifecycle.md`.

## Roadmap

Ordered. Each item is a few lines: what it is, why, its size in
sessions. An item becomes a phase or a task when it opens, and leaves
the Roadmap when it is delivered in full.

1. **The guardrails on another machine.** The machine check and the
   proposal of the deny list and the guard scripts, tried on a machine
   that has none. Half a session, on that machine.
2. **The fine tuning of the templates.** After a few sessions on real
   projects: the size of `state.md`, the number of memory notes, the
   close routine, the task form. What the sessions show. One session.
3. **The internal folder in the package test.** The test reads
   `skill/`, `tests/` and the README, not the internal folder, which
   is now committed. A test for this project's folder, or a note that
   the review covers it. Small.

## Parked

Asks set aside, each with the condition for its return.

- A pointer note in Claude Code's own memory folder, and a session
  start hook that prints the snapshot: back if a session ever opens
  without the phrase or the file read, and misses the rules.
- The `autoMemoryDirectory` setting pointing Claude Code's memory at the
  folder: back only if the user accepts a file under `.claude/`.
- The guard scripts in a repository of their own: back if a second user
  installs the skill, or if the scripts this machine runs change and
  the copies of `skill/machine/hooks/` fall behind (D31).

## Blocked

What waits on something outside, with what it waits for.

- **The name of the reference project in the history.** The name is
  out of the files since `c3eee97`, and two commits from `aca0d06`
  still hold it. A rewrite of the history and a forced push remove it,
  and change the hash of each commit. Waits on the user's decision.

The decisions on the Roadmap and on the plan are in `decisions.md`.
