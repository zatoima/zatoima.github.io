"""State management for processed papers (deduplication)."""

import json
import logging
from datetime import datetime
from pathlib import Path

from config import STATE_FILE

logger = logging.getLogger(__name__)


def load_state() -> dict:
    """Load processed papers state from JSON file."""
    default = {"processed_ids": {}, "last_run": None}
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "processed_ids" not in data:
            return default
        return data
    return default


def save_state(state: dict) -> None:
    """Save processed papers state to JSON file."""
    state["last_run"] = datetime.now().isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    logger.info("State saved to %s", STATE_FILE)


def is_processed(state: dict, paper_id: str) -> bool:
    """Check if a paper has already been processed."""
    return paper_id in state["processed_ids"]


def mark_processed(state: dict, paper_id: str, title: str) -> None:
    """Mark a paper as processed."""
    state["processed_ids"][paper_id] = {
        "title": title,
        "processed_at": datetime.now().isoformat(),
    }
