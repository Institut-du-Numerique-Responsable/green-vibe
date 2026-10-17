# Changelog

## 0.1.0 — 2026-10-17

Première version : réécriture native pour Mistral Vibe des règles des projets
Green Claude et Green Codex (réécriture autorisée par l'auteur INR).

- 149 règles NR-*, fiches LLM-natives (`what/why/how/verify/limits`,
  provenance, référence RGESN) : 13 familles transversales, 6 langages,
  16 pratiques d'usage responsable de Vibe.
- Moteur de sélection déterministe par contexte (index compact + familles).
- Moteur d'audit statique : 73 règles avec détection (regex avec scoping,
  détecteurs spéciaux), masquage chaînes/commentaires, statuts
  FAIL/REVIEW avec notes de limites.
- Rapport normalisé à 5 statuts ; `verified` uniquement avec preuve d'un
  contrôle exécuté ; bilan pédagogique (modes discret / pédagogique / audit).
- Hook Vibe `post_tool` fail-open auditant le contenu ajouté par chaque
  écriture.
- Plugin Agent Plugins 1.0 (skill, hooks, knowledge), installateur, 40 tests
  unitaires et d'intégration, matrice de correspondance générée
  (`scripts/matrix.py --check` comme garde de provenance).
- Documentation : installation, utilisation, architecture (socle commun /
  adaptateur), règles, validateurs, maintenance.
