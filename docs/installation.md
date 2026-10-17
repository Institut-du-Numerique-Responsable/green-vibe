# Installation et configuration

## Prérequis

- Mistral Vibe (le plugin est au format Agent Plugins 1.0, supporté nativement).
- `python3` (stdlib uniquement, aucune dépendance à installer).

## Installation

### Portée utilisateur (recommandée)

```bash
./scripts/install.sh            # copie vers ~/.vibe/plugins/green-vibe
```

### Portée projet (dossier de confiance requis)

```bash
./scripts/install.sh project    # copie vers ./.vibe/plugins/green-vibe
```

Puis dans Vibe : `/reload-plugins` (ou redémarrage), et `/plugins` pour
vérifier que `green-vibe` apparaît avec ses composants (skill, hooks,
knowledge).

Le skill devient utilisable :

- explicitement : `/green-vibe` (user-invocable) ;
- automatiquement : le modèle le charge quand une tâche concerne l'écoconception,
  la sobriété ou une revue de code (voir la `description` du SKILL.md).

### Installation skill seule (sans plugin)

Copier `skills/green-vibe/` dans `~/.vibe/skills/` ou `.vibe/skills/`, et le
reste du dépôt (règles, validateurs) à côté, puis pointer `GV` dans la session
vers la racine. Le plugin est la voie canonique : il seul apporte hooks et
knowledge.

## Configuration

Le plugin fonctionne sans configuration. Options disponibles :

| Option | Effet |
|---|---|
| Désactiver le hook d'audit | Supprimer `ai.mistral.vibe/hooks.toml` de la copie installée (le hook est fail-open, il ne bloque jamais) |
| Réduire le bruit | Ajouter un fichier `.green-vibe/decisions.md` à la racine du projet audité (`NR-XXX  fichier  ACCEPTED  raison`) |
| Forcer des familles | `select --family ai --family infra` pour une tâche hors détection de contexte |

## Vérification de l'installation

```bash
python3 ~/.vibe/plugins/green-vibe/validators/green-vibe stats
# doit afficher 149 règles et les familles
```

Dans Vibe, `/plugins` doit lister `green-vibe` ; `/green-vibe` doit charger le
skill.

## Mise à jour

```bash
git -C <dépôt green-vibe> pull        # ou nouvelle version téléchargée
./scripts/install.sh                  # recopie par-dessus (idempotent)
# puis dans Vibe : /reload-plugins
```

Les sessions en cours gardent le snapshot du plugin au moment de leur
ouverture : `/reload-plugins` resynchronise.

## Désinstallation

```bash
rm -rf ~/.vibe/plugins/green-vibe
# puis /reload-plugins
```
