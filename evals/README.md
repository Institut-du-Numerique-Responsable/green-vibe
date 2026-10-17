# Demo evaluation: the full pipeline

**English** · [Français](README.fr.md)

This scenario replays on the repository fixtures: a small project (a Python
API module, an HTML page, SQL, and a shell script) goes through the four
pipeline steps. It's the scenario for the project's demo phase.

Run these commands from the repository root:

```bash
GV=$(pwd)
FIX=tests/fixtures

# 1. Context and rule selection
python3 validators/green-vibe select $FIX > /tmp/gv-select.json

# 2. Deterministic audit
python3 validators/green-vibe audit \
  $FIX/api_bad.py $FIX/query_bad.sql $FIX/page_bad.html \
  > /tmp/gv-audit.json

# 3. Normalised report and teaching report
python3 validators/green-vibe report \
  --audit /tmp/gv-audit.json \
  --selected $(python3 -c "import json;print(' '.join(json.load(open('/tmp/gv-select.json'))['selected_rules']))") \
  --verified "NR-DATA-004=tests/integration/test_pipeline.py::fixture" \
  --intervention "API module rework: pagination, HTTP calls, SQL queries" \
  --mode pedagogique
```

Expected results on the non-conforming fixtures:

- selection: backend, data, api, frontend, content, and ux families, the py,
  sql, html, and sh languages, and the always-on families
- audit: `FAIL` on `SELECT *` (NR-LANG-SQL-001), `REVIEW` on N+1
  (NR-LANG-PY-003), video autoplay (NR-CONTENT-002), a blocking script
  (NR-FRONT-003), and more
- report: no `verified` status without `--verified` and its evidence
- teaching report: counts consistent with the statuses, no unmeasured
  environmental claim

The same sequence on the `_good` fixtures produces no finding: it's the
regression test for the catalog's false-positive rate.

## Functional scenarios covered by the test suite

Each project scenario maps to an automated test.

| Scenario | Test |
|---|---|
| API (N+1, timeout, SQL injection) | `test_audit.py::test_api_bad_flags_expected_rules` |
| Frontend page (media, scripts, a11y) | `test_audit.py::test_html_bad_flags_expected_rules` |
| SQL query (SELECT *, subqueries) | `test_audit.py::test_sql_bad_flags_expected_rules` |
| Already-conforming code | `test_audit.py` (`_good` fixtures) + `test_pipeline.py::test_conforming_project_reports_no_findings` |
| Rule not applicable or not selected | `test_select.py::test_no_relevant_rules_for_plain_docs` |
| Detector unavailable (missing tool) | SKILL.md fallback + fail-open hook (`test_hook_fails_open_on_bad_input`) |
| Languages and frameworks (Go, Rust, PHP, Ruby, C#, Kotlin, Swift, C/C++, Scala, Julia, Nim, Zig, React, Vue, Angular, Svelte, Solid, Astro) | `test_lang_catalogs.py::test_bad_fixtures_flag_expected_rules` |
| Accessibility (language, zoom, focus, captions, animations) | `test_lang_catalogs.py` (`a11y_bad.html`) |
| Concern already handled in the file (guard) | `test_lang_catalogs.py::TestFileGuards` |
| Teaching report | `test_report.py::test_bilan_counts` |
| Unmeasured gain | `test_report.py::test_bilan_contains_no_unmeasured_environmental_claim` |

The "complex request", "conflicting rules", and "new dependency" scenarios
run as guided reviews: the matching rules (NR-ARCH-008, NR-MEASURE-002, and
the SKILL.md trade-offs) are process rules (`automation: none`). Their sheets
document the evidence, which a static check can't automate.
