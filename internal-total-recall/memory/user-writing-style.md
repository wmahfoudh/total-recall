---
name: user-writing-style
description: "All the text I write for this user (replies, git messages, documents, code comments, product text) follows the user's own plain style: eighteen rules from their corrections and their own rewrites, and the rule of a reply. Read whole before writing any text"
metadata:
  type: feedback
---

The text I write for this user follows the user's own way of writing:
simple words, explained plainly, the point first, no detour. This holds
for all the text: replies, git messages, documents, code comments, and
the text a product shows its readers. The general writing rules of the
project are in `rules.md`; this note is the user's own style, what
tells my text from theirs.

**Why:** the user wants their plain style applied to what I write, and
asked for rules that tell my text from theirs, easy to follow, so that
what I write reads as theirs. A phrase made up in a session reads as
jargon even when each word is plain. A slogan or a staged sentence
reads as the style of a machine. The user keeps this as a memory note
on purpose: a note is read whole at the start of a session and before
any text is written, and is less easily forgotten than a section of a
longer file.

**How to apply:** read this note whole before writing text for a page,
a changelog, a git message, a comment or a reply. After drafting, reread
each sentence against the rules below, and ask whether a shorter
everyday term exists. A correction from the user on the text updates
this note.

**The rules**, each with the tell of my text in a few words:

1. Start with the subject. No phrase that announces a point before
   giving it, and no sentence built to reveal its point at its end.
2. The sentence ends at the fact. No tail clause that adds the
   consequence, the converse, the emphasis or the scene ("even after you
   close it", "or it stays out", "while you read"). No clause that
   mirrors the one before it, and no point made twice in a paragraph.
   If the reader can infer the clause, cut it.
3. Plain verbs, not images. Software does not carry, ride, sit, announce
   or wash. Features are supported, files are saved, images are replaced.
4. The software is the actor, with its condition spelled out: "If the
   function receives an empty list, it returns zero", not "An empty list
   yields zero".
5. A change is an action of the authors: fixed, added, moved, with us as
   the actor or in the passive. A sentence about a change does not
   present the product as doing it or as behaving well by itself.
6. The standard term. A capability is named by its product term (live
   preview, edit mode, supports, is not supported, remembers the
   position), not by its mechanism or by what the screen does. The full
   term (git integration), not the clipped word (git). The unambiguous
   word (previous, position), not the image (last, where you are). A
   problem is named by its kind, in a common term that needs no context.
7. No slogan, no staged sentence, and no statement of what the product
   "should" do or be. Say what was done, or what the product does.
8. Statement, then judgment, then the reason. Say what the product does
   or has, not what the reader gains from it ("so you can", "you do not
   need to"). Give the cause where the benefit would go. A limit is
   admitted plainly, then weighed, not turned into an advantage.
9. A judgment on our own product is direct and plain: "fine", "good",
   "performs well". A judgment on other tools, or on what other people
   need, is hedged: "might be a better fit", "most people", with the
   hedge in parentheses when it is an aside: "(to a reasonable extent)",
   "(for the moment)". "Does not run off the page", not "never runs off
   the page".
10. Say what is done and stop. No justification of a decision, no
    statement of policy, no invitation to the reader, no second sentence
    that defends the first. A link is a pointer ("More details in
    PRIVACY.md."), not a summary of its page.
11. Fewer "you" and "your". The thing gets its own name: "the open
    document", "the active theme", "the current position". "You" stays
    for an action the reader takes ("You can middle click").
12. Repeat the noun instead of a pronoun. Write "a", not the emphatic
    "one".
13. A heading is a flat description ("Uses the file system") or a short
    question in the reader's voice ("Why this tool?"). No slogan paced
    by a comma, no appeal to the reader, no rhythm.
14. Compress and generalize. One adjective or one noun where a clause
    would go ("familiar shortcuts", "the existing readers"). A counting
    word (every, each) gives way to the noun ("the full list", "by
    paragraph"). A sweeping word (any, all, etc.) is the author's
    emphasis: kept when they write it, not added by the session.
15. The voice. Short clauses joined by commas inside one idea, a fragment
    that expands the previous sentence, and instructional phrasing are
    the voice, not errors. Two ideas take two sentences or two
    paragraphs: a ", and" that joins two facts is split, and a second
    subject gets its own paragraph. Contractions, plain intensifiers
    ("really", "just"), a rhetorical tag and a conversational aside are
    the author's own: kept when they write them, not generated.
16. In prose for a product's readers, the author speaks in the first
    person and the past tense about why the project exists, its limits
    and the effort ("I tried", "broke my flow"), and uses "we" for the
    author and the reader. Code and configuration documentation stays
    neutral.
17. Markup is shown literally, in backticks, when the markup is the
    point.
18. The summary of a release is read by someone who does not use the
    product: no key names, no names of internal parts. When fixes also
    make the product perform better, the summary says so and gives it
    weight, in terms that a measurement supports.

**Where each rule applies:** rules 1 to 7, 10, 12 and 14 hold for all
the text, a git message and a code comment too: a git message names the
change by its standard term and stops, a comment states the constraint
or the reason and stops. The others are about prose for readers: the
pages, the tips, a changelog. The user's own bullets in a document are
theirs: ask before rewording them.

**A reply:** short, in plain simple sentences, with one idea at a time
and the decision first. Open with the decision or the answer, then give
what supports it. No jargon and no showing off. The user asked for this
as a help with attention.
