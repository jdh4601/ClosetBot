#!/usr/bin/env bash
set -euo pipefail

# Simple helper to submit an analysis job and poll until it's done.
# Usage:
#   ./scripts/submit_and_poll.sh <brand_username> <influencer1,influencer2,...> [timeout_seconds]
# Env:
#   API_URL (default: http://localhost:8000/api/v1)

API_URL=${API_URL:-http://localhost:8000/api/v1}

if [ $# -lt 2 ]; then
  echo "Usage: $0 <brand_username> <influencer1,influencer2,...> [timeout_seconds]" >&2
  exit 1
fi

BRAND="$1"
IFS=',' read -r -a INFLUENCERS <<< "$2"
TIMEOUT=${3:-300}

payload=$(jq -n --arg brand "$BRAND" --argjson infl "$(printf '%s\n' "${INFLUENCERS[@]}" | jq -R . | jq -s .)" '{brand_username:$brand, influencer_usernames:$infl}')

echo "[1/3] Submitting job to $API_URL/analysis/jobs"
resp=$(curl -sS -X POST "$API_URL/analysis/jobs" -H 'Content-Type: application/json' -d "$payload")
echo "$resp" | jq . >/dev/null || { echo "Invalid response: $resp" >&2; exit 1; }
job_id=$(echo "$resp" | jq -r .job_id)
echo "Job ID: $job_id"

echo "[2/3] Polling status..."
start=$(date +%s)
while true; do
  status_resp=$(curl -sS "$API_URL/analysis/jobs/$job_id")
  status=$(echo "$status_resp" | jq -r .status)
  echo "status=$status"
  if [ "$status" = "done" ] || [ "$status" = "failed" ]; then
    break
  fi
  now=$(date +%s)
  elapsed=$(( now - start ))
  if [ $elapsed -ge $TIMEOUT ]; then
    echo "Timeout after ${TIMEOUT}s" >&2
    exit 2
  fi
  sleep 5
done

echo "[3/3] Fetching results..."
results=$(curl -sS "$API_URL/analysis/jobs/$job_id/results")
echo "$results" | jq .

