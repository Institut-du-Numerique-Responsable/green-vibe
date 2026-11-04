#!/bin/bash
# Green Vibe installation for Mistral Vibe.
#
# Copies the plugin into ~/.vibe/plugins (user scope, default) or
# .vibe/plugins (project scope, requires a trusted folder), then verifies the
# validators run. Re-running the script updates the copy in place: rsync
# --delete prunes files removed upstream, and development artifacts
# (.git, tests, evals, caches) are excluded from the installed copy.
#
# Modes:
#   install.sh [user|project]        install (or reinstall over) a scope
#   install.sh update                sync the user-scope copy from this
#                                    repository (git pull if it is a clone)
#   install.sh uninstall [project]   remove a scope's installed copy
#
# A user-scope install records the source path in ~/.vibe/.green-vibe/ so
# `update` and the auto-update hook can re-sync from it. Project-scope
# installs do not auto-update: they belong to a project's workflow.

set -euo pipefail

# Reproducibility: the validators use PEP 604 unions and need python3 >= 3.10.
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
  echo "green-vibe: python3 >= 3.10 required (found: $(python3 --version 2>&1))" >&2
  exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
  echo "green-vibe: rsync required (not found in PATH)" >&2
  exit 1
fi

PLUGIN_NAME="green-vibe"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="${HOME}/.vibe/.green-vibe"

if [ ! -f "$SCRIPT_DIR/plugin.json" ]; then
  echo "green-vibe: plugin.json not found next to $SCRIPT_DIR" >&2
  exit 1
fi

version_of() {  # $1 = path to plugin.json
  python3 -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$1"
}

VERSION="$(version_of "$SCRIPT_DIR/plugin.json")"

is_git() {  # $1 = directory
  git -C "$1" rev-parse --is-inside-work-tree >/dev/null 2>&1
}

is_clean() {  # $1 = a git directory with nothing uncommitted
  [ -z "$(git -C "$1" status --porcelain 2>/dev/null)" ]
}

project_dest() {
  # Resolve the caller's project root, not the directory they ran the script
  # from; fall back to $PWD outside a git repository.
  git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || echo "$PWD"
}

write_state() {  # record the source so update/auto-update can re-sync
  mkdir -p "$STATE_DIR"
  printf '%s\n' "$SCRIPT_DIR" > "$STATE_DIR/source"
  if is_git "$SCRIPT_DIR"; then
    git -C "$SCRIPT_DIR" rev-parse HEAD > "$STATE_DIR/commit"
  else
    rm -f "$STATE_DIR/commit"
  fi
  date +%s > "$STATE_DIR/last-check"
}

EXCLUDES=(
  --exclude='.git'
  --exclude='.gitignore'
  --exclude='.DS_Store'
  --exclude='.remember'
  --exclude='__pycache__'
  --exclude='*.pyc'
  --exclude='.pytest_cache'
  --exclude='tests'
  --exclude='evals'
)

sync_plugin() {  # $1 = destination directory
  mkdir -p "$(dirname "$1")"
  rsync -a --delete --delete-excluded "${EXCLUDES[@]}" "$SCRIPT_DIR"/ "$1"/
}

SCOPE="${1:-user}"
case "$SCOPE" in
  user)   DEST="$HOME/.vibe/plugins/$PLUGIN_NAME" ;;
  project) DEST="$(project_dest)/.vibe/plugins/$PLUGIN_NAME" ;;
  update)
    DEST="$HOME/.vibe/plugins/$PLUGIN_NAME"
    OLD_VERSION="not installed"
    [ -f "$DEST/plugin.json" ] && OLD_VERSION="$(version_of "$DEST/plugin.json")"
    if is_git "$SCRIPT_DIR"; then
      if is_clean "$SCRIPT_DIR"; then
        git -C "$SCRIPT_DIR" pull --ff-only --quiet 2>/dev/null \
          || echo "green-vibe: pull skipped (cannot fast-forward)" >&2
      else
        echo "green-vibe: uncommitted changes in $SCRIPT_DIR, syncing them as-is" >&2
      fi
    fi
    sync_plugin "$DEST"
    write_state
    NEW_VERSION="$(version_of "$SCRIPT_DIR/plugin.json")"
    echo "updated: $DEST ($OLD_VERSION -> $NEW_VERSION)"
    echo "In Vibe: /reload-plugins (or restart) to refresh the session."
    exit 0
    ;;
  uninstall)
    # Optional second arg: "project" to remove the project-scope copy.
    if [ "${2:-user}" = "project" ]; then
      DEST="$(project_dest)/.vibe/plugins/$PLUGIN_NAME"
    else
      DEST="$HOME/.vibe/plugins/$PLUGIN_NAME"
    fi
    if [ -d "$DEST" ]; then
      rm -rf "$DEST"
      echo "removed: $DEST"
      echo "In Vibe: /reload-plugins (or restart) to refresh the session."
    else
      echo "not installed: $DEST"
    fi
    exit 0
    ;;
  *)
    echo "usage: install.sh [user|project|update|uninstall [project]]" >&2
    exit 1
    ;;
esac

sync_plugin "$DEST"

if [ "$SCOPE" = "user" ]; then
  write_state
fi

echo "installed: $DEST (v$VERSION)"
echo "verifying validators..."
# -B: verify without writing bytecode into the installed copy.
TOTAL="$(python3 -B "$DEST/validators/$PLUGIN_NAME" stats \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["total"])')"
echo "validators OK ($TOTAL rules)"

if [ "$SCOPE" = "user" ] && [ -f "$STATE_DIR/no-autoupdate" ]; then
  AUTOUPDATE_NOTE="auto-update: off (~/.vibe/.green-vibe/no-autoupdate present)"
elif [ "$SCOPE" = "user" ]; then
  AUTOUPDATE_NOTE="auto-update: on (daily check from $(cat "$STATE_DIR/source"))"
else
  AUTOUPDATE_NOTE="auto-update: n/a (project scope)"
fi

cat <<EOF

Done. In Vibe:
  1. /reload-plugins          (or restart Vibe)
  2. verify in /plugins that "$PLUGIN_NAME" is listed
  3. the skill loads with: /green-vibe   (user-invocable)
     or automatically when coding NR-relevant work

$AUTOUPDATE_NOTE
To pause auto-update:    touch ~/.vibe/.green-vibe/no-autoupdate
To update manually:      ./scripts/install.sh update
To remove the plugin:    ./scripts/install.sh uninstall

The post-edit hook is active automatically (post_tool, fail-open).
To disable it: remove ai.mistral.vibe/hooks.toml from the installed copy.
EOF
