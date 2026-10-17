# Architecture

## Vue d'ensemble

```
green-vibe/
├── plugin.json                    Manifeste Agent Plugins 1.0 (namespace greenVibe)
├── skills/green-vibe/SKILL.md     Entrée du modèle : pipeline, disciplines, bilan
├── rules/                         SOCLE COMMUN (sans dépendance Vibe)
│   ├── index.json                 Index compact (1 ligne par règle, généré)
│   ├── core/*.json                13 familles transversales (79 règles)
│   ├── lang/*.json                6 langages (31 règles)
│   └── usage.json                 16 pratiques d'usage de Vibe
├── references/                    3U, mesure, critères, charte IA
├── validators/
│   ├── green-vibe                 Lanceur CLI (aucune installation)
│   └── green_vibe/                rules, context (sélection), audit, report, cli
├── ai.mistral.vibe/
│   ├── hooks.toml                 Hook post_tool (audit de l'écrit, fail-open)
│   └── hooks/post_edit.py         Implémentation du hook
│   └── knowledge/nr-referentiels/ Entrée knowledge (routage référentiels)
├── scripts/                       install.sh, matrix.py
├── tests/                         unit + integration + fixtures
├── evals/                         Scénarios de démonstration
└── docs/
```

## Socle commun / adaptateur

La séparation demandée pour la mutualisation future est explicite :

- **Socle commun NR** : `rules/` + `references/`. Zéro dépendance envers Vibe,
  zéro référence à l'agent dans les fiches (sauf `rules/usage.json`, propre à
  chaque assistant). Ce répertoire est extractible tel quel vers un futur
  dépôt **GREEN-NR-KNOWLEDGE** partagé par les adaptateurs Green Claude,
  Green Codex et Green Vibe.
- **Adaptateur Vibe** : `skills/`, `ai.mistral.vibe/`, `validators/`. Il encode
  le pipeline, les hooks et le bilan propre à Vibe.

La matrice de correspondance (`scripts/matrix.py`) garantit la traçabilité
socle -> sources et sert de garde de dérive (`--check`) quand les projets
sources évoluent.

## Choix de conception

| Choix | Raison |
|---|---|
| Plugins Agent Plugins 1.0 | Format natif Vibe (skills + hooks + knowledge) ; aligne la proposition INR |
| Index JSON + sélection déterministe | Pas de RAG : la sélection doit être rapide, explicable, reproductible |
| Python stdlib pour les validateurs | Aucune dépendance, exécutable partout, testable |
| Statuts 5 états avec `verified` réservé | Anti « déclaration = conformité » : la preuve est le contrôle exécuté |
| Hook post_tool fail-open | Garantie d'audit sans jamais bloquer le travail |
| Bilan dans le SKILL + rendu par `report` | La pédagogie est obligatoire mais fondée sur les résultats réels |
| Masquage chaînes/commentaires avant détection | Faux positifs : le code mort dans un littéral n'est pas du code |

## Capacités Vibe utilisées

| Capacité | Classe | Usage |
|---|---|---|
| Skills natifs + plugins Agent Plugins 1.0 | native (vérifiée) | distribution, entrée du pipeline |
| Hooks `post_tool` (`additional_context`) | native (vérifiée) | audit automatique de l'écrit |
| Knowledge `KNOWLEDGE.md` | native (présence vérifiée ; sémantique d'injection vérifiée à l'installation) | routage référentiels |
| Bash + outils fichiers | native | exécution des validateurs |
| Hooks `UserPromptSubmit`/`Stop` | indisponible | le cache zéro-token de Green Claude n'est pas transposé |
| RAG vectoriel | indisponible (et non voulu) | sélection déterministe par index |

## Intégration produit (pour les équipes Mistral)

L'objectif de cette architecture est de rendre l'adoption native triviale :

1. **Compatibilité zéro-code** : le plugin fonctionne sans aucun changement de
   Vibe ; l'installation est une copie de répertoire.
2. **Contenu extractible** : `rules/` + `references/` forment un socle NR
   autonome (JSON documenté), réutilisable pour une intégration native
   (skill proposé à l'onboarding, base d'un mode audit produit) ou pour un
   référentiel commun multi-assistants.
3. **Droits clairs** : Apache-2.0 (code) + CC BY 4.0 (contenu), paternité INR,
   réécriture autorisée par l'auteur des projets sources.
4. **Aucun service externe** : pas d'appel réseau, pas de télémétrie, aucune
   dépendance pip/npm ; le hook a un timeout et un fail-open explicites.
5. **Canaux proposés** (cf. proposition INR niveau 1->3) : page de doc Vibe
   référençant le plugin ; registre de plugins ; à terme skill NR proposé par
   défaut et pratiques d'usage de l'agent co-écrites.

Ce dossier tient lieu de dossier d'intégration pour un éventuel travail
conjoint avec l'équipe produit Vibe.
