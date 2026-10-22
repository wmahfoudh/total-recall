# Review of the total-recall package, 07/10/2026

The report of the fresh reviewer (a read-only agent on the most capable
model), kept as received. The four Important findings were fixed the
same day, test first. The thirteen Minor findings are item 2 of the
Roadmap.

Read: the spec, the plan, the ledger, every file under `skill/`, `README.md`, the four test files. Run: the test suite, a render with the name `My Project`, a second render on the same folder, `doc-check.py` on the result, twelve edge cases on `doc-check.py`, thirteen on `machine-check.py`, a comparison of the snippet and the scripts with `/etc/claude-code/`, a `git check-ignore` of the spaced pattern, and the guard scripts fed a `git commit` and an `rm -rf`. Everything I wrote went under `$TMPDIR`. Nothing in the repository was changed.

Two facts about the repository that differ from the brief: it has one commit (`aca0d06 feat: the total-recall skill, its templates, tools and tests`), and the skill is already linked (`~/.claude/skills/total-recall -> ~/code/total-recall/skill`). `internal-total-recall/` does not exist yet, so Task 13 of the plan (the skill applied to this project) is still to come, by the user's hand as planned.

## Strengths

- The suite passes: `python3 -m unittest discover -s tests -v`, 53 tests, OK (run).
- The five review focus items hold (run): `My Project` is kept verbatim in every rendered file and the pattern `/internal-My Project/` matches `internal-My Project/CLAUDE.md` under `git check-ignore -v`; `### Task 10:` after `### Task 9:` is clean; a list line inside a fence after a sentence is not reported; an absent, empty or non-JSON settings file gives a full table of `missing` with exit 0; a second render on a folder with one edited file and one deleted file keeps the 16 existing files (hashes identical before and after) and rewrites only the missing one, byte for byte equal to the first render.
- A fresh render of the real templates gives 17 `wrote` lines, `doc-check.py` says `clean`, no `{{` is left (run).
- No em dash, en dash, figure dash, horizontal bar or minus sign in `README.md`, `skill/` or `tests/`; no `the reference project`, `/home/` or the user's login in `README.md` or `skill/` (run).
- The three guard scripts are byte for byte the machine's (`cmp` on each), and the snippet's 35 deny patterns equal the managed list in content and order (run). The copies deny `git commit -m x` and `rm -rf x` and allow `ls` (run).
- The six commands in the fences of `SKILL.md` parse under `bash -n`; `${CLAUDE_SKILL_DIR}` is used at each place a path into the skill is needed, and `render.py` resolves its templates through the symlink (run and reading).
- `machine-check.py` reads a hook with no `matcher`, a command with arguments, `~`, `$HOME` and `${HOME}` as present (run), and this machine's table reads `present` on all seven rows (run).
- `close.md`, `lifecycle.md` and the sessions section of `CLAUDE.md` agree with each other and with the spec's eight close steps (reading). The ledger's rulings are sound: the 358 lines of `rules.md` are the user's own words; the history qualifier matches a real habit; the cache skip and the `.gitignore` line are right.

## Issues

### Critical (must fix)

None.

### Important (should fix)

1. `skill/SKILL.md` lines 58 to 72, step 2 (repair mode). The step offers "the render of step 6" but the session has no answers file in that mode: the questions are skipped and the render refuses to run without all nine answers. If the session reconstructs them and chooses a different slug or name, the render writes a second `phases/phase-01-<slug>.md` with its own `### Task 1:`, and `doc-check.py` then reports `Task 1 is already in phase-01-first.md` (run: `review-render2.*/t3`). A re-rendered `history.md` or `decisions.md` would also carry today's date as the install date. A reasonable person expects repair mode to add a missing `close.md` or `rules.md` and nothing else. Fix: say where the answers come from in repair mode (read from the existing `CLAUDE.md`, `state.md` and the existing phase file name), and have the render add only the files that carry no placeholder, or have the skill name the files it will add and refuse a second phase file.

2. `skill/templates/tools/README.md` lines 8 and 9. The rendered command is unquoted: `python3 internal-My Project/tools/doc-check.py internal-My Project` (run). Copied into a shell it fails on any folder name with a space, the case the review focus names. `SKILL.md` and `close.md` quote theirs. Fix: `` `python3 "{{internal}}/tools/doc-check.py" "{{internal}}"` `` and the same for the machine check.

3. `skill/templates/tools/doc-check.py` line 180, `check_folder`. A `.md` file with a byte that is not UTF-8 (a pasted `café` in Latin-1 in `story.md`) stops the tool with a traceback that does not name the file (run: `UnicodeDecodeError ... byte 0xe9`). A close then fails at step 8 with nothing to act on. Fix: catch `UnicodeDecodeError` per file and report `path:0: not UTF-8`.

