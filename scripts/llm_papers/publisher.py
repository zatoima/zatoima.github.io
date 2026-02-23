"""Hugo content generation and Git publishing."""

import logging
import re
from datetime import datetime
from pathlib import Path

from config import CONTENT_DIR, HUGO_CATEGORIES, HUGO_TAGS
from fetchers import Paper

logger = logging.getLogger(__name__)


def _sanitize_slug(text: str) -> str:
    """Create a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80].strip("-")


def generate_hugo_content(
    papers: list[Paper],
    summaries: dict[str, str],
    screenshots: dict[str, str],
    date: str | None = None,
) -> Path:
    """Generate a Hugo blog post with paper summaries."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    dir_name = f"{date}-llm-papers-daily"
    post_dir = CONTENT_DIR / dir_name
    post_dir.mkdir(parents=True, exist_ok=True)

    slug = f"llm-papers-{date}"

    tags_str = ", ".join(f'"{t}"' for t in HUGO_TAGS)
    cats_str = ", ".join(f'"{c}"' for c in HUGO_CATEGORIES)

    lines = [
        "---",
        f'title: "LLM論文サーベイ（{date}）"',
        'subtitle: ""',
        'summary: " "',
        f"tags: [{tags_str}]",
        f"categories: [{cats_str}]",
        f"url: {slug}",
        f"date: {date}",
        "featured: false",
        "draft: false",
        "---",
        "",
        "## はじめに",
        "",
        f"本記事は{date}時点でのLLM関連の注目論文をまとめたものです。arXiv、Semantic Scholar、Hugging Face Daily Papersから自動収集し、Claude APIで日本語要約を生成しています。",
        "",
    ]

    for i, paper in enumerate(papers, 1):
        summary = summaries.get(paper.paper_id, "（要約取得失敗）")
        screenshot_file = screenshots.get(paper.paper_id)

        lines.append(f"## {i}. {paper.title}")
        lines.append("")

        # Metadata table
        authors_str = ", ".join(paper.authors[:5])
        if len(paper.authors) > 5:
            authors_str += " ほか"

        lines.append(f"- **著者**: {authors_str}")
        lines.append(f"- **公開日**: {paper.published}")
        lines.append(f"- **ソース**: [{paper.source}]({paper.url})")
        if paper.arxiv_id:
            lines.append(f"- **arXiv ID**: {paper.arxiv_id}")
        lines.append("")

        # Screenshot
        if screenshot_file:
            lines.append(f"![{paper.title}]({screenshot_file})")
            lines.append("")

        # Summary
        lines.append("### 要約")
        lines.append("")
        lines.append(summary)
        lines.append("")

        # Original abstract (collapsed)
        lines.append("{{< details \"原文Abstract\" >}}")
        lines.append(paper.abstract)
        lines.append("{{< /details >}}")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(
        "*この記事は自動生成されています。論文の詳細は各ソースURLをご参照ください。*"
    )

    content = "\n".join(lines)
    filepath = post_dir / "index.md"
    filepath.write_text(content, encoding="utf-8")

    logger.info("Hugo content generated: %s", filepath)
    return post_dir
