# Code map

Where the work of each phase lives in the tree, newest phase first. An
entry per delivered task that touched code is added at each close, with
the commit it describes, and the section of a phase is rewritten at its
close. Read it when the work touches code, before exploring the code.
Check a claim when the code contradicts it, or when `git log` on the
files since the commit named shows changes.

## Phase 04

The names are those of the tree on 11/10/2026.

- Task 45 (`e01301f`): `mapping`, `listing`, `matches_bash`,
  `bash_hooks` and `script_of` in
  `skill/templates/tools/machine-check.py`; the answer checks of `plan`
  in `skill/scripts/render.py`; `find_list_breaks`, `OPEN_STEP_RE`,
  `check_done_steps`, `HISTORY_TITLE_RE` and the `utf-8-sig` reads in
  `skill/templates/tools/doc-check.py`; steps 1, 2, 5 and 7 of
  `skill/SKILL.md`; `skill/templates/state.md`; ten tests across
  `tests/test_machine_check.py`, `tests/test_render.py` and
  `tests/test_doc_check.py`.

## Phase 03

The names are those of the tree on 11/10/2026.

- Task 40 (`a0d3281`): `START_LINE`, `START_MARKER` and the row
  "start phrases" in `skill/templates/tools/machine-check.py`; step 8
  and 9 of `skill/SKILL.md`; the class `StartPhrases` of
  `tests/test_package.py`, two tests of `tests/test_machine_check.py`.
- Task 39 (`f9d0d2c`): the comment on the wording checks at the top of
  `tests/test_package.py`.
- Task 37 (`008bde2`): `TEMPLATE_NAMES` and `destination_of` in
  `skill/scripts/render.py`; `skill/templates/CLAUDE.template.md`, the
  template project file; the template note `project-instruction-file`
  deleted; two tests of `tests/test_render.py`, three of
  `tests/test_package.py`.
- Task 33 (`06a7077`, `6c4354d`, `5f844b2`, `798e5df`):
  `skill/templates/tools/start.py`, new (`open_phase`, `sections`,
  `items`, `plan_head`, `tasks`, `current_task`, `preamble`,
  `start_text`, `StartError`, `main`); `start_script`, `words_of` and
  `start_size` in `skill/templates/tools/doc-check.py`;
  `ROUTINE_FILES` in `skill/scripts/update.py`; the start routine of
  `skill/templates/CLAUDE.template.md`; `tests/test_start.py`, new, the class
  `StartSize` of `tests/test_doc_check.py`.

## Phase 02

The names are those of the tree on 10/10/2026.

- Task 29 (`03f1d12`, `e2f9edc`): `skill/scripts/update.py`, new
  (`is_total_recall`, `backup`, `decisions_to_migrate`, `plan_update`,
  `apply_update`, `print_plan`, `main`), `render.present` in
  `skill/scripts/render.py`, `tests/test_update.py` (the classes
  `Backup` and `Update`), the class `BackupAndUpdate` of
  `tests/test_package.py`.
- Task 28 (`c3eee97`): `tests/test_package.py`, `FORBIDDEN_HASHES`,
  `HOME_PATH`, `forbidden_words`.
- Tasks 20 to 27: templates and text, with the classes `GitQuestion`,
  `WhenToAsk`, `Review`, `Readme`, `AnotherSystem` of
  `tests/test_package.py` and `RealTemplates` of `tests/test_render.py`.
- Task 19 (`9201de6`): `skill/scripts/render.py`, `split_decisions`,
  `migrate_decisions`, `run_migration`, the option
  `--migrate-decisions`; the class `MigrateDecisions` of
  `tests/test_render.py`.
- Task 18 (`d64cf13`): `skill/templates/tools/doc-check.py`,
  `check_decisions`, `start_size`, `size_limit`, the option `--size`.
- Task 17 (`f1bf102`): the templates
  (`skill/templates/memory/user-writing-style.md`, new; the memory
  index; `rules.md`) and the package test
  (`test_the_style_note_is_in_the_index_and_pointed_to_by_the_rules`).

## Phase 01

The package as first built is commit `aca0d06`. The fixes of the review
(Task 12: `needs_of`, `check_templates`, `plan_repair` and the
`--repair` option of `render.py`; the UTF-8 guard and the header rule of
`check_documents_table` in `doc-check.py`; the quoting of the tools
README; step 2 of `SKILL.md`) are commits `3d49152` and `45ed75f`.
The names are those of the tree on 07/10/2026.

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
