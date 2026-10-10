import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "skill" / "templates" / "tools" / "machine-check.py"

DENY = ["Bash(sudo *)", "Bash(sudo)", "Bash(git commit*)", "Bash(git push*)",
        "Bash(dd *)", "Bash(mkfs*)", "Bash(shred *)"]


def run_tool(home, managed, path=""):
    env = {"PATH": path, "HOME": str(home)}
    return subprocess.run([sys.executable, "-I", str(TOOL), "--home", str(home),
                           "--managed", str(managed)], capture_output=True, text=True, env=env)


def rows_of(output):
    rows = {}
    for line in output.splitlines()[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[cells[0]] = (cells[1], cells[2])
    return rows


class MachineCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        (self.home / ".claude").mkdir(parents=True)
        self.managed = Path(self.tmp.name) / "managed.json"

    def tearDown(self):
        self.tmp.cleanup()

    def write_settings(self, data):
        (self.home / ".claude" / "settings.json").write_text(json.dumps(data), encoding="utf-8")

    def test_an_empty_machine_reports_everything_missing(self):
        result = run_tool(self.home, self.managed)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = rows_of(result.stdout)
        self.assertEqual(set(rows), {"global rules file", "start phrases", "deny list: git writes", "deny list: sudo",
                                     "deny list: destructive tools", "guard hooks on Bash", "jq", "sandbox"})
        self.assertTrue(all(status == "missing" for status, _ in rows.values()), rows)

    def test_a_settings_file_that_is_not_json_is_missing_not_a_crash(self):
        (self.home / ".claude" / "settings.json").write_text("{not json", encoding="utf-8")
        self.managed.write_text("", encoding="utf-8")
        result = run_tool(self.home, self.managed)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows_of(result.stdout)["deny list: sudo"][0], "missing")

    def test_the_deny_list_is_found_in_the_managed_settings(self):
        self.managed.write_text(json.dumps({"permissions": {"deny": DENY}}), encoding="utf-8")
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["deny list: git writes"], ("present", "managed settings"))
        self.assertEqual(rows["deny list: sudo"], ("present", "managed settings"))
        self.assertEqual(rows["deny list: destructive tools"], ("present", "managed settings"))

    def test_the_deny_list_is_found_in_the_user_settings(self):
        self.write_settings({"permissions": {"deny": DENY}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["deny list: git writes"], ("present", "~/.claude/settings.json"))

    def test_a_partial_deny_list_reports_what_is_missing(self):
        self.write_settings({"permissions": {"deny": ["Bash(git commit*)", "Bash(git push*)"]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["deny list: git writes"][0], "present")
        self.assertEqual(rows["deny list: sudo"][0], "missing")

    def test_the_rules_file_is_found(self):
        (self.home / ".claude" / "CLAUDE.md").write_text("# Rules\n", encoding="utf-8")
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["global rules file"][0], "present")

    def test_the_start_phrases_are_missing_from_a_global_file_without_the_line(self):
        (self.home / ".claude" / "CLAUDE.md").write_text("# My rules\n", encoding="utf-8")
        result = run_tool(self.home, self.managed)
        self.assertEqual(rows_of(result.stdout)["start phrases"][0], "missing")

    def test_the_start_phrases_are_found_by_the_path_of_the_project_file(self):
        line = 'In a project, "let\'s start" means: read `internal-<project-name>/CLAUDE.md`.\n'
        (self.home / ".claude" / "CLAUDE.md").write_text("# My rules\n\n" + line, encoding="utf-8")
        result = run_tool(self.home, self.managed)
        self.assertEqual(rows_of(result.stdout)["start phrases"][0], "present")

    def test_a_hook_counts_when_its_script_exists_and_runs(self):
        hooks = self.home / ".claude" / "hooks"
        hooks.mkdir()
        script = hooks / "git-guard.sh"
        script.write_text("#!/bin/sh\n", encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
        self.write_settings({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": "$HOME/.claude/hooks/git-guard.sh"}]}]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["guard hooks on Bash"], ("present", "~/.claude/settings.json: git-guard.sh"))

    def test_a_hook_whose_script_is_not_executable_is_missing(self):
        hooks = self.home / ".claude" / "hooks"
        hooks.mkdir()
        (hooks / "git-guard.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        self.write_settings({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
            {"type": "command", "command": "~/.claude/hooks/git-guard.sh"}]}]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["guard hooks on Bash"][0], "missing")

    def guard_script(self):
        hooks = self.home / ".claude" / "hooks"
        hooks.mkdir()
        script = hooks / "git-guard.sh"
        script.write_text("#!/bin/sh\n", encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IXUSR)

    def test_a_hook_is_found_in_the_forms_a_settings_file_may_use(self):
        self.guard_script()
        for matcher, command in (("Bash|Write", "$HOME/.claude/hooks/git-guard.sh"),
                                 ("*", "$HOME/.claude/hooks/git-guard.sh"),
                                 ("Bash", '"$HOME/.claude/hooks/git-guard.sh"'),
                                 ("Bash", "bash $HOME/.claude/hooks/git-guard.sh"),
                                 ("Bash", "sh ~/.claude/hooks/git-guard.sh --strict")):
            self.write_settings({"hooks": {"PreToolUse": [{"matcher": matcher, "hooks": [
                {"type": "command", "command": command}]}]}})
            rows = rows_of(run_tool(self.home, self.managed).stdout)
            self.assertEqual(rows["guard hooks on Bash"][0], "present", (matcher, command))

    def test_a_hook_on_another_tool_is_not_counted(self):
        self.guard_script()
        self.write_settings({"hooks": {"PreToolUse": [{"matcher": "Write|Edit", "hooks": [
            {"type": "command", "command": "$HOME/.claude/hooks/git-guard.sh"}]}]}})
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["guard hooks on Bash"][0], "missing")

    def test_a_settings_file_of_the_wrong_shape_is_missing_not_a_crash(self):
        for data in ({"permissions": "nope"}, {"permissions": {"deny": [{"a": 1}, 3]}},
                     {"hooks": {"PreToolUse": ["nope"]}}, {"hooks": {"PreToolUse": [{"hooks": ["x"]}]}},
                     {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "   "}]}]}},
                     {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "'open"}]}]}},
                     {"hooks": {"PreToolUse": [{"matcher": "(", "hooks": []}]}},
                     {"sandbox": "yes"}, [1], "text", 3):
            self.write_settings(data)
            result = run_tool(self.home, self.managed)
            self.assertEqual(result.returncode, 0, (data, result.stderr))
            rows = rows_of(result.stdout)
            self.assertEqual(rows["deny list: sudo"][0], "missing", data)
            self.assertEqual(rows["guard hooks on Bash"][0], "missing", data)

    def test_jq_is_looked_up_on_the_path(self):
        bin_dir = Path(self.tmp.name) / "bin"
        bin_dir.mkdir()
        jq = bin_dir / "jq"
        jq.write_text("#!/bin/sh\n", encoding="utf-8")
        jq.chmod(jq.stat().st_mode | stat.S_IXUSR)
        rows = rows_of(run_tool(self.home, self.managed, path=str(bin_dir)).stdout)
        self.assertEqual(rows["jq"], ("present", str(jq)))

    def test_the_sandbox_is_read_from_either_file(self):
        self.managed.write_text(json.dumps({"sandbox": {"enabled": True}}), encoding="utf-8")
        rows = rows_of(run_tool(self.home, self.managed).stdout)
        self.assertEqual(rows["sandbox"], ("present", "managed settings"))


if __name__ == "__main__":
    unittest.main()
