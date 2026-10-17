from __future__ import annotations

import json
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tests import REPO_ROOT, load_hook_script
from green_vibe import audit as audit_mod
from green_vibe import context, report, rules as rules_mod
from green_vibe import cli

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
RULES = rules_mod.load_rules(REPO_ROOT)
BY_ID = {r["id"]: r for r in RULES}


class TestPipeline(unittest.TestCase):
    """End-to-end: select -> audit -> report on the fixture mini-project."""

    def test_full_pipeline(self):
        ctx = context.analyze([FIXTURES])
        selected = context.select_rule_ids(ctx, RULES)
        self.assertGreater(len(selected), 30)

        findings = audit_mod.audit_files(
            [FIXTURES / "api_bad.py", FIXTURES / "query_bad.sql", FIXTURES / "page_bad.html"],
            RULES,
        )
        self.assertGreater(len(findings), 5)

        results = report.results_from_audit(findings, selected, BY_ID)
        statuses = {r["status"] for r in results}
        self.assertIn("manual_review_required", statuses)

        verified = {"NR-DATA-004": "tests/integration/test_pipeline.py::fixture"}
        results = report.mark_verified(results, verified)
        got = next(r for r in results if r["rule_id"] == "NR-DATA-004")
        self.assertEqual(got["status"], "verified")

        text = report.bilan(results, "Démo pipeline sur fixtures", mode="pedagogique")
        self.assertIn("Vérifiées : 1", text)

    def test_conforming_project_reports_no_findings(self):
        findings = audit_mod.audit_files(
            [FIXTURES / "api_good.py", FIXTURES / "page_good.html", FIXTURES / "script_good.sh"],
            RULES,
        )
        self.assertEqual(findings, [], f"unexpected findings: {findings}")


class TestCli(unittest.TestCase):
    def test_audit_json_output(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main(["audit", str(FIXTURES / "query_bad.sql")])
        payload = json.loads(buf.getvalue())
        self.assertGreaterEqual(payload["count"], 2)

    def test_stats(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.main(["stats"])
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["total"], len(RULES))


class TestHook(unittest.TestCase):
    def test_hook_reports_candidates(self):
        hook = load_hook_script()
        payload = {
            "hook_event_name": "post_tool",
            "tool_name": "write_file",
            "tool_input": {
                "file_path": "/tmp/demo.py",
                "content": (
                    "import requests\n"
                    "def get(url):\n"
                    "    return requests.get(url).text\n"
                ),
            },
        }
        stdin = json.dumps(payload)
        hook.sys.stdin = io.StringIO(stdin)
        hook.sys.stdout = io.StringIO()
        code = hook.main()
        self.assertEqual(code, 0)
        out = hook.sys.stdout.getvalue()
        if out.strip():
            response = json.loads(out)
            self.assertEqual(response["decision"], "allow")
            self.assertIn("additional_context", response["hook_specific_output"])
            self.assertIn("NR-BACK-001", response["hook_specific_output"]["additional_context"])

    def test_hook_silent_when_clean(self):
        hook = load_hook_script()
        payload = {
            "hook_event_name": "post_tool",
            "tool_name": "write_file",
            "tool_input": {
                "file_path": "/tmp/demo_good.py",
                "content": "def add(a, b):\n    return a + b\n",
            },
        }
        hook.sys.stdin = io.StringIO(json.dumps(payload))
        hook.sys.stdout = io.StringIO()
        code = hook.main()
        self.assertEqual(code, 0)
        self.assertEqual(hook.sys.stdout.getvalue(), "")

    def test_hook_fails_open_on_bad_input(self):
        hook = load_hook_script()
        hook.sys.stdin = io.StringIO("not json at all")
        hook.sys.stdout = io.StringIO()
        self.assertEqual(hook.main(), 0)


if __name__ == "__main__":
    unittest.main()
