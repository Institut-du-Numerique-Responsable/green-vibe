# Usage: the pipeline

**English** · [Français](fr/utilisation.md)

Green Vibe follows the same pipeline for every change.

```text
Request -> Context analysis -> Rule selection -> Application
        -> Verification -> Normalised results -> Teaching report
```

## 1. Select the rules

Run the selection on the files the task touches:

```bash
GV="$HOME/.vibe/plugins/green-vibe"
python3 "$GV/validators/green-vibe" select src/ --family ai
```

The JSON output lists the detected scopes (languages), project markers,
selected families, and rule IDs. The always-on families (strategy, service,
architecture, measure, and algorithms) join every selection. The frontend,
backend, data, api, and infra families turn on only when the context calls
for them. The 29 `NR-USAGE-*` rules (use of Vibe itself) are never selected
automatically: they concern the conversation, not the files.

Show a compact view of a rule or a family:

```bash
python3 "$GV/validators/green-vibe" rules NR-DATA-004
python3 "$GV/validators/green-vibe" rules usage
```

Each sheet carries `what` (the rule), `why` (the teaching rationale), `how`
(how to apply it), `verify` (how to check it), `limits`, `priority`,
`applies`, `origin` (provenance: INR and referentials), and `rgesn` (the
related criterion, when one applies).

## 2. Apply

The model applies the selected rules while it writes the code. Three
principles guide it:

- a Sustainable IT rule never trades away security, correctness, resilience,
  or accessibility
- no optimisation without profiling (NR-ALGO-001)
- when a rule conflicts with an explicit user decision, the model states the
  trade-off in one sentence, then delivers what the user decided

## 3. Verify

Run the audit on the changed files:

```bash
python3 "$GV/validators/green-vibe" audit src/ > /tmp/gv-audit.json
```

Each finding carries the rule, `FAIL` (deterministic detector, high
confidence) or `REVIEW` (a candidate the context must settle), file:line, a
note (the detector's limits), and `how` (how to fix it).

Rules with `automation: none` (process rules) are checked by the test,
measurement, or review named in their `verify` field. Until that check runs,
the status stays `not_tested`; `verified` requires an execution.

## 4. Write the teaching report

Build the normalised results and the report:

```bash
python3 "$GV/validators/green-vibe" report \
  --audit /tmp/gv-audit.json \
  --selected NR-DATA-001 NR-DATA-002 ... \
  --verified "NR-DATA-004=tests/test_pagination.py::test_last_page" \
  --intervention "Cursor pagination on /orders" \
  --mode pedagogique
```

The report uses these normalised statuses:

| Status | Meaning |
|---|---|
| `verified` | the rule's own check ran and passed |
| `failed` | confirmed violation |
| `manual_review_required` | candidate the context must settle |
| `not_tested` | applied, but no check ran |
| `not_applicable` | out of scope, with a reason |

### The three modes

The mode sets the report's level of detail.

- **discret**: rules, statuses, and one takeaway (small changes)
- **pedagogique** (default): rules, actions, rationale, checks, and lessons
- **audit**: every evaluated rule, provenance, RGESN references, evidence,
  limits, and trade-offs

The report cites the rules selected, applied, and verified during the change.
It reports an environmental gain only with its measurement.

## Full example

See [evals/README.md](../evals/README.md) for the end-to-end demo scenario
(selection, audit, report) you can replay on `tests/fixtures/`.
