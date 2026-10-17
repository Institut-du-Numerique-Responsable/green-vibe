from __future__ import annotations

import unittest
from pathlib import Path

from tests import REPO_ROOT
from green_vibe import audit as audit_mod
from green_vibe import rules as rules_mod

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class TestAuditBadFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)

    def _rules_of(self, findings):
        return {f["rule"] for f in findings}

    def test_api_bad_flags_expected_rules(self):
        findings = audit_mod.audit_files([FIXTURES / "api_bad.py"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertIn("NR-LANG-PY-003", rules_hit)   # N+1 loop over queryset
        self.assertIn("NR-LANG-PY-004", rules_hit)  # bare open()
        self.assertIn("NR-ALGO-002", rules_hit)     # nested loops
        self.assertIn("NR-BACK-001", rules_hit)     # requests without timeout
        self.assertIn("NR-DATA-007", rules_hit)     # SQL built by concatenation
        self.assertIn("NR-API-003", rules_hit)      # HTTP call inside a loop

    def test_api_good_is_clean(self):
        findings = audit_mod.audit_files([FIXTURES / "api_good.py"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertNotIn("NR-LANG-PY-003", rules_hit)
        self.assertNotIn("NR-LANG-PY-004", rules_hit)
        self.assertNotIn("NR-DATA-007", rules_hit)

    def test_sql_bad_flags_expected_rules(self):
        findings = audit_mod.audit_files([FIXTURES / "query_bad.sql"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertIn("NR-LANG-SQL-001", rules_hit)  # SELECT * (automation full)
        self.assertIn("NR-LANG-SQL-002", rules_hit)  # correlated subquery
        self.assertIn("NR-LANG-SQL-004", rules_hit)  # LOWER() on indexed column
        # full automation => FAIL status, not REVIEW
        sel = [f for f in findings if f["rule"] == "NR-LANG-SQL-001"]
        self.assertTrue(all(f["status"] == "FAIL" for f in sel))

    def test_html_bad_flags_expected_rules(self):
        findings = audit_mod.audit_files([FIXTURES / "page_bad.html"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertIn("NR-CONTENT-002", rules_hit)  # autoplay video
        self.assertIn("NR-CONTENT-001", rules_hit)  # img without srcset
        self.assertIn("NR-UX-001", rules_hit)       # img without alt
        self.assertIn("NR-SERVICE-008", rules_hit) # third-party script
        self.assertIn("NR-FRONT-003", rules_hit)    # blocking script
        self.assertIn("NR-LANG-HTML-001", rules_hit)  # div role=button / clickable span
        self.assertIn("NR-LANG-HTML-002", rules_hit)  # img without dimensions
        self.assertIn("NR-LANG-HTML-003", rules_hit)  # input without label
        self.assertIn("NR-CONTENT-004", rules_hit)   # google fonts
        self.assertIn("NR-INFRA-001", rules_hit)    # http:// subresource

    def test_html_good_is_clean(self):
        findings = audit_mod.audit_files([FIXTURES / "page_good.html"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertNotIn("NR-CONTENT-002", rules_hit)
        self.assertNotIn("NR-UX-001", rules_hit)
        self.assertNotIn("NR-FRONT-003", rules_hit)

    def test_shell_bad_flags_expected_rules(self):
        findings = audit_mod.audit_files([FIXTURES / "script_bad.sh"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertIn("NR-LANG-SH-001", rules_hit)  # loop over $(ls, grep|grep
        self.assertIn("NR-LANG-SH-002", rules_hit)  # no set -euo pipefail (special)
        self.assertIn("NR-LANG-SH-003", rules_hit)  # fixed /tmp path
        self.assertIn("NR-LANG-SH-004", rules_hit)  # while true

    def test_shell_good_is_clean(self):
        findings = audit_mod.audit_files([FIXTURES / "script_good.sh"], self.rules)
        rules_hit = self._rules_of(findings)
        self.assertNotIn("NR-LANG-SH-002", rules_hit)
        self.assertNotIn("NR-LANG-SH-003", rules_hit)
        self.assertNotIn("NR-LANG-SH-004", rules_hit)

    def test_masking_prevents_literal_hits(self):
        # page_bad.html contains the string "SELECT * FROM nothing" inside JS:
        # masking keeps it out of SQL findings
        findings = audit_mod.audit_files([FIXTURES / "page_bad.html"], self.rules)
        sql_hits = [f for f in findings if f["rule"] == "NR-LANG-SQL-001"]
        self.assertEqual(sql_hits, [], "string literals must not be flagged")

    def test_candidate_status_is_review(self):
        findings = audit_mod.audit_files([FIXTURES / "api_bad.py"], self.rules)
        n1 = [f for f in findings if f["rule"] == "NR-LANG-PY-003"]
        self.assertTrue(n1 and all(f["status"] == "REVIEW" for f in n1),
                        "partial automation yields REVIEW candidates")


if __name__ == "__main__":
    unittest.main()
