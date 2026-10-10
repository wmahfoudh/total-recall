---
name: project-instruction-file
description: "The rules of the project are in the internal folder, in CLAUDE.md and rules.md, read whole at the start of a session. The memory notes of the project live in this folder, not in the memory folder of Claude Code"
metadata:
  type: project
---

The instruction file of the project is `{{internal}}/CLAUDE.md`, and
the rules it imports are `{{internal}}/rules.md`. The repository has no
instruction file at its root.

**Why:** the user keeps the instruction file, the documents and the
notes in one folder of the project, and wants them to work on any
machine without a setting.

**How to apply:** at the start of a session, read both files whole,
then `state.md`, then the notes of this folder. A new note is written
in this folder, in this format, with its line in `MEMORY.md`. Claude
Code's own memory folder is left alone.
