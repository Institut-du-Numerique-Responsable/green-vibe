from __future__ import annotations

import unittest
from pathlib import Path

from tests import REPO_ROOT
from green_vibe import context
from green_vibe import rules as rules_mod

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class TestScopes(unittest.TestCase):
    def test_python_file(self):
        scopes = context.file_scopes(Path("src/app.py"))
        self.assertIn("py", scopes)
        self.assertIn("any", scopes)

    def test_tsx_file(self):
        scopes = context.file_scopes(Path("src/Widget.tsx"))
        self.assertIn("tsx", scopes)
        self.assertIn("jsx", scopes)

    def test_workflow_yaml(self):
        p = Path(".github/workflows/ci.yml")
        self.assertIn("workflow-yaml", context.file_scopes(p))

    def test_dockerfile(self):
        self.assertIn("dockerfile", context.file_scopes(Path("Dockerfile")))


class TestSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)

    def test_python_project_selects_python_lang_rules(self):
        ctx = context.analyze([FIXTURES / "api_bad.py"])
        selected = set(context.select_rule_ids(ctx, self.rules))
        self.assertIn("NR-LANG-PY-003", selected)
        self.assertIn("NR-DATA-001", selected)  # SQL rule selected? no: scope applies
        # core rules selected via 'any' applicability:
        self.assertIn("NR-ARCH-001", selected)

    def test_usage_rules_never_auto_selected(self):
        ctx = context.analyze([FIXTURES / "api_bad.py"])
        selected = set(context.select_rule_ids(ctx, self.rules))
        self.assertFalse([s for s in selected if s.startswith("NR-USAGE-")])

    def test_sql_file_selects_sql_rules(self):
        ctx = context.analyze([FIXTURES / "query_bad.sql"])
        selected = set(context.select_rule_ids(ctx, self.rules))
        self.assertIn("NR-LANG-SQL-001", selected)
        self.assertIn("NR-LANG-SQL-002", selected)

    def test_html_selects_frontend_families(self):
        ctx = context.analyze([FIXTURES / "page_bad.html"])
        selected = set(context.select_rule_ids(ctx, self.rules))
        self.assertIn("NR-CONTENT-001", selected)
        self.assertIn("NR-CONTENT-002", selected)
        self.assertIn("NR-SERVICE-005", selected)

    def test_no_relevant_rules_for_plain_docs(self):
        ctx = context.analyze([FIXTURES / "notes.md"])
        selected = context.select_rule_ids(ctx, self.rules)
        # docs-only files still select strategy/measure-level core rules via 'any'
        self.assertIn("NR-STRAT-001", selected)
        self.assertNotIn("NR-LANG-PY-001", selected)


if __name__ == "__main__":
    unittest.main()
