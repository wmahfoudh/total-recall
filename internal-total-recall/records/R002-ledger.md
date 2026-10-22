# SDD ledger, plan: <the session scratchpad>/2026-10-07-total-recall-plan.md

Spec: 2026-10-07-total-recall-design.md in the same folder.

Setup: Ruling: no worktree and no commit by the session. The user's rules make every git write theirs, the guard refuses them, and the repository has no commit yet. Each task ends with the git line for the user. Cost if wrong: none, the user commits when they choose.
Setup: Ruling: the ledger and the briefs live in the session scratchpad, not in a workspace inside the repository, which git would list as untracked. Cost if wrong: the ledger does not survive the session, which the memory system itself covers at the close.

Pre-flight: Task 1 produces find_dashes, find_list_breaks, is_list, is_table; Tasks 2, 4, 8, 12 consume them by those names. Clean.
Pre-flight: Task 3 produces report, render_table and the seven row names; Tasks 9 and 10 consume the row names. Clean.
Pre-flight: Task 5 produces PLACEHOLDERS, plan, write and the wrote/kept lines; Tasks 4, 8 and 10 consume them. Clean.
Pre-flight: Task 8's phase template file name phases/phase-01-{{phase1_slug}}.md matches Task 4's expected list. Clean.

Task 1: complete (tests: python3 -m unittest tests.test_doc_check, 10 pass). Git line handed over.

Task 2: Ruling: the table test expected line 6 where the minimal file has the row on line 7; the test was corrected, the tool was right. Cost if wrong: none.
Task 2: Ruling: a history title may carry a qualifier after the date (", later", ", evening"), the user habit seen in the reference history for a second session of a day. The spec form stays the default. Cost if wrong: a looser title check.
Task 2: complete (tests: python3 -m unittest tests.test_doc_check, 26 pass; trial on the reference folder read only, 695 findings, five read and true). Git line handed over.

Task 3: complete (tests: python3 -m unittest tests.test_machine_check, 10 pass; the table on this machine reads present on every row, matching the managed settings). Git line handed over.
Task 4: complete (tests/test_package.py written; the three writing tests pass, the structure tests fail until the files exist, as planned). Git line handed over.
Task 5: complete (tests: python3 -m unittest tests.test_render, 6 pass). Git line handed over.

Task 6: Ruling: rules.md is 358 lines, over the plan figure of about 250: the wrong and right pairs and the full sections are the user own words, and cutting them drops rules. Cost if wrong: about 1,000 tokens a session.
Task 6: complete (the writing tests pass on rules.md; the seventeen rules and each heading of the global file mapped while writing). Git line handed over.
Task 7: complete (close.md and lifecycle.md written from the spec; writing tests pass). Git line handed over.
Task 8: Ruling: the render skips __pycache__ and hidden files, and the test loaders no longer write bytecode; a stray cache file had been copied into the sample. Test first, then the fix. Cost if wrong: none.
Task 8: complete (tests: python3 -m unittest tests.test_render tests.test_doc_check, 33 pass; the sample renders 17 files, doc-check clean, no placeholder left). Git line handed over.

Task 9: complete (the three guard scripts copied byte for byte, the snippet carries the 35 deny patterns; tests: tests.test_package.MachineFolder, 3 pass). Git line handed over.
Task 10: complete (SKILL.md, 214 lines, frontmatter checked by the package test; the six commands it names parse with bash -n). Git line handed over.
Task 11: complete (README.md in the user voice; the package test passes). Git line handed over.
Task 11: Ruling: the four ", so " of the README and the three of SKILL.md were split into two sentences, the tic rule of the user. Cost if wrong: none.
Task 12: complete (suite: python3 -m unittest discover -s tests, 53 pass; the dry run renders 17 files, doc-check clean, 0 placeholders; no dash and no origin name in README.md, skill/ and tests/; machine-check present on every row; SKILL.md 214 lines with the three fields).
Task 12: Ruling: a .gitignore with __pycache__/ added at the root, outside the plan, because running the tests creates tests/__pycache__ and the user would otherwise commit it. Cost if wrong: one line to remove.
Final review: self-review by the author so far; a fresh reviewer is proposed to the user under their agent rule.

Task 13: Ruling: the import line @rules.md resolves relative to the project file: Claude Code loaded both files into the session when the folder was first read (seen 07/10/2026). Roadmap item 2 is verified early. Cost if wrong: none.
Task 13: Ruling: a Done mark wrapped at the line break is accepted (the continuation lines are stripped before the join), test first. Cost if wrong: none.

Final: fixed the repair mode of the render (Important 1): test_a_repair_adds_only_the_files_that_need_no_answer red then green, suite 57/57.
Final: fixed the quoting of the tools README (Important 2): the rendered command is quoted; checked by the sample render.
Final: fixed a file that is not UTF-8 (Important 3): test_a_file_that_is_not_utf8_is_reported_by_name red then green, suite 57/57.
Final: fixed the table of documents read by its header (Important 4): test_only_the_table_of_documents_is_checked_for_files red then green, suite 57/57.
Final: minor (deferred): the thirteen Minor findings of the review, listed in records/2026-10-07-review.md and in item 2 of the Roadmap.
Final: Ruling: the reviewer set nine behaviors aside as outside the form the templates use (other fences, a nested Done mark, a path in the index, a YAML list in a note, a quote in a folder name, the expansion of variables by Claude Code, the snippet without the sandbox block, the double rules on this machine, Task 13 left to the user); each stands, the README names the form as the limit. Cost if wrong: a finding to read at a close, not an error.
Final review: a fresh reviewer, read only, on the most capable model, allowed by the user.
