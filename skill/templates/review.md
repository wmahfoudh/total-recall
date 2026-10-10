# The review of the memory

Read when the user says "review the memory". The review reads the whole
folder, writes a report of the changes it proposes, and applies the
ones the user approves. Nothing is changed before the user approves the
report.

## What it reads

- Living documents, which the review may rewrite: `CLAUDE.md`,
  `rules.md`, the memory notes, `plan.md`, `state.md`, `decisions.md`,
  `lifecycle.md`, `close.md`, `review.md`, `code-map.md` and the open
  phase file.
- Records, which the review does not rewrite: `history.md`, `story.md`,
  `obsolete.md`, the closed phase files and `records/`. They are read
  for the dates and the facts.

## The steps

1. Run the check with the size:

   ```
   python3 "<internal folder>/tools/doc-check.py" --size "<internal folder>"
   ```

   Note the size read at each start and the findings.

2. Read the whole folder and look for five kinds of items:
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
3. Write the report in `records/YYYY-MM-DD-review.md`. List the name
   first, and add `-2` for a second review on the same day. The report
   gives the size before, then the items numbered from 1, grouped by
   kind. Each item gives the file and the heading, the current text,
   the proposed text and the reason.
4. Show the report in the reply, a line per item, and ask the user to
   answer by number: "all", "all but 3", "1 and 4". A contradiction is
   settled only by the user's choice. The other items can be approved
   together.
5. Apply the approved items. A replaced decision moves whole to the top
   of `obsolete.md`, with the line `Replaced by Dn on DD/MM/YYYY.`
   under its title, and the newer decision names it.
6. Add the report to `records/README.md`, run the check with the size
   again, and fix what it reports.

## The reply

The items applied and the items left, a line each, the size before and
after, and the last line of the check.
