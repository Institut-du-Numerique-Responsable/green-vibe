---
name: green-vibe
description: |
  Apply Numérique Responsable (Sustainable IT) practices when designing,
  writing, modifying or reviewing code - Green IT (sobriety), IT for Green,
  IT for Social and Social for IT: architecture, frontend, backend, APIs,
  databases, hosting, algorithms, AI workloads, accessibility, inclusion,
  reliability, ethics. Also use for sobriety or accessibility audits
  ("écoconception", "audit sobriété", "green IT", "accessibilité", "RGAA",
  "inclusion", "RGESN", "GR491", "eco-check", "numérique responsable"), and for the
  responsible use of Vibe itself. Ends every significant intervention with a
  pedagogical NR report (bilan) grounded in rules actually applied and verified.
author: Institut du Numérique Responsable
version: 0.2.2
license: Apache-2.0 (code); CC BY 4.0 (rule content); see LICENSE
user-invocable: true
---

# Green Vibe

Comprendre, appliquer, vérifier, transmettre. Numérique Responsable is more
than Green IT: it covers Green IT (consume fewer resources - context, CPU,
memory, network, storage), IT for Green, IT for Social and Social for IT
(digital services that are accessible, inclusive and bring people together),
and reliable, ethical software. This skill exists to make code changes
sober, accessible, reliable and ethical - and to teach why, with evidence.

Why by design: you set these qualities while you write the code. A fix costs
one line now and an audit, a ticket and a redeploy later. You replicate your
patterns in every file you touch. Design choices fix most of the resources a
service consumes, and light, accessible software keeps older devices in use.
Apply the rules as you write. Two hard disciplines shape everything below:

1. **Never claim verified without a check that ran.** A rule is `verified` only
   when its own check was actually executed with a passing result. Model
   inspection alone is `not_tested`, not `verified`.
2. **Technical gains are technical claims.** Fewer bytes/CPU/tokens is real and
   worth doing. Energy, water or CO2 claims require their own measurement -
   never a ratio derived from a proxy, never a vendor percentage (see
   `references/measurement.md`, NR-USAGE-016).

## The tool

Everything runs through one CLI, stdlib Python, no installation. Locate the
plugin root once per session - try in this order and stop at the first hit:

```bash
GV="$HOME/.vibe/plugins/green-vibe"                     # user-scope install
GV=".vibe/plugins/green-vibe"                          # project-scope install
GV="$(dirname "$SKILL_DIR")/../.."                     # from the skill base dir
python3 "$GV/validators/green-vibe" stats              # smoke test
```

A silent failure of the tool is not an audit result: say so and continue with
the rule knowledge alone (rules stay readable in `rules/`).

## Pipeline

### 1. Understand and select (before writing)

Run the selection on the files the task touches - never load the whole catalog:

```bash
python3 "$GV/validators/green-vibe" select <files-or-dirs> [--family ai]
```

Read its output: scopes detected, families selected, rule ids. Load only the
compact views you need for those ids or families:

```bash
python3 "$GV/validators/green-vibe" rules <family|rule-id>
```

The full sheets carry what/why/how/verify/limits/origin per rule; the `why` and
`limits` fields are the pedagogical material - keep them for the bilan. If the
task concerns the value of a service or AI feature, read
`references/three-u.md`. If measurements are involved, read
`references/measurement.md`. If a charter assessment is requested, read
`references/responsible-ai-charter.md`.

Do not apply a rule blindly: check its `applies`/scope against the real
context, and when a rule conflicts with an explicit user decision, state the
trade-off in one sentence and deliver what the user decided.

### 2. Apply (while writing)

Follow the `how` of the selected rules when writing or modifying code.
Security, correctness, resilience and accessibility are never traded away for
sobriety (NR-UX-001, NR-SERVICE-004 note). On anything users see or read,
apply the IT for Social rules too: inclusive access (NR-SERVICE-010),
captions (NR-UX-009), zoom (NR-UX-010), visible focus (NR-UX-011), plain
language (NR-UX-012), page language (NR-LANG-HTML-004). Do not optimise without profiling
(NR-ALGO-001). One line at the end naming what you applied beats a running
commentary; stay quiet in the code itself.

### 3. Verify (after writing)

Run the audit on the files you touched:

```bash
python3 "$GV/validators/green-vibe" audit <files> > /tmp/gv-audit.json
```

A finding is a **candidate**, not a verdict. `FAIL` items come from
deterministic detectors (high confidence); `REVIEW` items need the surrounding
context - read it before relaying anything, and say what would settle each one.
Rules with `automation: none` are process rules: for those, the check is the
test, measurement or review the `verify` field names. Run it, or mark it
`not_tested`.

### 4. Report and teach (mandatory, every significant intervention)

Build the normalized results, declaring as `verified` only what actually ran
and passed:

```bash
python3 "$GV/validators/green-vibe" report --audit /tmp/gv-audit.json \
  --selected <ids...> \
  --verified "NR-XXX=tests/foo.py::test_bar" \
  --intervention "<one line>" \
  --mode pedagogique
```

Then produce the bilan in the user's language, grounded ONLY in the rules
selected, applied and verified above - never a generic best-practice list:

```
🌱 BILAN NUMÉRIQUE RESPONSABLE

INTERVENTION : <courte description>

RÈGLES NR APPLIQUÉES :
RÈGLE NR-XXX — <intitulé>
Action réalisée : <concret>
Pourquoi : <le champ why de la règle>
Vérification : <méthode réellement exécutée>
Résultat : Vérifié / Non vérifié / Échec

POINTS À EXAMINER : <règles non vérifiées ou à trancher>

💡 CE QUE TU PEUX RETENIR
<un ou deux principes réutilisables, tirés des règles ci-dessus>

BILAN : évaluées / appliquées / vérifiées / à examiner
```

Modes: **discret** (brief: rules + statuses + one takeaway) for small edits,
**pédagogique** (default, the format above), **audit** (all evaluated rules
with origins, RGESN refs, evidence, limits and arbitration). Facts go in
facts; the `why`/`limits` of the rule sheets are the teaching material.

If the project has a `.green-vibe/decisions.md`, record settled trade-offs
there (`NR-XXX  file  ACCEPTED/TODO  reason`) and read it before relaying a
finding the team has already answered.

## Sobriété of Vibe itself

The conversation has its own footprint. Apply the 29 practices of
`rules/usage.json` (view them: `rules usage`): minimal context, on-demand
retrieval, compaction, right model, deterministic tools before reasoning, no
blind retries. Present them as Green Vibe recommendations.

## What this skill does NOT do

- It does not certify: no RGESN/RGAA/GR491 compliance claim, ever - scores are
  indicators, audits are human exercises with their own procedure.
- It does not invent environmental gains: unmeasured means unknown.
- It does not block work: the post-edit hook is fail-open by design; a
  constraint that conflicts with the user's explicit decision is raised once,
  then the user decides.
