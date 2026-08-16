#!/usr/bin/env bash
set -euo pipefail

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly PORTAL_SITE="${PORTAL_SITE:-$HOME/snowflake-monitor-portal/site}"
readonly FEATURE_SITE="${FEATURE_SITE:-$HOME/snowflake-feature-monitor/site}"
readonly DIFF_SITE="${DIFF_SITE:-$HOME/snowflake-docs-diff/site}"
readonly STATIC_TARGET="$REPO_ROOT/static/snowflake-monitor"
readonly DOCS_TARGET="$REPO_ROOT/docs/snowflake-monitor"
readonly LOCK_FILE="${LOCK_FILE:-/tmp/snowflake-monitor-publish.lock}"
readonly PUBLISH_LOG="${PUBLISH_LOG-$HOME/logs/snowflake-monitor-publish.log}"
readonly PUBLIC_SUMMARY_URL="${PUBLIC_SUMMARY_URL:-https://zatoima.github.io/snowflake-monitor/summary.json}"
HTML_ONLY=(--include='*/' --include='*.html' --exclude='*' --prune-empty-dirs)
PREPARE_DIR=""

cleanup() {
  local exit_code=$?
  trap - EXIT
  if [[ -n "$PREPARE_DIR" && -d "$PREPARE_DIR" ]]; then
    rm -rf -- "$PREPARE_DIR"
  fi
  exit "$exit_code"
}
trap cleanup EXIT
trap 'exit 1' HUP INT TERM

if [[ -n "$PUBLISH_LOG" ]]; then
  mkdir -p "$(dirname "$PUBLISH_LOG")"
  if [[ -f "$PUBLISH_LOG" ]] && (( $(wc -c < "$PUBLISH_LOG") > 5242880 )); then
    mv "$PUBLISH_LOG" "$PUBLISH_LOG.1"
  fi
  exec > >(tee -a "$PUBLISH_LOG") 2>&1
fi

verify_public_summary() {
  local expected actual response_file attempt
  expected="$(sha256sum "$DOCS_TARGET/summary.json" | awk '{print $1}')"
  response_file="$(mktemp)"
  trap 'rm -f "$response_file"' RETURN
  for attempt in 1 2 3 4 5 6; do
    if curl --fail --silent --show-error "$PUBLIC_SUMMARY_URL" -o "$response_file"; then
      actual="$(sha256sum "$response_file" | awk '{print $1}')"
      if [[ "$actual" == "$expected" ]]; then
        echo "Verified public summary hash: $expected"
        return 0
      fi
    fi
    sleep 10
  done
  echo "Public summary did not reach expected hash: $expected" >&2
  return 1
}

validate_changed_paths() {
  local changed_path
  while IFS= read -r changed_path; do
    case "$changed_path" in
      static/snowflake-monitor/*.html | docs/snowflake-monitor/*.html | \
      static/snowflake-monitor/summary.json | docs/snowflake-monitor/summary.json | \
      docs/css/snowflake-monitor-shell.css | docs/js/snowflake-monitor-shell.js)
        ;;
      *)
        printf '%s\n' "$changed_path"
        ;;
    esac
  done
}

assert_only_monitor_changes() {
  local description="$1"
  local unexpected_paths="$2"
  if [[ -n "$unexpected_paths" ]]; then
    echo "Refusing to publish unexpected $description paths:" >&2
    printf '%s\n' "$unexpected_paths" >&2
    exit 1
  fi
}

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

PREPARE_DIR="$(mktemp -d "$REPO_ROOT/../.snowflake-monitor-publish.XXXXXX")"
readonly PREPARED_STATIC="$PREPARE_DIR/static/snowflake-monitor"
readonly PREPARED_DOCS="$PREPARE_DIR/docs/snowflake-monitor"
mkdir -p "$PREPARED_STATIC"
rsync -a --delete --delete-excluded "${HTML_ONLY[@]}" "$PORTAL_SITE/" "$PREPARED_STATIC/"
mkdir -p "$PREPARED_STATIC/features" "$PREPARED_STATIC/diff"
rsync -a --delete --delete-excluded "${HTML_ONLY[@]}" "$FEATURE_SITE/" "$PREPARED_STATIC/features/"
rsync -a --delete --delete-excluded "${HTML_ONLY[@]}" "$DIFF_SITE/" "$PREPARED_STATIC/diff/"

"$REPO_ROOT/scripts/process_snowflake_monitor.sh" "$PREPARED_STATIC"
for required_file in \
  index.html breaking.html urls.html credits.html \
  features/index.html diff/index.html summary.json; do
  if [[ ! -s "$PREPARED_STATIC/$required_file" ]]; then
    echo "Required generated file is missing or empty: $required_file" >&2
    exit 1
  fi
done
python3 -m json.tool "$PREPARED_STATIC/summary.json" >/dev/null

mkdir -p "$PREPARED_DOCS" "$PREPARE_DIR/docs/css" "$PREPARE_DIR/docs/js"
rsync -a --delete "$PREPARED_STATIC/" "$PREPARED_DOCS/"
install -m 0644 "$REPO_ROOT/static/css/snowflake-monitor-shell.css" "$PREPARE_DIR/docs/css/snowflake-monitor-shell.css"
install -m 0644 "$REPO_ROOT/static/js/snowflake-monitor-shell.js" "$PREPARE_DIR/docs/js/snowflake-monitor-shell.js"
cmp "$PREPARED_STATIC/summary.json" "$PREPARED_DOCS/summary.json"

if [[ -n "$(find "$PREPARE_DIR" -type l -print -quit)" ]]; then
  echo "Generated snapshot must not contain symbolic links" >&2
  exit 1
fi
unexpected_files="$(find "$PREPARED_STATIC" "$PREPARED_DOCS" -type f ! -name '*.html' ! -name 'summary.json' -print)"
if [[ -n "$unexpected_files" ]]; then
  echo "Generated snapshot contains unexpected files:" >&2
  printf '%s\n' "$unexpected_files" >&2
  exit 1
fi

mkdir -p "$STATIC_TARGET" "$DOCS_TARGET" "$REPO_ROOT/docs/css" "$REPO_ROOT/docs/js"
rsync -a --delete-delay --delay-updates "$PREPARED_STATIC/" "$STATIC_TARGET/"
rsync -a --delete-delay --delay-updates "$PREPARED_DOCS/" "$DOCS_TARGET/"
install -m 0644 "$PREPARE_DIR/docs/css/snowflake-monitor-shell.css" "$REPO_ROOT/docs/css/snowflake-monitor-shell.css"
install -m 0644 "$PREPARE_DIR/docs/js/snowflake-monitor-shell.js" "$REPO_ROOT/docs/js/snowflake-monitor-shell.js"

git add \
  static/snowflake-monitor \
  docs/snowflake-monitor \
  docs/css/snowflake-monitor-shell.css \
  docs/js/snowflake-monitor-shell.js

assert_only_monitor_changes \
  "staged" \
  "$(git diff --cached --name-only | validate_changed_paths)"

if git diff --cached --quiet; then
  echo "No Snowflake monitor changes to publish"
  # Retry a push if a previous run committed successfully but lost connectivity.
  assert_only_monitor_changes \
    "unpushed" \
    "$(git diff --name-only origin/main..HEAD | validate_changed_paths)"
  git push origin main
  verify_public_summary
  exit 0
fi

git commit -m "chore: update Snowflake monitor"
git pull --rebase origin main
assert_only_monitor_changes \
  "unpushed" \
  "$(git diff --name-only origin/main..HEAD | validate_changed_paths)"
git push origin main

verify_public_summary

echo "Published Snowflake monitor to GitHub Pages"
