# Matrice de correspondance des règles

Générée par `scripts/matrix.py`. Une ligne = une règle Green Vibe, avec sa
provenance dans Green Claude et Green Codex, et le critère RGESN associé quand
il s'applique. Les identifiants NR-* sont des identifiants Green Vibe, pas des
numéros de critères officiels.

- Règles Green Vibe : **149**
- Green Claude : **86/250** règles source couvertes
- Green Codex : **65/159** règles source couvertes

## Correspondance par règle Green Vibe

| ID Green Vibe | Règle | Green Claude | Green Codex | RGESN |
|---|---|---|---|---|
| `NR-AI-001` | Challenge the model behind the request | ECO-ALGO-08, ECO-ALGO-19 | AI-EFF-002 | 9.x |
| `NR-AI-002` | Size the model to the task | ECO-ALGO-02, ECO-ALGO-04, ECO-ALGO-17 | — | 9.x |
| `NR-AI-003` | Trim the input before trimming anything else | ECO-ALGO-06, ECO-ALGO-16 | AI-EFF-003 | 9.x |
| `NR-AI-004` | Cache AI results where stable | ECO-ALGO-15 | AI-EFF-004 | 9.x |
| `NR-AI-005` | Batch requests | ECO-ALGO-13 | AI-EFF-005 | 9.x |
| `NR-AI-006` | Enforce the AI budget at runtime | ECO-ALGO-05, ECO-ALGO-07 | — | 9.x |
| `NR-AI-007` | Count the whole cost of a successful task | ECO-ALGO-05 | AI-EFF-001 | 9.x |
| `NR-AI-008` | Prefer RAG over fine-tuning for knowledge | ECO-ALGO-25, ECO-ALGO-27 | — | 9.x, 3.1 |
| `NR-AI-009` | Responsible AI is part of the scope | — | AI-EFF-006, responsible-ai-charter.md | — |
| `NR-ALGO-001` | No premature optimisation | ECO-STRAT-01 area | LANG-PYTHON-002 | 1.4, 1.5 |
| `NR-ALGO-002` | Complexity under control on growing inputs | ECO-BACK-03 | CODE-EFF-009 | 7.x, 9.1 |
| `NR-ALGO-003` | Stream and chunk large data | ECO-BACK-04 area | LANG-PYTHON-001 | 7.x, 9.1 |
| `NR-ALGO-004` | Beware catastrophic regex | — | CODE-EFF-004 | 7.x |
| `NR-ALGO-005` | Memoise or precompute repeated work | ECO-BACK-04 | CODE-EFF-003 | 7.x |
| `NR-ALGO-006` | Bound concurrent work | ECO-ARCH-11 | CODE-EFF-006 | 3.2, 9.1 |
| `NR-ALGO-007` | Fail fast, avoid zombie work | ECO-BACK-07 area | CODE-EFF-007 | 9.1 |
| `NR-ALGO-008` | Use the platform's async/blocking model correctly | ECO-FRONT-07 area | CODE-EFF-008 | 7.x |
| `NR-ALGO-009` | Memory bounded, swap avoided | ECO-ALGO-22, ECO-ALGO-24 | CODE-EFF-010 | 8.x, 9.x |
| `NR-API-001` | Return only the fields the client uses | ECO-BACK-09 area | API-EFF-001 | 7.1 |
| `NR-API-002` | Compression and caching headers on responses | ECO-HEB-02, ECO-HEB-03 | API-EFF-003 | 8.x |
| `NR-API-003` | Batch over chatty exchanges | ECO-ALGO area | API-EFF-001 | 7.x |
| `NR-API-004` | Rate limiting protects everyone's resources | ECO-HEB area | API-EFF-002 area | 8.x |
| `NR-API-005` | Version consciously | ECO-ARCH-03 area | SERVICE-EFF-005 | 3.4 |
| `NR-API-006` | Errors that are lightweight and useful | — | — | 4.4, 7.x |
| `NR-ARCH-001` | The least code that solves the problem | ECO-ARCH-07 | — | 3.1 |
| `NR-ARCH-002` | Prefer the simplest solution | ECO-ARCH-01 | ARCH-DIST-001 | 3.1 |
| `NR-ARCH-003` | Size resources to the real load | ECO-ARCH-02 | INFRA-EFF-001 | 3.2 |
| `NR-ARCH-004` | Bound a function before you scale it | ECO-ARCH-08 | CODE-EFF-001 | 3.2, 9.1 |
| `NR-ARCH-005` | Do not chain functions where one would do | ECO-ARCH-09 | ARCH-SERVERLESS-001 | 3.1 |
| `NR-ARCH-006` | Cache with explicit keys, TTLs and purge limits | ECO-ARCH-10 | CODE-EFF-003 | 8.x, 3.2 |
| `NR-ARCH-007` | Sober environments and CI | ECO-ARCH-04, ECO-ARCH-06 | — | 3.7 |
| `NR-ARCH-008` | Minimise and justify dependencies | ECO-FRONT-01, ECO-FRONT-04 | — | 6.x |
| `NR-ARCH-009` | Design to last | ECO-ARCH-03, ECO-ARCH-05 | — | 3.4, 3.5, 3.6 |
| `NR-BACK-001` | Timeout and retry cap on every remote call | ECO-BACK-06 | CODE-EFF-002 | 7.2, 9.1 |
| `NR-BACK-002` | Bound every loop, queue and pool | ECO-BACK-05 | CODE-EFF-001 | 9.1 |
| `NR-BACK-003` | Cache stable results with explicit invalidation | ECO-BACK-04 | CODE-EFF-003 | 7.x |
| `NR-BACK-004` | Paginate and stream, never return unbounded results | ECO-BACK-09 | API-EFF-002 | 7.1 |
| `NR-BACK-005` | Sober logging, bounded retention | ECO-BACK-08, ECO-HEB-12 | — | 7.x, 8.x |
| `NR-BACK-006` | Release resources on every path | ECO-BACK-07 | CODE-EFF-005 | 9.1 |
| `NR-BACK-007` | Prefer events over polling | — | NET-EFF-002 | 7.x |
| `NR-BACK-008` | Compute derived data once | ECO-BACK-13 | — | 7.x |
| `NR-BACK-009` | Connection pools sized and shared | ECO-BACK-02 | DB-EFF-006 | 7.x |
| `NR-BACK-010` | Incremental, restartable pipelines | ECO-BACK-12 | OPS-EFF-003 | 3.1, 7.x |
| `NR-CONTENT-001` | Optimise images | ECO-CONT-01 | WEB-EFF-001 | 5.x |
| `NR-CONTENT-002` | Video sized to the need | ECO-CONT-02 | WEB-EFF-004 | 5.x |
| `NR-CONTENT-003` | Icons as SVG | ECO-CONT-03 | — | 5.x |
| `NR-CONTENT-004` | Limit downloaded fonts | ECO-UX-05 | — | 4.5 |
| `NR-CONTENT-005` | No unused or orphaned content | ECO-STRAT-07 | SERVICE-EFF-005 | 2.7 |
| `NR-CONTENT-006` | Open and lightweight document formats | ECO-STRAT-03 | — | 5.5 |
| `NR-CONTENT-007` | Data minimisation at collection | ECO-HEB-12 | — | 5.5, 8.x |
| `NR-DATA-001` | Explicit columns, never SELECT * | ECO-BACK-01 | DB-EFF-001 | 7.x |
| `NR-DATA-002` | No N+1 query | ECO-BACK-01 | DB-EFF-002 | 7.x |
| `NR-DATA-003` | Indexes aligned with access paths | ECO-BACK-01 | DB-EFF-003 | 7.x |
| `NR-DATA-004` | Pagination by cursor on large collections | ECO-BACK-09 | DB-EFF-004 | 7.1 |
| `NR-DATA-005` | Retention and deletion from day one | ECO-HEB-12 | DB-EFF-005 | 8.x |
| `NR-DATA-006` | Right store for the data shape | — | ARCH-DATA-001, ARCH-NOSQL-001 | 3.x |
| `NR-DATA-007` | Parameterised queries, reused plans | ECO-BACK-10 | — | 7.1 |
| `NR-DATA-008` | Compact and archive at rest | ECO-HEB-11 | — | 8.x |
| `NR-FRONT-001` | No heavy library for a minor need | ECO-FRONT-01 | — | 6.x |
| `NR-FRONT-002` | Load on demand | ECO-FRONT-02 | — | 6.x |
| `NR-FRONT-003` | No blocking or synchronous requests | ECO-FRONT-07, ECO-FRONT-13 | — | 6.x |
| `NR-FRONT-004` | DOM neither too large nor too deep | ECO-FRONT-08 | — | 6.x |
| `NR-FRONT-005` | No dead code and no dead CSS | ECO-FRONT-05, ECO-FRONT-12 | — | 6.x |
| `NR-FRONT-006` | CSS without duplication or !important escalation | ECO-FRONT-09, ECO-FRONT-10, ECO-FRONT-11 | — | 6.x |
| `NR-FRONT-007` | Clean up listeners, timers and observers | ECO-FRONT-06 area | LANG-JS-* | 6.x |
| `NR-FRONT-008` | Debounce and throttle user-driven compute | ECO-ALGO area | WEB-EFF-003 | 6.x, 9.1 |
| `NR-FRONT-009` | Defer what is deferrable, keep what the user waits for | ECO-FRONT-13, ECO-FRONT-14 | — | 6.x |
| `NR-FRONT-010` | Minify and compress transport | ECO-FRONT-03, ECO-HEB-02 | — | 6.x, 8.x |
| `NR-INFRA-001` | HTTPS, modern TLS, secure transport | ECO-HEB-04, ECO-HEB-05, ECO-HEB-06 | — | 8.x |
| `NR-INFRA-002` | Containers sized to what runs | ECO-HEB-07 | INFRA-EFF-004 | 8.x |
| `NR-INFRA-003` | Region and locality decisions on evidence | ECO-HEB-09 | INFRA-EFF-003 | 8.x |
| `NR-INFRA-004` | Deferrable work in low-impact windows | ECO-HEB-08 | OPS-EFF-001 | 8.x |
| `NR-INFRA-005` | Clean environments and orphaned resources | ECO-ARCH-04 | OPS-EFF-001 | 3.7 |
| `NR-INFRA-006` | Extend hardware life | ECO-SPEC-02 | HW-EFF-001, HW-EFF-002 | 2.1, 2.2 |
| `NR-INFRA-007` | CI that spends what it must | ECO-ARCH-04, ECO-ARCH-06 | — | 3.7 |
| `NR-INFRA-008` | Scalability without waste | ECO-ARCH-02 | ARCH-SERVERLESS-001 | 3.2, 8.x |
| `NR-MEASURE-001` | Baseline and functional unit before comparing | ECO-STRAT-08 | MEASURE-EFF-001 | 1.4, 1.5 |
| `NR-MEASURE-002` | A tool score is an indicator, not compliance | — | MEASURE-EFF-002 | — |
| `NR-MEASURE-003` | Distinguish technical gain from environmental impact | ECO-ALGO-09 | MEASURE-EFF-003 | 9.x |
| `NR-MEASURE-004` | Unknown is not zero | — | — | — |
| `NR-MEASURE-005` | Monitor what grows | ECO-HEB-10 | OPS-EFF-002 | 8.x |
| `NR-SERVICE-001` | Confirm the need before building | ECO-SPEC-05 | SERVICE-EFF-001 | 2.6 |
| `NR-SERVICE-002` | Apply the 3U before investing | — | three-u.md | 1.1, 2.9 |
| `NR-SERVICE-003` | Keep features to what is needed | ECO-SPEC-05 | — | 1.1, 2.9 |
| `NR-SERVICE-004` | Support older devices and slow networks | ECO-SPEC-02, ECO-SPEC-03 | SERVICE-EFF-002 | 2.1, 2.2, 2.3, 2.4 |
| `NR-SERVICE-005` | User control over engagement mechanics | ECO-UX-01, ECO-UX-02 | SERVICE-EFF-003 | 4.1, 4.2 |
| `NR-SERVICE-006` | Environmental criteria in user stories | ECO-SPEC-01 | — | 2.6 |
| `NR-SERVICE-007` | Plan retirement from the start | ECO-STRAT-07 | SERVICE-EFF-005 | 2.7 |
| `NR-SERVICE-008` | Assess third-party services before integrating | ECO-SPEC-04, ECO-UX-04 | — | 2.10 |
| `NR-STRAT-001` | Measure before optimising | ECO-STRAT-01 | MEASURE-EFF-001 | 1.4, 1.5 |
| `NR-STRAT-002` | Reduce targets, not just technical metrics | ECO-STRAT-01 | — | 1.4, 1.5 |
| `NR-STRAT-003` | Hold regular ecodesign reviews | ECO-STRAT-01 | — | 1.8, 1.9 |
| `NR-STRAT-004` | Standard, open, interoperable technologies | ECO-STRAT-03 | — | 1.x |
| `NR-STRAT-005` | State the functional unit and the boundary | ECO-STRAT-08 | — | 1.4, 1.5 |
| `NR-STRAT-006` | Check the rebound before claiming a win | ECO-STRAT-09 | — | 1.4, 1.5 |
| `NR-UX-001` | Accessibility is the floor | ECO-UX-08 | — | 4.8 |
| `NR-UX-002` | The lightest medium that carries the information | ECO-UX-06 | — | 4.6, 4.7 |
| `NR-UX-003` | Native components rather than reimplemented ones | ECO-UX-03 | — | 4.5 |
| `NR-UX-004` | Honour reduced-motion preference | ECO-UX-07 | — | 4.x |
| `NR-UX-005` | Short and direct journeys | ECO-UX-06 | — | 4.3 |
| `NR-UX-006` | Errors that save work | — | — | 4.4 |
| `NR-UX-007` | Third-party UI on demand | ECO-UX-04 | WEB-EFF-002 | 4.4 |
| `NR-LANG-HTML-001` | Semantic HTML | ECO-UX-03 | LANG-HTML-001 | — |
| `NR-LANG-HTML-002` | Media with explicit dimensions and lazy loading | ECO-CONT-01 | LANG-HTML-002 | — |
| `NR-LANG-HTML-003` | Forms: labels, autocomplete, validation | — | — | — |
| `NR-LANG-CSS-001` | Modern layout over hacks | ECO-FRONT-12 | LANG-CSS-001 | — |
| `NR-LANG-CSS-002` | System fonts or subset web fonts | ECO-UX-05 | — | — |
| `NR-LANG-JAVA-001` | Stream over imperative loops only when it reads better | java.json | LANG-JAVA-001 | — |
| `NR-LANG-JAVA-002` | Try-with-resources everywhere | java.json | DB-EFF-006 | — |
| `NR-LANG-JAVA-003` | Lazy or batched JPA access | java.json | DB-EFF-002 | — |
| `NR-LANG-JAVA-004` | Bound the JVM to the container | java.json | INFRA-EFF-004 | — |
| `NR-LANG-JAVA-005` | No reflection on hot paths | java.json | LANG-JAVA-003 | — |
| `NR-LANG-JS-001` | Native APIs before libraries | javascript.json | LANG-JS-001 | — |
| `NR-LANG-JS-002` | No sync I/O on the request path | javascript.json | CODE-EFF-008 | — |
| `NR-LANG-JS-003` | No unbounded Promise.all over collections | javascript.json | CODE-EFF-006 | — |
| `NR-LANG-JS-004` | Await in loops only with cause | javascript.json | API-EFF-001 | — |
| `NR-LANG-JS-005` | Tree-shake and measure the bundle | javascript.json | — | — |
| `NR-LANG-JS-006` | JSON without silent serialization traps | javascript.json | CODE-EFF-010 | — |
| `NR-LANG-PY-001` | Iterators and chunked I/O for large data | python.json | LANG-PYTHON-001 | — |
| `NR-LANG-PY-002` | Vectorise only after profiling | — | LANG-PYTHON-002, LANG-PYTHON-005 | — |
| `NR-LANG-PY-003` | No N+1 with the ORM | python.json | DB-EFF-002 | — |
| `NR-LANG-PY-004` | Bound multiprocessing and close resources | python.json | LANG-PYTHON-003 | — |
| `NR-LANG-PY-005` | Don't ship a framework for a script | python.json | — | — |
| `NR-LANG-PY-006` | Async without blocking | python.json | CODE-EFF-008 | — |
| `NR-LANG-SH-001` | One tool call instead of a pipeline of greps | shell.json | LANG-SHELL-001 | — |
| `NR-LANG-SH-002` | Set -euo pipefail in scripts, quoted variables | shell.json | LANG-SHELL-002 | — |
| `NR-LANG-SH-003` | Trap cleanup, mktemp files always | shell.json | LANG-SHELL-003 | — |
| `NR-LANG-SH-004` | Bounded loops, no infinite retries | shell.json | LANG-SHELL-004 | — |
| `NR-LANG-SQL-001` | Explicit column lists | sql.json | DB-EFF-001, LANG-SQL-001 | — |
| `NR-LANG-SQL-002` | JOINs over correlated subqueries on growing data | sql.json | LANG-SQL-002 | — |
| `NR-LANG-SQL-003` | Batch inserts, not row-by-row loops | sql.json | DB-EFF-004 | — |
| `NR-LANG-SQL-004` | No function on the indexed column in predicates | sql.json | — | — |
| `NR-LANG-SQL-005` | Transactions short and bounded | sql.json | CODE-EFF-002 | — |
| `NR-USAGE-001` | Context minimalism | USAGE-CTX-01 | — | — |
| `NR-USAGE-002` | Ask the one question that changes the work | USAGE-BRIEF-03 | — | — |
| `NR-USAGE-003` | Let the model fetch on demand | USAGE-CTX-01 | — | — |
| `NR-USAGE-004` | Compact instead of dragging history | — | usage-practices.md | — |
| `NR-USAGE-005` | Right model for the task | USAGE-COMPUTE-* | usage-practices.md | — |
| `NR-USAGE-006` | Deterministic tools before model reasoning | USAGE-VERIF-* | usage-practices.md | — |
| `NR-USAGE-007` | One turn, one goal | USAGE-BRIEF-* | — | — |
| `NR-USAGE-008` | No blind retries | — | usage-practices.md | — |
| `NR-USAGE-009` | Reuse validated artifacts | — | usage-practices.md | — |
| `NR-USAGE-010` | Subagents keep the main context clean | — | usage-practices.md | — |
| `NR-USAGE-011` | Images only when they carry the task | USAGE-CTX-* | usage-practices.md | — |
| `NR-USAGE-012` | Close what you opened | USAGE-COMPUTE-* | — | — |
| `NR-USAGE-013` | Batch related work in the queue | — | usage-practices.md | — |
| `NR-USAGE-014` | Verify before you regenerate | USAGE-VERIF-* | — | — |
| `NR-USAGE-015` | Automation proportional to need | hooks discipline | usage-practices.md | — |
| `NR-USAGE-016` | Directions, not ratios | ECO-ALGO-09, SKILL.md token-energy discipline | — | 9.x |

