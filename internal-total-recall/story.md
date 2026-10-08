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
