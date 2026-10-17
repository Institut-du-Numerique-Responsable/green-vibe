# Green Vibe

[![Version](https://img.shields.io/github/v/release/Institut-du-Numerique-Responsable/green-vibe?sort=semver)](https://github.com/Institut-du-Numerique-Responsable/green-vibe/releases/latest)
[![Licence](https://img.shields.io/badge/licence-Apache--2.0%20%2B%20CC%20BY%204.0-yellow.svg)](LICENSE)
[![Mistral Vibe](https://img.shields.io/badge/Mistral%20Vibe-Agent%20Plugins%201.0-fa500f)](https://docs.mistral.ai/vibe/code/overview)
[![Règles NR](https://img.shields.io/badge/r%C3%A8gles%20NR-286-1b7a4a)](#ce-que-fait-green-vibe)
[![Python](https://img.shields.io/badge/python-%E2%89%A5%203.10-3776ab?logo=python&logoColor=white)](#démarrage-rapide)
[![RGESN](https://img.shields.io/badge/RGESN-crit%C3%A8res%20r%C3%A9f%C3%A9renc%C3%A9s-0b6e4f)](https://ecoresponsable.numerique.gouv.fr/publications/referentiel-general-ecoconception/)
[![GR491](https://img.shields.io/badge/GR491-INR-0b6e4f)](https://gr491.isit-europe.org/)
[![INR](https://img.shields.io/badge/INR-Institut%20du%20Num%C3%A9rique%20Responsable-4CAF50)](https://institutnr.org/)

[English](README.md) · **Français**

Numérique Responsable (Sustainable IT) natif pour [Mistral Vibe](https://docs.mistral.ai/vibe/code/overview) :
un plugin Agent Plugins 1.0 qui intègre le Numérique Responsable dans le
cycle de développement : comprendre, appliquer, vérifier, transmettre.

Le Numérique Responsable couvre quatre champs :

- **Green IT** : un numérique plus sobre (CPU, mémoire, réseau, stockage,
  contexte de l'agent) ;
- **IT for Green** : le numérique au service de la transition écologique ;
- **IT for Social** : un numérique accessible et inclusif, qui rapproche les
  gens ;
- **Social for IT** : des pratiques humaines et éthiques dans la fabrique du
  numérique.

Avec Green Vibe, l'agent écrit un code plus sobre, plus accessible, plus
fiable et plus éthique.

Par l'Institut du Numérique Responsable.

## Pourquoi un skill NR by design

Un service crée de la valeur durable s'il reste utile, accessible, sobre,
fiable et maintenable pendant toute sa vie. Vous fixez ces qualités en
écrivant le code ; un audit six mois plus tard ne peut que les constater.

- **Vous corrigez pour une ligne au lieu d'un cycle complet.** Pendant
  l'écriture, une requête non bornée ou un bouton sans libellé se corrige en
  une ligne. En production, la même correction demande un audit, un ticket,
  une revue et un déploiement.
- **L'agent reproduit ses motifs dans chaque fichier qu'il touche.** S'il
  applique les règles NR, il diffuse les bonnes pratiques à la même échelle
  que la dette qu'il aurait créée.
- **Vous décidez de la consommation dès la conception.** L'architecture, le
  modèle de données et le choix d'un modèle d'IA fixent l'essentiel des
  ressources ; une optimisation tardive ne joue que sur la marge.
- **Vous écrivez chaque écran pour tout le monde.** Une personne qui ne peut
  pas utiliser le service n'en tire aucune valeur. Green Vibe applique les
  règles d'accessibilité à chaque modification d'interface.
- **Vous décidez sur des faits.** Green Vibe ne marque `verified` que les
  règles dont le contrôle a tourné, et refuse les gains environnementaux non
  mesurés. Vos déclarations restent défendables.
- **Votre équipe apprend à chaque intervention.** Le bilan explique pourquoi
  chaque règle s'applique, et l'équipe garde ces réflexes sans l'agent.
- **Vos utilisateurs gardent leurs appareils plus longtemps.** Un code léger,
  compatible avec les terminaux anciens et les réseaux lents, retarde leur
  renouvellement. La fabrication des terminaux pèse le plus dans l'empreinte
  du numérique.

## Ce que fait Green Vibe

Green Vibe accompagne l'agent à chaque étape d'une modification de code.

- **286 règles NR** rédigées en fiches LLM-natives (`what/why/how/verify/limits`,
  provenance et référence RGESN par règle) : 13 familles transversales
  (128 règles, dont accessibilité et inclusion), 25 catalogues langages et
  frameworks (129 règles), 29 pratiques d'usage responsable de Vibe lui-même.
- **Sélection par le contexte** : le pipeline ne charge que les règles pertinentes
  (`select`), jamais tout le catalogue.
- **Vérification exécutable** : audit statique déterministe (164 règles avec
  détection : regex + détecteurs spéciaux), masquage des chaînes/commentaires
  pour éviter les faux positifs, statuts normalisés
  (`verified` uniquement si le contrôle a tourné).
- **Bilan pédagogique obligatoire** : à chaque intervention significative, un
  bilan qui cite les règles appliquées et vérifiées pendant cette intervention.
- **Hook post-edit** (fail-open) : l'audit passe même si le modèle n'y pense pas ;
  il n'audite que ce que l'écriture a ajouté.

## Démarrage rapide

Il vous faut Mistral Vibe et `python3 >= 3.10` (bibliothèque standard
uniquement).

Installez le plugin, puis rechargez les plugins dans Vibe :

```bash
# installation (portée utilisateur par défaut)
./scripts/install.sh
# dans Vibe : /reload-plugins, puis /plugins pour vérifier
```

Lancez les validateurs directement :

```bash
# les validateurs (python3 stdlib, aucune dépendance)
python3 validators/green-vibe stats
python3 validators/green-vibe select src/
python3 validators/green-vibe audit src/ > /tmp/audit.json
python3 validators/green-vibe report --audit /tmp/audit.json --intervention "..."
```

Dans Vibe, `/green-vibe` charge le skill. Le modèle le charge aussi seul pour
une tâche d'écoconception, d'accessibilité, de sobriété ou de revue de code.
Pour un scénario complet à rejouer, voir [evals/README.fr.md](evals/README.fr.md).

Lancez la suite de tests :

```bash
# tests (stdlib, aucune dépendance)
python3 -m unittest discover -s tests -t . -p "test_*.py"
```

## Documentation

Chaque document couvre un aspect du plugin. La version anglaise fait
référence ; les pages ci-dessous en sont la traduction française.

| Document | Contenu |
|---|---|
| [docs/fr/installation.md](docs/fr/installation.md) | Installation, configuration, mise à jour |
| [docs/fr/utilisation.md](docs/fr/utilisation.md) | Pipeline, modes pédagogiques, exemples |
| [docs/fr/architecture.md](docs/fr/architecture.md) | Architecture, socle commun, intégration produit |
| [docs/fr/regles.md](docs/fr/regles.md) | Base de règles, gouvernance, versionnement |
| [docs/fr/validateurs.md](docs/fr/validateurs.md) | Moteur d'audit, statuts, traçabilité |
| [docs/fr/maintenance.md](docs/fr/maintenance.md) | Maintenance, contribution, tests |
| [evals/README.fr.md](evals/README.fr.md) | Scénario de démonstration et couverture des tests |
| [CHANGELOG.fr.md](CHANGELOG.fr.md) | Historique des versions |

## Limites explicites

Green Vibe aide à décider ; il ne remplace ni un audit ni une mesure.

- Green Vibe **ne certifie rien** : aucun claim de conformité RGESN/RGAA/GR491 ;
  les scores d'outils sont des indicateurs, pas des preuves.
- Un gain technique (octets, CPU, tokens) reste un gain **technique** : toute
  affirmation environnementale exige sa propre mesure.
- L'audit statique produit des **candidats** ; seul le contexte tranche.

## Licence

Code : Apache-2.0. Règles et documentation : CC BY 4.0. Voir [LICENSE](LICENSE),
[NOTICE](NOTICE) et `LICENSES/`.
