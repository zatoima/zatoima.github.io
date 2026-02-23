#!/bin/bash
# LLM Papers Daily Pipeline - Wrapper script
# Summarization uses `claude -p` (Claude Code CLI), so no API key is needed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/cron.log"

# Redirect all output to log
exec >> "${LOG_FILE}" 2>&1

echo "========================================"
echo "Pipeline started at $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# Activate virtual environment if exists
if [ -d "${SCRIPT_DIR}/venv" ]; then
    source "${SCRIPT_DIR}/venv/bin/activate"
fi

# Ensure PATH includes hugo, git, and claude
export PATH="/usr/local/bin:/opt/homebrew/bin:${HOME}/.claude/local:${PATH}"

# Run the pipeline
cd "${SCRIPT_DIR}"
python3 pipeline.py --verbose

echo "Pipeline finished at $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
