# Utilisation : le pipeline

```
Demande -> Analyse du contexte -> Sélection des règles -> Application
        -> Vérification -> Résultats normalisés -> Bilan pédagogique
```

## 1. Sélection des règles

```bash
GV="$HOME/.vibe/plugins/green-vibe"
python3 "$GV/validators/green-vibe" select src/ --family ai
```

Sortie JSON : scopes détectés (langages), marqueurs projet, familles retenues,
liste des IDs de règles. Les familles toujours actives (stratégie, service,
architecture, mesure, algorithmie) s'ajoutent automatiquement ; les familles
frontend/backend/data/api/infra ne s'activent que si le contexte les justifie ;
les 16 règles `NR-USAGE-*` (usage de Vibe lui-même) ne sont jamais
auto-sélectionnées : elles concernent la conversation, pas les fichiers.

Vue compacte d'une règle ou d'une famille :

```bash
python3 "$GV/validators/green-vibe" rules NR-DATA-004
python3 "$GV/validators/green-vibe" rules usage
```

Chaque fiche : `what` (la règle), `why` (raison pédagogique), `how`
(application), `verify` (méthode de vérification), `limits`, `priority`,
`applies`, `origin` (provenance Green Claude / Green Codex), `rgesn`
(critère associé quand il s'applique).

## 2. Application

Le modèle applique les règles sélectionnées en écrivant le code. Trois règles
de conduite :

- une règle NR ne sacrifie jamais sécurité, correction, résilience ni
  accessibilité ;
- pas d'optimisation sans profilage (NR-ALGO-001) ;
- conflit avec une décision explicite de l'utilisateur : on expose l'arbitrage
  en une phrase, puis on livre la décision de l'utilisateur.

## 3. Vérification

```bash
python3 "$GV/validators/green-vibe" audit src/ > /tmp/gv-audit.json
```

Chaque constat porte : règle, `FAIL` (détecteur déterministe, haute confiance)
ou `REVIEW` (candidat — le contexte doit trancher), fichier:ligne, note
(limites du détecteur), `how` (comment corriger).

Les règles `automation: none` (règles de processus) se vérifient par le test,
la mesure ou la revue nommée dans leur champ `verify`. Sans exécution, le
statut est `not_tested` — jamais `verified`.

## 4. Bilan pédagogique

```bash
python3 "$GV/validators/green-vibe" report \
  --audit /tmp/gv-audit.json \
  --selected NR-DATA-001 NR-DATA-002 ... \
  --verified "NR-DATA-004=tests/test_pagination.py::test_last_page" \
  --intervention "Pagination par curseur sur /orders" \
  --mode pedagogique
```

Statuts normalisés :

| Statut | Signifie |
|---|---|
| `verified` | le contrôle propre à la règle a réellement été exécuté et passe |
| `failed` | violation confirmée |
| `manual_review_required` | candidat à trancher par le contexte |
| `not_tested` | appliquée mais aucun contrôle exécuté |
| `not_applicable` | hors périmètre, avec raison |

### Les trois modes

- **discret** : règles + statuts + une notion à retenir (petites modifications).
- **pédagogique** (défaut) : règles, actions, justifications, vérifications,
  enseignements.
- **audit** : toutes les règles évaluées, provenances, références RGESN,
  preuves, limites, arbitrages.

Le bilan ne mentionne que les règles réellement sélectionnées, appliquées et
vérifiées, et ne présente jamais de gain environnemental non mesuré.

## Exemple complet

Voir `evals/README.md` pour le scénario de démonstration bout-en-bout
(sélection -> audit -> rapport -> bilan) rejouable sur `tests/fixtures/`.
