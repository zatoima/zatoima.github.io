"""Paper fetchers for arXiv, Semantic Scholar, and Hugging Face Daily Papers."""

import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta

import arxiv
import requests

from config import (
    ARXIV_CATEGORIES,
    ARXIV_KEYWORDS,
    ARXIV_MAX_RESULTS,
    HF_DAILY_PAPERS_URL,
    LLM_FILTER_KEYWORDS,
    MAX_RETRIES,
    REQUEST_DELAY,
    RETRY_DELAY,
    SEMANTIC_SCHOLAR_KEYWORDS,
    SEMANTIC_SCHOLAR_LIMIT,
)

logger = logging.getLogger(__name__)


@dataclass
class Paper:
    """Unified paper representation."""

    paper_id: str
    title: str
    authors: list[str]
    abstract: str
    published: str  # ISO date string
    url: str
    source: str  # "arxiv", "semantic_scholar", "huggingface"
    arxiv_id: str | None = None
    doi: str | None = None
    categories: list[str] = field(default_factory=list)


def _retry_request(func, *args, **kwargs):
    """Retry a function call with exponential backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_DELAY * (2**attempt)
                logger.warning(
                    "Attempt %d failed: %s. Retrying in %ds...",
                    attempt + 1,
                    e,
                    wait,
                )
                time.sleep(wait)
            else:
                logger.error("All %d attempts failed: %s", MAX_RETRIES, e)
                raise


def fetch_arxiv_papers() -> list[Paper]:
    """Fetch LLM-related papers from arXiv."""
    logger.info("Fetching papers from arXiv...")
    papers = []

    cat_query = " OR ".join(f"cat:{cat}" for cat in ARXIV_CATEGORIES)
    keyword_query = " OR ".join(f'abs:"{kw}"' for kw in ARXIV_KEYWORDS[:5])
    query = f"({cat_query}) AND ({keyword_query})"

    def _fetch():
        client = arxiv.Client(
            page_size=ARXIV_MAX_RESULTS,
            delay_seconds=5.0,
            num_retries=5,
        )
        search = arxiv.Search(
            query=query,
            max_results=ARXIV_MAX_RESULTS,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        return list(client.results(search))

    try:
        results = _retry_request(_fetch)
        for result in results:
            arxiv_id = result.entry_id.split("/abs/")[-1]
            paper = Paper(
                paper_id=f"arxiv:{arxiv_id}",
                title=result.title.strip(),
                authors=[a.name for a in result.authors],
                abstract=result.summary.strip(),
                published=result.published.strftime("%Y-%m-%d"),
                url=result.entry_id,
                source="arxiv",
                arxiv_id=arxiv_id,
                doi=result.doi,
                categories=list(result.categories),
            )
            papers.append(paper)
        logger.info("Fetched %d papers from arXiv", len(papers))
    except Exception as e:
        logger.error("Failed to fetch from arXiv: %s", e)

    return papers


def _build_s2_paper_id(ext_ids: dict, fallback_id: str) -> str:
    """Build a paper ID from Semantic Scholar external IDs."""
    arxiv_id = ext_ids.get("ArXiv")
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    doi = ext_ids.get("DOI")
    if doi:
        return f"doi:{doi}"
    return f"s2:{fallback_id}"


def _parse_s2_paper(item: dict, today: str) -> Paper | None:
    """Parse a single Semantic Scholar paper entry."""
    if not item.get("abstract"):
        return None

    ext_ids = item.get("externalIds", {}) or {}
    arxiv_id = ext_ids.get("ArXiv")
    doi = ext_ids.get("DOI")
    paper_id = _build_s2_paper_id(ext_ids, item.get("paperId", ""))

    url = item.get("url", "")
    if arxiv_id:
        url = f"https://arxiv.org/abs/{arxiv_id}"

    return Paper(
        paper_id=paper_id,
        title=item["title"].strip(),
        authors=[a.get("name", "") for a in (item.get("authors") or [])],
        abstract=item["abstract"].strip(),
        published=item.get("publicationDate", today) or today,
        url=url,
        source="semantic_scholar",
        arxiv_id=arxiv_id,
        doi=doi,
    )


def _fetch_s2_keyword(base_url: str, params: dict) -> dict:
    """Fetch papers from Semantic Scholar for a single keyword."""
    resp = requests.get(base_url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_semantic_scholar_papers() -> list[Paper]:
    """Fetch LLM-related papers from Semantic Scholar API."""
    logger.info("Fetching papers from Semantic Scholar...")
    papers = []
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")

    for keyword in SEMANTIC_SCHOLAR_KEYWORDS:
        time.sleep(REQUEST_DELAY)
        params = {
            "query": keyword,
            "limit": SEMANTIC_SCHOLAR_LIMIT,
            "fields": "title,authors,abstract,externalIds,publicationDate,url,openAccessPdf",
            "publicationDateOrYear": f"{one_week_ago}:{today}",
            "openAccessPdf": "",
        }

        try:
            data = _retry_request(_fetch_s2_keyword, base_url, params)
            for item in data.get("data", []):
                paper = _parse_s2_paper(item, today)
                if paper:
                    papers.append(paper)

            logger.info(
                "Fetched %d papers from Semantic Scholar for '%s'",
                len(data.get("data", [])),
                keyword,
            )

        except Exception as e:
            logger.error(
                "Failed to fetch from Semantic Scholar for '%s': %s",
                keyword,
                e,
            )

    return papers


def _is_llm_related(title: str, abstract: str) -> bool:
    """Check if a paper is LLM-related based on title and abstract."""
    text = (title + " " + abstract).lower()
    return any(kw.lower() in text for kw in LLM_FILTER_KEYWORDS)


def _parse_hf_paper(item: dict) -> Paper | None:
    """Parse a single Hugging Face daily paper entry."""
    paper_info = item.get("paper", {})
    arxiv_id = paper_info.get("id", "")
    title = paper_info.get("title", "").strip()
    abstract = paper_info.get("summary", "").strip()

    if not title or not abstract or not _is_llm_related(title, abstract):
        return None

    authors = [a.get("name", "") for a in paper_info.get("authors", [])]
    pub_date = paper_info.get("publishedAt", "")
    if pub_date:
        pub_date = pub_date[:10]

    return Paper(
        paper_id=f"arxiv:{arxiv_id}" if arxiv_id else f"hf:{title[:50]}",
        title=title,
        authors=authors,
        abstract=abstract,
        published=pub_date or datetime.now().strftime("%Y-%m-%d"),
        url=f"https://arxiv.org/abs/{arxiv_id}"
        if arxiv_id
        else f"https://huggingface.co/papers/{arxiv_id}",
        source="huggingface",
        arxiv_id=arxiv_id if arxiv_id else None,
    )


def fetch_huggingface_daily_papers() -> list[Paper]:
    """Fetch papers from Hugging Face Daily Papers API."""
    logger.info("Fetching papers from Hugging Face Daily Papers...")

    api_url = "https://huggingface.co/api/daily_papers"

    try:

        def _fetch():
            resp = requests.get(api_url, timeout=30)
            resp.raise_for_status()
            return resp.json()

        data = _retry_request(_fetch)
        papers = [p for item in data if (p := _parse_hf_paper(item)) is not None]

        logger.info(
            "Fetched %d LLM-related papers from Hugging Face Daily Papers",
            len(papers),
        )
        return papers

    except Exception as e:
        logger.error("Failed to fetch from Hugging Face Daily Papers: %s", e)
        return []


def deduplicate_papers(papers: list[Paper]) -> list[Paper]:
    """Remove duplicate papers based on paper_id, preferring arXiv source."""
    seen = {}
    for paper in papers:
        key = paper.paper_id
        if key not in seen or paper.source == "arxiv":
            seen[key] = paper

    # Also deduplicate by normalized title
    title_seen = {}
    unique = []
    for paper in seen.values():
        normalized = re.sub(r"\s+", " ", paper.title.lower().strip())
        if normalized not in title_seen:
            title_seen[normalized] = True
            unique.append(paper)

    logger.info(
        "Deduplicated %d -> %d papers", len(papers), len(unique)
    )
    return unique


def fetch_all_papers() -> list[Paper]:
    """Fetch papers from all sources and deduplicate."""
    all_papers = []

    all_papers.extend(fetch_arxiv_papers())
    all_papers.extend(fetch_semantic_scholar_papers())
    all_papers.extend(fetch_huggingface_daily_papers())

    unique = deduplicate_papers(all_papers)

    # Sort by publication date (newest first)
    unique.sort(key=lambda p: p.published, reverse=True)

    return unique
