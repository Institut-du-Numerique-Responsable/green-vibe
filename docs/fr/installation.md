# Installation et configuration

[English](../installation.md) · **Français**

Cette page explique comment installer, configurer, mettre à jour et retirer Green Vibe.

## Prérequis

Pour installer Green Vibe, il vous faut :

- Mistral Vibe (le plugin est au format Agent Plugins 1.0, que Vibe charge sans adaptation).
- `python3 >= 3.10` (stdlib uniquement, aucune dépendance à installer).
  L'installeur vérifie la version.
- `rsync` (l'installeur synchronise la copie installée et supprime les
  fichiers périmés). L'installeur vérifie sa présence.

L'installeur ne copie que le nécessaire au plugin : les artefacts de
développement (`.git`, `tests/`, `evals/`, caches) sont exclus de la copie
installée.

## Installation

Deux portées d'installation sont disponibles.

### Portée utilisateur (recommandée)

Lancez l'installeur sans argument :

```bash
./scripts/install.sh            # copie vers ~/.vibe/plugins/green-vibe
```

### Portée projet (dossier de confiance requis)

Passez `project` à l'installeur :

```bash
./scripts/install.sh project    # copie vers ./.vibe/plugins/green-vibe
```

Puis dans Vibe : `/reload-plugins` (ou redémarrage), et `/plugins` pour
vérifier que `green-vibe` apparaît avec ses composants (skill, hooks,
knowledge).

Vous pouvez ensuite utiliser le skill de deux façons :

- tapez `/green-vibe` (user-invocable) ;
- laissez le modèle le charger quand une tâche concerne l'écoconception,
  l'accessibilité, la sobriété ou une revue de code (voir la `description` du SKILL.md).

### Installation skill seule (sans plugin)

Copier `skills/green-vibe/` dans `~/.vibe/skills/` ou `.vibe/skills/`, et le
reste du dépôt (`rules/`, `references/`, `validators/`) à côté. Le SKILL.md
appelle les validateurs via la variable `GV`, qui désigne la racine Green
Vibe ; la définir dans la session :

```bash
export GV="$HOME/.vibe/skills/green-vibe-root"   # exemple : là où le dépôt a été copié
python3 "$GV/validators/green-vibe" stats
```

Le plugin reste la voie canonique : lui seul apporte hooks et knowledge.

## Configuration

Le plugin fonctionne sans configuration. Options disponibles :

| Option | Effet |
|---|---|
| Désactiver le hook d'audit | Supprimer `ai.mistral.vibe/hooks.toml` de la copie installée (le hook est fail-open, il ne bloque jamais) |
| Réduire le bruit | Ajouter un fichier `.green-vibe/decisions.md` à la racine du projet audité (`NR-XXX  fichier  ACCEPTED/TODO  raison`). Le modèle le lit avant de relayer un constat déjà tranché ; l'audit CLI, lui, ne le lit pas et continue de remonter le constat |
| Forcer des familles | `select --family ai --family infra` pour une tâche hors détection de contexte |
| Suspendre la mise à jour automatique | `touch ~/.vibe/.green-vibe/no-autoupdate` (le hook de vérification sort immédiatement ; le hook d'audit n'est pas affecté) |

## Vérification de l'installation

Lancez la commande `stats` depuis la copie installée :

```bash
python3 ~/.vibe/plugins/green-vibe/validators/green-vibe stats
# doit afficher 312 règles et les familles
```

Dans Vibe, `/plugins` doit lister `green-vibe` ; `/green-vibe` doit charger le
skill.

## Mise à jour

Lancez le mode `update` de l'installeur : il récupère les changements du
dépôt source (fast-forward uniquement) et resynchronise la copie installée :

```bash
git -C <dépôt green-vibe> pull        # optionnel : le mode update fait le pull lui-même
./scripts/install.sh update            # resynchronise la copie utilisateur
# puis dans Vibe : /reload-plugins
```

Le mode `update` ne fait rien en silence : il affiche le changement de
version (`0.2.2 -> 0.2.3`) ou resynchronise les modifications locales non
committées, avec un avertissement.

Les sessions en cours gardent le snapshot du plugin au moment de leur
ouverture : `/reload-plugins` les resynchronise.

## Mises à jour automatiques

Une installation en portée utilisateur se met à jour seule, sans action :

- L'installeur enregistre le chemin du dépôt source dans
  `~/.vibe/.green-vibe/`.
- Après chaque tour, un hook fail-open vérifie le dépôt source au plus une
  fois par jour (un fichier tampon limite la vérification ; les autres tours
  coûtent un seul `stat`).
- Quand l'amont a bougé, le hook récupère les changements (fast-forward
  uniquement, uniquement si l'arbre source est propre : jamais les travaux
  non committés) et resynchronise la copie installée, puis demande un
  `/reload-plugins` dans la session.
- Les sessions en cours gardent leur snapshot jusqu'au `/reload-plugins`.

| Contrôle | Commande |
|---|---|
| Suspendre la mise à jour automatique | `touch ~/.vibe/.green-vibe/no-autoupdate` |
| Reprendre | `rm ~/.vibe/.green-vibe/no-autoupdate` |
| Mettre à jour immédiatement | `./scripts/install.sh update` |

La mise à jour automatique est propre à la portée utilisateur. Les copies
en portée projet appartiennent au workflow du projet et ne pull jamais
d'elles-mêmes.

## Dépannage

Le tableau suivant liste les symptômes courants et leur correction.

| Symptôme | Cause probable | Action |
|---|---|---|
| `install.sh` refuse de continuer | `python3` absent ou < 3.10, ou `rsync` absent du PATH | Installer Python 3.10+ et rsync, vérifier `python3 --version` et `rsync --version` |
| `green-vibe` absent de `/plugins` | Session ouverte avant l'installation | `/reload-plugins` ou redémarrer Vibe |
| Portée projet ignorée | Dossier non marqué de confiance dans Vibe | Marquer le dossier de confiance, puis `/reload-plugins` |
| Aucun retour du hook après une écriture | Normal si rien à signaler (silence) ; sinon erreur avalée (fail-open) | Lancer l'audit à la main sur le fichier : `python3 <racine>/validators/green-vibe audit <fichier>` |
| `select` ne retient aucune règle | Aucun langage reconnu dans les chemins fournis | Forcer une famille : `select <chemins> --family <famille>` |

## Désinstallation

Utilisez le mode `uninstall` de l'installeur, puis rechargez les plugins :

```bash
./scripts/install.sh uninstall             # portée utilisateur
./scripts/install.sh uninstall project    # portée projet
# puis /reload-plugins
```
