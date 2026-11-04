# Installation and configuration

**English** · [Français](fr/installation.md)

This page explains how to install, configure, update, and remove Green Vibe.

## Prerequisites

To install Green Vibe, you need:

- Mistral Vibe (the plugin uses the Agent Plugins 1.0 format, which Vibe loads as is)
- `python3 >= 3.10` (standard library only, nothing to install); the
  installer checks the version
- `rsync` (the installer syncs the plugin copy and prunes stale files); the
  installer checks it is available

The installer copies only what the plugin needs: development artifacts
(`.git`, `tests/`, `evals/`, caches) are excluded from the installed copy.

## Installation

Two installation scopes are available.

### User scope (recommended)

Run the installer with no argument:

```bash
./scripts/install.sh            # copies to ~/.vibe/plugins/green-vibe
```

### Project scope (trusted folder required)

Pass `project` to the installer:

```bash
./scripts/install.sh project    # copies to ./.vibe/plugins/green-vibe
```

Then, in Vibe, run `/reload-plugins` (or restart), and `/plugins` to check
that `green-vibe` appears with its components (skill, hooks, and knowledge).

You can then use the skill in two ways:

- type `/green-vibe` (user-invocable)
- let the model load it when a task involves eco-design, accessibility,
  sobriety, or code review (see the `description` in SKILL.md)

### Skill-only installation (no plugin)

Copy `skills/green-vibe/` to `~/.vibe/skills/` or `.vibe/skills/`, and the
rest of the repository (`rules/`, `references/`, `validators/`) next to it.
SKILL.md calls the validators through the `GV` variable, which points to the
Green Vibe root. Set it in the session:

```bash
export GV="$HOME/.vibe/skills/green-vibe-root"   # example: wherever you copied the repository
python3 "$GV/validators/green-vibe" stats
```

The plugin stays the canonical route: only the plugin brings hooks and
knowledge.

## Configuration

The plugin works without configuration. The following options are available.

| Option | Effect |
|---|---|
| Turn off the audit hook | Remove `ai.mistral.vibe/hooks.toml` from the installed copy (the hook is fail-open and never blocks) |
| Reduce noise | Add a `.green-vibe/decisions.md` file at the root of the audited project (`NR-XXX  file  ACCEPTED/TODO  reason`). The model reads it before relaying a finding the team already settled; the CLI audit doesn't read it and keeps reporting the finding |
| Force families | `select --family ai --family infra` for a task the context detection doesn't cover |
| Pause auto-update | `touch ~/.vibe/.green-vibe/no-autoupdate` (the check hook exits immediately; the audit hook is unaffected) |

## Check the installation

Run the `stats` command from the installed copy:

```bash
python3 ~/.vibe/plugins/green-vibe/validators/green-vibe stats
# should print 312 rules and the families
```

In Vibe, `/plugins` should list `green-vibe`, and `/green-vibe` should load
the skill.

## Update

Run the installer's `update` mode: it pulls the source repository
(fast-forward only) and syncs the installed copy:

```bash
git -C <green-vibe repository> pull   # optional: update mode pulls by itself
./scripts/install.sh update            # syncs the user-scope copy
# then, in Vibe: /reload-plugins
```

`update` refuses nothing silently: it reports the version change
(`0.2.2 -> 0.2.3`) or syncs uncommitted local changes as-is, with a warning.

Running sessions keep the plugin snapshot from when they started:
`/reload-plugins` syncs them.

## Automatic updates

A user-scope install updates itself, no action needed:

- The installer records the source path in `~/.vibe/.green-vibe/`.
- After each turn, a fail-open hook checks the source repository at most
  once a day (a stamp file throttles it; every other turn costs one `stat`).
- When the upstream moved, the hook pulls (fast-forward only, only when the
  source tree is clean: it never touches uncommitted work) and re-syncs the
  installed copy, then asks for `/reload-plugins` in the session.
- Sessions in progress keep their pinned snapshot until `/reload-plugins`.

| Control | Command |
|---|---|
| Pause auto-update | `touch ~/.vibe/.green-vibe/no-autoupdate` |
| Resume | `rm ~/.vibe/.green-vibe/no-autoupdate` |
| Update now | `./scripts/install.sh update` |

Auto-update is a user-scope feature. Project-scope copies belong to a
project's workflow and never pull on their own.

## Troubleshooting

The following table lists common symptoms and how to fix them.

| Symptom | Likely cause | Action |
|---|---|---|
| `install.sh` refuses to continue | `python3` missing or older than 3.10, or `rsync` not in PATH | Install Python 3.10+ and rsync, check `python3 --version` and `rsync --version` |
| `green-vibe` missing from `/plugins` | Session started before the installation | Run `/reload-plugins` or restart Vibe |
| Project scope ignored | Folder not trusted in Vibe | Trust the folder, then run `/reload-plugins` |
| No hook output after a write | Normal when there's nothing to report; otherwise a swallowed error (fail-open) | Run the audit on the file by hand: `python3 <root>/validators/green-vibe audit <file>` |
| `select` keeps no rule | No known language in the given paths | Force a family: `select <paths> --family <family>` |

## Uninstall

Use the installer's `uninstall` mode, then reload plugins:

```bash
./scripts/install.sh uninstall             # user scope
./scripts/install.sh uninstall project    # project scope
# then /reload-plugins
```
