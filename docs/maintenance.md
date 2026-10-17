# Maintenance and contribution

**English** · [Français](fr/maintenance.md)

This page describes how to test, evolve, and contribute to the catalog.

## Tests

The test suite uses the standard library. Run it from the repository root:

```bash
python3 -m unittest discover -s tests -t . -p "test_*.py"
```

- `tests/unit/test_rules.py`: full sheet schema, unique IDs, every pattern
  compiles, expected families.
- `tests/unit/test_select.py`: scope detection, selection by family, usage
  rules excluded.
- `tests/unit/test_audit.py`: non-conforming fixtures trigger the expected
  rules; conforming fixtures produce no finding; FAIL/REVIEW statuses;
  masking.
- `tests/unit/test_lang_catalogs.py`: one non-conforming fixture per language
  and framework triggers the expected rules; conforming Go/Rust fixtures
  produce no finding; file guards and `in_loop`; selection by detected
  framework (React vs Solid); linear-time checks (no `^\s` in patterns,
  large masked blocks in every language).
- `tests/unit/test_report.py`: normalised statuses, `verified` needs
  evidence, a FAIL can't be overridden, no unmeasured environmental claim in
  the report.
- `tests/integration/test_pipeline.py`: the full select, audit, and report
  pipeline, the CLI, and the hook (clean input, silence, fail-open).

Every change to the catalog or the engine must pass the full suite and
regenerate `rules/index.json` (`python3 validators/green-vibe index`).

## Release cycle

Versions follow SemVer.

- `VERSION` and `plugin.json` `version` follow SemVer: patch (fixes), minor
  (new rules), major (schema change).
- `CHANGELOG.md` and `CHANGELOG.fr.md` are updated for every release.
- No remote publication without explicit INR approval.

## Contribution

Every contribution meets these requirements:

1. A complete sheet with every field (see [rules.md](rules.md)). Rule content
   and documentation are in English; keep the French translation in sync in
   `docs/fr/`, `README.fr.md`, `evals/README.fr.md`, and `CHANGELOG.fr.md`.
2. Every automatable rule has a `note` that describes the detector's limits,
   plus conforming and non-conforming fixtures and a test.
3. Provenance (`origin`) is mandatory; a contribution without a verifiable
   reference stays a draft until the INR validates it.
4. An environmental claim in a sheet needs the measurement behind it, or it
   doesn't go in.
5. Code contributions (validators, hook, tests) follow the same rules:
   standard library only, tests, and a fail-open hook.
