# NR referentials and routing

Green Vibe rule identifiers (NR-*) are project rules, not official criterion
numbers. Each rule sheet records its provenance (`origin`) and, when one
applies, the related RGESN criterion (`rgesn`).

## Referentials

- **RGESN 2024** (78 criteria, 9 families; ARCEP/ARCOM/ADEME): environmental
  design of digital services. The 9 families map to the rule families:
  strategy (NR-STRAT), specifications/service (NR-SERVICE), architecture
  (NR-ARCH), UX (NR-UX), content (NR-CONTENT), frontend (NR-FRONT), backend
  (NR-BACK, NR-DATA, NR-API), hosting (NR-INFRA), algorithms (NR-ALGO, NR-AI).
- **GR491** (INR): lifecycle design decisions, cross-cutting.
- **RGAA 4.1 / WCAG 2.2**: accessibility and inclusion (IT for Social) —
  NR-UX-001, NR-UX-009 to NR-UX-012, NR-SERVICE-010, NR-LANG-HTML-003,
  NR-LANG-HTML-004. Criterion numbers are cited in each sheet's `origin`.
- **Opquast**: web quality — NR-UX-006, NR-API-006.

## Discipline

- Never convert a tool score (EcoIndex, Lighthouse, sonar) into compliance
  with a referential.
- Cite a referential only when the evidence supports the reference.
- Attribution to a person requires a verifiable primary source for the exact
  claim; without one, present content as project guidance.

## Where the full material lives

- Rule catalog: `rules/core/*.json`, `rules/lang/*.json`, `rules/usage.json`, `rules/tokens.json`,
  compact index at `rules/index.json`.
- Methodology: `references/three-u.md` (3U test),
  `references/measurement.md` (measurement discipline),
  `references/criteria.md` (referential routing),
  `references/responsible-ai-charter.md` (AI charter).
