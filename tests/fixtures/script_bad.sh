#!/bin/bash
# Fixture: shell script with detectable anti-patterns
OUT=/tmp/backup_out.txt
for f in $(ls *.log); do
  grep ERROR "$f" | grep CRITICAL | cut -d' ' -f3 >> "$OUT"
done

i=0
while true; do
  curl -s http://status.example.com/ping || true
  sleep 5
done
