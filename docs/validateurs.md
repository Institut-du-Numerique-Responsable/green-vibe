# Les validateurs

## Vue d'ensemble

Un CLI unique (`validators/green-vibe`), Python stdlib, aucune installation :

| Commande | Rôle |
|---|---|
| `select <paths> [--family f]` | Analyse du contexte, familles, règles sélectionnées |
| `rules <filtre>` | Vue compacte des fiches (what/why/how/verify/auto/origin) |
| `audit <paths>` | Audit statique : constats `FAIL`/`REVIEW` par fichier:ligne |
| `report --audit f [--selected ids] [--verified R=preuve] [--mode m]` | Résultats normalisés + bilan pédagogique |
| `index` | Régénère `rules/index.json` |
| `stats` | Statistiques du catalogue |

## Moteur d'audit

1. **Énumération** : fichiers texte pertinents, exclusions standard
   (`.git`, `node_modules`, `dist`, `__pycache__`...).
2. **Masquage** : chaînes et commentaires remplacés par des espaces (positions
   préservées) avant tout matching — un anti-pattern cité dans un littéral ou
   une docstring n'est pas du code. Le shebang des scripts shell est préservé.
3. **Matching** : regex par règle, compilées une fois, scoping par type de
   fichier (`scope`) ; détecteurs spéciaux en code pour les contrôles plus
   propres qu'une regex (imbrication de boucles par indentation, `set -euo
   pipefail` en en-tête de script).
4. **Statuts** : `FAIL` pour les détecteurs déterministes (`automation: full`
   ou détecteur spécial confirmé), `REVIEW` pour les candidats — le constat
   porte toujours la `note` qui décrit ses limites.

## Statuts normalisés (rapport)

| Statut | Attribution |
|---|---|
| `verified` | uniquement via `--verified RULE=preuve`, jamais depuis une déclaration ; jamais si un constat FAIL existe |
| `failed` | constat FAIL confirmé |
| `manual_review_required` | constat REVIEW à trancher |
| `not_tested` | règle applicable sans contrôle exécuté |

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

- L'audit statique produit des **candidats** ; `FAIL` = motif déterministe
  confirmé, jamais une certitude sémantique.
- Le masquage protège des faux positifs mais rend invisibles les motifs dans
  les littéraux (choix assumé) ; la détection SQL par concaténation matche le
  motif de construction, pas le contenu masqué (statut REVIEW).
- Aucune mesure environnementale n'est faite par le validateur : les mesures
  (temps, mémoire, octets) appartiennent aux tests du projet audité.
