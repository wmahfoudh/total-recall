# 11/10/2026, fifth - The review of the README

The README read in full against the skill, the tools and the
decisions, for errors and incoherences.

- Task 49: fifteen items, all approved. Among them the template name
  `CLAUDE.template.md`, the three commands where the text said one,
  the rows of the machine check, what the guardrails refuse, and a
  token count never measured replaced by the size of the folder in
  words. `cdf9d41`, 153 tests green.
- A paragraph over 100 words split by the user, `2f1e8a6`.

# 11/10/2026, fourth - The review of the memory and Task 48

The review of the memory at the close of Phase 04, then its changes
carried into the templates.

- The review, `records/2026-10-11-review.md`: two items from the
  session, six numbered, all applied on the user's word. D5 and D8
  moved to `obsolete.md`, an item leaves the Roadmap when it opens as
  a phase or a task, the hash check replaces the grep of the note.
- The reference name checked by hash over the tracked files and this
  folder: no hit.
- The two empty `.claude/` folders of this folder removed by the user.
- Task 48: the same changes in the templates, `ca32cec`. 153 tests
  green.

# 11/10/2026, third - Phase 04 closed, Phase 05 opened

The reviewer's minors fixed in one pass, then Phase 04 closed.

- The plain "let's start" tried and passed. The commit of the Phase 03
  close done by the user.
- The fifteen findings listed, then fixed at once on the user's word
  (D33), test first: the machine check, the render, the document
  check, the install steps and the state template. 8, 9 and 10 were
  already fixed, 12 dropped. 153 tests green, `e01301f`.
- Phase 05, A second real project, opened (D34). The project is still
  to be chosen.

# 11/10/2026, later - Phase 03 closed, Phase 04 opened

Tasks 34 to 44 discussed one at a time, then Phase 03 closed against
its baseline.

- The start script tried by the user and passed. A plain "let's start"
  found the folder only by listing the tree: the global file named no
  folder. A line for it, reported by the machine check and proposed by
  the install (D29).
- The repeats removed from the rules and the style note (D23) and from
  the templates, with the template project file renamed so that it no
  longer loads here (D26). The close reads the tasks of the session
  (D27).
- Ended with no change: the compressed copy, the start levels, the
  short close entries, the wording tests, the guard scripts. The second
  real project moved to the Roadmap.
- The benchmark: 5,566 words a start, from 10,022 to 13,891. 143 tests
  green. Phase 04, The reviewer's minors, opened (D32).

# 11/10/2026 - The start script

The first task of Phase 03: a script prints what a session reads at
its start, and the start no longer reads the rules twice.

- The tokens left out of the baseline on the user's word: the phase
  measures words.
- Found in the design: Claude Code loads `CLAUDE.md` and `rules.md` of
  the folder when the session reads a file there, and the routine read
  them too, about 3,500 words a start. The same happens for the
  templates of the skill when a session works in `skill/templates/`.
- Task 33, steps 1 to 5, test first: `tools/start.py`, the measure of
  `doc-check.py --size` through it, the start routine of the template
  and of this folder, the note `project-instruction-file`. 134 tests
  green, D22.
- The start of this folder: 7,022 words with the script, 8,059 by the
  old routine, 11,621 with the double read. Step 6, the trial, is the
  user's.

# 10/10/2026, later - Phase 02 closed, Phase 03 Optimization opened

A session of exploration and discussion, with no change to the code.

- The repository explored and six points raised: the cost of a start,
  the phase file that grows, the tests that pin the wording, a single
  real user, the global rules file, the guard hooks.
- The cost of a start measured: 6,207 words in this project, 4,854 in
  the template, of which `rules.md` and the style note are 3,742.
- The tools that cut tokens read (caveman, caveman-compress, ponytail,
  rtk): a start script chosen first, with three other ideas planned.
- The baseline in `records/2026-10-10-baseline.md`. Phase 02 closed
  (Task 31), Phase 03 opened with Tasks 32 to 44, D21. The backup by
  the script refused by the permission check of the session: the
  baseline names the commit `b315d2c`.

# 10/10/2026 - The memory used with care, the backup and the update

The user's notes on the first trials, turned into the skill's second
version, then run on this folder.

- The notes discussed one at a time: the git question at the install,
  the memory used with care with a review command, the README for a
  public skill; the user's ideas of decisions newest first and of
  `obsolete.md`. The spec and the plan in `records/`, Tasks 18 to 25,
  each test first.
- The document check gained the order of the decisions, the obsolete
  entries and the size read at each start; `render.py` gained the
  migration of the decisions; the templates, `SKILL.md` and the README
  followed.
