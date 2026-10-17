# Architecture

**English** · [Français](fr/architecture.md)

This page describes how the repository is organised and the choices behind it.

## Overview

The repository separates the rule core from the Vibe adapter.

```text
green-vibe/
├── plugin.json                    Agent Plugins 1.0 manifest (namespace greenVibe)
├── skills/green-vibe/SKILL.md     Model entry point: pipeline, disciplines, report
├── rules/                         SHARED CORE (no Vibe dependency)
│   ├── index.json                 Compact index (one line per rule, generated)
│   ├── core/*.json                13 cross-cutting families (128 rules)
│   ├── lang/*.json                19 languages + 6 frameworks (129 rules)
│   └── usage.json                 29 practices for using Vibe
├── references/                    3U, measurement, criteria, AI charter
├── validators/
│   ├── green-vibe                 CLI launcher (no installation)
│   └── green_vibe/                rules, context (selection), audit, report, cli
├── ai.mistral.vibe/
│   ├── hooks.toml                 post_tool hook (audits what was written, fail-open)
│   ├── hooks/post_edit.py         Hook implementation
│   └── knowledge/nr-referentiels/ Knowledge entry (referential routing)
├── scripts/                       install.sh
├── tests/                         unit + integration + fixtures (fixtures/lang/ per language)
├── evals/                         Demo scenarios
└── docs/                          English documentation (French in docs/fr/)
```

## Data flow

The commands chain like this, from rule selection to the report.

```text
project files ──> select ──> selected rule IDs ─┐
      │                                         ├──> report ──> teaching report
      └────────> audit ──> FAIL/REVIEW findings ┘      (text or --json)
                                ▲
Vibe write (write_file|edit) ──> post_edit.py hook ──> additional_context
```

- `select` and `audit` write their JSON to **stdout**; `audit` also
  summarises each finding on **stderr** (human-readable, and it leaves the
  redirected JSON intact).
- `report` reads the audit JSON and gives `verified` only to rules passed
  with `--verified RULE=evidence`.
- The hook reuses the audit engine on the content the write added, and on
  nothing else.

## Shared core and adapter

The split is explicit, so other agents can reuse the core later:

- **Sustainable IT core**: `rules/` and `references/`. No dependency on Vibe,
  and no reference to the agent in the sheets (except `rules/usage.json`,
  which is specific to each assistant). You can extract this directory as is
  into a Sustainable IT referential shared by several coding agents.
- **Vibe adapter**: `skills/`, `ai.mistral.vibe/`, and `validators/`. It
  encodes the pipeline, the hooks, and the Vibe-specific report.

## Design choices

Each choice answers an explicit constraint.

| Choice | Reason |
|---|---|
| Agent Plugins 1.0 plugin | Native Vibe format (skills, hooks, and knowledge); matches the INR proposal |
| JSON index and deterministic selection | No RAG: selection must be fast, explainable, and reproducible |
| Standard-library Python validators | No dependency, runs anywhere, testable |
| Five statuses with `verified` reserved | Guards against "declared means compliant": the evidence is the check that ran |
| Fail-open post_tool hook | Guarantees an audit without ever blocking the work |
| Report in SKILL.md, rendered by `report` | Teaching is mandatory but grounded in real results |
| Mask strings and comments before detection | Fewer false positives: dead code in a literal isn't code |

## Vibe capabilities used

The plugin uses only native Vibe capabilities.

| Capability | Class | Use |
|---|---|---|
| Native skills + Agent Plugins 1.0 plugins | native (verified) | distribution, pipeline entry point |
| `post_tool` hooks (`additional_context`) | native (verified) | automatic audit of what was written |
| `KNOWLEDGE.md` knowledge | native (presence verified; injection behaviour checked at install) | referential routing |
| Bash and file tools | native | running the validators |
| `post_agent` hook | native (documented) | not used: forcing a retry costs a full turn; SKILL.md carries the report |
| `UserPromptSubmit` hook | unavailable | no context cache before the prompt is sent |
| Vector RAG | unavailable (and not wanted) | deterministic selection by index |

## Product integration (for Mistral teams)

This architecture aims to make native adoption trivial:

1. **Zero-code compatibility**: the plugin works with no change to Vibe;
   installing it means copying a directory.
2. **Extractable content**: `rules/` and `references/` form a standalone
   Sustainable IT core (documented JSON), reusable for a native integration
   (a skill offered at onboarding, the base of a product audit mode) or for a
   referential shared by several assistants.
3. **Clear rights**: Apache-2.0 (code) and CC BY 4.0 (content), INR authorship.
4. **No external service**: no network call, no telemetry, no pip or npm
   dependency; the hook has an explicit timeout and fails open.
5. **Proposed channels** (see the INR proposal, levels 1 to 3): a Vibe docs
   page listing the plugin, the plugin registry, and later a Sustainable IT
   skill offered by default with co-written agent usage practices.

This document doubles as the integration file for any joint work with the
Vibe product team.
