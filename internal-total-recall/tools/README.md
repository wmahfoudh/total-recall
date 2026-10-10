# Tools

The scripts of the project, each with its use. A new script gets its
line here in the same session.

| Script | Use |
|---|---|
| `doc-check.py` | `python3 "internal-total-recall/tools/doc-check.py" "internal-total-recall"` checks the documents of the folder: the files named in the table of `CLAUDE.md` exist, no dash character, a blank line before each list and table, the task numbers grow and repeat nowhere, a ticked step has its date, `state.md` under 150 lines, the history titles, the memory index, the decisions numbered and newest first, each obsolete decision with its "Replaced by" line and the most recently replaced first, the size read at each start under the limit of `CLAUDE.md` (`--size` prints it). Run at each close |
| `machine-check.py` | `python3 "internal-total-recall/tools/machine-check.py"` reports the guardrails of the machine: the global rules file, the permission deny list, the guard hooks, `jq`, the sandbox. Run on a new machine |
