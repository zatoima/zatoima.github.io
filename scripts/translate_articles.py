#!/usr/bin/env python3
"""Detect untranslated Japanese blog articles and translate them to English via Claude CLI."""

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
JA_BLOG = PROJECT_ROOT / "content" / "ja" / "blog"
EN_BLOG = PROJECT_ROOT / "content" / "en" / "blog"

# Default: translate only recent articles (2026-02 and 2026-03)
DEFAULT_PREFIXES = ("2026-02", "2026-03")

TRANSLATE_PROMPT = """以下のHugoブログ記事（日本語）を英語に翻訳してください。

ルール:
- フロントマター（---で囲まれた部分）のtitle, subtitle, summaryを英語に翻訳する
- tagsとcategoriesの日本語値は英語に翻訳する（フィールド名は変更しない）
- url, translationKey, date, featured, draft, imageフィールドはそのまま保持する
- 本文を自然な英語に翻訳する
- Markdownの構造（見出し、箇条書き、コードブロック等）はそのまま保持する
- コードブロック（```で囲まれた部分）の内容は翻訳しない
- 翻訳したMarkdown全文のみを出力する（説明文・前置き・コードブロック外への注釈は不要）

---記事内容---
{content}"""


def get_articles_needing_translation(prefixes: tuple[str, ...]) -> list[Path]:
    """Find ja articles without corresponding en counterparts, filtered by date prefix."""
    missing = []
    for ja_dir in sorted(JA_BLOG.iterdir()):
        if not (ja_dir.is_dir() and (ja_dir / "index.md").exists()):
            continue
        if prefixes and not any(ja_dir.name.startswith(p) for p in prefixes):
            continue
        if not (EN_BLOG / ja_dir.name / "index.md").exists():
            missing.append(ja_dir)
    return missing


def translate_one(ja_dir: Path) -> tuple[Path, str | None]:
    """Translate a single article. Returns (ja_dir, error_message_or_None)."""
    try:
        content = (ja_dir / "index.md").read_text(encoding="utf-8")
        prompt = TRANSLATE_PROMPT.format(content=content)
        # Remove CLAUDECODE to allow calling claude from inside a Claude Code session
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True, text=True, timeout=120,
            env=env
        )
        if result.returncode != 0:
            return ja_dir, result.stderr.strip() or "claude CLI returned non-zero exit code"

        translated = result.stdout.strip()
        en_dir = EN_BLOG / ja_dir.name
        en_dir.mkdir(parents=True, exist_ok=True)
        (en_dir / "index.md").write_text(translated, encoding="utf-8")
        # Copy non-Markdown assets (images, charts, etc.)
        for asset in ja_dir.iterdir():
            if asset.is_file() and asset.suffix != ".md":
                (en_dir / asset.name).write_bytes(asset.read_bytes())
        return ja_dir, None
    except Exception as e:
        return ja_dir, str(e)


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate missing Japanese blog articles to English.")
    parser.add_argument("--all", action="store_true", help="Translate all untranslated articles (not just recent ones)")
    parser.add_argument("--workers", type=int, default=3, help="Number of parallel workers (default: 3)")
    args = parser.parse_args()

    prefixes = () if args.all else DEFAULT_PREFIXES
    articles = get_articles_needing_translation(prefixes)

    if not articles:
        print("All articles are translated. Nothing to do.")
        return 0

    scope = "all years" if args.all else f"prefixes: {', '.join(DEFAULT_PREFIXES)}"
    print(f"Found {len(articles)} article(s) to translate ({scope}, workers={args.workers}):")
    for a in articles:
        print(f"  - {a.name}")
    print()

    failed = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(translate_one, ja_dir): ja_dir for ja_dir in articles}
        for future in as_completed(futures):
            ja_dir, error = future.result()
            if error:
                print(f"FAILED: {ja_dir.name} — {error}")
                failed.append(ja_dir.name)
            else:
                print(f"done:   {ja_dir.name}")

    if failed:
        print(f"\n{len(failed)} article(s) failed to translate:")
        for f in failed:
            print(f"  - {f}")
        print("Deploy will continue. Retry failed articles manually.")
        return 1

    print(f"\nTranslated {len(articles)} article(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
