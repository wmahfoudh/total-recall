import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "skill" / "templates" / "tools" / "start.py"

PLAN = ("# P: the plan\n\n## Goal\n\nThe goal text.\n\n## Constraints\n\n- A constraint.\n\n"
        "## Roadmap\n\nOrdered. Intro text.\n\n"
        "1. **First item.** Its body line one\n   and its body line two.\n"
        "2. **Second item.** Second body words.\n"
        "3. **Third item.** Third body words.\n\n"
        "## Parked\n\n- **Parked item.** Parked body.\n\n"
        "## Blocked\n\nWhat waits.\n\n- **Blocked item.** Blocked body.\n\n"
        "The decisions are in decisions.md.\n")

PHASE = ("# Phase 02: second\n\nThe preamble text.\n\n**The order:**\n\n1. Task 3.\n\n"
         "### The opening of the phase\n\nNo opening step.\n\n"
         "### Task 2: done one\n\n- [x] **Step 1: a** b. Done 05/10/2026: ok.\n\n"
         "### Task 3: current one\n\nWhat it does.\n\n"
         "- [x] **Step 1: a** b. Done 06/10/2026: ok.\n- [ ] **Step 2: c** d.\n\n"
         "### Task 4: planned one\n\nPlanned text.\n\n"
         "**Checkpoint for the phase:** later.\n")

FOLDER = {
    "CLAUDE.md": "@rules.md\n\n# P\n\nClaude file text.\n",
    "rules.md": "# Rules\n\nRules file text.\n",
    "state.md": "# State\n\n## Position\n\n- Phase 02, open: `phases/phase-02-second.md`.\n",
    "memory/MEMORY.md": "- [Note](note.md): the index line\n",
    "memory/note.md": "---\nname: note\n---\n\nThe note text.\n",
    "plan.md": PLAN,
    "phases/phase-01-first.md": "# Phase 01: first\n\nOld preamble.\n\n### Task 1: old\n\n"
                                "- [x] **Step 1: a** b. Done 01/10/2026: ok.\n",
    "phases/phase-02-second.md": PHASE,
}


def load():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("start", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make(root, files):
    for name, text in files.items():
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class Start(unittest.TestCase):
    def setUp(self):
        self.start = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name) / "internal-p"

    def tearDown(self):
        self.tmp.cleanup()

    def output(self, changes=None):
        files = dict(FOLDER)
        files.update(changes or {})
        make(self.folder, files)
        return self.start.start_text(self.folder)

    def run_tool(self, *args):
        return subprocess.run([sys.executable, "-I", str(TOOL), *args], capture_output=True, text=True)

    def test_the_open_phase_is_the_file_with_the_highest_number(self):
        make(self.folder, FOLDER)
        self.assertEqual(self.start.open_phase(self.folder).name, "phase-02-second.md")

    def test_each_part_is_headed_with_its_file(self):
        out = self.output()
        for heading in ("==> state.md <==", "==> memory/MEMORY.md <==", "==> memory/note.md <==",
                        "==> plan.md", "==> phases/phase-02-second.md"):
            self.assertIn(heading, out)

    def test_the_state_and_the_notes_are_printed_whole(self):
        out = self.output()
        for text in ("## Position", "phases/phase-02-second.md", "the index line", "name: note", "The note text."):
            self.assertIn(text, out)

    def test_the_project_file_and_the_rules_are_left_out(self):
        out = self.output()
        self.assertNotIn("Claude file text.", out)
        self.assertNotIn("Rules file text.", out)

    def test_the_plan_gives_the_goal_the_first_item_in_full_and_the_titles(self):
        out = self.output()
        for text in ("The goal text.", "Its body line one", "and its body line two.",
                     "Second item.", "Third item.", "Blocked item."):
            self.assertIn(text, out)
        for text in ("A constraint.", "Intro text.", "Second body words.", "Third body words.",
                     "Parked item.", "Blocked body.", "The decisions are in"):
            self.assertNotIn(text, out)

    def test_the_phase_gives_the_preamble_and_the_current_task(self):
        out = self.output()
        for text in ("The preamble text.", "### Task 3: current one", "What it does.", "**Step 2: c** d."):
            self.assertIn(text, out)
        for text in ("Old preamble.", "No opening step.", "Task 2: done one", "Task 4: planned one",
                     "Planned text.", "Checkpoint for the phase"):
            self.assertNotIn(text, out)

    def test_without_an_open_step_the_current_task_follows_the_last_ticked_one(self):
        phase = PHASE.replace("- [ ] **Step 2: c** d.", "- [x] **Step 2: c** d. Done 07/10/2026: ok.")
        out = self.output({"phases/phase-02-second.md": phase})
        self.assertIn("### Task 4: planned one", out)
        self.assertNotIn("### Task 3: current one", out)

    def test_a_phase_with_every_task_done_has_no_current_task(self):
        out = self.output({"phases/phase-02-second.md": "# Phase 02: second\n\nPreamble.\n\n### Task 2: a\n\n"
                           "- [x] **Step 1: a** b. Done 05/10/2026: ok.\n"})
        self.assertIn("No current task.", out)

    def test_a_state_that_names_another_phase_file_gives_a_warning(self):
        out = self.output({"state.md": "# State\n\n- Phase 01: `phases/phase-01-first.md`.\n"})
        self.assertIn("warning: state.md names phases/phase-01-first.md, "
                      "the open phase is phases/phase-02-second.md", out)

    def test_an_empty_roadmap_is_said_plainly(self):
        plan = "# P: the plan\n\n## Goal\n\nThe goal text.\n\n## Roadmap\n\nNothing yet.\n\n## Blocked\n\nNothing yet.\n"
        out = self.output({"plan.md": plan})
        self.assertIn("The goal text.", out)
        self.assertIn("No item.", out)

    def test_the_template_plan_reads_without_error(self):
        template = (ROOT / "skill" / "templates" / "plan.md").read_text(encoding="utf-8")
        out = self.output({"plan.md": template})
        self.assertIn("No item.", out)

    def test_the_command_prints_the_start(self):
        make(self.folder, FOLDER)
        result = self.run_tool(str(self.folder))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("==> state.md <==", result.stdout)
        self.assertIn("### Task 3: current one", result.stdout)

    def test_a_missing_state_fails_so_that_the_routine_reads_the_files(self):
        files = dict(FOLDER)
        del files["state.md"]
        make(self.folder, files)
        result = self.run_tool(str(self.folder))
        self.assertEqual(result.returncode, 1)
        self.assertIn("state.md is missing", result.stderr)

    def test_a_missing_folder_is_a_usage_error(self):
        result = self.run_tool("/nonexistent/folder")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
