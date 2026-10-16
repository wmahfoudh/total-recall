# The review of the memory

Read when the user says "review the memory". The review reads the whole
folder, writes a report of the changes it proposes, and applies the
ones the user approves. Nothing is changed before the user approves the
report.

## What it reads

- Living documents, which the review may rewrite: `AGENTS.md`,
  `rules.md`, the memory notes, `plan.md`, `state.md`, `decisions.md`,
  `lifecycle.md`, `close.md`, `review.md`, `code-map.md` and the open
  phase file.
- Records, which the review does not rewrite: `history.md`, `story.md`,
  `obsolete.md`, the closed phase files and `records/`. They are read
  for the dates and the facts.

## The steps

1. List what this session decided or learned that the folder does not
   hold yet: the proposals held by "When to ask before a write" of
   `rules.md`, the decisions, the user's corrections, the rulings. They
   go first in the report, under "From this session", since the memory
   of a session is lost when its context is compacted or the session
   ends. In a contradiction, these items are the newest statements. A
   review that opens a session starts with an empty list.

2. Run the check with the size:

   ```
   python3 "<internal folder>/tools/doc-check.py" --size "<internal folder>"
   ```

   Note the size read at each start and the findings.

3. Read the whole folder and look for six kinds of items:
   1. Contradictions: two statements that disagree. Give both, with
      their dates and their places, and propose the one that wins,
      usually the newer.
   2. Duplicates: the same fact in two places. The fact stays in the
      file that owns it, and the other place links to it.
   3. Out of date: a file, a task or a state named that no longer
      exists. Check it against the tree before the item is written.
   4. Misplaced: text read at each start that a session needs rarely.
      Propose the file read when it applies.
   5. Replaced decisions: a decision of `decisions.md` that a newer one
      replaces.
   6. The memory notes: each note checked against the decisions in
      force and against the tree. A rule stated in a note ("never write
      X", "read only", "always do Y") is checked where it applies: a
      rule about the repository is checked across the repository, its
      tracked files included, and the report names the place found
      without the word that must not be written. A note that repeats a
      file read at each start is a duplicate. The index is matched with
      the notes.
4. Write the report in `records/YYYY-MM-DD-review.md`. List the name
   first, and add `-2` for a second review on the same day. The report
   gives the size before, the items from this session, then the items
   numbered from 1, grouped by kind. Each item gives the file and the heading, the current text,
   the proposed text and the reason.
5. Show the report in the reply, a line per item, and ask the user to
   answer by number: "all", "all but 3", "1 and 4". A contradiction is
   settled only by the user's choice. The other items can be approved
   together.
6. Apply the approved items. A replaced decision moves whole to
   `obsolete.md`, at its place by the date it was replaced, the top for
   a decision replaced today, with the line
   `Replaced by Dn on DD/MM/YYYY.` under its title, and the newer
   decision names it.
7. Add the report to `records/README.md`, run the check with the size
   again, and fix what it reports.

## The reply

The items applied and the items left, a line each, the size before and
after, and the last line of the check.
