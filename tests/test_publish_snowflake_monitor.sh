#!/usr/bin/env bash
set -euo pipefail

readonly PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_ROOT="$(mktemp -d)"
cleanup() {
  local exit_code=$?
  trap - EXIT
  rm -rf -- "$TEST_ROOT"
  exit "$exit_code"
}
trap cleanup EXIT

readonly TEST_REPO="$TEST_ROOT/repo"
readonly TEST_REMOTE="$TEST_ROOT/remote.git"
readonly TEST_PORTAL_SITE="$TEST_ROOT/portal"
readonly TEST_FEATURE_SITE="$TEST_ROOT/features"
readonly TEST_DIFF_SITE="$TEST_ROOT/diff"
readonly TEST_BIN="$TEST_ROOT/bin"

mkdir -p \
  "$TEST_REPO/scripts" "$TEST_REPO/static/css" "$TEST_REPO/static/js" \
  "$TEST_PORTAL_SITE" "$TEST_FEATURE_SITE" "$TEST_DIFF_SITE" "$TEST_BIN"
install -m 0755 "$PROJECT_ROOT/scripts/publish_snowflake_monitor.sh" "$TEST_REPO/scripts/"
install -m 0755 "$PROJECT_ROOT/scripts/process_snowflake_monitor.sh" "$TEST_REPO/scripts/"
install -m 0755 "$PROJECT_ROOT/scripts/build_snowflake_monitor_summary.py" "$TEST_REPO/scripts/"
install -m 0644 "$PROJECT_ROOT/static/css/snowflake-monitor-shell.css" "$TEST_REPO/static/css/"
install -m 0644 "$PROJECT_ROOT/static/js/snowflake-monitor-shell.js" "$TEST_REPO/static/js/"

printf '%s\n' '<html><body>baseline</body></html>' >"$TEST_REPO/static/snowflake-monitor-placeholder.html"
printf '%s\n' '<html><body>invalid monitor fixture</body></html>' >"$TEST_PORTAL_SITE/index.html"
printf '%s\n' '#!/usr/bin/env bash' 'exit 0' >"$TEST_BIN/flock"
chmod 0755 "$TEST_BIN/flock"

git init --bare --initial-branch=main "$TEST_REMOTE" >/dev/null
git -C "$TEST_REPO" init -b main >/dev/null
git -C "$TEST_REPO" config user.name "Monitor Test"
git -C "$TEST_REPO" config user.email "monitor-test@example.com"
git -C "$TEST_REPO" add .
git -C "$TEST_REPO" commit -m "test: create publisher fixture" >/dev/null
git -C "$TEST_REPO" remote add origin "$TEST_REMOTE"
git -C "$TEST_REPO" push -u origin main >/dev/null

set +e
PATH="$TEST_BIN:$PATH" \
PORTAL_SITE="$TEST_PORTAL_SITE" \
FEATURE_SITE="$TEST_FEATURE_SITE" \
DIFF_SITE="$TEST_DIFF_SITE" \
LOCK_FILE="$TEST_ROOT/publish.lock" \
PUBLISH_LOG="" \
PUBLIC_SUMMARY_URL="file://$TEST_ROOT/never-used.json" \
  "$TEST_REPO/scripts/publish_snowflake_monitor.sh" >"$TEST_ROOT/command.log" 2>&1
publish_rc=$?
set -e

if [[ $publish_rc -eq 0 ]]; then
  echo "Publisher unexpectedly succeeded with an invalid generated snapshot" >&2
  exit 1
fi

if ! grep -q "Could not extract feature card" "$TEST_ROOT/command.log"; then
  echo "Publisher did not fail in the expected snapshot processing stage" >&2
  sed -n '1,160p' "$TEST_ROOT/command.log" >&2
  exit 1
fi

if [[ -n "$(git -C "$TEST_REPO" status --porcelain)" ]]; then
  echo "Publisher failure left the tracked worktree dirty" >&2
  git -C "$TEST_REPO" status --short >&2
  exit 1
fi

echo "Publisher processing failure preserved a clean worktree"
