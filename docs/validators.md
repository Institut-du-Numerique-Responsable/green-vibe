# The validators

**English** · [Français](fr/validateurs.md)

This page describes the CLI, the audit engine, the statuses, and the hook.

## Overview

A single CLI (`validators/green-vibe`), standard-library Python, no
installation, provides these commands.

| Command | Role |
|---|---|
| `select <paths> [--family f]` | Context analysis, families, selected rules |
| `rules <filter>` | Compact view of the sheets (what/why/how/verify/auto/origin) |
| `audit <paths>` | Static audit: `FAIL`/`REVIEW` findings per file:line |
| `report --audit f [--selected ids] [--verified R=evidence] [--mode m]` | Normalised results and teaching report |
| `index [--out f]` | Regenerates `rules/index.json` (or `f`) |
| `stats` | Catalog statistics |

Common options and behaviour:

- `--root DIR` (before the subcommand): the Green Vibe root to use, detected
  automatically by default. `stats` ignores this option.
- `select --family f` can be repeated (`--family ai --family infra`).
- `rules` filters by ID or family substring (`rules data`,
  `rules NR-DATA-004`); with no argument, it lists the whole catalog.
- `report --json` prints the full report (results, findings, and report text)
  instead of the report text alone. Without `--selected`, the report covers
  the rules that have at least one finding.
- `--selected` expects **separate** IDs: `--selected NR-A NR-B`. A quoted
  string such as `"NR-A NR-B"` reads as a single ID.
- Output: JSON on stdout; `audit` also summarises each finding on stderr.
  Every command exits with code 0, findings or not: the audit informs, it
  doesn't block.

## Audit engine

The audit runs in four steps.

1. **Enumeration**: files covered by the 25 catalogs (Python, JS/TS, Java,
   Go, Rust, PHP, Ruby, C#, Kotlin, Swift, C/C++, Scala, Julia, Nim, Zig, SQL,
   HTML/CSS, shell, Vue, Svelte, Astro…), with standard exclusions (`.git`,
   `node_modules`, `dist`, `__pycache__`...).
2. **Masking**: strings and comments become spaces (positions preserved)
   before any matching, so the engine ignores an anti-pattern quoted in a
   literal or a docstring. Shell script shebangs stay intact.
3. **Matching**: one regex set per rule, compiled once, scoped by file type
   (`scope`), with file guards (`exclude_file` on the masked text,
   `exclude_import` and `require_file` on the raw text) and the `in_loop`
   option (a hit is kept only inside a loop body, by indentation). Special
   detectors in code handle checks cleaner than a regex (loop nesting by
   indentation, `set -euo pipefail` in a script header).
4. **Statuses**: `FAIL` for deterministic detectors (`automation: full` or a
   confirmed special detector), `REVIEW` for candidates. Each finding carries
   the `note` that describes the detector's limits.

## Normalised statuses (report)

The report assigns one status per rule under these conditions.

| Status | Assigned when |
|---|---|
| `verified` | only through `--verified RULE=evidence`, never from a declaration, and never while a FAIL finding exists |
| `failed` | a confirmed FAIL finding |
| `manual_review_required` | a REVIEW finding to settle |
| `not_tested` | an applicable rule with no check run |
| `not_applicable` | a rule outside the change's scope, with a reason |

## Traceability

The report embeds each rule's identifier and version, its status, the check
method (`verify.method`), the evidence (file:line or test), the limits
(`limits`), and a timestamp. The raw findings stay in the report JSON
(`findings`).

## Post-edit hook

`ai.mistral.vibe/hooks.toml` declares a `post_tool` hook on
`write_file|edit`: Vibe runs `post_edit.py` after each write, with the added
content. The hook audits only what was written (not the whole file) and hands
the candidates back to the model through `additional_context`. It stays
silent when there's nothing to report, fails open on any error, and times out
after 20 s. To turn it off, remove `hooks.toml` from the installed copy.

## Documented limits

These limits come with every audit result.

- The static audit produces **candidates**; `FAIL` means a confirmed
  deterministic pattern, never a semantic certainty.
- Masking prevents false positives but hides patterns inside literals (a
  deliberate choice); SQL-by-concatenation detection matches the building
  pattern, not the masked content (REVIEW status).
- The validator measures nothing environmental: measurements (time, memory,
  bytes) belong to the audited project's tests.
