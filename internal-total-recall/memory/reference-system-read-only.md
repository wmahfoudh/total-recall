---
name: reference-system-read-only
description: "The reference memory system is a production folder of the user: read only, never written, moved or deleted, and never named in this repository or in this folder. The user gives its path when a session needs it"
metadata:
  type: project
---

The skill was made from the memory system of another project of the
user. That folder is a production folder of the user. It is read only
for every session of this project: nothing is written, moved or deleted
there, and nothing of it is copied into this repository.

The name of that project and the path of its folder are not written
anywhere: not in `skill/`, `tests/` or `README.md`, and not in this
internal folder, its records included. The user gives the path when a
session needs to read the reference again.

**Why:** the user's word at the start of the project, 07/10/2026,
repeated twice: "NEVER write to it". And the user's correction at the
end of the same day: the name of the reference project was found in
this folder, where it must not be.

**How to apply:** read the reference with `cat`, `sed` or `grep`, on
the path the user gives. When a comparison needs a copy, copy into the
session scratchpad. Write "the reference project" or "the reference
folder" in any document. The package test checks `skill/`, `tests/`
and `README.md` for the name by its hash, so that the test does not
name it. The review runs the same hash check over the tracked files
and this folder, and prints only the paths, until item 3 of the
Roadmap brings this folder into the package test.
