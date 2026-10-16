# Lifecycle

The rules for phases, tasks and steps, in full. Read when a phase opens
or closes, and for the numbers. `AGENTS.md` has the summary.

## Always an open phase

The project always has an open phase, named in `state.md`. There is no
state between phases: when a phase closes, the next one opens in the
same close. Every piece of work has a home, a task of the open phase at
its place in time.

## Opening a phase

- A phase opens on the user's word, with a number (two digits, counting
  from 01), a name, and a file `phases/phase-NN-<name>.md`, where
  `<name>` is a short lowercase name with hyphens.
- At the close of a phase the next one opens with the name of the head
  of the Roadmap. The user can rename it.
- The project's own opening steps (a branch, a version) are listed in
  `AGENTS.md` under "The project's own routines", and the phase file
  records them under "The opening of the phase".

## The form of a phase file

- `# Phase NN: <name>`, then the preamble: opened DD/MM/YYYY on whose
  word, what the phase is for, its rules, and the order of its tasks as
  a numbered list.
- `### The opening of the phase`: the project's own steps, or "no step".
- `### Task N: <name>`, one per task, in the task form:
  - "What it does and why", a short paragraph, before any step.
  - For code, the files and the interfaces at its opening.
  - `**The steps:**`, each `- [ ] **Step K: <name>** <what the step
    does>`. A done step reads `- [x]` and ends with `Done DD/MM/YYYY:`
    and what happened, in a line or two.
  - What was found on the way, under the task, with its evidence.
  - The suggested git line.
- `**Checkpoint for the phase:**` at the end, then the close paragraph
  when the phase closes: the date, what was delivered, what stays open.

## The numbers

- Phases count from 01 across the project. Tasks count from 1 across
  phases, in the order they are done. Steps count inside a task.
- A task has its number from the moment it is written in a phase file.
  A planned task's number appears in its phase file only, until it
  starts. A delivered task's number never changes and may appear
  anywhere.
- A new task takes the next number. When it is done before planned
  tasks that have not started, it takes its place before them, and
  those are renumbered in the phase file the same day.
- Work that no task planned (the tools, the documents, a rule) is
  recorded as tasks too, grouped into a few that represent the work,
  not a task per action.
- A check that is run again is a new task with a new number.
- The close is the last task of the phase, numbered when it is written.
- A sentence about the numbers themselves keeps the old number and
  gives the new one beside it.

## During a phase

- The work follows the phase file, a task at a time. A task opens with
  what it does and why.
- A step is ticked with its date the moment it is done, with a line on
  what happened. The phase file is then always current. The snapshot
  and the history are the close's.
- What is found on the way goes under the task, with its evidence, and
  becomes a task of its own when it changes code.
- The user tests each delivery before the git line.

## Closing a phase

A phase closes when:

- each task is delivered, tested and validated by the user
- the project's own checks of `AGENTS.md` pass
- the close routine of `close.md` has run, as the last task

## The Roadmap

Asks and ideas collect in the Roadmap of `plan.md`, ordered, until a
phase takes them. Each item is a few lines: what it is, why, its size in
sessions. An item leaves the Roadmap when it opens as a phase or a
task: the phase file holds it from then on. An ask set aside goes under
Parked with the condition for its return. What waits on something
outside goes under Blocked with what it waits for. The decisions on the
Roadmap are in `decisions.md`, and the replaced ones in `obsolete.md`.