## Règles sources non reprises en v1

Ces règles ne sont pas portées telles quelles : elles sont couvertes par une
règle Green Vibe existante (voir la matrice), jugées non applicables au
périmètre Vibe, ou laissées pour une version ultérieure.

### Green Claude

- `ECO-ALGO-01`
- `ECO-ALGO-03`
- `ECO-ALGO-10`
- `ECO-ALGO-11`
- `ECO-ALGO-12`
- `ECO-ALGO-14`
- `ECO-ALGO-18`
- `ECO-ALGO-20`
- `ECO-ALGO-21`
- `ECO-ALGO-23`
- `ECO-ALGO-26`
- `ECO-ARCH-12`
- `ECO-ASTRO-01`
- `ECO-ASTRO-02`
- `ECO-BACK-11`
- `ECO-C-01`
- `ECO-C-02`
- `ECO-C-03`
- `ECO-C-04`
- `ECO-C-05`
- `ECO-C-06`
- `ECO-CPP-01`
- `ECO-CPP-02`
- `ECO-CPP-03`
- `ECO-CPP-04`
- `ECO-CPP-05`
- `ECO-CPP-06`
- `ECO-CS-01`
- `ECO-CS-02`
- `ECO-CS-03`
- `ECO-CS-04`
- `ECO-CS-05`
- `ECO-CS-06`
- `ECO-CS-07`
- `ECO-CS-08`
- `ECO-FRONT-06`
- `ECO-GO-01`
- `ECO-GO-02`
- `ECO-GO-03`
- `ECO-GO-04`
- `ECO-GO-05`
- `ECO-GO-06`
- `ECO-HEB-01`
- `ECO-HOST-01`
- `ECO-HOST-02`
- `ECO-HOST-03`
- `ECO-HOST-04`
- `ECO-JAVA-01`
- `ECO-JAVA-02`
- `ECO-JAVA-03`
- `ECO-JAVA-04`
- `ECO-JAVA-05`
- `ECO-JAVA-06`
- `ECO-JAVA-07`
- `ECO-JAVA-08`
- `ECO-JS-01`
- `ECO-JS-02`
- `ECO-JS-03`
- `ECO-JS-04`
- `ECO-JS-05`
- `ECO-JS-06`
- `ECO-JS-07`
- `ECO-JS-08`
- `ECO-JS-09`
- `ECO-JULIA-01`
- `ECO-JULIA-02`
- `ECO-JULIA-03`
- `ECO-KT-01`
- `ECO-KT-02`
- `ECO-KT-03`
- `ECO-KT-04`
- `ECO-KT-05`
- `ECO-NG-01`
- `ECO-NG-02`
- `ECO-NG-03`
- `ECO-NIM-01`
- `ECO-NIM-02`
- `ECO-NIM-03`
- `ECO-PHP-01`
- `ECO-PHP-02`
- `ECO-PHP-03`
- `ECO-PHP-04`
- `ECO-PHP-05`
- `ECO-PHP-06`
- `ECO-PHP-07`
- `ECO-PY-01`
- `ECO-PY-02`
- `ECO-PY-03`
- `ECO-PY-04`
- `ECO-PY-05`
- `ECO-PY-06`
- `ECO-PY-07`
- `ECO-PY-08`
- `ECO-PY-09`
- `ECO-PY-10`
- `ECO-PY-11`
- `ECO-RB-01`
- `ECO-RB-02`
- `ECO-RB-03`
- `ECO-RB-04`
- `ECO-RB-05`
- `ECO-RB-06`
- `ECO-RB-07`
- `ECO-REACT-01`
- `ECO-REACT-02`
- `ECO-REACT-03`
- `ECO-RS-01`
- `ECO-RS-02`
- `ECO-RS-03`
- `ECO-RS-04`
- `ECO-RS-05`
- `ECO-RS-06`
- `ECO-RS-07`
- `ECO-SCALA-01`
- `ECO-SCALA-02`
- `ECO-SCALA-03`
- `ECO-SH-01`
- `ECO-SH-02`
- `ECO-SH-03`
- `ECO-SH-04`
- `ECO-SH-05`
- `ECO-SH-06`
- `ECO-SOLID-01`
- `ECO-SOLID-02`
- `ECO-SQL-01`
- `ECO-SQL-02`
- `ECO-SQL-03`
- `ECO-SQL-04`
- `ECO-SQL-05`
- `ECO-SQL-06`
- `ECO-SQL-07`
- `ECO-SQL-08`
- `ECO-SQL-09`
- `ECO-SQL-10`
- `ECO-SQL-11`
- `ECO-STRAT-02`
- `ECO-STRAT-04`
- `ECO-STRAT-05`
- `ECO-STRAT-06`
- `ECO-SVELTE-01`
- `ECO-SVELTE-02`
- `ECO-SW-01`
- `ECO-SW-02`
- `ECO-SW-03`
- `ECO-SW-04`
- `ECO-SW-05`
- `ECO-VUE-01`
- `ECO-VUE-02`
- `ECO-ZIG-01`
- `ECO-ZIG-02`
- `USAGE-BRIEF-01`
- `USAGE-BRIEF-02`
- `USAGE-CPU-01`
- `USAGE-CPU-02`
- `USAGE-CPU-03`
- `USAGE-CTX-02`
- `USAGE-CTX-03`
- `USAGE-CTX-04`
- `USAGE-CTX-05`
- `USAGE-CTX-06`
- `USAGE-MEM-01`
- `USAGE-MEM-02`
- `USAGE-MEM-03`
- `USAGE-VERIF-01`

