# Code map

Where the work of each phase lives in the tree, newest phase first. An
entry per delivered task that touched code is added at each close, with
the commit it describes, and the section of a phase is rewritten at its
close. Read it when the work touches code, before exploring the code.
Check a claim when the code contradicts it, or when `git log` on the
files since the commit named shows changes.

## Phase 02

No code: Task 17 (`f1bf102`) changed the templates
(`skill/templates/memory/user-writing-style.md`, new; the memory index;
`rules.md`) and the package test (`test_the_style_note_is_in_the_index_and_pointed_to_by_the_rules`).

## Phase 01

The package as first built is commit `aca0d06`. The fixes of the review
(Task 12: `needs_of`, `check_templates`, `plan_repair` and the
`--repair` option of `render.py`; the UTF-8 guard and the header rule of
`check_documents_table` in `doc-check.py`; the quoting of the tools
README; step 2 of `SKILL.md`) are uncommitted at the close of the
phase. The names are those of the tree on 07/10/2026.

- Task 4: `skill/templates/tools/doc-check.py` (`find_dashes`,
  `find_list_breaks`, `check_documents_table`, `check_tasks`,
  `check_done_steps`, `check_state`, `check_history`, `check_memory`,
  `check_folder`, `main`), `tests/test_doc_check.py` (the classes
  `TextRules` and `FolderRules`, the helper `make_folder`, the minimal
  folder `MINIMAL`).
- Task 5: `skill/templates/tools/machine-check.py` (`read_json`,
  `deny_list`, `bash_hooks`, `script_of`, `report`, `render_table`,
  `main`), `tests/test_machine_check.py`.
- Task 6: `skill/scripts/render.py` (`PLACEHOLDERS`, `placeholders_in`,
  `render_text`, `template_files`, `plan`, `write`, `main`),
  `tests/test_render.py`, `tests/test_package.py` (the classes
  `WritingRules`, `SkillStructure`, `MachineFolder`).
- Task 9: `skill/machine/settings-guardrails.json`,
  `skill/machine/hooks/` (`bash-guard.sh`, `git-guard.sh`,
  `guard-lib.sh`, copies of the machine's own).
- Tasks 7, 8, 10: the templates under `skill/templates/`, `skill/SKILL.md`,
  `README.md`, `.gitignore`.
