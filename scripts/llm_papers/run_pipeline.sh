#!/bin/bash
# LLM Papers Daily Pipeline - Wrapper script
# Summarization uses `claude -p` (Claude Code CLI), so no API key is needed.

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/cron.log"

# Redirect all output to log
exec >> "${LOG_FILE}" 2>&1

echo "========================================"
echo "Pipeline started at $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Ensure PATH includes hugo, git, and claude
export PATH="/usr/local/bin:/opt/homebrew/bin:${HOME}/.claude/local:${PATH}"

# Use venv python directly instead of activate (more reliable in launchd)
cd "${SCRIPT_DIR}"
./venv/bin/python3 pipeline.py --verbose

echo "Pipeline finished at $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
