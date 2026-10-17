# Évaluation de démonstration : pipeline complet

Scénario rejouable sur les fixtures du dépôt : un mini-projet (module API
Python + page HTML + SQL + script shell) passe par les quatre étapes du
pipeline. C'est le scénario de la phase de démonstration du projet.

```bash
GV=$(pwd)
FIX=tests/fixtures

# 1. Contexte et sélection des règles
python3 validators/green-vibe select $FIX > /tmp/gv-select.json

# 2. Audit déterministe
python3 validators/green-vibe audit \
  $FIX/api_bad.py $FIX/query_bad.sql $FIX/page_bad.html \
  > /tmp/gv-audit.json

# 3. Rapport normalisé + bilan pédagogique
python3 validators/green-vibe report \
  --audit /tmp/gv-audit.json \
  --selected $(python3 -c "import json;print(' '.join(json.load(open('/tmp/gv-select.json'))['selected_rules']))") \
  --verified "NR-DATA-004=tests/integration/test_pipeline.py::fixture" \
  --intervention "Refonte d'un module API : pagination, appels HTTP, requêtes SQL" \
  --mode pedagogique
```

Attendu (versions non conformes des fixtures) :

- sélection : familles backend/data/api/frontend/content/ux + langages
  py/sql/html/sh + familles toujours actives ;
- audit : `FAIL` sur `SELECT *` (NR-LANG-SQL-001), `REVIEW` sur N+1
  (NR-LANG-PY-003), autoplay vidéo (NR-CONTENT-002), script bloquant
  (NR-FRONT-003), etc. ;
- rapport : aucun statut `verified` sans `--verified` avec preuve ;
- bilan : comptes cohérents avec les statuts, aucune affirmation
  environnementale non mesurée.

La même séquence sur les fixtures `_good` ne produit aucun constat : c'est le
test de non-régression du taux de faux positifs du catalogue.

## Scénarios fonctionnels couverts par la suite de tests

Chaque scénario du projet correspond à un test automatisé.

| Scénario | Test |
|---|---|
| API (N+1, timeout, injection SQL) | `test_audit.py::test_api_bad_flags_expected_rules` |
| Page frontend (médias, scripts, a11y) | `test_audit.py::test_html_bad_flags_expected_rules` |
| Requête SQL (SELECT *, sous-requêtes) | `test_audit.py::test_sql_bad_flags_expected_rules` |
| Code déjà conforme | `test_audit.py` (`_good` fixtures) + `test_pipeline.py::test_conforming_project_reports_no_findings` |
| Règle non applicable / non sélectionnée | `test_select.py::test_no_relevant_rules_for_plain_docs` |
| Détecteur indisponible (outil absent) | SKILL.md fallback + fail-open du hook (`test_hook_fails_open_on_bad_input`) |
| Langages et frameworks (Go, Rust, PHP, Ruby, C#, Kotlin, Swift, C/C++, Scala, Julia, Nim, Zig, React, Vue, Angular, Svelte, Solid, Astro) | `test_lang_catalogs.py::test_bad_fixtures_flag_expected_rules` |
| Accessibilité (langue, zoom, focus, sous-titres, animations) | `test_lang_catalogs.py` (`a11y_bad.html`) |
| Préoccupation déjà traitée dans le fichier (garde) | `test_lang_catalogs.py::TestFileGuards` |
| Bilan pédagogique | `test_report.py::test_bilan_counts` |
| Gain non mesuré | `test_report.py::test_bilan_contains_no_unmeasured_environmental_claim` |

Les scénarios « demande complexe », « règles contradictoires » et
« ajout de dépendance » s'exercent en revue guidée : les règles correspondantes
(NR-ARCH-008, NR-MEASURE-002, arbitrages SKILL.md) sont de processus
(`automation: none`) ; leurs preuves sont documentées dans les fiches, pas
automatisables en statique.
