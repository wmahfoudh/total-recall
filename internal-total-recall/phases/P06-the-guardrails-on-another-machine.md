# Phase 06: The guardrails on another machine

Opened 22/10/2026 at the close of Phase 05, named from the head of the
Roadmap. The phase tries the machine check and the proposal of the deny
list and the guard scripts on a machine that has none, and brings back
here what that shows. The user can rename it.

**The rules:**

- The work on the other machine follows `SKILL.md`, step 8, as a user
  would. This file records what comes back: the faults, the findings,
  the changes they lead to here.
- A change to a tool or to a script starts with a failing test, in both
  forms (D35). A change to a template is checked by the sample render
  and `tools/doc-check.py`.
- The installed copies of the tools in this folder follow the
  templates: a changed tool is copied here in the same task.
- The rules of `lifecycle.md`, "The numbers", hold.

**The order:**

1. Task 55, the guardrails on another machine.
2. The close of the phase, as its last task, numbered when it is
   written.

### The opening of the phase

No step: the project has no opening routine.

### Task 55: The guardrails on another machine

What it does and why: the machine check and the proposal of the deny
list and the guard scripts, tried on a machine that has none, half a
session on that machine, to see that the install of the Claude Code
form gives a user the guardrails from nothing.

**The steps:**

- [ ] **Step 1: The trial** On the other machine, the skill linked,
  `/total-recall` run on a test repository up to step 8, each row of
  the table read, the proposed lines run, the table read again.
- [ ] **Step 2: What came back** The findings written here, and the
  changes they lead to, in both forms, test first.

**Checkpoint for the phase:** the machine check and the proposals tried
on a machine without the guardrails, the findings applied, the suite
green.
