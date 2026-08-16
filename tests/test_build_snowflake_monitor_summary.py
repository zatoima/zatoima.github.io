import unittest

from scripts.build_snowflake_monitor_summary import build_payload


def monitor_html(event: str) -> str:
    return f"""
<a class="stat feat"><div class="v">86</div></a>
<a class="stat page"><div class="v">8,332</div></a>
<a class="stat url"><div class="v">8,331</div></a>
<div class="day"><div class="date">2026-08-12</div><div class="body">
<div class="ev page">{event}</div></div></div>
"""


class BuildPayloadTests(unittest.TestCase):
    def test_prefers_ai_overview_when_present(self) -> None:
        source = monitor_html("""
<div class="t"><a href="/diff/reports/2026-08-12.html">ドキュメント本文の改訂</a></div>
<div class="d">新規 1 ・ 改訂 2 <span>影響大 1</span></div>
<div class="s">主要な<strong>仕様変更</strong>を検知しました。</div>
""")

        payload = build_payload(source)

        self.assertEqual(payload["updated_date"], "2026-08-12")
        self.assertEqual(payload["headline"], "ドキュメント本文の改訂")
        self.assertEqual(payload["summary"], "主要な仕様変更を検知しました。")

    def test_falls_back_to_change_detail_without_overview(self) -> None:
        source = monitor_html("""
<div class="t"><a href="/diff/reports/2026-08-12.html">ドキュメント本文の改訂</a></div>
<div class="d">新規 6 ・ 改訂 21 <span>影響大 1</span><span>新規ページ 6</span></div>
""")

        payload = build_payload(source)

        self.assertEqual(payload["new_features"], "86")
        self.assertEqual(payload["compared_pages"], "8,332")
        self.assertEqual(payload["active_pages"], "8,331")
        self.assertEqual(
            payload["summary"],
            "変更内訳: 新規 6 ・ 改訂 21 影響大 1 新規ページ 6",
        )

    def test_uses_generic_fallback_without_overview_or_detail(self) -> None:
        source = monitor_html("""
<div class="t"><a href="/diff/reports/2026-08-12.html">ドキュメント本文の改訂</a></div>
""")

        payload = build_payload(source)

        self.assertEqual(
            payload["summary"],
            "ドキュメントの変更を検知しました。詳細は変更履歴で確認できます。",
        )


if __name__ == "__main__":
    unittest.main()
