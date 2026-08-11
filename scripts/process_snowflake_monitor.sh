#!/usr/bin/env bash
set -euo pipefail

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly TARGET_DIR="${1:-$REPO_ROOT/static/snowflake-monitor}"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Monitor directory not found: $TARGET_DIR" >&2
  exit 1
fi

export MONITOR_HEAD_START='<script>(function(){var t=localStorage.getItem("theme");if(t==="dark"||((!t||t==="system")&&window.matchMedia("(prefers-color-scheme: dark)").matches)){document.documentElement.setAttribute("data-theme","dark");}else{document.documentElement.setAttribute("data-theme","light");}})();</script>
<link rel="stylesheet" href="/css/zenn.css">'
export MONITOR_HEAD_END='<link rel="stylesheet" href="/css/snowflake-monitor-shell.css">
<script src="/js/snowflake-monitor-shell.js" defer></script>
<script src="/js/dark-mode.js" defer></script>
<script src="/js/mobile-nav.js" defer></script>
<script src="/js/search.js" defer></script>
<script src="/js/lang-switcher.js" defer></script>'

while IFS= read -r -d '' html_file; do
  HTML_FILE="$html_file" perl -0pi -e '
    unless (/snowflake-monitor-shell\.js/) {
      s{(<meta name="viewport"[^>]*>)}{$1 . "\n" . $ENV{MONITOR_HEAD_START}}e;
      s{</head>}{$ENV{MONITOR_HEAD_END} . "\n</head>"}e;
    }
    s{href="/features/}{href="/snowflake-monitor/features/}g;
    s{href="/diff/}{href="/snowflake-monitor/diff/}g;
    s{href="/assets/}{href="/snowflake-monitor/assets/}g;
    s{src="/assets/}{src="/snowflake-monitor/assets/}g;
    s{url\("/assets/}{url("/snowflake-monitor/assets/}g;
    s{content="noindex, nofollow"}{content="index, follow"}g;
  ' "$html_file"
done < <(find "$TARGET_DIR" -type f -name '*.html' -print0)

echo "Processed Snowflake monitor HTML in $TARGET_DIR"
