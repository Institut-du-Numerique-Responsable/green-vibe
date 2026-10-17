# The rule catalog

**English** · [Français](fr/regles.md)

This page describes what the catalog contains, the schema of a rule sheet,
and how the catalog is governed.

## Content

The catalog has three parts.

- **13 cross-cutting families** (`rules/core/`): strategy, service,
  architecture, ux, content, frontend, backend, data, api, infra, algo, ai,
  and measure. They cover the 9 RGESN 2024 families.
- **25 language and framework catalogs** (`rules/lang/`):
  - languages: python, javascript (JS/TS), java, sql, html-css, shell, go,
    rust, php, ruby, csharp, kotlin, swift, c, cpp, scala, julia, nim, and zig
  - frameworks: react, vue, angular, svelte, solid, and astro. They share the
    JS/TS extensions, so `select` keeps them based on the detected framework
    (file name, import) rather than the extension alone.
- **29 usage practices** (`rules/usage.json`): lean, reliable, and ethical
  use of Vibe itself (brief, context, `/compact`, `/branch`, `/rewind`,
  model choice, subagents, bounded headless runs, least privilege, AGENTS.md,
  skills, and inclusive content).

## Rule sheet schema

Each rule carries the required metadata.

| Field | Content |
|---|---|
| `id`, `title` | Stable NR-* identifier and title |
| `what` | The rule, imperative, one sentence |
| `why` | The rationale (teaching material for the report) |
| `how` | How to apply it |
| `detect` | `automation`: `full` / `partial` / `special` / `none`, plus `patterns` (regex + `scope`, optional guards `exclude_file` / `exclude_import` / `require_file`, options `in_loop` and `text`) or `detector` |
| `verify` | `method` (static/test/measure/review) + `how`: the rule's own check |
| `limits` | Known limits, shown with the results |
| `priority` | high / medium / low |
| `applies` | Scopes it applies to |
| `origin` | Provenance: `INR`, then the related referentials (`RGESN 7.1`, `RGAA 4.1 criterion 10.7`, `WCAG 2.2 SC 2.4.7`…) |
| `rgesn` | Related RGESN criterion when one applies (otherwise null) |
| `see` | Related rules and references |

NR-* identifiers are Green Vibe identifiers, not official criterion numbers;
the official criterion appears in `rgesn` and `origin`.

## Governance

These principles govern how the catalog evolves.

- **Provenance**: each sheet carries `INR` and the referentials it applies
  (RGESN, RGAA, WCAG…). A sheet cites a referential only if it applies that
  criterion.
- **Versioning**: a version per catalog (`version` at the top of the file)
  and a plugin version (`VERSION`, `plugin.json`). SemVer: a sheet fix bumps
  the patch, a new rule the minor, and a schema change the major.
  `CHANGELOG.md` records the changes.
- **Validation status**: the INR validates the sheets. An external
  contribution starts as a draft and joins the catalog only after review and
  validation.
- **Contradictions**: never merge silently. When two rules diverge, the sheet
  takes a position and records the divergence in `limits`.
- **Deprecation**: a dropped rule stays in the catalog with
  `status: deprecated` (once introduced) or leaves with a `CHANGELOG` entry;
  IDs are never reused.

## Add a rule (language scope)

Follow these steps to add a language rule:

1. Write the sheet in `rules/lang/<language>.json` with every field. A new
   language also needs its extension in `EXT_SCOPES`, its masking in
   `audit.mask_text`, and its family in `context._lang_family_scopes` (or
   `FRAMEWORK_FAMILIES` for a framework).
2. If it can be automated, add the `pattern` with a `scope` and a `note` that
   states its limits precisely (the catalog lives with its declared false
   positives). Three file-level guards reduce noise:
   - `exclude_file`: regexes read on the masked text. A match means the code
     already handles the concern (`defer resp.Body.Close()`,
     `takeUntilDestroyed`…) and silences the pattern. A call quoted in a
     comment doesn't count.
   - `exclude_import`: regexes read on the raw text. An import rules the
     pattern out (another framework, a virtualisation library).
   - `require_file`: regexes read on the raw text. The pattern applies only
     if the file contains one of them (an `@angular/core` or `solid-js`
     import…).

   A guard acts on the whole file, so keep it precise or it silences real
   candidates. The pattern itself reads the masked text. Two pattern options
   are available: `"in_loop": true` keeps a hit only inside a for/while body
   (by indentation), and `"text": "raw"` matches literals too. For line-start
   indentation, write `^[ \t]*`, never `^\s*`: `\s` swallows newlines and
   makes the scan quadratic (a test checks this).
3. Run `python3 validators/green-vibe index` (regenerates `rules/index.json`).
4. Add a test on a conforming and a non-conforming fixture
   (`tests/unit/test_lang_catalogs.py`, fixtures in `tests/fixtures/lang/`).
5. Run the test suite, and update `CHANGELOG.md` and `CHANGELOG.fr.md`.
