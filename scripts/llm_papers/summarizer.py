"""Summary generation using Claude Code CLI."""

import logging
import os
import subprocess
import time

from config import REQUEST_DELAY
from fetchers import Paper

logger = logging.getLogger(__name__)


def _get_claude_env() -> dict:
    """Get environment with CLAUDECODE unset to allow nested invocation."""
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    return env


def generate_summary(paper: Paper) -> str:
    """Generate a Japanese summary of a paper using claude CLI."""
    prompt = (
        f"以下の論文のAbstractを日本語で要約してください。要約は3〜5文程度で、"
        f"技術的な内容を正確に伝えてください。要約のテキストのみを出力し、"
        f"前置きや説明は不要です。\n\n"
        f"タイトル: {paper.title}\n"
        f"著者: {', '.join(paper.authors[:5])}{'...' if len(paper.authors) > 5 else ''}\n"
        f"Abstract:\n{paper.abstract}"
    )

    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            env=_get_claude_env(),
        )
        if result.returncode == 0 and result.stdout.strip():
            summary = result.stdout.strip()
            logger.info("Generated summary for: %s", paper.title[:50])
            return summary
        else:
            logger.error(
                "claude CLI failed for '%s': rc=%d, stderr=%s",
                paper.title[:40],
                result.returncode,
                result.stderr[:200],
            )
            return paper.abstract[:300] + "..."
    except subprocess.TimeoutExpired:
        logger.error("claude CLI timed out for '%s'", paper.title[:40])
        return paper.abstract[:300] + "..."
    except FileNotFoundError:
        logger.error("claude CLI not found. Is Claude Code installed?")
        return paper.abstract[:300] + "..."


def generate_summaries(papers: list[Paper]) -> dict[str, str]:
    """Generate summaries for a list of papers."""
    summaries = {}
    for i, paper in enumerate(papers):
        if i > 0:
            time.sleep(REQUEST_DELAY)
        summaries[paper.paper_id] = generate_summary(paper)
    return summaries
