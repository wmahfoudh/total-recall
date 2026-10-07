# Tools

The scripts of the project, each with its use. A new script gets its
line here in the same session.

| Script | Use |
|---|---|
| `doc-check.py` | `python3 {{internal}}/tools/doc-check.py {{internal}}` checks the documents of the folder: the files named in the table of `CLAUDE.md` exist, no dash character, a blank line before each list and table, the task numbers grow and repeat nowhere, a ticked step has its date, `state.md` under 150 lines, the history titles, the memory index. Run at each close |
| `machine-check.py` | `python3 {{internal}}/tools/machine-check.py` reports the guardrails of the machine: the global rules file, the permission deny list, the guard hooks, `jq`, the sandbox. Run on a new machine |
