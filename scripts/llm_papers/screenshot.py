"""Screenshot capture for paper pages using Playwright."""

import logging
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from config import MAX_RETRIES, RETRY_DELAY
from fetchers import Paper

logger = logging.getLogger(__name__)


def capture_paper_screenshot(paper: Paper, output_path: Path) -> bool:
    """Capture a screenshot of a paper's arXiv abstract page."""
    url = paper.url
    if not url:
        logger.warning("No URL for paper: %s", paper.title)
        return False

    # Prefer arXiv abstract page
    if paper.arxiv_id:
        url = f"https://arxiv.org/abs/{paper.arxiv_id}"

    for attempt in range(MAX_RETRIES):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1280, "height": 960})
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2)  # Wait for rendering
                page.screenshot(path=str(output_path), full_page=False)
                browser.close()

            logger.info("Screenshot saved: %s", output_path.name)
            return True

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_DELAY * (2**attempt)
                logger.warning(
                    "Screenshot attempt %d failed for '%s': %s. Retrying in %ds...",
                    attempt + 1,
                    paper.title[:40],
                    e,
                    wait,
                )
                time.sleep(wait)
            else:
                logger.error(
                    "Failed to capture screenshot for '%s': %s",
                    paper.title,
                    e,
                )
                return False

    return False


def capture_screenshots(
    papers: list[Paper], output_dir: Path
) -> dict[str, str]:
    """Capture screenshots for top papers. Returns {paper_id: filename}."""
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshots = {}

    for i, paper in enumerate(papers):
        filename = f"paper_{i + 1}.png"
        filepath = output_dir / filename
        if capture_paper_screenshot(paper, filepath):
            screenshots[paper.paper_id] = filename

    return screenshots
