#!/usr/bin/env bash

set -uo pipefail

DOCKER_BUILD_TIMEOUT=600

run_with_timeout() {
  local secs="$1"; shift
  if command -v timeout &>/dev/null; then
    timeout "$secs" "$@"
  else
    "$@" &
    local pid=$!
    ( sleep "$secs" && kill "$pid" 2>/dev/null ) &
    local watcher=$!
    wait "$pid" 2>/dev/null
    local rc=$?
    kill "$watcher" 2>/dev/null
    wait "$watcher" 2>/dev/null
    return $rc
  fi
}

PING_URL="${1:-}"
REPO_DIR="${2:-.}"

if [ -z "$PING_URL" ]; then
  echo "Usage: ./validate-submission.sh <ping_url> [repo_dir]"
  exit 1
fi

PING_URL="${PING_URL%/}"

echo "========================================"
echo "  OpenEnv Submission Validator"
echo "========================================"
echo "Repo:     $REPO_DIR"
echo "Ping URL: $PING_URL"
echo ""

# -----------------------------
# STEP 1: Ping HF Space
# -----------------------------
echo "Step 1/3: Pinging HF Space ($PING_URL/reset)..."

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" -d '{}' \
  "$PING_URL/reset" --max-time 30 || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
  echo "PASSED -- HF Space is live"
else
  echo "FAILED -- Space not reachable (HTTP $HTTP_CODE)"
  exit 1
fi

# -----------------------------
# STEP 2: Docker Build
# -----------------------------
echo "Step 2/3: Running docker build..."

if ! command -v docker &>/dev/null; then
  echo "FAILED -- docker not installed"
  exit 1
fi

if [ ! -f "$REPO_DIR/Dockerfile" ]; then
  echo "FAILED -- Dockerfile not found"
  exit 1
fi

if run_with_timeout "$DOCKER_BUILD_TIMEOUT" docker build "$REPO_DIR"; then
  echo "PASSED -- Docker build succeeded"
else
  echo "FAILED -- Docker build failed"
  exit 1
fi

# -----------------------------
# STEP 3: OpenEnv Validate
# -----------------------------
echo "Step 3/3: Running openenv validate..."

if ! command -v openenv &>/dev/null; then
  echo "FAILED -- openenv not installed"
  echo "Run: pip install openenv-core"
  exit 1
fi

if (cd "$REPO_DIR" && openenv validate); then
  echo "PASSED -- openenv validate passed"
else
  echo "FAILED -- openenv validate failed"
  exit 1
fi

echo ""
echo "========================================"
echo "  ALL CHECKS PASSED ✅"
echo "========================================"