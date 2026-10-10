# The total-recall story

A journal of how total-recall is being made, kept as short stories
rather than a changelog. Each entry stands alone, is dated, and is
written in my voice at the close of a session, about the debates, the
decisions and the wrong turns, not the technical detail. The technical
log is `history.md`. New entries go at the end.

## 07/10/2026: a memory for the memory

I had a memory system that worked. Thirty seven phases of another
project ran on it, and I know what it saved me. I also knew what was
wrong with it: a plan file of a million bytes, a snapshot that had
grown seventy guardrails nobody promoted, and a trick with a memory
note so that the rules would load at all. Today I asked for a skill
that installs the good part on any project, and I asked for the bad
part to be challenged, not copied.

The first proposal came back with a `CLAUDE.local.md` at the root. No.
The whole point is that a stranger reading the repository sees a folder
called internal and nothing else. Then a file under `.claude/`. No
again, I don't want to depend on a setting that lives on one machine. We
ended with the plainest answer: the folder loads itself when it is read,
and "read the file" is a fine way to open a session.

The idea I liked most came from a small objection. Work done between
phases had no number. The fix was not a rule for the gap, it was no
gap: a project always has an open phase. Twelve changes like that, each
with its reason, and the session argued back on a few of them. Good.

The build went test first, and the tests caught the session twice: a
line number off by one, and a cache file that slipped into the
templates. The dashes were the funny one. The plan said no dash
characters anywhere, and the tool that wrote the plan turned the escape
codes into the characters themselves. We spelled them in code instead.

Then a reviewer I had never met read the whole thing. No disasters,
four things worth fixing, and the one that mattered was a path I had
not walked: run the skill a second time on a folder that already
exists, and it could have written a second first phase. Fixed with a
test, like the rest.

Tomorrow I try it on a scratch repository, and I will take notes. That
is what Phase 02 is for.

## 10/10/2026: one yes

I came back with three notes and left with a second version of the
skill. The notes were small: ask me about git, use the memory with
care, write a README a stranger can read. The care part grew. Memory
is precious, so the skill now asks only when a line will be read in
every session, and keeps the rest quiet.

Then I asked the skill to review its own project, and it missed the
memory folder. It also missed that the tests named the project I swore
never to name. Not a slip of the session: the routine never told it to
look there. We fixed the routine, not the run.

The best moment was the stupid one. The update showed me differences
and handed me five copy commands to type, for files that are not even
mine. I said stop. Now there is a backup folder, and an update is one
yes. The skill ran it on itself, reviewed itself, and the folder reads
clean.

## 10/10/2026, later: what a start costs

I asked for an exploration, no code. It came back with six points, and
the first one stopped me: each session starts by reading six thousand
words of my own rules and notes. Most of it is the template, the same
in every project. My memory is not free.

So I asked what other people do. Caveman makes the replies short, and
the replies are the cheap part. Its sibling compresses the memory
files, and that is where the cost is. Ponytail asks the model to write
less code. The idea we kept is the plainest: a small script that prints
the part of the plan a start needs, the same trick as the check tool.

I closed Phase 02 without the trial on a scratch repository. The
backup works, the update already ran on this folder, good enough. Phase
03 is called Optimization, and it starts with a number to beat.

## 11/10/2026: read twice

I dropped the tokens first. Words are enough to compare, and I did not
want a measure that needs me in a fresh session each time.

The design of the script brought the real find. Claude Code loads the
rules of the folder by itself as soon as a session reads a file there,
and my own routine told it to read them again. Three and a half
thousand words, each start, since the first day. Nobody had looked,
because the routine looked right.

The script itself is small: the snapshot, the notes, the head of the
plan, the current task. The tests went red first, then green, and the
sample render caught a note that still said to read the rules whole.
The next start is the trial. If it opens the rules again, we will know.

## 11/10/2026, later: the end of Optimization

The trial passed, the rules were read once. Then Claude told me the
global file never said where the folder is. "let's start" worked
because the session went looking. One line in the global file fixed
it, and the install now offers the same line to anyone.

Half the tasks ended with nothing, and that was fine. The compressed
copy of the rules would have taught Claude the shorthand the rules
forbid. The start levels could not skip the rules, Claude Code loads
them anyway.

Claude also got things wrong. It said the skill link was missing, from
a listing cut at ten lines, and its link command made a loop inside the
skill. It left a box unticked, and the start script pointed at an old
task. Each slip was found and said plainly.

The number I wanted: 5,566 words a start, from ten to fourteen
thousand. Next, the minors, before a second project.
