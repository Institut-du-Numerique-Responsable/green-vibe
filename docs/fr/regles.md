# La base de règles

[English](../rules.md) · **Français**

Cette page décrit le contenu du catalogue, le schéma d'une fiche et sa gouvernance.

## Contenu

Le catalogue se répartit en trois ensembles.

- **13 familles transversales** (`rules/core/`) : strategy, service,
  architecture, ux, content, frontend, backend, data, api, infra, algo, ai,
  measure. Elles couvrent les 9 familles RGESN 2024.
- **25 catalogues langages et frameworks** (`rules/lang/`) :
  - langages : python, javascript (JS/TS), java, sql, html-css, shell, go,
    rust, php, ruby, csharp, kotlin, swift, c, cpp, scala, julia, nim, zig ;
  - frameworks : react, vue, angular, svelte, solid, astro. Ils partagent
    les extensions JS/TS : `select` les retient selon le framework détecté
    (nom de fichier, import), pas selon l'extension seule.
- **29 pratiques d'usage** (`rules/usage.json`) : usage sobre, fiable et
  éthique de Vibe lui-même (brief, contexte, `/compact`, `/branch`,
  `/rewind`, modèle, sous-agents, exécutions headless bornées, moindre
  privilège, AGENTS.md, skills, contenus inclusifs).

## Schéma d'une fiche

Chaque règle porte les métadonnées exigées :

| Champ | Contenu |
|---|---|
| `id`, `title` | Identifiant stable NR-* et intitulé |
| `what` | La règle, impérative, une phrase |
| `why` | La raison (matière pédagogique du bilan) |
| `how` | Application concrète |
| `detect` | `automation` : `full` / `partial` / `special` / `none` + `patterns` (regex + `scope`, gardes optionnelles `exclude_file` / `exclude_import` / `require_file`, options `in_loop` et `text`) ou `detector` |
| `verify` | `method` (static/test/measure/review) + `how` : le contrôle propre à la règle |
| `limits` | Limites connues, affichées avec les résultats |
| `priority` | high / medium / low |
| `applies` | Périmètres d'application |
| `origin` | Provenance : `INR`, puis les référentiels liés (`RGESN 7.1`, `RGAA 4.1 criterion 10.7`, `WCAG 2.2 SC 2.4.7`…) |
| `rgesn` | Critère RGESN associé quand il s'applique (sinon null) |
| `see` | Règles liées / références |

Les identifiants NR-* sont des identifiants Green Vibe, pas des numéros de
critères officiels ; le critère officiel figure dans `rgesn` et `origin`.

## Gouvernance

Ces principes encadrent l'évolution du catalogue.

- **Provenance** : chaque fiche porte `INR` et les référentiels qu'elle
  applique (RGESN, RGAA, WCAG…). Une fiche cite un référentiel seulement
  si elle en applique le critère.
- **Versionnement** : version par catalogue (`version` en tête de fichier) et
  version du plugin (`VERSION`, `plugin.json`). SemVer : une correction de
  fiche incrémente le patch, une nouvelle règle le minor, un changement de
  schéma le major. `CHANGELOG.md` consigne les évolutions.
- **Statut de validation** : les fiches sont validées par l'INR. Une
  contribution externe entre en statut draft : elle ne rejoint le catalogue
  qu'après relecture et validation.
- **Contradictions** : jamais de fusion silencieuse. Si deux règles
  divergent, la fiche choisit une position et porte la divergence dans
  `limits`.
- **Dépréciation** : une règle abandonnée reste dans le catalogue avec
  `status: deprecated` (si introduit) ou est retirée avec une entrée
  `CHANGELOG` ; les IDs ne sont jamais réutilisés.

## Ajouter une règle (périmètre langages)

Suivez ces étapes pour ajouter une règle de langage :

1. Écrire la fiche dans `rules/lang/<langage>.json` avec tous les champs. Un
   nouveau langage demande aussi son extension dans `EXT_SCOPES`, son
   masquage dans `audit.mask_text` et sa famille dans
   `context._lang_family_scopes` (ou `FRAMEWORK_FAMILIES` pour un framework).
2. Si automatisable : ajouter le `pattern` avec `scope` et une `note` décrivant
   précisément ses limites (le catalogue vit avec ses faux positifs déclarés).
   Trois gardes au niveau du fichier réduisent le bruit :
   - `exclude_file` : liste de regex lues sur le texte masqué ; une
     correspondance signifie que le code traite déjà le sujet
     (`defer resp.Body.Close()`, `takeUntilDestroyed`…) et rend le motif
     silencieux. Un appel cité en commentaire ne compte pas ;
   - `exclude_import` : liste de regex lues sur le texte brut ; un import
     écarte le motif (autre framework, bibliothèque de virtualisation) ;
   - `require_file` : liste de regex lues sur le texte brut ; le motif ne
     s'applique que si le fichier en contient une (import `@angular/core`,
     `solid-js`…).
   Une garde agit sur tout le fichier : choisissez-la précise, sinon elle
   fait taire de vrais candidats. Le motif lui-même lit le texte masqué.
   Deux options de motif existent : `"in_loop": true` ne garde un constat
   que dans le corps d'une boucle for/while (par indentation), et
   `"text": "raw"` lit aussi les littéraux. Pour l'indentation en début de
   ligne, écrivez l'indentation `^[ \t]*`, jamais `^\s*` : `\s`
   avale les retours ligne et rend le scan quadratique (un test le vérifie).
3. `python3 validators/green-vibe index` (régénère `rules/index.json`).
4. Ajouter un test sur fixture conforme + non conforme
   (`tests/unit/test_lang_catalogs.py`, fixtures dans `tests/fixtures/lang/`).
5. Exécuter la suite de tests ; mettre à jour `CHANGELOG.md` et
   `CHANGELOG.fr.md`.
