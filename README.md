# Green Vibe

**English** · [Français](README.fr.md)

Native Sustainable IT (Numérique Responsable) for [Mistral Vibe](https://docs.mistral.ai/vibe/code/overview):
an Agent Plugins 1.0 plugin that brings Sustainable IT into the development
cycle: understand, apply, verify, and pass it on.

Sustainable IT covers four fields:

- **Green IT**: leaner software (CPU, memory, network, storage, and the
  agent's own context)
- **IT for Green**: digital services that support the ecological transition
- **IT for Social**: accessible, inclusive digital services that bring people
  together
- **Social for IT**: human, ethical practices in the way software gets built

With Green Vibe, the agent writes code that's leaner, more accessible, more
reliable, and more ethical.

By the Institut du Numérique Responsable (INR).

## Why a Sustainable IT by design skill

A service creates lasting value when it stays useful, accessible, lean,
reliable, and maintainable over its whole life. You set those qualities while
you write the code; an audit six months later can only record them.

- **You fix a line instead of a whole cycle.** While you write, an unbounded
  query or an unlabelled button takes one line to fix. In production, the
  same fix needs an audit, a ticket, a review, and a deployment.
- **The agent repeats its patterns in every file it touches.** When it
  applies Sustainable IT rules, it spreads good practice at the same scale as
  the debt it would otherwise create.
- **You decide resource use at design time.** Architecture, the data model,
  and the choice of AI model set most of the resources a service consumes;
  late optimisation only moves the margin.
- **You write every screen for everyone.** A person who can't use the service
  gets no value from it. Green Vibe applies accessibility rules to every
  interface change.
- **You decide on facts.** Green Vibe marks a rule `verified` only when its
  check ran, and refuses unmeasured environmental gains. Your claims stay
  defensible.
- **Your team learns from every change.** The report explains why each rule
  applies, and the team keeps the habit without the agent.
- **Your users keep their devices longer.** Light code that works on older
  devices and slow networks delays their replacement. Manufacturing devices
  weighs the most in the footprint of digital services.

## What Green Vibe does

Green Vibe supports the agent at each step of a code change.

- **286 Sustainable IT rules** written as LLM-native sheets
  (`what/why/how/verify/limits`, provenance, and RGESN reference per rule):
  13 cross-cutting families (128 rules, including accessibility and
  inclusion), 25 language and framework catalogs (129 rules), and 29
  practices for using Vibe itself responsibly.
- **Context-driven selection**: the pipeline loads only the relevant rules
  (`select`), never the whole catalog.
- **Executable verification**: a deterministic static audit (164 rules with
  detection, regex plus special detectors), masking of strings and comments
  to avoid false positives, and normalised statuses (`verified` only when the
  check ran).
- **Mandatory teaching report**: after each significant change, a report
  that cites the rules applied and verified during that change.
- **Post-edit hook** (fail-open): the audit runs even if the model forgets,
  and it audits only what the write added.

## Quickstart

You need Mistral Vibe and `python3 >= 3.10` (standard library only).

Install the plugin, then reload plugins in Vibe:

```bash
# install (user scope by default)
./scripts/install.sh
# in Vibe: /reload-plugins, then /plugins to check
```

Run the validators directly:

```bash
# the validators (python3 standard library, no dependencies)
python3 validators/green-vibe stats
python3 validators/green-vibe select src/
python3 validators/green-vibe audit src/ > /tmp/audit.json
python3 validators/green-vibe report --audit /tmp/audit.json --intervention "..."
```

In Vibe, `/green-vibe` loads the skill. The model also loads it on its own for
eco-design, accessibility, sobriety, or code review tasks. For a full scenario
you can replay, see [evals/README.md](evals/README.md).

Run the test suite:

```bash
# tests (standard library, no dependencies)
python3 -m unittest discover -s tests -t . -p "test_*.py"
```

## Documentation

Each document covers one part of the plugin. French translations live in
[docs/fr/](docs/fr/).

| Document | Content |
|---|---|
| [docs/installation.md](docs/installation.md) | Installation, configuration, updates |
| [docs/usage.md](docs/usage.md) | Pipeline, report modes, examples |
| [docs/architecture.md](docs/architecture.md) | Architecture, shared core, product integration |
| [docs/rules.md](docs/rules.md) | Rule catalog, governance, versioning |
| [docs/validators.md](docs/validators.md) | Audit engine, statuses, traceability |
| [docs/maintenance.md](docs/maintenance.md) | Maintenance, contribution, tests |
| [evals/README.md](evals/README.md) | Demo scenario and test coverage |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## Explicit limits

Green Vibe helps you decide; it replaces neither an audit nor a measurement.

- Green Vibe **certifies nothing**: it makes no RGESN, RGAA, or GR491
  compliance claim, and tool scores are indicators, not evidence.
- A technical gain (bytes, CPU, tokens) stays a **technical** gain: every
  environmental claim needs its own measurement.
- The static audit produces **candidates**; only the context settles them.

## License

Code: Apache-2.0. Rules and documentation: CC BY 4.0. See [LICENSE](LICENSE),
[NOTICE](NOTICE), and `LICENSES/`.
