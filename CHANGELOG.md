# Changelog

**English** · [Français](CHANGELOG.fr.md)

This file records the changes in each version (SemVer).

## 0.2.0 (2026-10-17)

Extended catalog and a broader Sustainable IT scope (Green IT, IT for Green,
IT for Social, Social for IT).

- 286 rules (+137): 128 cross-cutting, 129 languages and frameworks, 29 usage.
- 19 new catalogs: Go, Rust, PHP, Ruby, C#, Kotlin, Swift, C, C++, Scala,
  Julia, Nim, Zig, React, Vue, Angular, Svelte, Solid, and Astro.
- Existing languages extended (Python, JS/TS, Java, SQL, shell, HTML/CSS).
- Accessibility and inclusion: captions (NR-UX-009), zoom (NR-UX-010),
  visible focus (NR-UX-011), plain language (NR-UX-012), document language
  (NR-LANG-HTML-004), an essential task that works for everyone
  (NR-SERVICE-010), and the impact of choices shown to users (NR-UX-008).
- Cross-cutting: AI (deterministic baseline, measurement, quantisation,
  streaming, filtered data), network, NoSQL, distributed systems, mobile,
  IoT, and governance (a named owner, dated evidence, no self-certification).
- Vibe usage: 13 new practices, and the 16 existing ones checked against
  Vibe 2.26 and its documentation (`/compact`, `/branch`, `/rewind`, the
  `explore` subagent, bounded `vibe --prompt` runs, least privilege,
  AGENTS.md, skills, inclusive content). NR-USAGE-007/013 no longer promise
  an input queue.
- Engine: `exclude_file`, `exclude_import`, and `require_file` file guards,
  `in_loop` and `text` pattern options, masking for Rust (lifetimes),
  PHP/Ruby, and Julia/Nim, framework selection by detection (file name,
  import), and patterns compiled once.
- Review fixes: five `^\s*` patterns made linear (`^[ \t]*`); `exclude_file`
  reads the masked text and `exclude_import` handles imports; overly broad
  guards removed (NR-LANG-RS-005 `#[cfg(test)]`, NR-LANG-GO-001/002);
  single-pass PHP/Ruby masking (`'#'` inside a string); `async for`
  recognised.
- False positive fixed: NR-ALGO-009 no longer reads `function List(props)` as
  `list(x)` in JS.
- Provenance: each sheet carries `INR` and its referentials (RGESN, RGAA,
  WCAG); the correspondence matrix and `scripts/matrix.py` were removed.
- Documentation: in English, with a French translation (`docs/fr/`,
  `README.fr.md`, `evals/README.fr.md`, `CHANGELOG.fr.md`); troubleshooting,
  CLI options, data flow, and Sustainable IT wording (more than Green IT).

## 0.1.0 (2026-10-17)

First release: native Sustainable IT rules for Mistral Vibe.

- 149 NR-* rules as LLM-native sheets (`what/why/how/verify/limits`,
  provenance, RGESN reference): 13 cross-cutting families, 6 languages, and
  16 practices for using Vibe responsibly.
- Deterministic, context-driven selection engine (compact index + families).
- Static audit engine: 73 rules with detection (scoped regex, special
  detectors), string and comment masking, and FAIL/REVIEW statuses with
  limit notes.
- Normalised report with 5 statuses; `verified` only with evidence of a check
  that ran; teaching report (discret / pedagogique / audit modes).
- Fail-open Vibe `post_tool` hook that audits the content each write adds.
- Agent Plugins 1.0 plugin (skill, hooks, knowledge), installer, and 40 unit
  and integration tests.
- Documentation: installation, usage, architecture (shared core / adapter),
  rules, validators, and maintenance.
