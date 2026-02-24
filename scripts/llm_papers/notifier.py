"""Slack notification via Claude Code CLI + Slack MCP."""

import logging
import os
import subprocess

from fetchers import Paper

logger = logging.getLogger(__name__)

SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID", "")


def _get_claude_env() -> dict:
    """Get environment with CLAUDECODE unset to allow nested invocation."""
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    return env


def _format_slack_message(
    papers: list[Paper], summaries: dict[str, str], date: str, blog_url: str
) -> str:
    """Format papers into a Slack message."""
    lines = [
        f"📄 *LLM論文サーベイ（{date}）*",
        f"本日の注目論文 {len(papers)}件をピックアップしました。",
        "",
    ]
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i, paper in enumerate(papers):
        emoji = emojis[i] if i < len(emojis) else f"{i+1}."
        summary = summaries.get(paper.paper_id, "")
        # Truncate summary for Slack readability
        if len(summary) > 150:
            summary = summary[:147] + "..."
        lines.append(f"{emoji} *{paper.title}*")
        lines.append(summary)
        lines.append(f"🔗 <{paper.url}|{paper.source}>")
        lines.append("")

    lines.append(f"📝 ブログ記事: <{blog_url}|zatoima.github.io>")
    return "\n".join(lines)


def notify_slack(
    papers: list[Paper], summaries: dict[str, str], date: str
) -> bool:
    """Send paper summary to Slack #notify channel via claude CLI + MCP."""
    blog_url = f"https://zatoima.github.io/llm-papers-{date}/"
    message = _format_slack_message(papers, summaries, date, blog_url)

    # Escape single quotes in message for shell
    escaped_message = message.replace("'", "'\\''")

    prompt = (
        f"以下のメッセージをSlackのnotifyチャンネル(ID: {SLACK_CHANNEL_ID})に"
        f"mcp__slack__slack_post_messageツールを使って投稿してください。"
        f"メッセージの内容をそのまま投稿し、それ以外の出力は不要です。\n\n"
        f"メッセージ:\n{escaped_message}"
    )

    try:
        result = subprocess.run(
            ["claude", "-p", "--allowedTools", "mcp__slack__slack_post_message"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60,
            env=_get_claude_env(),
        )
        if result.returncode == 0:
            logger.info("Slack notification sent successfully")
            return True
        else:
            logger.error(
                "Slack notification failed: rc=%d, stderr=%s",
                result.returncode,
                result.stderr[:200],
            )
            return False
    except subprocess.TimeoutExpired:
        logger.error("Slack notification timed out")
        return False
    except FileNotFoundError:
        logger.error("claude CLI not found for Slack notification")
        return False
