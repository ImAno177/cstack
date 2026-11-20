from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "hooks"
NODE = shutil.which("node")
SHA = "a" * 40
OTHER = "b" * 40


@unittest.skipUnless(NODE, "node is required for hook tests")
class HookTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.data = self.tmp / "data"
        self.project = self.tmp / "project"
        self.home = self.tmp / "home"
        self.project.mkdir()
        self.home.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def run_hook(self, name: str, payload: dict, **env: str) -> subprocess.CompletedProcess:
        environ = {
            **os.environ,
            "CLAUDE_PLUGIN_ROOT": str(ROOT),
            "CLAUDE_PLUGIN_DATA": str(self.data),
            "CLAUDE_PROJECT_DIR": str(self.project),
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "CSTACK_HOOKS": "",
            "CSTACK_HOOKS_DISABLE": "",
            "CLAUDE_CODE_SUBAGENT_MODEL_FORCE": "",
            **env,
        }
        return subprocess.run(
            [NODE, str(HOOKS / name)], input=json.dumps(payload), capture_output=True, text=True, env=environ, timeout=30
        )

    def context(self, result: subprocess.CompletedProcess) -> str:
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"] if result.stdout else ""

    def merge(self, sha: str = SHA) -> subprocess.CompletedProcess:
        cmd = f"gh pr merge 5 --squash --delete-branch --match-head-commit {sha}"
        return self.run_hook("merge-gate.js", {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}})

    def handback(self, message: str, agent_type: str = "general-purpose", event: str = "PostToolUse") -> subprocess.CompletedProcess:
        return self.run_hook(
            "verdict-record.js",
            {
                "hook_event_name": event,
                "session_id": "s1",
                "agent_id": "a1",
                "agent_type": agent_type,
                "tool_name": "SubagentHandback",
                "tool_input": {"message": message},
            },
        )

    def test_merge_gate_requires_sha_and_passing_verdict(self):
        no_sha = self.run_hook("merge-gate.js", {"tool_name": "Bash", "tool_input": {"command": "gh pr merge 5 --squash"}})
        self.assertEqual(no_sha.returncode, 2)
        self.assertIn("--match-head-commit", no_sha.stderr)
        self.assertEqual(self.merge().returncode, 2)
        self.assertEqual(self.handback(f"checked {SHA}\nVERDICT: PASS").returncode, 0)
        self.assertEqual(self.merge().returncode, 0)
        self.assertEqual(self.handback(f"checked {OTHER}\nVERDICT: FAIL").returncode, 0)
        failed = self.merge(OTHER)
        self.assertEqual(failed.returncode, 2)
        self.assertIn("FAIL", failed.stderr)

    def test_merge_gate_ignores_other_commands_and_bad_input(self):
        unrelated = self.run_hook("merge-gate.js", {"tool_name": "Bash", "tool_input": {"command": "gh pr view 5 && git status"}})
        self.assertEqual(unrelated.returncode, 0)
        garbage = subprocess.run([NODE, str(HOOKS / "merge-gate.js")], input="not json", capture_output=True, text=True)
        self.assertEqual(garbage.returncode, 0)

    def test_merge_gate_blocks_writes_to_verdict_records(self):
        target = str(self.data / "verdicts" / f"{SHA}.json")
        write = self.run_hook("merge-gate.js", {"tool_name": "Write", "tool_input": {"file_path": target, "content": "{}"}})
        self.assertEqual(write.returncode, 2)
        shell = self.run_hook("merge-gate.js", {"tool_name": "Bash", "tool_input": {"command": f"echo x > {target}"}})
        self.assertEqual(shell.returncode, 2)

    def test_verdict_record_needs_agent_sha_and_final_line(self):
        self.handback(f"checked {SHA}\nVERDICT: PASS\nthanks")
        self.assertFalse((self.data / "verdicts" / f"{SHA}.json").exists())
        no_agent = self.run_hook(
            "verdict-record.js",
            {"hook_event_name": "PostToolUse", "tool_name": "SubagentHandback", "tool_input": {"message": f"{SHA}\nVERDICT: PASS"}},
        )
        self.assertEqual(no_agent.returncode, 0)
        self.assertFalse((self.data / "verdicts" / f"{SHA}.json").exists())
        refused = self.handback("looks fine", agent_type="cstack:verifier", event="PreToolUse")
        self.assertEqual(refused.returncode, 2)
        self.assertIn("VERDICT", refused.stderr)

    def edit(self, name: str = "app.py", agent: str | None = None) -> None:
        payload = {"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Edit", "tool_input": {"file_path": str(self.project / name)}}
        if agent:
            payload["agent_id"] = agent
        self.assertEqual(self.run_hook("check-gate.js", payload).returncode, 0)

    def stop(self, active: bool = False, agent: str | None = None) -> subprocess.CompletedProcess:
        payload = {"hook_event_name": "SubagentStop" if agent else "Stop", "session_id": "s1", "stop_hook_active": active}
        if agent:
            payload["agent_id"] = agent
        return self.run_hook("check-gate.js", payload)

    def test_check_gate_blocks_once_until_a_check_runs(self):
        self.assertEqual(self.stop().returncode, 0)
        self.edit()
        blocked = self.stop()
        self.assertEqual(blocked.returncode, 2)
        self.assertIn("app.py", blocked.stderr)
        self.assertEqual(self.stop().returncode, 0)
        self.edit()
        self.assertEqual(self.stop(active=True).returncode, 0)
        self.assertEqual(self.stop().returncode, 2)
        check = {"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Bash", "tool_input": {"command": "python -m pytest -q"}}
        self.run_hook("check-gate.js", check)
        self.edit()
        self.run_hook("check-gate.js", check)
        self.assertEqual(self.stop().returncode, 0)

    def test_check_gate_ignores_docs_and_files_outside_project(self):
        self.edit("README.md")
        outside = {"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Write", "tool_input": {"file_path": str(self.tmp / "scratch.py")}}
        self.run_hook("check-gate.js", outside)
        self.assertEqual(self.stop().returncode, 0)

    def test_check_gate_tracks_subagents_separately(self):
        self.edit(agent="sub1")
        self.assertEqual(self.stop().returncode, 0)
        self.assertEqual(self.stop(agent="sub1").returncode, 2)

    def test_check_gate_reads_codex_apply_patch(self):
        patch = "*** Begin Patch\n*** Update File: src/main.go\n@@\n-a\n+b\n*** End Patch"
        payload = {"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "apply_patch", "tool_input": {"command": patch}}
        self.run_hook("check-gate.js", payload)
        self.assertEqual(self.stop().returncode, 2)

    def test_model_skill_injects_the_matching_skill(self):
        for model, skill in [
            ("claude-opus-5-5", "if-u-are-opus-5-5"),
            ("claude-fable-5-2[1m]", "if-u-are-fable-5-2"),
            ("gpt-6.1-sol", "if-u-are-gpt-6-1-sol"),
            ("gpt-5.6-luna", "if-u-are-gpt-5-6-luna"),
        ]:
            text = self.context(self.run_hook("model-skill.js", {"hook_event_name": "SessionStart", "session_id": "s", "model": model}))
            self.assertIn(skill, text)
            self.assertNotIn("\n---\n", text[:400])
        self.assertEqual(self.context(self.run_hook("model-skill.js", {"hook_event_name": "SessionStart", "model": "gpt-x"})), "")

    def test_model_skill_for_subagents(self):
        forced = self.run_hook(
            "model-skill.js",
            {"hook_event_name": "SubagentStart", "agent_id": "a", "agent_type": "Explore"},
            CLAUDE_CODE_SUBAGENT_MODEL="haiku",
            CLAUDE_CODE_SUBAGENT_MODEL_FORCE="1",
        )
        self.assertIn("if-u-are-haiku-5-5", self.context(forced))
        preloaded = self.run_hook(
            "model-skill.js",
            {"hook_event_name": "SubagentStart", "agent_type": "cstack:verifier"},
            CLAUDE_CODE_SUBAGENT_MODEL="haiku",
            CLAUDE_CODE_SUBAGENT_MODEL_FORCE="1",
        )
        self.assertEqual(self.context(preloaded), "")

    def test_standing_rules_cadence_and_pins(self):
        (self.project / ".claude").mkdir()
        (self.project / ".claude" / "pinned-rules.md").write_text("- ask before deleting files under data/\n", encoding="utf-8")
        prompt = {"hook_event_name": "UserPromptSubmit", "session_id": "s1", "cwd": str(self.project)}
        outputs = [self.context(self.run_hook("standing-rules.js", prompt, CSTACK_REMIND_EVERY="3")) for _ in range(6)]
        self.assertEqual([bool(o) for o in outputs], [False, False, True, False, False, True])
        self.assertIn("force-pushing", outputs[2])
        self.assertIn("data/", outputs[2])
        compact = self.context(self.run_hook("standing-rules.js", {"hook_event_name": "SessionStart", "source": "compact"}))
        self.assertIn("Reminder from the cstack hook", compact)
        self.assertIn("data/", compact)
        startup = self.context(self.run_hook("standing-rules.js", {"hook_event_name": "SessionStart", "source": "startup"}))
        self.assertIn("data/", startup)
        self.assertNotIn("force-pushing", startup)

    def test_usage_log_records_skill_reads(self):
        for path in [r"C:\x\.claude\plugins\cstack\skills\tdd\SKILL.md", "/repo/notes.txt"]:
            self.run_hook("usage-log.js", {"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Read", "tool_input": {"file_path": path}})
        self.run_hook("usage-log.js", {"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Skill", "tool_input": {"skill": "cstack:why"}})
        rows = [json.loads(line) for line in (self.data / "logs" / "skill-usage.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["skill"] for r in rows], ["tdd", "cstack:why"])

    def test_disable_switches(self):
        self.edit()
        self.assertEqual(self.run_hook("check-gate.js", {"hook_event_name": "Stop", "session_id": "s1"}, CSTACK_HOOKS="off").returncode, 0)
        self.assertEqual(
            self.run_hook("check-gate.js", {"hook_event_name": "Stop", "session_id": "s1"}, CSTACK_HOOKS_DISABLE="merge-gate,check-gate").returncode, 0
        )
        self.assertEqual(self.stop().returncode, 2)

    def test_hooks_json_references_existing_scripts(self):
        config = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))
        for groups in config["hooks"].values():
            for group in groups:
                for hook in group["hooks"]:
                    script = hook["command"].split("/hooks/")[1].rstrip('"')
                    self.assertTrue((HOOKS / script).is_file(), script)


if __name__ == "__main__":
    unittest.main()
