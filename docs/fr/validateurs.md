# Les validateurs

[English](../validators.md) · **Français**

Cette page décrit le CLI, le moteur d'audit, les statuts et le hook.

## Vue d'ensemble

Un CLI unique (`validators/green-vibe`), Python stdlib, aucune installation :

| Commande | Rôle |
|---|---|
| `select <paths> [--family f]` | Analyse du contexte, familles, règles sélectionnées |
| `rules <filtre>` | Vue compacte des fiches (what/why/how/verify/auto/origin) |
| `audit <paths>` | Audit statique : constats `FAIL`/`REVIEW` par fichier:ligne |
| `report --audit f [--selected ids] [--verified R=preuve] [--mode m]` | Résultats normalisés + bilan pédagogique |
| `index [--out f]` | Régénère `rules/index.json` (ou `f`) |
| `stats` | Statistiques du catalogue |

Options et comportements communs :

- `--root DIR` (avant la sous-commande) : racine Green Vibe à utiliser ;
  autodétectée par défaut. `stats` ignore cette option.
- `select --family f` est répétable (`--family ai --family infra`).
- `rules` filtre par sous-chaîne d'ID ou de famille (`rules data`,
  `rules NR-DATA-004`) ; sans argument, liste tout le catalogue.
- `report --json` sort le rapport complet (résultats, constats, bilan) au lieu
  du seul bilan texte. Sans `--selected`, le rapport porte sur les règles qui
  ont au moins un constat.
- `--selected` attend des IDs **séparés** : `--selected NR-A NR-B`. Une chaîne
  entre guillemets `"NR-A NR-B"` est lue comme un seul ID.
- Sorties : JSON sur stdout ; `audit` résume aussi chaque constat sur stderr.
  Toutes les commandes sortent en code 0, constats ou non : l'audit informe,
  il ne bloque pas.

## Moteur d'audit

L'audit procède en quatre étapes.

1. **Énumération** : fichiers des 25 catalogues (Python, JS/TS, Java, Go,
   Rust, PHP, Ruby, C#, Kotlin, Swift, C/C++, Scala, Julia, Nim, Zig, SQL,
   HTML/CSS, shell, Vue, Svelte, Astro…), exclusions standard (`.git`,
   `node_modules`, `dist`, `__pycache__`...).
2. **Masquage** : chaînes et commentaires remplacés par des espaces (positions
   préservées) avant tout matching : le moteur ignore ainsi un anti-pattern
   cité dans un littéral ou une docstring. Le shebang des scripts shell est préservé.
3. **Matching** : regex par règle, compilées une fois, scoping par type de
   fichier (`scope`), gardes de fichier (`exclude_file` sur le texte masqué,
   `exclude_import` / `require_file` sur le texte brut), garde `in_loop`
   (constat gardé seulement dans le corps d'une boucle, par indentation) ; détecteurs spéciaux en code pour les contrôles plus
   propres qu'une regex (imbrication de boucles par indentation, `set -euo
   pipefail` en en-tête de script).
4. **Statuts** : `FAIL` pour les détecteurs déterministes (`automation: full`
   ou détecteur spécial confirmé), `REVIEW` pour les candidats. Chaque constat
   porte la `note` qui décrit les limites du détecteur.

## Statuts normalisés (rapport)

Le rapport attribue un statut par règle selon ces conditions.

| Statut | Attribution |
|---|---|
| `verified` | uniquement via `--verified RULE=preuve`, jamais depuis une déclaration ; jamais si un constat FAIL existe |
| `failed` | constat FAIL confirmé |
| `manual_review_required` | constat REVIEW à trancher |
| `not_tested` | règle applicable sans contrôle exécuté |
| `not_applicable` | règle hors périmètre de l'intervention, avec raison |

## Traçabilité

Le rapport embarque : identifiant et version de chaque règle, statut, méthode
de vérification (`verify.method`), preuves (fichier:ligne ou test), limites
(`limits`), horodatage. Les constats bruts sont conservés dans le JSON du
rapport (`findings`).

## Hook post-edit

`ai.mistral.vibe/hooks.toml` déclare un hook `post_tool` sur `write_file|edit` :
Vibe exécute `post_edit.py` après chaque écriture, avec le contenu ajouté.
Le hook n'audite que ce qui a été écrit (pas le fichier entier), et rend les
candidats au modèle via `additional_context`. Silence si rien à signaler,
fail-open sur toute erreur, timeout 20 s. Désactivation : supprimer
`hooks.toml` de la copie installée.

## Limites documentées

Ces limites accompagnent chaque résultat d'audit.

- L'audit statique produit des **candidats** ; `FAIL` = motif déterministe
  confirmé, jamais une certitude sémantique.
- Le masquage protège des faux positifs mais rend invisibles les motifs dans
  les littéraux (choix assumé) ; la détection SQL par concaténation matche le
  motif de construction, pas le contenu masqué (statut REVIEW).
- Aucune mesure environnementale n'est faite par le validateur : les mesures
  (temps, mémoire, octets) appartiennent aux tests du projet audité.
