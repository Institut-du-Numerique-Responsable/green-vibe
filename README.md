# Green Vibe

Numérique Responsable natif pour [Mistral Vibe](https://docs.mistral.ai/vibe/code/overview) :
un plugin Agent Plugins 1.0 qui intègre l'écoconception dans le cycle de
développement — comprendre, appliquer, vérifier, transmettre.

Par l'Institut du Numérique Responsable. Dérivé de
[Green Claude](https://github.com/Institut-du-Numerique-Responsable/green-claude)
et [Green Codex](https://github.com/Institut-du-Numerique-Responsable/green-codex),
dont les règles ont été réécrites pour l'agent.

## Ce que fait Green Vibe

- **149 règles NR** réécrites en fiches LLM-natives (`what/why/how/verify/limits`,
  provenance et référence RGESN par règle) : 13 familles transversales, 6
  langages, 16 pratiques d'usage responsable de Vibe lui-même.
- **Sélection par le contexte** : le pipeline ne charge que les règles pertinentes
  (`select`), jamais tout le catalogue.
- **Vérification exécutable** : audit statique déterministe (73 règles avec
  détection : regex + détecteurs spéciaux), masquage des chaînes/commentaires
  pour éviter les faux positifs, statuts normalisés
  (`verified` uniquement si le contrôle a réellement tourné).
- **Bilan pédagogique obligatoire** : à chaque intervention significative, un
  bilan fondé sur les règles réellement appliquées et vérifiées — jamais une
  liste générique.
- **Hook post-edit** (fail-open) : l'audit passe même si le modèle n'y pense pas ;
  il n'audite que ce que l'écriture a ajouté.

## Démarrage rapide

```bash
# installation (portée utilisateur par défaut)
./scripts/install.sh
# dans Vibe : /reload-plugins, puis /plugins pour vérifier
```

```bash
# les validateurs (python3 stdlib, aucune dépendance)
python3 validators/green-vibe stats
python3 validators/green-vibe select src/
python3 validators/green-vibe audit src/ > /tmp/audit.json
python3 validators/green-vibe report --audit /tmp/audit.json --intervention "..."
```

## Documentation

| Document | Contenu |
|---|---|
| [docs/installation.md](docs/installation.md) | Installation, configuration, mise à jour |
| [docs/utilisation.md](docs/utilisation.md) | Pipeline, modes pédagogiques, exemples |
| [docs/architecture.md](docs/architecture.md) | Architecture, socle commun, intégration produit |
| [docs/regles.md](docs/regles.md) | Base de règles, gouvernance, versionnement |
| [docs/validateurs.md](docs/validateurs.md) | Moteur d'audit, statuts, traçabilité |
| [docs/maintenance.md](docs/maintenance.md) | Maintenance, contribution, tests |
| [docs/matrice-correspondance.md](docs/matrice-correspondance.md) | Correspondance avec Green Claude / Green Codex |

## Limites explicites

- Green Vibe **ne certifie rien** : aucun claim de conformité RGESN/RGAA/GR491 ;
  les scores d'outils sont des indicateurs, pas des preuves.
- Un gain technique (octets, CPU, tokens) reste un gain **technique** : toute
  affirmation environnementale exige sa propre mesure.
- L'audit statique produit des **candidats** ; seul le contexte tranche.

## Licence

Code : Apache-2.0. Règles et documentation : CC BY 4.0. Voir [LICENSE](LICENSE),
[NOTICE](NOTICE) et `LICENSES/`.
