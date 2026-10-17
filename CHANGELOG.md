# Changelog

Ce fichier consigne les évolutions de chaque version (SemVer).

## 0.2.0 (2026-10-17)

Catalogue étendu et cadrage Numérique Responsable élargi
(Green IT, IT for Green, IT for Social, Social for IT).

- 286 règles (+137) : 128 transversales, 129 langages/frameworks, 29 usages.
- 19 nouveaux catalogues : Go, Rust, PHP, Ruby, C#, Kotlin, Swift, C, C++,
  Scala, Julia, Nim, Zig, React, Vue, Angular, Svelte, Solid, Astro.
- Langages existants complétés (Python, JS/TS, Java, SQL, shell, HTML/CSS).
- Accessibilité et inclusion : sous-titres (NR-UX-009), zoom (NR-UX-010),
  focus visible (NR-UX-011), langage clair (NR-UX-012), langue du document
  (NR-LANG-HTML-004), tâche essentielle accessible à tous (NR-SERVICE-010),
  impact des choix montré aux usagers (NR-UX-008).
- Transversal : IA (baseline déterministe, mesure, quantisation, streaming,
  données filtrées), réseau, NoSQL, systèmes distribués, mobile, IoT,
  gouvernance (responsable nommé, preuves datées sans auto-certification).
- Usage de Vibe : 13 pratiques ajoutées et les 16 existantes vérifiées sur
  Vibe 2.26 et sa documentation (`/compact`, `/branch`, `/rewind`, sous-agent
  `explore`, `vibe --prompt` borné, moindre privilège, AGENTS.md, skills,
  contenus inclusifs). NR-USAGE-007/013 ne promettent plus de file d'entrée.
- Moteur : gardes de fichier `exclude_file` / `require_file`, masquage Rust
  (lifetimes), PHP/Ruby, Julia/Nim ; sélection des frameworks par détection
  (nom de fichier, import) ; motifs compilés une seule fois.
- Faux positif corrigé : NR-ALGO-009 ne prend plus `function List(props)`
  pour `list(x)` en JS.
- Provenance : chaque fiche porte `INR` et ses référentiels (RGESN, RGAA,
  WCAG) ; matrice de correspondance et `scripts/matrix.py` retirés.
- Documentation : dépannage, options CLI, flux de données, wording NR
  (Sustainable IT, pas seulement Green IT).

## 0.1.0 (2026-10-17)

Première version : règles Numérique Responsable natives pour Mistral Vibe.

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
  unitaires et d'intégration.
- Documentation : installation, utilisation, architecture (socle commun /
  adaptateur), règles, validateurs, maintenance.
