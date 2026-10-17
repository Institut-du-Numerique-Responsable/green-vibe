# Maintenance et contribution

## Tests

```bash
python3 -m unittest discover -s tests -t . -p "test_*.py"
```

- `tests/unit/test_rules.py` : schéma complet des 149 fiches, unicité des IDs,
  compilation de chaque pattern, familles attendues.
- `tests/unit/test_select.py` : détection de scopes, sélection par familles,
  exclusion des règles usage.
- `tests/unit/test_audit.py` : fixtures non conformes -> règles attendues ;
  fixtures conformes -> zéro constat ; statuts FAIL/REVIEW ; masquage.
- `tests/unit/test_report.py` : statuts normalisés, `verified` exige une
  preuve, un FAIL ne peut être surdéclaré, bilan sans affirmation
  environnementale non mesurée.
- `tests/integration/test_pipeline.py` : pipeline complet select -> audit ->
  report -> bilan, CLI, et hook (entrées propres, silencieux, fail-open).

Toute modification du catalogue ou du moteur doit passer la suite complète et
régénérer `rules/index.json` + `docs/matrice-correspondance.md`.

## Garde de dérive

```bash
python3 scripts/matrix.py --check
```

Vérifie que chaque provenance en forme d'ID pointe bien vers une règle
existante dans Green Claude / Green Codex locaux (chemin configurable via
`--sources`). Sortie non nulle = provenance cassée.

## Synchronisation avec les sources

Les projets sources évoluent ; Green Vibe ne les modifie jamais et ne
synchronise jamais automatiquement. Procédure :

1. `python3 scripts/matrix.py` : régénérer la matrice et lire les changements
   de couverture (nouvelles règles source non couvertes, changements d'IDs).
2. Décider règle par règle : reprise, couverture par une règle existante, ou
   non-applicable au périmètre Vibe — et le documenter.
3. Toute reprise passe par le processus de validation (contribution),
   avec provenance et fiche complète.

## Cycle de version

- `VERSION` + `plugin.json.version` au rythme SemVer : patch (corrections),
  minor (règles ajoutées), major (changement de schéma).
- `CHANGELOG.md` obligatoire à chaque version.
- Pas de publication distante sans autorisation explicite de l'INR.

## Contribution

1. Fiche complète, tous les champs (cf. [regles.md](regles.md)) ; anglais pour
   le contenu des règles (cohérence avec les sources), français pour la doc.
2. Toute règle automatisable : `note` décrivant les limites du détecteur,
   fixtures conforme/non conforme + test.
3. Provenance obligatoire (`origin`) ; une contribution sans source vérifiable
   reste en statut draft jusqu'à validation INR.
4. Une affirmation environnementale dans une fiche exige la mesure qui la
   fonde, sinon elle n'entre pas.
5. Les contributions de code (validateurs, hook, tests) suivent les mêmes
   exigences : stdlib uniquement, tests, fail-open pour le hook.
