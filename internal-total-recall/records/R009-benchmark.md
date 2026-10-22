# The cost of a start, at the end of Phase 03

Measured 11/10/2026, Task 43, in words, by the method of
`2026-10-10-baseline.md`. Tokens are not measured, the user's word.

## The files measured

The folder and the templates as committed in `b1b1c97`, with Task 43
open in Phase 03.

## The method

- `wc -w` on each file read at each start, as in the baseline.
- `python3 internal-total-recall/tools/doc-check.py --size internal-total-recall`
  for the total the tool reports. Since D22 the tool counts `CLAUDE.md`,
  `rules.md` and the output of `tools/start.py`.

## The words of the files read at each start

| File | Template before | Template now | Project before | Project now |
|---|---|---|---|---|
| `rules.md` | 2,585 | 2,426 | 2,585 | 2,426 |
| `memory/user-writing-style.md` | 1,157 | 1,139 | 1,157 | 1,139 |
| `CLAUDE.md` | 690 | 735 | 932 | 977 |
| `plan.md` | 115 | 130 | 742 | 546 |
| `state.md` | 94 | 94 | 281 | 242 |
| Other memory notes and index | 213 | 37 | 510 | 334 |
| **Total** | **4,854** | **4,561** | **6,207** | **5,664** |

The template `CLAUDE.md` is `CLAUDE.template.md` since D26. The files
alone went down by 293 words in the template and 543 in this project.

## What a start reads

The baseline counted the files and left out two parts found later: the
rules read twice (D22) and the phase file, read from its preamble to
the whole file. The start now reads `CLAUDE.md` and `rules.md` once,
loaded by Claude Code, and the output of `start.py`, which prints the
parts a start needs.

| Part | Before, 10/10/2026 | Now |
|---|---|---|
| `CLAUDE.md` and `rules.md` | 7,034, read twice | 3,403, once |
| `state.md` and the memory notes | 1,948 | 1,715 |
| `plan.md` | 742, whole | 106, the goal and the head of the Roadmap |
| The phase file | 298 to 4,167 | 311, the preamble and the current task |
| **Total** | **10,022 to 13,891** | **5,566**, by `doc-check.py --size` |

The parts of the right column add up to 5,535. The other 31 words are
the headings the script prints between the parts. `doc-check.py --size`
reports `read at each start: 5566 words, limit 8000`. The global rules
file of this machine, 2,052 words, is loaded on top, before and now.

## What changed the figures

| Task | Change | Words |
|---|---|---|
| 33 | The start script, the rules read once | about 3,500 a start, and the plan and phase parts |
| 34 | The repeats between `rules.md` and the style note | 177 |
| 37 | The goal pointer, the note `project-instruction-file` | 271 here, 199 in a sample render |
| 37 | `CLAUDE.template.md` | about 3,200 in a session here that touches the templates |
| 38 | The close reads the tasks of the session | at each close, not at the start |

Tasks 35, 36, 39, 41 and 42 ended without a change to the start. Task
40 added nothing to the start. It made a plain "let's start" find the
folder.
