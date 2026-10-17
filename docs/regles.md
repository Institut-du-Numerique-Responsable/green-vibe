# La base de règles

## Contenu

- **13 familles transversales** (`rules/core/`) : strategy, service,
  architecture, ux, content, frontend, backend, data, api, infra, algo, ai,
  measure. Elles couvrent les 9 familles RGESN 2024.
- **6 catalogues langages** (`rules/lang/`) : python, javascript (JS/TS),
  java, sql, html-css, shell.
- **16 pratiques d'usage** (`rules/usage.json`) : sobriété de la conversation
  Vibe elle-même (contexte, modèle, retries, sous-agents, hooks).

## Schéma d'une fiche

Chaque règle porte les métadonnées exigées :

| Champ | Contenu |
|---|---|
| `id`, `title` | Identifiant stable NR-* et intitulé |
| `what` | La règle, impérative, une phrase |
| `why` | La raison (matière pédagogique du bilan) |
| `how` | Application concrète |
| `detect` | `automation` : `full` / `partial` / `special` / `none` + `patterns` (regex + `scope`) ou `detector` |
| `verify` | `method` (static/test/measure/review) + `how` : le contrôle propre à la règle |
| `limits` | Limites connues, affichées avec les résultats |
| `priority` | high / medium / low |
| `applies` | Périmètres d'application |
| `origin` | Provenance : `green-claude:ECO-XXX`, `green-codex:CODE-EFF-00X`, référence documentaire |
| `rgesn` | Critère RGESN associé quand il s'applique (sinon null) |
| `see` | Règles liées / références |

Les identifiants NR-* sont des identifiants Green Vibe, pas des numéros de
critères officiels ; la correspondance est dans
[matrice-correspondance.md](matrice-correspondance.md).

## Gouvernance

- **Provenance** : chaque fiche cite ses règles sources ; `scripts/matrix.py
  --check` échoue si une provenance en forme d'ID ne se résout plus dans les
  sources (garde de dérive). Les références documentaires (p. ex.
  `usage-practices.md`) sont descriptives.
- **Versionnement** : version par catalogue (`version` en tête de fichier) et
  version du plugin (`VERSION`, `plugin.json`). SemVer : une correction de
  fiche incrémente le patch, une nouvelle règle le minor, un changement de
  schéma le major. `CHANGELOG.md` consigne les évolutions.
- **Statut de validation** : les fiches v1 sont validées par l'auteur INR
  (également auteur des projets sources, qui a autorisé la réécriture). Une
  contribution externe entre en statut draft : elle ne rejoint le catalogue
  qu'après relecture et validation, avec provenance.
- **Contradictions** : jamais de fusion silencieuse. Si deux règles sources
  divergent, la fiche choisit une position, cite les deux origines et porte la
  divergence dans `limits` ou dans la matrice.
- **Dépréciation** : une règle abandonnée reste dans le catalogue avec
  `status: deprecated` (si introduit) ou est retirée avec une entrée
  `CHANGELOG` et la matrice régénérée ; les IDs ne sont jamais réutilisés.

## Ajouter une règle (v1, périmètre langages)

1. Écrire la fiche dans `rules/lang/<langage>.json` avec tous les champs.
2. Si automatisable : ajouter le `pattern` avec `scope` et une `note` décrivant
   précisément ses limites (le catalogue vit avec ses faux positifs déclarés).
3. `python3 validators/green-vibe index` (régénère `rules/index.json`).
4. Ajouter un test sur fixture conforme + non conforme
   (`tests/unit/test_audit.py`, fixtures dans `tests/fixtures/`).
5. `python3 scripts/matrix.py --check` puis régénérer la matrice.
6. Exécuter la suite de tests ; mettre à jour `CHANGELOG.md`.
