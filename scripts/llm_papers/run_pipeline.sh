#!/bin/bash
# LLM Papers Daily Pipeline - Cron wrapper script
# Usage: Add to crontab for daily execution
#   0 7 * * * /Users/zatoima/work/hugo/zatoima.github.io/scripts/llm_papers/run_pipeline.sh

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

# Ensure ANTHROPIC_API_KEY is set
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    # Try loading from .env file
    if [ -f "${SCRIPT_DIR}/.env" ]; then
        export $(grep -v '^#' "${SCRIPT_DIR}/.env" | xargs)
    else
        echo "ERROR: ANTHROPIC_API_KEY is not set and no .env file found"
        exit 1
    fi
fi

# Ensure PATH includes hugo and git
export PATH="/usr/local/bin:/opt/homebrew/bin:${PATH}"

# Run the pipeline
cd "${SCRIPT_DIR}"
python3 pipeline.py --verbose

echo "Pipeline finished at $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