### Green Codex

- `ARCH-DATA-002`
- `ARCH-DIST-002`
- `ARCH-DIST-003`
- `ARCH-EDGE-001`
- `ARCH-EDGE-002`
- `ARCH-EMBEDDED-001`
- `ARCH-IOT-001`
- `ARCH-IOT-002`
- `ARCH-MOBILE-001`
- `ARCH-MOBILE-002`
- `ARCH-MOBILE-003`
- `ARCH-NOSQL-002`
- `ARCH-SERVERLESS-002`
- `CODE-EFF-011`
- `CODE-EFF-012`
- `CODE-EFF-013`
- `DB-EFF-007`
- `DB-EFF-008`
- `DB-EFF-009`
- `DB-EFF-010`
- `HW-EFF-003`
- `INFRA-EFF-002`
- `INFRA-EFF-005`
- `LANG-ANGULAR-001`
- `LANG-ANGULAR-002`
- `LANG-ANGULAR-003`
- `LANG-ASTRO-001`
- `LANG-ASTRO-002`
- `LANG-ASTRO-003`
- `LANG-C-001`
- `LANG-C-002`
- `LANG-C-003`
- `LANG-CPP-001`
- `LANG-CPP-002`
- `LANG-CPP-003`
- `LANG-CSS-002`
- `LANG-CSS-003`
- `LANG-GO-001`
- `LANG-GO-002`
- `LANG-GO-003`
- `LANG-GO-004`
- `LANG-HTML-003`
- `LANG-JAVA-002`
- `LANG-JAVA-004`
- `LANG-JAVA-005`
- `LANG-JS-002`
- `LANG-JS-003`
- `LANG-JS-004`
- `LANG-JS-005`
- `LANG-JULIA-001`
- `LANG-JULIA-002`
- `LANG-KOTLIN-001`
- `LANG-KOTLIN-002`
- `LANG-NIM-001`
- `LANG-NIM-002`
- `LANG-PHP-001`
- `LANG-PHP-002`
- `LANG-PLSQL-001`
- `LANG-PLSQL-002`
- `LANG-PLSQL-003`
- `LANG-PREACT-001`
- `LANG-PREACT-002`
- `LANG-PREACT-003`
- `LANG-PYTHON-004`
- `LANG-REACT-001`
- `LANG-REACT-002`
- `LANG-REACT-003`
- `LANG-RUBY-001`
- `LANG-RUBY-002`
- `LANG-RUST-001`
- `LANG-RUST-002`
- `LANG-RUST-003`
- `LANG-SCALA-001`
- `LANG-SCALA-002`
- `LANG-SHELL-005`
- `LANG-SHELL-006`
- `LANG-SOLID-001`
- `LANG-SOLID-002`
- `LANG-SOLID-003`
- `LANG-SQL-003`
- `LANG-SVELTE-001`
- `LANG-SVELTE-002`
- `LANG-SVELTE-003`
- `LANG-VUE-001`
- `LANG-VUE-002`
- `LANG-VUE-003`
- `LANG-ZIG-001`
- `LANG-ZIG-002`
- `MEASURE-EFF-004`
- `NET-EFF-001`
- `NET-EFF-003`
- `NET-EFF-004`
- `SERVICE-EFF-004`
- `SERVICE-EFF-006`
