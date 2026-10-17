# Maintenance et contribution

Cette page décrit comment tester, faire évoluer et contribuer au catalogue.

## Tests

La suite de tests utilise la bibliothèque standard. Lancez-la depuis la racine du dépôt :

```bash
python3 -m unittest discover -s tests -t . -p "test_*.py"
```

- `tests/unit/test_rules.py` : schéma complet des fiches, unicité des IDs,
  compilation de chaque pattern, familles attendues.
- `tests/unit/test_select.py` : détection de scopes, sélection par familles,
  exclusion des règles usage.
- `tests/unit/test_audit.py` : fixtures non conformes -> règles attendues ;
  fixtures conformes -> zéro constat ; statuts FAIL/REVIEW ; masquage.
- `tests/unit/test_lang_catalogs.py` : une fixture non conforme par langage
  et framework -> règles attendues ; fixtures conformes Go/Rust -> zéro
  constat ; gardes `exclude_file`/`require_file` ; sélection par framework
  détecté (React vs Solid).
- `tests/unit/test_report.py` : statuts normalisés, `verified` exige une
  preuve, un FAIL ne peut être surdéclaré, bilan sans affirmation
  environnementale non mesurée.
- `tests/integration/test_pipeline.py` : pipeline complet select -> audit ->
  report -> bilan, CLI, et hook (entrées propres, silencieux, fail-open).

Toute modification du catalogue ou du moteur doit passer la suite complète et
régénérer `rules/index.json` (`python3 validators/green-vibe index`).

## Cycle de version

Les versions suivent SemVer.

- `VERSION` + `plugin.json.version` au rythme SemVer : patch (corrections),
  minor (règles ajoutées), major (changement de schéma).
- `CHANGELOG.md` obligatoire à chaque version.
- Pas de publication distante sans autorisation explicite de l'INR.

## Contribution

Toute contribution respecte ces exigences :

1. Fiche complète, tous les champs (cf. [regles.md](regles.md)) ; anglais pour
   le contenu des règles, français pour la doc.
2. Toute règle automatisable : `note` décrivant les limites du détecteur,
   fixtures conforme/non conforme + test.
3. Provenance obligatoire (`origin`) ; une contribution sans référence
   vérifiable reste en statut draft jusqu'à validation INR.
4. Une affirmation environnementale dans une fiche exige la mesure qui la
   fonde, sinon elle n'entre pas.
5. Les contributions de code (validateurs, hook, tests) suivent les mêmes
   exigences : stdlib uniquement, tests, fail-open pour le hook.
