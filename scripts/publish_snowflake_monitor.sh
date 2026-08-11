#!/usr/bin/env bash
set -euo pipefail

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly PORTAL_SITE="${PORTAL_SITE:-/home/opc/snowflake-monitor-portal/site}"
readonly FEATURE_SITE="${FEATURE_SITE:-/home/opc/snowflake-feature-monitor/site}"
readonly DIFF_SITE="${DIFF_SITE:-/home/opc/snowflake-docs-diff/site}"
readonly STATIC_TARGET="$REPO_ROOT/static/snowflake-monitor"
readonly DOCS_TARGET="$REPO_ROOT/docs/snowflake-monitor"
readonly LOCK_FILE="${LOCK_FILE:-/tmp/snowflake-monitor-publish.lock}"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "Another Snowflake monitor publish is already running"
  exit 0
fi

for source_dir in "$PORTAL_SITE" "$FEATURE_SITE" "$DIFF_SITE"; do
  if [[ ! -d "$source_dir" ]]; then
    echo "Required source directory not found: $source_dir" >&2
    exit 1
  fi
done

cd "$REPO_ROOT"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Repository has uncommitted changes; refusing to publish" >&2
  git status --short >&2
  exit 1
fi

git pull --rebase origin main

mkdir -p "$STATIC_TARGET/features" "$STATIC_TARGET/diff" "$STATIC_TARGET/assets"
rsync -a --delete --exclude .DS_Store "$PORTAL_SITE/" "$STATIC_TARGET/"
rsync -a --delete --exclude .DS_Store --exclude assets "$FEATURE_SITE/" "$STATIC_TARGET/features/"
rsync -a --delete --exclude .DS_Store "$FEATURE_SITE/assets/" "$STATIC_TARGET/assets/"
rsync -a --delete --exclude .DS_Store "$DIFF_SITE/" "$STATIC_TARGET/diff/"

"$REPO_ROOT/scripts/process_snowflake_monitor.sh" "$STATIC_TARGET"

mkdir -p "$DOCS_TARGET" "$REPO_ROOT/docs/css" "$REPO_ROOT/docs/js"
rsync -a --delete "$STATIC_TARGET/" "$DOCS_TARGET/"
install -m 0644 "$REPO_ROOT/static/css/snowflake-monitor-shell.css" "$REPO_ROOT/docs/css/snowflake-monitor-shell.css"
install -m 0644 "$REPO_ROOT/static/js/snowflake-monitor-shell.js" "$REPO_ROOT/docs/js/snowflake-monitor-shell.js"

git add \
  static/snowflake-monitor \
  docs/snowflake-monitor \
  docs/css/snowflake-monitor-shell.css \
  docs/js/snowflake-monitor-shell.js

if git diff --cached --quiet; then
  echo "No Snowflake monitor changes to publish"
  # Retry a push if a previous run committed successfully but lost connectivity.
  git push origin main
  exit 0
fi

git commit -m "chore: update Snowflake monitor"
git pull --rebase origin main
git push origin main

echo "Published Snowflake monitor to GitHub Pages"
