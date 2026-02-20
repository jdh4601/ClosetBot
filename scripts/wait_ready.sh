#!/usr/bin/env bash
set -euo pipefail

# Poll readiness endpoint until ready or timeout.
# Usage: ./scripts/wait_ready.sh [url] [timeout_seconds]
# Defaults: url=http://localhost:8000/api/v1/health/ready, timeout=120

URL=${1:-http://localhost:8000/api/v1/health/ready}
TIMEOUT=${2:-120}

echo "Waiting for ready: $URL (timeout=${TIMEOUT}s)"
start=$(date +%s)
while true; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || true)
  if [ "$code" = "200" ]; then
    echo "Service is ready."
    exit 0
  fi
  now=$(date +%s)
  elapsed=$(( now - start ))
  if [ $elapsed -ge $TIMEOUT ]; then
    echo "Not ready after ${TIMEOUT}s (last code=$code)" >&2
    exit 1
  fi
  sleep 3
done