4. `skill/templates/tools/doc-check.py` lines 80 to 96, `check_documents_table`. The check runs on every table of `CLAUDE.md`, not on the table of documents only. When a project fills the routines table (`| Routine | File | When |`) with a backticked name in the first cell, `| \`release\` | \`records/release.md\` | before a tag |`, the tool reports `release is named in the table and does not exist` (run, case G). The template invites that table to be filled and the Working documents table teaches the backtick habit. Fix: stop at the first heading after "## Working documents", or read the `File` column by its header.

### Minor (nice to have)

1. `skill/templates/tools/machine-check.py` line 38. A matcher written as a regex (`"Bash|Write"`), a quoted command (`"\"$HOME/.claude/hooks/git-guard.sh\""`) or a command run through an interpreter (`bash $HOME/.claude/hooks/git-guard.sh`) reads as `missing` (run). The skill would then propose a duplicate hook. A `re.fullmatch` on the matcher and a skip of a leading `bash`/`sh` word would cover the first and the last.

2. `skill/templates/tools/machine-check.py` lines 31, 37, 48. A settings file that is JSON of the wrong shape (`{"permissions":"nope"}`, `{"hooks":{"PreToolUse":["nope"]}}`, `[1]`, or a hook whose command is spaces only) ends in a traceback (run). The plan's focus covered absent and non-JSON files, which pass. An `isinstance` check at each `.get` keeps the promise "does not crash".

3. `skill/scripts/render.py` lines 34 and 102. An answer that is not a string (`"constraints": ["a", "b"]`, a shape a session could write for a list) raises `TypeError`, uncaught, exit 1 with a traceback, after the empty target folder was created (run). `SKILL.md` says to join the lines, so the path is unlikely; a check in `plan()` that every answer is a string would give the exit 2 and message the docstring promises.

4. `skill/templates/tools/doc-check.py` line 148. A UTF-8 BOM at the start of `history.md` makes the first title invisible to the check: `﻿# The install` passes as clean (run, case F). Reading with `utf-8-sig` fixes it.

5. `skill/templates/tools/doc-check.py` lines 60 to 66. A table that follows a list item with no blank line, at the top level (`- item` then `| a |`), is not reported (run, case J). The rule says a blank line before every table.

6. `skill/SKILL.md` lines 45 to 52, step 1. In a git worktree or a submodule `.git` is a file, and in a subfolder of a repository there is no `.git`: both get the advice "run git init", which is wrong there, and the exclusion command of step 7 would fail on a worktree (reading). The message could say "go to the root of the repository, or run git init".

7. `skill/templates/state.md` lines 8 and 9 say Task 1 "has no steps yet"; the phase file written at the same time has `Step 1: The design` (reading). The first briefing reads both.

8. `skill/templates/history.md` line 8 records "The exclusion line in `.git/info/exclude`, added by the user" at render time, one step before the user adds it (reading). A session that stops after step 6 leaves a false line.

9. `README.md` line 104 says "two hook scripts", line 97 says "three guard scripts" (reading). Three files, two hooks and a library.

10. `skill/SKILL.md` line 3. The description says "or asks to set up, install, check or repair", but `disable-model-invocation: true` means a request never runs it; only `/total-recall` does (reading).

11. `skill/SKILL.md` line 107, step 5. The spec asks for the list "file by file"; the step shows the table, where `phases/`, `records/`, `tools/` and `memory/` stand for several files each, and the phase file name with its slug is not shown (reading).

12. Spec, "Verification": "The skill-creator checks on the package" is in the spec, in neither the plan's Task 12 nor the ledger (reading).

13. `skill/templates/close.md` line 25 and `doc-check.py` line 76: the qualifier after the date accepts lowercase letters and spaces only, so `# 07/10/2026, Later - x` is reported (reading).

## Declined to judge

- A `~~~` fence or a sentence starting with a number and a full stop ("2024. The year") read by `find_list_breaks`: outside the form the templates use, which the README states as the limit.
- A `Done` mark on a nested bullet under a ticked step reported as missing (run, case I): the form puts the mark at the end of the step, so the finding is right.
- An index line with a path prefix (`(memory/note.md)`) giving two findings (run, case L): the index form is a bare file name, as Claude Code's own index.
- A YAML list in a note's frontmatter reported as a list break (run, case K): the shipped note form has no list.
- A folder name with a quote or a glob character in the exclusion line: the focus names spaces and capitals; the rest is rare and the user reads the line before running it.
- Claude Code's expansion of `$HOME` in a hook command and of `${CLAUDE_SKILL_DIR}` in a skill: a reading from the documented behavior, not verified here (no subagent, no local docs found).
- The snippet without `statusMessage` and without the `sandbox` block: the spec limits it to the deny list and the hooks.
- The repetition of the global file and `rules.md` on this machine: accepted by the spec.
- Task 13 of the plan not done: the user's step, after this review.

## Verdict

The package does what the spec and the plan say, the tests and the dry run back it, and nothing in it overwrites or commits. For a first install on a folder name without a space it is ready. Fix the four Important items before relying on repair mode (step 2 of the skill) and on spaced folder names: the repair path as written can produce a duplicate phase file, the tools README hands over a command that breaks on a space, and the document check can crash without naming the file or report a false finding on the routines table.
