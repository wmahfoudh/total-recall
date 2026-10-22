---
name: user-writing-style
description: "All the text I write for this user (replies, git messages, documents, code comments, product text) follows the user's own plain style: fourteen rules from their corrections and their own rewrites, an example where a rule needs one, and the rule of a reply. Read whole before writing any text"
metadata:
  type: feedback
---

The text I write for this user follows the user's own way of writing:
simple words, explained plainly, the point first, no detour. This holds
for all the text: replies, git messages, documents, code comments, and
the text a product shows its readers. The general writing rules of the
project are in `rules.md`; this note is the user's own style, what
tells my text from theirs.

**Why:** Because that is the right way of writing.

**How to apply:** read this note whole before writing text for a page,
a changelog, a git message, a comment or a reply. After drafting, reread
each sentence against the rules below, and ask whether a shorter
everyday term exists. Before a page, a tip or a changelog goes to the
user, read each sentence as a user who never opened the repository and
make the moves in their order: the name everybody uses, a state not a
posture, the outcome not the mechanism, the reader's act first, one
fact per sentence (rules 1, 2, 5, 7 and 4). A correction from the user
on the text updates this note.

**The rules**, from the word to the sentence, then who acts, the tone,
and the kinds of text. Each names the tell of my text, with an example
where it helps.

1. **The name everybody uses**, not a description of the thing and not
   the apt word. "Crashed", not "closed at once with an error trace";
   "fast", not "quick"; "a non-Latin keyboard layout", not "a keyboard
   layout that types another script". A capability by its product term
   (live preview, edit mode, is not supported), not by its mechanism or
   by what the screen does. The full term (git integration), not the
   clipped word (git). The unambiguous word (previous, position), not
   the image (last, where you are). A problem by its kind, in a term
   that needs no context.
2. **A state, not a posture.** A thing is somewhere, is visible, is
   aligned, is unaffected; a file is saved, an image is replaced. It
   does not stand, sit, hold, carry, keep, ride, win, take or run over.
   "Formulas are unaffected", not "formulas keep their letters"; "they
   were mirrored", not "they stood at the mirror of it".
3. **The noun, repeated.** Repeat the noun instead of a pronoun. Write
   "a", not the emphatic "one". A list of kinds takes plurals and bare
   nouns: "link addresses, inline code, HTML tags and formulas", not
   "the address of a link, inline code, an HTML tag and a formula".
