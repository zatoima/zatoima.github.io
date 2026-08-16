#!/usr/bin/env python3
"""Build the small homepage summary payload from the generated monitor HTML."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path


def extract(pattern: str, source: str, label: str) -> str:
    match = re.search(pattern, source, re.DOTALL)
    if not match:
        raise ValueError(f"Could not extract {label}")
    return match.group(1 if match.lastindex else 0).strip()


def plain_text(fragment: str) -> str:
    separated_blocks = re.sub(r"</[^>]+>\s*<[^>]+>", " ", fragment)
    without_tags = re.sub(r"<[^>]+>", "", separated_blocks)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def build_payload(source: str) -> dict[str, str]:
    feature_card = extract(r'<a class="stat feat".*?</a>', source, "feature card")
    page_card = extract(r'<a class="stat page".*?</a>', source, "page card")
    url_card = extract(r'<a class="stat url".*?</a>', source, "URL card")
    day_starts = list(re.finditer(r'<div class="day"><div class="date">([^<]+)</div>', source))
    latest_day = ""
    latest_event = ""
    for index, day_match in enumerate(day_starts):
        block_end = day_starts[index + 1].start() if index + 1 < len(day_starts) else len(source)
        day_block = source[day_match.start():block_end]
        event_match = re.search(r'<div class="ev page">(.*?)(?=<div class="ev |</div></div></div>)', day_block, re.DOTALL)
        if event_match:
            latest_day = day_match.group(1).strip()
            latest_event = event_match.group(1).strip()
            break

    if not latest_day or not latest_event:
        raise ValueError("Could not extract the latest document-change event")

    summary_match = re.search(r'<div class="s">(.*?)</div>', latest_event, re.DOTALL)
    detail_match = re.search(r'<div class="d">(.*?)</div>', latest_event, re.DOTALL)
    if summary_match:
        summary = plain_text(summary_match.group(1))
    elif detail_match:
        summary = f"変更内訳: {plain_text(detail_match.group(1))}"
    else:
        summary = "ドキュメントの変更を検知しました。詳細は変更履歴で確認できます。"

    return {
        "updated_date": latest_day,
        "new_features": plain_text(extract(r'<div class="v">(.*?)</div>', feature_card, "new feature count")),
        "compared_pages": plain_text(extract(r'<div class="v">(.*?)</div>', page_card, "compared page count")),
        "active_pages": plain_text(extract(r'<div class="v">(.*?)</div>', url_card, "active page count")),
        "headline": plain_text(extract(r'<div class="t">(.*?)</div>', latest_event, "latest headline")),
        "summary": summary,
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: build_snowflake_monitor_summary.py INPUT_HTML OUTPUT_JSON", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    payload = build_payload(input_path.read_text(encoding="utf-8"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built Snowflake Doc Monitor summary: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
