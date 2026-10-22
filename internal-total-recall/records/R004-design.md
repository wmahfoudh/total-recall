# The memory used with care: the design

Written 10/10/2026 with the brainstorming skill, from the user's notes
on the first trials (Phase 02, Task 15). The skill asks before the git
exclusion, writes to the memory with judgment, gains a review of the
memory that also brings an older folder to the current form, keeps the
decisions newest first with the replaced ones in `obsolete.md`, and
ships a README written for a public skill.

## What was asked

1. **The git exclusion.** The skill asks the user whether the internal
   folder stays out of git, and writes the exclusion line only on a
   yes. The docs, the README and the memory notes do not mention the
   choice, either way.
2. **The memory used with care.** The memory is precious. The skill
   knows when to ask before a write and when not to, so that the user
   keeps working on the project and the documents follow alongside.
3. **A review of the memory.** A command that reviews the material:
   the coherence of the documents, entries reordered, merged and
   cleaned, contradictions found and settled. It shows the proposed
   changes before it applies them. It also brings the folders of
   projects installed with an older version of the skill to the
   current form.
4. **The decisions newest first, and a file of replaced decisions.**
   The latest decision is found first. A decision replaced by a newer
   one leaves `decisions.md` for `obsolete.md`, with a note: replaced
   by which decision, on which date.
5. **The README.** Written for a public skill, in the user's voice and
   by the user's writing rules, without saying so. The path reads
   `internal-<project-name>/CLAUDE.md`.

## What exists