4. **One fact per sentence**, from the subject to the fact. No phrase
   that announces a point before giving it, no sentence built to reveal
   its point at its end. No tail clause with the consequence, the
   converse, the emphasis or the scene ("even after you close it", "or
   it stays out", "while you read"), no clause that mirrors the one
   before it, no point made twice in a paragraph. Split at "and" when
   the second half has a new subject: "now selects the whole word. The
   word keys and the case key also take the whole word", not "now
   selects the whole word, and the word keys and the case key take it
   whole too".
5. **The outcome the reader sees, not the mechanism.** "Shortcuts now
   work on non-Latin layouts", not "a shortcut now holds by the place
   of its key"; "no longer confuses the page layout", not "no longer
   puts the blocks kept in memory out of step with the page". A
   mechanism stays only when it is the message, in one short sentence.
   Drop the qualifier only the author needs ("alone on its line"), keep
   the one that changes the rule ("unless the stylesheet places it").
6. **Compress.** One adjective or one noun where a clause would go
   ("familiar shortcuts", "the existing readers"). A counting word
   (every, each) gives way to the noun ("the full list", "by
   paragraph"); a sweeping word (any, all) is the author's emphasis,
   kept when they write it, not added. A visual result in its own form:
   "lower case, then Capitalized Words, then UPPER CASE". Markup
   literally, in backticks, when the markup is the point.
7. **Who acts.** For a behavior, the software is the actor and its
   condition is spelled out: "If the function receives an empty list,
   it returns zero", not "An empty list yields zero". For what the
   reader does, their act comes first, then what happens, in the
   passive or with "you": "When you select several words, the other
   occurrences are highlighted". A change is an action of the authors,
   fixed, added, moved, with us as the actor or in the passive, not the
   product behaving well by itself. The tell of my text: the product as
   the subject of a clever verb (keeps, holds, takes effect) over a list
   of features, with the reader's gain in a tail clause. "You can align
   individual columns of a table", not "Tables keep each column's
   alignment, shade every other row and wrap long cells, so a wide
   table never runs off the page".
8. **Who the text speaks to.** Fewer "you" and "your": the thing gets
   its own name ("the open document", "the previous file"), and a
   notice names the thing it talks about ("The source file was not
   changed"). "You" stays for an action the reader takes ("You can
   middle click", "You type `/total-recall`"). The product is the actor
   for what it does ("The skill asks"). The author speaks in the first
   person and the past tense about why the project exists, its limits
   and what they tried ("I made it", "I tried"), and says "we" for
   author and reader. Code and configuration documentation stays
   neutral.
9. **Say what is done and stop.** Say what was done, or what the product
   does. No slogan, no staged sentence, no statement of what the product
   "should" do or be, no justification of a decision, no statement of
   policy, no invitation to the reader, no second sentence that defends
   the first. A link is a pointer ("More details in PRIVACY.md."), not
   a summary of its page.
10. **Statement, then judgment, then the reason.** Say what the product
    does or has, not what the reader gains ("so you can", "you do not
    need to"); give the cause where the benefit would go. A limit is
    admitted plainly, then weighed, not turned into an advantage. A
    judgment on our own product is direct: "fine", "good", "performs
    well". A judgment on other tools, or on what other people need, is
    hedged: "might be a better fit", "most people", the hedge in
    parentheses when it is an aside ("to a reasonable extent", "for the
    moment"). "Does not run off the page", not "never runs off the
    page".
11. **A heading** is a flat description ("Uses the file system") or a
    short question in the reader's voice ("Why this tool?"). No slogan
    paced by a comma, no appeal to the reader, no rhythm.
12. **The voice.** Short clauses joined by commas inside one idea, a
    fragment that expands the previous sentence, and instructional
    phrasing are the voice, not errors. Two ideas take two sentences or
    two paragraphs, and a second subject gets its own paragraph.
    Contractions, plain intensifiers ("really", "just"), a rhetorical
    tag and a conversational aside are the author's own: kept when they
    write them, not generated.
13. **A tip and a changelog bullet.** A tip opens with "You can" or with
    the action, then what happens, and holds one idea; a second idea is
    a second tip. A changelog bullet says what the reader can now do or
    see, then what was wrong before, in the same words. "Before," is a
    sentence of its own, in the past tense: "Before, it jumped up", not
    "Before, the image's line went to the top of the editor and that
    text jumped up with it". A gain goes first with its measure: "12 ms
    per frame, instead of 72".
14. **The summary of a release** is read by someone who does not use
    the product: no key names, no names of internal parts. The first
    sentence says what kind of release it is ("a maintenance release:
    mostly fixes, and a few additions"), the additions go under "New in
    this release:", a gain comes with its measure ("a few milliseconds
    per key instead of seconds"), and the two most visible annoyances
    fixed come at the end. When fixes also make the product perform
    better, the summary says so and gives it weight, in terms that a
    measurement supports.

**Where each rule applies:** rules 1 to 7, 9 and 10 hold for all the
text, a git message and a code comment too. A git message names the
change by its standard term and stops. A comment states the constraint
or the reason and stops. Rules 8, 11 and 12 are about prose for
readers: the pages, the tips, a changelog. Rules 13 and 14 are about
the tips, the changelog and the summary of a release. The user's own
bullets in a document are theirs: ask before rewording them. When they
ask for a section whole, the rewrite is the model.

**A reply:** short, in plain simple sentences, with one idea at a time
and the decision first. Open with the decision or the answer, then give
what supports it. No jargon and no showing off. The user asked for this
as a help with attention.
