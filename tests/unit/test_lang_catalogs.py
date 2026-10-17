from __future__ import annotations

import unittest
from pathlib import Path

from tests import REPO_ROOT
from green_vibe import audit as audit_mod
from green_vibe import context
from green_vibe import rules as rules_mod

LANG = Path(__file__).resolve().parents[1] / "fixtures" / "lang"

# fixture -> rules its non-conforming code must trigger
EXPECTED = {
    "go_bad.go": {"NR-LANG-GO-001", "NR-LANG-GO-002", "NR-LANG-GO-003", "NR-LANG-GO-004", "NR-LANG-GO-005"},
    "rust_bad.rs": {"NR-LANG-RS-001", "NR-LANG-RS-002", "NR-LANG-RS-003", "NR-LANG-RS-004", "NR-LANG-RS-005"},
    "php_bad.php": {"NR-LANG-PHP-001", "NR-LANG-PHP-002", "NR-LANG-PHP-003", "NR-LANG-PHP-004",
                    "NR-LANG-PHP-005", "NR-LANG-PHP-006"},
    "ruby_bad.rb": {"NR-LANG-RB-001", "NR-LANG-RB-002", "NR-LANG-RB-003", "NR-LANG-RB-004", "NR-LANG-RB-005"},
    "csharp_bad.cs": {"NR-LANG-CS-001", "NR-LANG-CS-002", "NR-LANG-CS-003", "NR-LANG-CS-004",
                      "NR-LANG-CS-005", "NR-LANG-CS-006", "NR-LANG-CS-007"},
    "kotlin_bad.kt": {"NR-LANG-KT-001", "NR-LANG-KT-002", "NR-LANG-KT-003", "NR-LANG-KT-004"},
    "swift_bad.swift": {"NR-LANG-SWIFT-001", "NR-LANG-SWIFT-002", "NR-LANG-SWIFT-003", "NR-LANG-SWIFT-004"},
    "c_bad.c": {"NR-LANG-C-001", "NR-LANG-C-002", "NR-LANG-C-003"},
    "cpp_bad.cpp": {"NR-LANG-CPP-001", "NR-LANG-CPP-002", "NR-LANG-CPP-003", "NR-LANG-CPP-004"},
    "scala_bad.scala": {"NR-LANG-SCALA-001", "NR-LANG-SCALA-002"},
    "julia_bad.jl": {"NR-LANG-JL-001", "NR-LANG-JL-002", "NR-LANG-JL-003"},
    "nim_bad.nim": {"NR-LANG-NIM-001", "NR-LANG-NIM-002"},
    "zig_bad.zig": {"NR-LANG-ZIG-001", "NR-LANG-ZIG-002"},
    "page.astro": {"NR-LANG-ASTRO-001", "NR-LANG-ASTRO-002"},
    "react_bad.tsx": {"NR-LANG-REACT-001", "NR-LANG-REACT-002", "NR-LANG-REACT-003"},
    "solid_bad.tsx": {"NR-LANG-SOLID-001"},
    "Router.vue": {"NR-LANG-VUE-001", "NR-LANG-VUE-002", "NR-LANG-VUE-003"},
    "orders.component.ts": {"NR-LANG-NG-001", "NR-LANG-NG-003"},
    "Store.svelte": {"NR-LANG-SVELTE-001", "NR-LANG-SVELTE-002"},
    "a11y_bad.html": {"NR-LANG-HTML-004", "NR-UX-009", "NR-UX-010", "NR-UX-011", "NR-LANG-CSS-003"},
}


class TestLanguageFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)

    def _hits(self, name):
        return {f["rule"] for f in audit_mod.audit_files([LANG / name], self.rules)}

    def test_bad_fixtures_flag_expected_rules(self):
        for name, expected in EXPECTED.items():
            with self.subTest(fixture=name):
                missing = expected - self._hits(name)
                self.assertEqual(missing, set(), f"{name}: rules not triggered")

    def test_good_fixtures_are_clean(self):
        # The conforming versions use the very APIs the file-level guards look for.
        self.assertEqual(self._hits("go_good.go"), set())
        self.assertEqual(self._hits("rust_good.rs"), set())

    def test_solid_file_does_not_trigger_react_rules(self):
        hits = self._hits("solid_bad.tsx")
        self.assertFalse({h for h in hits if h.startswith("NR-LANG-REACT-")}, hits)

    def test_lowercase_list_call_is_not_a_copy_in_js(self):
        # Patterns are case-insensitive: a component named List must not read as list(x).
        self.assertNotIn("NR-ALGO-009", self._hits("solid_bad.tsx"))


class TestFileGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)

    def _audit(self, text, name):
        return {f["rule"] for f in audit_mod.audit_text(text, name, self.rules)}

    def test_exclude_file_silences_handled_concern(self):
        leak = "package m\nfunc f() { go func() { work() }() }\n"
        handled = "package m\nimport \"context\"\nfunc f(ctx context.Context) { go func() { <-ctx.Done() }() }\n"
        self.assertIn("NR-LANG-GO-001", self._audit(leak, "a.go"))
        self.assertNotIn("NR-LANG-GO-001", self._audit(handled, "a.go"))

    def test_require_file_gates_framework_patterns(self):
        sub = "export class S { init() { this.x$.subscribe(v => v); } }\n"
        self.assertNotIn("NR-LANG-NG-003", self._audit(sub, "s.ts"))
        angular = "import { Component } from '@angular/core';\n" + sub
        self.assertIn("NR-LANG-NG-003", self._audit(angular, "s.ts"))

    def test_in_loop_guard_keeps_only_loop_bodies(self):
        text = ("import requests\ndef f(urls):\n    out = ''\n    for u in urls:\n"
                "        requests.get(u)\n        out += 'x'\n    return out\n"
                "requests.get('https://example.org')\n")
        hits = {(f["rule"], f["line"]) for f in audit_mod.audit_text(text, "a.py", self.rules)}
        self.assertIn(("NR-LANG-PY-009", 5), hits)
        self.assertIn(("NR-LANG-PY-008", 6), hits)
        self.assertNotIn(("NR-LANG-PY-009", 8), hits)

    def test_audit_stays_linear_on_real_code(self):
        # Regression guard against catastrophic backtracking (NR-ALGO-004):
        # the whole validator package must audit in well under a second.
        import time

        start = time.monotonic()
        audit_mod.audit_files([REPO_ROOT / "validators", REPO_ROOT / "scripts"], self.rules)
        self.assertLess(time.monotonic() - start, 5.0)

    def test_rust_lifetimes_do_not_break_masking(self):
        text = "fn f<'a>(x: &'a str) -> &'a str { let s = \"Client::new()\"; x }\n"
        self.assertNotIn("NR-LANG-RS-004", self._audit(text, "a.rs"))


class TestFrameworkSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = rules_mod.load_rules(REPO_ROOT)

    def _selected(self, *names):
        ctx = context.analyze([str(LANG / n) for n in names])
        return set(context.select_rule_ids(ctx, self.rules))

    def test_framework_rules_follow_detected_framework(self):
        react = self._selected("react_bad.tsx")
        self.assertIn("NR-LANG-REACT-001", react)
        self.assertNotIn("NR-LANG-SOLID-001", react)
        solid = self._selected("solid_bad.tsx")
        self.assertIn("NR-LANG-SOLID-001", solid)
        self.assertNotIn("NR-LANG-REACT-001", solid)

    def test_new_languages_select_their_catalog(self):
        for name, rid in [("go_bad.go", "NR-LANG-GO-001"), ("rust_bad.rs", "NR-LANG-RS-001"),
                          ("php_bad.php", "NR-LANG-PHP-001"), ("kotlin_bad.kt", "NR-LANG-KT-001"),
                          ("page.astro", "NR-LANG-ASTRO-001"), ("zig_bad.zig", "NR-LANG-ZIG-001")]:
            with self.subTest(fixture=name):
                self.assertIn(rid, self._selected(name))


if __name__ == "__main__":
    unittest.main()
