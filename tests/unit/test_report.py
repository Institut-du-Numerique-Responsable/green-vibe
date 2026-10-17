from __future__ import annotations

import unittest

from tests import REPO_ROOT
from green_vibe import report
from green_vibe import rules as rules_mod


RULES = rules_mod.load_rules(REPO_ROOT)
BY_ID = {r["id"]: r for r in RULES}


class TestReport(unittest.TestCase):
    def test_finding_maps_to_failed_for_full_automation(self):
        findings = [{"rule": "NR-LANG-SQL-001", "status": "FAIL"}]
        results = report.results_from_audit(findings, ["NR-LANG-SQL-001"], BY_ID)
        self.assertEqual(results[0]["status"], "failed")

    def test_review_candidate_maps_to_manual_review(self):
        findings = [{"rule": "NR-LANG-PY-003", "status": "REVIEW"}]
        results = report.results_from_audit(findings, ["NR-LANG-PY-003"], BY_ID)
        self.assertEqual(results[0]["status"], "manual_review_required")

    def test_declaration_alone_never_verifies(self):
        results = report.results_from_audit([], ["NR-DATA-004"], BY_ID,
                                             applied=["NR-DATA-004"])
        self.assertEqual(results[0]["status"], "not_tested")

    def test_verified_requires_evidence(self):
        results = report.results_from_audit([], ["NR-DATA-004"], BY_ID)
        results = report.mark_verified(
            results, {"NR-DATA-004": "tests/test_pagination.py::test_last_page"}
        )
        self.assertEqual(results[0]["status"], "verified")
        self.assertIn("tests/test_pagination.py", results[0]["evidence"][0])

    def test_failed_not_overridden_by_verified_claim(self):
        findings = [{"rule": "NR-LANG-SQL-001", "status": "FAIL"}]
        results = report.results_from_audit(findings, ["NR-LANG-SQL-001"], BY_ID)
        results = report.mark_verified(results, {"NR-LANG-SQL-001": "claimed"})
        self.assertEqual(results[0]["status"], "failed",
                         "a verified claim cannot override a confirmed violation")

    def test_not_applicable_is_reported(self):
        results = report.results_from_audit([], ["NR-INFRA-004"], BY_ID, applied=[])
        self.assertEqual(results[0]["status"], "not_tested")

    def test_bilan_counts(self):
        findings = [
            {"rule": "NR-LANG-SQL-001", "status": "FAIL"},
            {"rule": "NR-LANG-PY-003", "status": "REVIEW"},
        ]
        results = report.results_from_audit(findings, ["NR-LANG-SQL-001", "NR-LANG-PY-003"], BY_ID)
        results = report.mark_verified(results, {"NR-LANG-PY-003": "tests/x.py"})
        text = report.bilan(results, "Demo intervention", mode="pedagogique")
        self.assertIn("BILAN NUMÉRIQUE RESPONSABLE", text)
        self.assertIn("Vérifiées : 1", text)
        self.assertIn("En échec : 1", text)
        self.assertIn("À examiner : 0", text)

    def test_bilan_contains_no_unmeasured_environmental_claim(self):
        findings = [{"rule": "NR-LANG-SQL-001", "status": "FAIL"}]
        results = report.results_from_audit(findings, ["NR-LANG-SQL-001"], BY_ID)
        text = report.bilan(results, "Demo", mode="pedagogique")
        for banned in ("CO2", "gCO2", "kWh", "watts"):
            self.assertNotIn(banned, text)
        self.assertNotIn("carbone", text.lower())


if __name__ == "__main__":
    unittest.main()
