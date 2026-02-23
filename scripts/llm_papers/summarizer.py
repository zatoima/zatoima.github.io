"""Summary generation using Anthropic API."""

import logging
import time

import anthropic

from config import REQUEST_DELAY
from fetchers import Paper

logger = logging.getLogger(__name__)


def generate_summary(paper: Paper) -> str:
    """Generate a Japanese summary of a paper using Claude API."""
    client = anthropic.Anthropic()

    prompt = f"""以下の論文のAbstractを日本語で要約してください。要約は3〜5文程度で、技術的な内容を正確に伝えてください。

タイトル: {paper.title}
著者: {', '.join(paper.authors[:5])}{'...' if len(paper.authors) > 5 else ''}
Abstract:
{paper.abstract}

要約（日本語で）:"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        summary = message.content[0].text.strip()
        logger.info("Generated summary for: %s", paper.title[:50])
        return summary
    except Exception as e:
        logger.error("Failed to generate summary for '%s': %s", paper.title, e)
        return paper.abstract[:300] + "..."


def generate_summaries(papers: list[Paper]) -> dict[str, str]:
    """Generate summaries for a list of papers."""
    summaries = {}
    for i, paper in enumerate(papers):
        if i > 0:
            time.sleep(REQUEST_DELAY)
        summaries[paper.paper_id] = generate_summary(paper)
    return summaries
