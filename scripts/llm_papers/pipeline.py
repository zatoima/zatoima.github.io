#!/usr/bin/env python3
"""LLM Papers Daily Pipeline - Main entry point.

Fetches LLM-related papers from arXiv, Semantic Scholar, and Hugging Face,
generates Japanese summaries using Claude API, captures screenshots,
and publishes to Hugo blog.
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from config import LOG_FILE, MIN_PAPERS_TO_POST, POPULARITY_THRESHOLD, PROJECT_ROOT, TOP_N_PAPERS
from fetchers import fetch_all_papers
from notifier import notify_slack
from publisher import generate_hugo_content
from screenshot import capture_screenshots
from state import is_seen, load_state, mark_processed, mark_seen, save_state
from summarizer import generate_summaries


def setup_logging(verbose: bool = False) -> None:
    """Configure logging to both file and console."""
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    logging.basicConfig(level=level, format=fmt)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt))
    logging.getLogger().addHandler(file_handler)


def git_commit_and_push(post_dir: Path) -> None:
    """Commit and push the generated content to GitHub."""
    logger = logging.getLogger(__name__)

    try:
        # Add the content directory and state file
        from config import STATE_FILE
        subprocess.run(
            ["git", "add", str(post_dir), str(STATE_FILE)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )

        date = datetime.now().strftime("%Y-%m-%d")
        subprocess.run(
            ["git", "commit", "-m", f"Add LLM papers survey ({date})"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )

        # Hugo build
        subprocess.run(
            ["hugo", "--config", "hugo.toml", "-d", "docs"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )

        # Commit build output
        subprocess.run(
            ["git", "add", "docs/"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Build website"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )

        # Sync with remote before pushing to avoid rejection
        logger.info("Pulling latest changes from remote...")
        subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )

        # Push
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )

        logger.info("Successfully committed and pushed to GitHub")

    except subprocess.CalledProcessError as e:
        logger.error("Git operation failed: %s\nstderr: %s", e, e.stderr.decode())
        raise


def run_pipeline(
    skip_screenshots: bool = False,
    skip_push: bool = False,
    dry_run: bool = False,
    max_papers: int | None = None,
) -> None:
    """Run the full pipeline."""
    logger = logging.getLogger(__name__)
    today = datetime.now().strftime("%Y-%m-%d")

    logger.info("=== LLM Papers Pipeline Start (%s) ===", today)

    # 1. Load state
    state = load_state()
    logger.info(
        "Loaded state: %d processed, %d seen papers",
        len(state["processed_ids"]),
        len(state["seen_ids"]),
    )

    # 2. Fetch papers
    logger.info("--- Step 1: Fetching papers ---")
    all_papers = fetch_all_papers()
    logger.info("Total fetched: %d papers", len(all_papers))

    # 3. Delta detection: find papers not previously seen
    delta_papers = [p for p in all_papers if not is_seen(state, p.paper_id)]
    logger.info("Delta (new since last run): %d papers", len(delta_papers))

    # 4. Record ALL fetched papers as seen (for next run's delta)
    for paper in all_papers:
        mark_seen(state, paper.paper_id, paper.title)

    if not delta_papers:
        logger.info("No new papers since last run. Saving state and exiting.")
        save_state(state)
        return

    # 5. Filter by popularity threshold
    popular_papers = [
        p for p in delta_papers if p.popularity_score >= POPULARITY_THRESHOLD
    ]
    logger.info(
        "Popular papers (score >= %.1f): %d / %d delta",
        POPULARITY_THRESHOLD,
        len(popular_papers),
        len(delta_papers),
    )

    if len(popular_papers) < MIN_PAPERS_TO_POST:
        logger.info(
            "Not enough popular papers (%d < %d). Saving state and skipping post.",
            len(popular_papers),
            MIN_PAPERS_TO_POST,
        )
        save_state(state)
        return

    # 6. Limit number of papers
    limit = max_papers or TOP_N_PAPERS
    featured_papers = popular_papers[:limit]
    logger.info("Featuring top %d popular papers", len(featured_papers))

    if dry_run:
        logger.info("--- DRY RUN: Showing papers that would be processed ---")
        for i, p in enumerate(featured_papers, 1):
            logger.info(
                "  %d. [%s] %s (score=%.1f, sources=%d)",
                i, p.source, p.title, p.popularity_score, p.source_count,
            )
        save_state(state)
        return

    # 7. Generate summaries
    logger.info("--- Step 2: Generating summaries ---")
    summaries = generate_summaries(featured_papers)

    # 8. Capture screenshots
    screenshots = {}
    if not skip_screenshots:
        logger.info("--- Step 3: Capturing screenshots ---")
        from config import CONTENT_DIR

        post_dir = CONTENT_DIR / f"{today}-llm-papers-daily"
        screenshots = capture_screenshots(featured_papers, post_dir)
    else:
        logger.info("--- Step 3: Skipping screenshots ---")

    # 9. Generate Hugo content
    logger.info("--- Step 4: Generating Hugo content ---")
    post_dir = generate_hugo_content(
        featured_papers, summaries, screenshots, today,
        total_delta=len(delta_papers),
    )

    # 10. Mark featured papers as processed
    for paper in featured_papers:
        mark_processed(state, paper.paper_id, paper.title)
    save_state(state)

    # 11. Git commit and push
    if not skip_push:
        logger.info("--- Step 5: Committing and pushing ---")
        git_commit_and_push(post_dir)
    else:
        logger.info("--- Step 5: Skipping git push ---")

    # 12. Slack notification
    logger.info("--- Step 6: Sending Slack notification ---")
    notify_slack(featured_papers, summaries, today, total_delta=len(delta_papers))

    logger.info("=== Pipeline Complete ===")


def main():
    parser = argparse.ArgumentParser(
        description="LLM Papers Daily Pipeline"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--skip-screenshots",
        action="store_true",
        help="Skip screenshot capture",
    )
    parser.add_argument(
        "--skip-push",
        action="store_true",
        help="Skip git commit/push",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without executing",
    )
    parser.add_argument(
        "--max-papers",
        type=int,
        default=None,
        help="Max number of papers to feature",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    try:
        run_pipeline(
            skip_screenshots=args.skip_screenshots,
            skip_push=args.skip_push,
            dry_run=args.dry_run,
            max_papers=args.max_papers,
        )
    except Exception as e:
        logging.getLogger(__name__).error("Pipeline failed: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
