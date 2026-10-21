from __future__ import annotations

import unittest
from pathlib import Path

from tests import REPO_ROOT
from green_vibe import rules as rules_mod


class TestRuleCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)

    def test_catalog_loads(self):
        self.assertGreater(len(self.rules), 100, "expected a full catalog")

    def test_unique_ids(self):
        ids = [r["id"] for r in self.rules]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_metadata(self):
        for r in self.rules:
            self.assertIn("what", r)
            self.assertIn("why", r)
            self.assertIn("how", r)
            self.assertIn("verify", r, f"{r['id']} missing verify")
            self.assertIn("method", r["verify"], f"{r['id']} verify.method missing")
            self.assertIn("priority", r)
            self.assertIn(r["priority"], ("high", "medium", "low"))
            self.assertIn("origin", r, f"{r['id']} missing provenance")
            self.assertTrue(r["origin"], f"{r['id']} empty provenance")
            self.assertIn("applies", r)
            self.assertIn("id", r)
            self.assertIn("title", r)

    def test_detection_patterns_compile(self):
        import re

        for r in self.rules:
            detect = r.get("detect") or {}
            for p in detect.get("patterns", []):
                try:
                    re.compile(p["re"], re.I | re.M)
                except re.error as e:
                    self.fail(f"{r['id']} pattern does not compile: {p['re']!r} ({e})")

    def test_every_family_has_rules(self):
        fams = {r["_family"] for r in self.rules}
        expected = {
            "strategy", "service", "architecture", "measure", "ux", "content",
            "frontend", "backend", "data", "api", "infra", "algo", "ai", "usage", "tokens",
            "lang-python", "lang-javascript", "lang-java", "lang-sql",
            "lang-html-css", "lang-shell",
        }
        self.assertEqual(expected - fams, set(), f"missing families: {expected - fams}")

    def test_usage_rules_are_conversation_scoped(self):
        usage = [r for r in self.rules if r["_family"] == "usage"]
        self.assertEqual(len(usage), 29)


class TestTokenRules(unittest.TestCase):
    """NR-TOK: 30 token sobriety rules, with the INR priority levels."""

    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)
        cls.tokens = [r for r in cls.rules if r["_family"] == "tokens"]

    def test_thirty_rules_in_order(self):
        ids = [r["id"] for r in self.tokens]
        self.assertEqual(ids, [f"NR-TOK-{i:03d}" for i in range(1, 31)])

    def test_levels_match_the_inr_priorities(self):
        def level(name):
            return [r["id"][7:] for r in self.tokens if r["level"] == name]

        self.assertEqual(level("mandatory"), ["007", "011", "015", "016", "022", "027", "030"])
        self.assertEqual(level("conditional"), ["023", "024", "025", "026", "028"])
        for r in self.tokens:
            self.assertIn(r["level"], ("mandatory", "recommended", "conditional"))

    def test_mandatory_rules_are_high_priority(self):
        for r in self.tokens:
            if r["level"] == "mandatory":
                self.assertEqual(r["priority"], "high", r["id"])

    def test_see_references_exist(self):
        ids = {r["id"] for r in self.rules}
        for r in self.tokens:
            for ref in r.get("see", []):
                self.assertIn(ref, ids, f"{r['id']} cites unknown {ref}")

    def test_never_auto_selected(self):
        from green_vibe import context

        ctx = {"scopes": ["python", "js", "sql", "html"], "frameworks": []}
        selected = context.select_rule_ids(ctx, self.rules, ["ai"])
        self.assertFalse([s for s in selected if s.startswith("NR-TOK-")])

    def test_no_invented_metric_rule(self):
        report = next(r for r in self.tokens if r["id"] == "NR-TOK-030")
        self.assertIn("Never invent a metric", report["what"])


class TestIndex(unittest.TestCase):
    def test_index_matches_catalog(self):
        rules = rules_mod.load_rules(REPO_ROOT)
        index = rules_mod.rule_index(rules)
        self.assertEqual(len(index), len(rules))
        entry = next(e for e in index if e["id"] == "NR-DATA-001")
        self.assertEqual(entry["automation"], "full")
        self.assertIn("sql", entry["scopes"])


if __name__ == "__main__":
    unittest.main()
