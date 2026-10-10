# The close routine

Read when the user says "let's close", "docs routine", "documentation
routine" or "sync the docs". The routine runs without asking
permission, apart from the proposals of step 1. The user reads the
result.

## The steps

1. Ask the proposals held during the session in one message, by
   `rules.md`, "When to ask before a write", and write the approved
   ones. With no proposal held, go to step 2.
2. Rewrite `state.md` as a snapshot and nothing more: the position, the
   session just done, the next step, what waits on the user. Older
   sessions leave it, `history.md` has them. The file stays under about
   150 lines. What another file records is a pointer, not a copy.
3. In the open phase file, check that each piece of work of the session
   is under a numbered task, with its delivered steps ticked and dated.
   Work that no task planned is grouped into a few numbered tasks:
   `lifecycle.md`, "The numbers". For a code project, add an entry per
   delivered task that touched code to `code-map.md`, in the section of
   the open phase, with the commit it describes.
4. Clear the Roadmap in `plan.md`: an item delivered in full leaves it
   and the rest is renumbered. The Roadmap holds only what comes next.
   `history.md` keeps the record of what was delivered.
5. Add an entry at the top of `history.md`: the title
   `# DD/MM/YYYY - <meaningful name>`, a line of description, then short
   bullets of what was done. A second session on the same day adds a
   word after the date: `# DD/MM/YYYY, later - <name>`.
6. Append a dated entry to `story.md`: a narrative vignette in the
   user's voice, the size of a social media post, about the debates,
   decisions and wrong turns of the session, not its technical detail.
   Skip it only when the session gave nothing to tell.
7. Run the project's own close steps, listed in `CLAUDE.md` under "The
   project's own routines": a changelog, public pages, a check. Nothing
   at install.
8. Check `CLAUDE.md` against the project, sentence by sentence, and the
   memory notes with it: the index keeps a line per note, a stale fact
   is fixed, a note that became wrong is deleted, two notes on one topic
   are merged, and the folder stays around ten notes.
9. Run `python3 <internal folder>/tools/doc-check.py <internal folder>`
   and fix what it reports in the same close. It checks that each file
   named in `CLAUDE.md` exists, the dashes, the blank lines, the task
   numbers, the ticked steps, the length of `state.md`, the history
   titles and the memory index.
10. Suggest the review in one line when a reason exists: the check
    reports the size over the limit, a contradiction was found in the
    session, or a phase closes. The close does not start it.

## At a phase close

The close is the last task of the phase. Before it, each task is
delivered and the project's own checks of `CLAUDE.md` pass. The close
adds the close paragraph at the end of the phase file: the date, what
was delivered, what stays open. Then the next phase opens, named from
the head of the Roadmap, with its number, its name and its file, by
`lifecycle.md`, "Opening a phase". The user can rename it.

## The reply

The close changes several documents. The reply lists each file changed
and what changed in it, a line each, then the output of the check tool.
The close runs no git command.