- Step 7 of `SKILL.md` hands over the exclusion line without asking.
  The templates and the README describe the folder as kept out of git:
  `SKILL.md` (the opening and step 7), `templates/CLAUDE.md` ("Working
  documents"), `templates/memory/project-instruction-file.md`,
  `templates/rules.md` ("The internal folder"), the README (the opening,
  "Use it on a project", "Check it", "Limits"). Step 9 of the scenario
  starts with `git status`.
- The project file says "A correction from the user becomes a memory
  note at once" and "A decision is appended to `decisions.md` when it is
  taken". Nothing says when to ask. Step 7 of `close.md` keeps the
  notes "around ten".
- No review exists. The mode of step 2 of `SKILL.md` checks a folder
  and offers the repair, which adds missing files and keeps the rest.
  An older routine file (`close.md`, `lifecycle.md`, `rules.md`) stays
  old.
- `decisions.md` appends at the end, entries titled by date only.
  `history.md` is newest first. `story.md` appends at the end.
- The README is in the first person ("waiting on me", "the diary in my
  voice") and writes `internal-<folder>` outside backticks in three
  places. GitHub reads `<folder>` as an HTML tag and drops it, which
  shows `internal-/CLAUDE.md`.
- This project reads about 5,800 words at each start: `CLAUDE.md`,
  `rules.md`, `state.md`, the memory notes and `plan.md`.

## The design

### 1. The exclusion asked

- Step 5 of `SKILL.md`, "The list and the go", asks one more question:
  keep the internal folder out of git, yes or no. The answer is not a
  key of the render and is not written in any file.
- On a yes, step 7 hands over the line as today. On a no, step 7 is
  skipped and the scenario starts at the briefing.
- The templates and the README stop describing the folder as out of
  git. A sentence that depends on it is rewritten to hold in both
  cases: "A file replaced here does not come back from a commit"
  becomes a rule to list a file before replacing it, which already
  exists in `rules.md`. The README describes the question, not the
  answer.
- The check mode of step 2 still reads `.git/info/exclude` and reports
  the line, as information.

### 2. When the skill asks before a write

A new section of `templates/rules.md`, "The internal folder", replaces
the two sentences of the project file. The rule:

- **Written without asking**, when the place is obvious and the cost is
  small: a ticked step, a history entry, a decision, a Roadmap item, a
  fact in the file that owns it and is not read at each start (a phase
  file, a record, the code map).
- **Asked first**, when the user's judgment matters:
  - the text goes into a file read at each start (`CLAUDE.md`,
    `rules.md`, a memory note), each line of which costs tokens in
    every session;
  - the text changes, weakens or contradicts something written;
  - the place is unclear, or between two files;
  - the text is large: a new file, a new note, a section rewritten.
- **When the skill asks:** the questions are held for a natural pause,
  the end of a task or the close, and asked together. A correction from
  the user is proposed at once, since it changes the work of the same
  session.
- **Each proposal:** what would be added, where, the cost when the file
  is read at each start, and two or three options (this place, a
  cheaper place, nothing).

The close routine gains a step: the held proposals, asked in one
message before the snapshot is written.

### 3. The review of the memory

Two parts. The form belongs to the skill, because only the skill has
the current templates. The content belongs to the folder, so that it
runs without the skill.

**The form**, run by `/total-recall` on an existing folder, as an
extension of the check mode of step 2:

1. The missing files, added by the repair as today, `review.md` and
   `obsolete.md` among them.
2. The routine files that differ from the current templates
   (`rules.md`, `close.md`, `lifecycle.md`, `review.md`, the tools):
   the difference shown, the replacement proposed file by file.
   `rules.md` is replaced whole, since the project file adds to it and
   does not edit it. `close.md` and `lifecycle.md` may hold the
   project's own edits: the difference is shown and the user chooses.
3. `decisions.md` in the current form: entries newest first, numbered
   `D1`, `D2` in the order they were taken. The render script gains a
   `--migrate-decisions` mode that rewrites the file in a copy, and the
   copy is shown before it replaces the file.
4. Then the skill offers the content review.

**The content**, `review.md`, a routine of the folder, started by
"review the memory" in the project file:

1. Read the whole folder. Living documents can be rewritten:
   `CLAUDE.md`, `rules.md`, the memory notes, `plan.md`, `state.md`,
   `lifecycle.md`, `close.md`, `review.md`, `code-map.md`, the open
   phase file. Records are not rewritten: `history.md`, `story.md`,
   closed phase files, `records/`.
2. Look for:
   1. contradictions: both statements, their dates and places, the
      proposal of the one that wins (usually the newer); the user always
      chooses;
   2. duplicates: the fact stays in the file that owns it, the other
      place links to it;
   3. out of date: a file, a task or a state named that no longer
      exists, checked against the tree;
   4. misplaced: text read at each start that is rarely needed, moved to
      a file read when it applies;
   5. replaced decisions: moved to `obsolete.md`.
3. Write the report in `records/YYYY-MM-DD-review.md`: numbered items
   grouped by kind, each with the current text, the proposed text and
   the reason, and the size read at each start before and after.
4. The user answers by number ("all", "all but 3", "1 and 4"). A
   contradiction always needs the user's choice. The others can be
   approved together.
5. Apply the approved items, run `tools/doc-check.py`, report the new
   size.

**When it runs:** on demand, by the phrase. The close suggests it in
one line, without starting it, when a reason exists: the size read at
each start is over the limit of the project file, a contradiction was
found in the session, or a phase is closing.

**The size limit:** a line of `CLAUDE.md`, "The size read at each
start", 8,000 words by default. `tools/doc-check.py` reports the size
and warns over the limit.

### 4. The decisions and `obsolete.md`

- `decisions.md`: newest first, each entry `## D12, 10/10/2026: <name>`,
  then what was decided, on whose word, why. The file holds only the
  decisions in force.
- A decision replaced by a newer one moves whole to `obsolete.md`,
  newest first, with a line under its title: `Replaced by D14 on
  10/10/2026.` The new decision names the one it replaces and restates
  the part that still holds.
- `history.md` stays newest first. `story.md` stays oldest first: it is
  a diary, read as a story.
- `tools/doc-check.py` checks the order and the numbers of both files,
  and the "Replaced by" line of each obsolete entry.
- `lifecycle.md` and the table of documents gain `obsolete.md`.

### 5. The README

- Rewritten for readers who do not know the project: what the skill
  is, why it exists and its limits in the first person and the past
  tense, the install and the use in neutral instructions, by the rules
  of `memory/user-writing-style.md`. No sentence about the voice.
- Each path in backticks: `internal-<project-name>/CLAUDE.md`. The
  name `<project-name>` replaces `<folder>` in the README, `SKILL.md`
  and the templates.
- It describes the review and the question on git.

## The tests

Each change of behavior starts with a failing test, by `rules.md`.

- `test_package.py`: `SKILL.md` asks the git question in step 5; no
  template or README sentence states that the folder is out of git;
  `review.md` and `obsolete.md` are in the templates and in the table
  of documents; the README has no `<` outside backticks.
- `test_render.py`: the repair adds `review.md` and `obsolete.md`;
  `--migrate-decisions` reorders and numbers a sample file in a copy,
  keeps each entry's text, and leaves the original untouched.
- `test_doc_check.py`: decisions out of order, a missing number, an
  obsolete entry without its line, a size over the limit.
- The sample render reads clean with `tools/doc-check.py`.

## The cost

About two sessions: one for items 1, 4 and 5, one for items 2 and 3.
Then this project's folder is brought to the new form by the review
itself, as its first real run, with the docs updated to the user's
choice on git.
