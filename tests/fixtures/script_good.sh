#!/bin/bash
# Fixture: conforming shell script
set -euo pipefail

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

for f in *.log; do
  awk '/ERROR|CRITICAL/ {print $3}' "$f" >> "$tmp"
done

for attempt in $(seq 1 5); do
  if curl -sf --max-time 5 http://status.example.com/ping; then
    break
  fi
  sleep $((attempt * 2))
done