- The README rewritten with the user: "let's start", one line per
  paragraph, the commands, the templates to adapt and a fork, the
  reader as "you". Rule 16 of the style note changed to match.
- Found on the way: the skill would have touched another documentation
  system (Task 26); the review missed the memory folder and the
  session's own decisions (Task 27); the tests named the reference
  project (Task 28); the update was five `cp` lines and four yes, now
  `/total-recall update`, one yes after a backup (Task 29).
- This folder updated and reviewed: 25 items applied, D16 to D20, four
  decisions in `obsolete.md` (Task 30). 113 tests green, the check
  clean.

# 07/10/2026, later - The first feedback: the reference project named in the folder

Right after the close, the user read this folder and found two things.
The first was a mistake, fixed at once. The second is a proposal.

- The name of the reference project and the path of its folder were in
  seven files of this folder (the history, the phase file, a memory
  note and its index line, the four records), under a rule of Phase 01
  that allowed it inside the folder. The user wants it nowhere. Task 16:
  the prose files rewritten, the records scrubbed with placeholders,
  this machine's path and the session scratchpad with them. Zero
  mentions left, the check tool clean.
- The user looked for their writing style under `memory/` and found two
  notes. The style was in `rules.md`, "The user's style", eighteen
  rules loaded at every start, by the consolidation of the spec. The
  user's word: in memory it is stronger and less prone to be
  forgotten. Task 17: the style shipped as a memory note in every
  project, `memory/user-writing-style.md`, with `rules.md` pointing to
  it; test first, 58 tests green, installed here. Committed by the
  user as `f1bf102`.
- The folder aligned with the skill as it stands: a fresh render
  compared file by file, the fixed files identical, the filled ones
  different as expected. The project file gained its own writing rule:
  the name of the reference project and this machine are never written,
  and a close searches the folder for the name.
- The second close of the day: the check tool clean, the working tree
  clean.

# 07/10/2026 - The skill built, verified and installed on this project

One long session, the whole of Phase 01: the reference memory system
read and judged, the design agreed section by section, the spec and the
plan written and approved, the package built test first, a fresh
reviewer launched, the skill applied to this project.

- At the start: the user's brief, the questions, the reference folder
  named by the user (their production folder, read only; its path is
  not written in this folder).
- Task 1: the reference read whole; the memory wired through
  `.claude/settings.local.json` and a machine-wide git ignore, which the
  user did not want; the Claude Code documentation checked by a
  research agent.
- Task 2: four design sections agreed, with the user's corrections: no
  `CLAUDE.local.md`, nothing under `.claude/`, no dependency on the
  skill for the loading, a `tools/` folder, three to five questions at
  the install, the record as its own file, always an open phase. Twelve
  changes from the reference challenged and approved. The spec written
  and approved.
- Task 3: the plan, thirteen tasks, approved; native execution, the
  user's voice on every text.
- Tasks 4 to 11: the two tools and the render script test first (53
  tests green), the rules file, the templates, the machine folder, the
  skill file, the README, the verification. Three stumbles: the Write
  tool decoded the escape codes of the two dashes into the characters
  themselves, in the plan and again in this file (spelled with `chr()`
  in code, in words in prose); a test expected a table row on the wrong
  line; a stray bytecode cache was copied into a sample render.
- Task 12: the reviewer launched, read only, with the spec, the plan
  and the rulings. Its findings are open.
- Task 13: the install here, by the skill's own steps: the description
  approved, seventeen files rendered, the check clean, the machine
  table present on every row. The exclusion line is handed to the user.
  The import line `@rules.md` verified on the way: Claude Code loaded
  the project file and the rules together when the folder was first
  read. The check tool caught nine `Done` marks with a comma for a
  colon and seven without an outcome in the phase file, and learned
  that a mark may wrap at the line break.
- Task 12, the findings: no Critical; four Important fixed in one pass,
  test first (the repair mode of the render, the quoting in the tools
  README, a file that is not UTF-8 named by the check, the table of
  documents read by its header); thirteen Minor to the Roadmap; the
  report saved as `records/2026-10-07-review.md`. 57 tests green. The
  reviewer also found the first commit (`aca0d06`) and the link of the
  skill, made by the user during the build.
- Task 14, the close: this folder brought to the end of the session,
  Phase 01 closed, Phase 02 opened with Task 15.
- After the close: the user added the exclusion line and committed the
  fixes (`3d49152`, `45ed75f`). Git ignores the folder, read with
  `git check-ignore`. Left open: the trial on a scratch repository.
