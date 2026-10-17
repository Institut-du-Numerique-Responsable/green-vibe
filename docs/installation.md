# Installation et configuration

Cette page explique comment installer, configurer, mettre à jour et retirer Green Vibe.

## Prérequis

Pour installer Green Vibe, il vous faut :

- Mistral Vibe (le plugin est au format Agent Plugins 1.0, que Vibe charge sans adaptation).
- `python3 >= 3.10` (stdlib uniquement, aucune dépendance à installer).
  L'installeur vérifie la version.

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

## Vérification de l'installation

Lancez la commande `stats` depuis la copie installée :

```bash
python3 ~/.vibe/plugins/green-vibe/validators/green-vibe stats
# doit afficher 286 règles et les familles
```

Dans Vibe, `/plugins` doit lister `green-vibe` ; `/green-vibe` doit charger le
skill.

## Mise à jour

Récupérez la nouvelle version, puis relancez l'installeur :

```bash
git -C <dépôt green-vibe> pull        # ou nouvelle version téléchargée
./scripts/install.sh                  # recopie par-dessus (idempotent)
# puis dans Vibe : /reload-plugins
```

Les sessions en cours gardent le snapshot du plugin au moment de leur
ouverture : `/reload-plugins` resynchronise.

## Dépannage

Le tableau suivant liste les symptômes courants et leur correction.

| Symptôme | Cause probable | Action |
|---|---|---|
| `install.sh` refuse de continuer | `python3` absent ou < 3.10 | Installer Python 3.10+ et vérifier `python3 --version` |
| `green-vibe` absent de `/plugins` | Session ouverte avant l'installation | `/reload-plugins` ou redémarrer Vibe |
| Portée projet ignorée | Dossier non marqué de confiance dans Vibe | Marquer le dossier de confiance, puis `/reload-plugins` |
| Aucun retour du hook après une écriture | Normal si rien à signaler (silence) ; sinon erreur avalée (fail-open) | Lancer l'audit à la main sur le fichier : `python3 <racine>/validators/green-vibe audit <fichier>` |
| `select` ne retient aucune règle | Aucun langage reconnu dans les chemins fournis | Forcer une famille : `select <chemins> --family <famille>` |

## Désinstallation

Supprimez la copie installée, puis rechargez les plugins :

```bash
rm -rf ~/.vibe/plugins/green-vibe
# puis /reload-plugins
```
