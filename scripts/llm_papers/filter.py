"""AIDB-style relevance filter using Claude CLI."""

import logging
import os
import subprocess
import time

from config import AIDB_FILTER_ENABLED, AIDB_RELEVANCE_THRESHOLD, REQUEST_DELAY
from fetchers import Paper

logger = logging.getLogger(__name__)

_AIDB_SCORE_PROMPT = """\
あなたはAIDBというAI論文メディアの編集者です。AIDBは日々公開されるAI論文の中から「重要かつ興味深い」論文のみを厳選しています。

以下の論文がAIDBの掲載基準に合っているか、0〜10の整数スコアで評価してください（数字のみを返す）。

【高スコア（7-10）の基準】
- LLMの挙動・能力・限界に関する驚くべき・直感に反する知見がある
- AIエージェントや自律システムの実用的な改善・新パラダイム
- LLMの安全性・アライメント・倫理に関する重要な発見
- 今すぐ活用できるPrompt・CoT・推論技術の新知見
- 「なぜAIはこう動くか」を説明する基礎的・分析的な発見
- 実務のAI利用者が読んで「ほう、そうか」となる実践的洞察

【低スコア（0-4）の基準】
- 医療・法律・生物など特定ドメイン向けのNLP応用
- 既存手法のベンチマーク比較のみで新しい知見がない
- 翻訳・要約・質問応答などの個別タスクの性能改善
- データセットやアノテーションツールの作成のみ
- 広範な示唆のないアーキテクチャの細部改良
- 特定言語（英語以外）のNLP問題

タイトル: {title}
Abstract: {abstract}

スコア（0〜10の整数のみ）:\
"""


def _get_claude_env() -> dict:
    """Get environment with CLAUDECODE unset to allow nested invocation."""
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    return env


def score_paper_relevance(paper: Paper) -> int:
    """Score a paper's AIDB relevance using Claude CLI (0-10).

    Returns 5 (neutral) on failure so the paper is not silently excluded.
    """
    prompt = _AIDB_SCORE_PROMPT.format(
        title=paper.title,
        abstract=paper.abstract[:800],
    )

    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=60,
            env=_get_claude_env(),
        )
        if result.returncode == 0 and result.stdout.strip():
            score_str = result.stdout.strip().split()[0]
            score = int(score_str)
            return min(max(score, 0), 10)
        else:
            logger.warning(
                "claude CLI failed scoring '%s': rc=%d",
                paper.title[:40],
                result.returncode,
            )
    except ValueError:
        logger.warning("Could not parse score for '%s'", paper.title[:40])
    except subprocess.TimeoutExpired:
        logger.warning("claude CLI timed out scoring '%s'", paper.title[:40])
    except FileNotFoundError:
        logger.error("claude CLI not found; skipping AIDB filter")

    return 5  # Neutral fallback: include the paper


def filter_by_aidb_relevance(papers: list[Paper]) -> list[Paper]:
    """Filter papers to those matching AIDB's editorial style.

    Scores each paper with Claude and returns only those scoring at or
    above AIDB_RELEVANCE_THRESHOLD.  If the filter is disabled via config,
    returns the input list unchanged.
    """
    if not AIDB_FILTER_ENABLED:
        logger.info("AIDB relevance filter is disabled; skipping")
        return papers

    logger.info(
        "--- AIDB relevance filter: scoring %d papers (threshold=%d/10) ---",
        len(papers),
        AIDB_RELEVANCE_THRESHOLD,
    )

    filtered = []
    for i, paper in enumerate(papers):
        if i > 0:
            time.sleep(REQUEST_DELAY)
        score = score_paper_relevance(paper)
        status = "PASS" if score >= AIDB_RELEVANCE_THRESHOLD else "skip"
        logger.info(
            "  [%s %d/10] %s",
            status,
            score,
            paper.title[:70],
        )
        if score >= AIDB_RELEVANCE_THRESHOLD:
            filtered.append(paper)

    logger.info(
        "AIDB filter result: %d / %d papers passed",
        len(filtered),
        len(papers),
    )
    return filtered
