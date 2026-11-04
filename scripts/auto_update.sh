#!/bin/bash
# Green Vibe post_agent hook: keep the installed plugin in sync with its
# source repository, once a day, fail-open.
#
# Vibe calls this after the main agent finishes a turn. A stamp file
# throttles the check to one git fetch per day; every other turn the hook
# exits after a single stat. When the upstream moved, the hook pulls
# (ff-only, clean tree only, never touches uncommitted work) and re-syncs
# the installed copy, then emits a system_message asking for
# /reload-plugins. Any error exits 0 with no output: the hook never blocks,
# never warns, and never prompts.

set -u

STATE_DIR="${HOME}/.vibe/.green-vibe"
STAMP="$STATE_DIR/last-check"
SOURCE_FILE="$STATE_DIR/source"
COMMIT_FILE="$STATE_DIR/commit"
INTERVAL=86400  # seconds between checks

[ -f "$SOURCE_FILE" ] || exit 0
[ -f "$STATE_DIR/no-autoupdate" ] && exit 0
SOURCE="$(cat "$SOURCE_FILE" 2>/dev/null)" || exit 0
[ -d "$SOURCE" ] || exit 0
[ -f "$SOURCE/plugin.json" ] || exit 0

now="$(date +%s)"
last="$(cat "$STAMP" 2>/dev/null || echo 0)"
[ "$((now - last))" -lt "$INTERVAL" ] && exit 0

# Claim the day's check before doing the work, so a failure does not retry
# on every turn.
mkdir -p "$STATE_DIR" 2>/dev/null
echo "$now" > "$STAMP" 2>/dev/null

command -v git >/dev/null 2>&1 || exit 0
git -C "$SOURCE" rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || exit 0  # dirty tree: hands off

# Bound the network round-trip: give up on a stalled fetch instead of
# waiting for the hook timeout.
export GIT_HTTP_LOW_SPEED_LIMIT=1000
export GIT_HTTP_LOW_SPEED_TIME=10

git -C "$SOURCE" fetch --quiet 2>/dev/null || exit 0
HEAD_SHA="$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" || exit 0
UPSTREAM_SHA="$(git -C "$SOURCE" rev-parse '@{u}' 2>/dev/null)" || exit 0

if [ "$HEAD_SHA" != "$UPSTREAM_SHA" ]; then
  git -C "$SOURCE" pull --ff-only --quiet 2>/dev/null || exit 0
  HEAD_SHA="$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" || exit 0
fi

# Sync when the source moved since the last install, version bump or not.
RECORDED_SHA="$(cat "$COMMIT_FILE" 2>/dev/null)" || RECORDED_SHA=""
if [ -n "$RECORDED_SHA" ] && [ "$HEAD_SHA" = "$RECORDED_SHA" ]; then
  exit 0
fi

bash "$SOURCE/scripts/install.sh" user >/dev/null 2>&1 || exit 0

# install.sh refreshed the state; make sure the commit record matches what
# was actually synced.
git -C "$SOURCE" rev-parse HEAD > "$COMMIT_FILE" 2>/dev/null

NEW_VERSION="$(python3 -B -c \
  'import json,sys; print(json.load(open(sys.argv[1]))["version"])' \
  "${HOME}/.vibe/plugins/green-vibe/plugin.json" 2>/dev/null)" || exit 0
printf '{"decision":"allow","system_message":"green-vibe updated to %s. Run /reload-plugins to load it in this session."}\n' "$NEW_VERSION"
exit 0
