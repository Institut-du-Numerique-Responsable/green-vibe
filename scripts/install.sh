#!/bin/bash
# Green Vibe installation for Mistral Vibe.
#
# Copies the plugin into ~/.vibe/plugins (user scope, default) or
# .vibe/plugins (project scope, requires a trusted folder), then verifies the
# validators run. Re-running the script updates the copy in place.

set -euo pipefail

# Reproducibility: the validators use PEP 604 unions and need python3 >= 3.10.
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
  echo "green-vibe: python3 >= 3.10 required (found: $(python3 --version 2>&1))" >&2
  exit 1
fi

PLUGIN_NAME="green-vibe"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -f "$SCRIPT_DIR/plugin.json" ]; then
  echo "green-vibe: plugin.json not found next to $SCRIPT_DIR" >&2
  exit 1
fi

SCOPE="${1:-user}"
case "$SCOPE" in
  user) DEST="$HOME/.vibe/plugins/$PLUGIN_NAME" ;;
  project) DEST="$PWD/.vibe/plugins/$PLUGIN_NAME" ;;
  *) echo "usage: install.sh [user|project]" >&2; exit 1 ;;
esac

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SCRIPT_DIR" "$DEST"
rm -rf "$DEST/.git" "$DEST/tests" 2>/dev/null || true

echo "installed: $DEST"
echo "verifying validators..."
python3 "$DEST/validators/green-vibe" stats >/dev/null
echo "validators OK"

cat <<EOF

Done. In Vibe:
  1. /reload-plugins          (or restart Vibe)
  2. verify in /plugins that "$PLUGIN_NAME" is listed
  3. the skill loads with: /green-vibe   (user-invocable)
     or automatically when coding NR-relevant work

The post-edit hook is active automatically (post_tool, fail-open).
To disable it: remove ai.mistral.vibe/hooks.toml from the installed copy.
EOF
