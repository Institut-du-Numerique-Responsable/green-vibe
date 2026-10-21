# Utilisation : le pipeline

[English](../usage.md) · **Français**

Green Vibe suit le même pipeline à chaque intervention.

```text
Demande -> Analyse du contexte -> Sélection des règles -> Application
        -> Vérification -> Résultats normalisés -> Bilan pédagogique
```

## 1. Sélection des règles

Lancez la sélection sur les fichiers concernés par la tâche :

```bash
GV="$HOME/.vibe/plugins/green-vibe"
python3 "$GV/validators/green-vibe" select src/ --family ai
```

Sortie JSON : scopes détectés (langages), marqueurs projet, familles retenues,
liste des IDs de règles. Les familles toujours actives (stratégie, service,
architecture, mesure, algorithmie) s'ajoutent à chaque sélection ; les familles
frontend/backend/data/api/infra ne s'activent que si le contexte les justifie ;
les 29 règles `NR-USAGE-*` (usage de Vibe lui-même) et les 30 règles
`NR-TOK-*` de sobriété des tokens ne sont jamais auto-sélectionnées : elles
concernent la conversation, pas les fichiers.

Vue compacte d'une règle ou d'une famille :

```bash
python3 "$GV/validators/green-vibe" rules NR-DATA-004
python3 "$GV/validators/green-vibe" rules usage
python3 "$GV/validators/green-vibe" rules tokens
```

Chaque fiche : `what` (la règle), `why` (raison pédagogique), `how`
(application), `verify` (méthode de vérification), `limits`, `priority`,
`applies`, `origin` (provenance : INR et référentiels), `rgesn`
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

Lancez l'audit sur les fichiers modifiés :

```bash
python3 "$GV/validators/green-vibe" audit src/ > /tmp/gv-audit.json
```

Chaque constat porte : règle, `FAIL` (détecteur déterministe, haute confiance)
ou `REVIEW` (candidat que le contexte doit trancher), fichier:ligne, note
(limites du détecteur), `how` (comment corriger).

Les règles `automation: none` (règles de processus) se vérifient par le test,
la mesure ou la revue nommée dans leur champ `verify`. Sans exécution, le
statut reste `not_tested`, et `verified` exige une exécution.

## 4. Bilan pédagogique

Construisez le rapport normalisé et le bilan :

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
| `verified` | le contrôle propre à la règle a tourné et passe |
| `failed` | violation confirmée |
| `manual_review_required` | candidat à trancher par le contexte |
| `not_tested` | appliquée mais aucun contrôle exécuté |
| `not_applicable` | hors périmètre, avec raison |

### Les trois modes

Le mode règle le niveau de détail du bilan.

- **discret** : règles + statuts + une notion à retenir (petites modifications).
- **pédagogique** (défaut) : règles, actions, justifications, vérifications,
  enseignements.
- **audit** : toutes les règles évaluées, provenances, références RGESN,
  preuves, limites, arbitrages.

Le bilan cite les règles sélectionnées, appliquées et vérifiées pendant
l'intervention. Il n'annonce un gain environnemental qu'avec sa mesure.

### Bloc sobriété des tokens

Après toute tâche qui lance des outils ou modifie des fichiers, l'agent
ajoute au bilan un bloc « Sobriété des tokens » (NR-TOK-030) : règles NR-TOK
appliquées, optimisations, mesures fournies par Vibe (tokens d'entrée, de
sortie et de cache, appels) ou « non disponible », tests exécutés et limites.
Il n'invente aucune métrique et ne donne un pourcentage d'économie que face à
une référence comparable. Une simple question n'en reçoit pas.

## Exemple complet

Voir [evals/README.fr.md](../../evals/README.fr.md) pour le scénario de démonstration bout-en-bout
(sélection -> audit -> rapport -> bilan) rejouable sur `tests/fixtures/`.
