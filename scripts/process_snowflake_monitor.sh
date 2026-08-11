#!/usr/bin/env bash
set -euo pipefail

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly TARGET_DIR="${1:-$REPO_ROOT/static/snowflake-monitor}"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Monitor directory not found: $TARGET_DIR" >&2
  exit 1
fi

export MONITOR_HEAD_START='<script>(function(){var t=localStorage.getItem("theme");if(t==="dark"||((!t||t==="system")&&window.matchMedia("(prefers-color-scheme: dark)").matches)){document.documentElement.setAttribute("data-theme","dark");}else{document.documentElement.setAttribute("data-theme","light");}})();</script>
<link rel="stylesheet" href="/css/zenn.css">'
export MONITOR_HEAD_END='<link rel="stylesheet" href="/css/snowflake-monitor-shell.css">
<script src="/js/snowflake-monitor-shell.js" defer></script>
<script src="/js/dark-mode.js" defer></script>
<script src="/js/mobile-nav.js" defer></script>
<script src="/js/search.js" defer></script>
<script src="/js/lang-switcher.js" defer></script>'

while IFS= read -r -d '' html_file; do
  HTML_FILE="$html_file" perl -0pi -e '
    my %month_number = (January => 1, February => 2, March => 3, April => 4, May => 5, June => 6, July => 7, August => 8, September => 9, October => 10, November => 11, December => 12);
    unless (/snowflake-monitor-shell\.js/) {
      s{(<meta name="viewport"[^>]*>)}{$1 . "\n" . $ENV{MONITOR_HEAD_START}}e;
      s{</head>}{$ENV{MONITOR_HEAD_END} . "\n</head>"}e;
    }
    s{href="/features/}{href="/snowflake-monitor/features/}g;
    s{href="/diff/}{href="/snowflake-monitor/diff/}g;
    s{href="/assets/}{href="/snowflake-monitor/assets/}g;
    s{src="/assets/}{src="/snowflake-monitor/assets/}g;
    s{url\("/assets/}{url("/snowflake-monitor/assets/}g;
    s{\s*\@import\s+url\([^;\n]*mplus\.css[^;\n]*\);\s*}{}g;
    s{"M PLUS 1p",\s*}{}g;
    s{<p class="lead">docs\.snowflake\.com.*?Slack に流れた通知の蓄積版です。</p>}{<p class="lead">公式ドキュメントのページ追加・本文変更、新機能、料金表の改定を日付ごとに確認できます。</p>}s;
    s{<p class="lead">Snowflake公式ドキュメントと料金表の更新情報を、日付ごとに確認できます。</p>}{<p class="lead">公式ドキュメントのページ追加・本文変更、新機能、料金表の改定を日付ごとに確認できます。</p>}s;
    s{<footer>.*?</footer>}{}gs;
    s{<p class="lead">本文差分のうち重要度の高いものを時系列で全件並べています。\s*日々の通知を追えなくても、ここだけ見れば重要な変更は拾えます。</p>}{<p class="lead">Snowflake公式ドキュメントから、既存機能への影響が大きい変更と新しく追加されたページをまとめています。</p>}s;
    s{<p class="lead">既存ページの本文が書き換わったもの。<strong>Tier S（破壊的）</strong>と\s*<strong>Tier A（仕様変更）</strong>。</p>}{<p class="lead">既存機能の動作、料金、設定方法に影響する可能性がある変更です。</p>}s;
    s{<p class="lead">新しく追加されたドキュメント。既存の仕様が変わったわけではないので、\s*仕様変更とは分けています（<strong>Tier N</strong>）。</p>}{<p class="lead">Snowflake公式サイトに新しく追加されたページです。既存機能の変更とは分けて掲載しています。</p>}s;
    s{<p class="lead">sitemap\.xml の差分です。現在 <strong>([0-9,]+)</strong> URL を監視しています\s*（削除済み ([0-9,]+)）。</p>}{<p class="lead">Snowflake公式サイトのページ一覧を毎日比較し、新しく追加されたページと削除されたページを記録しています。現在 <strong>$1</strong> ページを監視中です（削除を確認したページは累計 $2 件）。</p>}s;
    s{<p class="lead">Snowflake の課金の一次情報である料金表 PDF の改定履歴です。\s*クレジット単価・Serverless 係数・Cortex のトークン単価はここが正になります。</p>}{<p class="lead">Snowflake公式の料金表 PDF を監視し、改定履歴を掲載しています。クレジット単価、Serverless係数、Cortexのトークン単価を確認できます。</p>}s;
    s{<p>docs\.snowflake\.com の全 [0-9,]+ ページを毎日取得し、本文の改訂を重要度付きで記録しています。</p>}{<p>Snowflake公式ドキュメントを毎日比較し、ページの追加・改訂・削除を日付ごとにまとめています。</p>}s;
    s{(<h1>新機能レポート</h1>)(?!\s*<p class="lead">)}{$1 . "\n<p class=\"lead\">Snowflake公式リリースノートから、新しく公開された機能を日付順にまとめています。</p>"}e;
    s{本文差分レポート}{ドキュメント変更履歴}g;
    s{ドキュメント差分レポート}{ドキュメント変更履歴}g;
    s{重要な変更}{主な変更}g;
    s{破壊的変更・仕様変更}{既存機能に影響する変更}g;
    s{判定根拠: 追加行に「breaking change」}{変更内容: Automatic Clustering の変更説明を追加}g;
    s{判定根拠: 新規ページ}{変更内容: 新しいページを追加}g;
    s{判定根拠: 本文の変更 \(\+(\d+)/-(\d+)\)}{変更内容: 本文を更新（$1行追加・$2行削除）}g;
    s{判定根拠: 変更行数が閾値未満 \(&lt;4\)}{変更内容: 3行以下の小規模な更新}g;
    s{当日のレポート}{変更日の詳細}g;
    s{※ diff は保存上限で切り詰められています}{差分が長いため、途中まで表示しています。}g;
    s{S — 破壊的}{影響の大きい変更}g;
    s{A — 仕様変更}{仕様変更}g;
    s{N — 新規ページ}{新しく追加されたページ}g;
    s{B — 実質更新}{内容の更新}g;
    s{C — 些末}{軽微な更新}g;
    s{S 破壊的}{影響大}g;
    s{A 仕様変更}{仕様変更}g;
    s{N 新規ページ}{新規ページ}g;
    s{B 実質更新}{内容更新}g;
    s{C 些末}{軽微な更新}g;
    s{S (\d+) ・ A (\d+) ・ N (\d+) ・ B (\d+) ・ C (\d+)}{影響大 $1 ・ 仕様変更 $2 ・ 新規ページ $3 ・ 内容更新 $4 ・ 軽微な更新 $5}g;
    s{<span class="chip">\+(\d+)/-(\d+)</span>}{<span class="chip">$1行追加・$2行削除</span>}g;
    s{<div class="k">監視中のページ</div>}{<div class="k">本文を比較したページ数</div>}g;
    s{<div class="m">最終改訂: ([^<]+)</div>}{<div class="m">最終比較: $1</div>}g;
    s{<div class="k">URL（active）</div>}{<div class="k">現在のページ数</div>}g;
    s{<div class="m">削除済み ([0-9,]+)</div>}{<div class="m">削除を確認: $1件</div>}g;
    s{<div class="v" style="font-size:1\.15rem">([^<]+)</div>\s*<div class="m">v([^ <]+) ／ Effective</div>}{<div class="v" style="font-size:1.15rem">適用日: $1</div>\n  <div class="m">料金表 v$2</div>}g;
    s{適用日: (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})}{sprintf("適用日: %04d-%02d-%02d", $3, $month_number{$1}, $2)}ge;
    s{ を筆頭に、}{の変更に加え、}g;
    s{が重なり、変更量・影響度ともに大きい日となった。}{が追加されました。}g;
    s{領域としては「Loading &amp; Unloading Data」と「Migrations」に新規ページが集中しており、ETL レス統合とデータ移行の強化という2つのトレンドが明確に読み取れる。}{新規ページは「Loading &amp; Unloading Data」と「Migrations」の分野に集中しています。}g;
    s{既存ユーザーは直近でのコスト影響の再試算が急務である。}{該当するテーブルを新規作成する場合は、コストへの影響を確認してください。}g;
    s{強制適用}{自動適用}g;
    s{破壊的変更}{影響の大きい変更}g;
    s{データ鮮度と運用コストの両面で大きな恩恵が見込まれる}{データ鮮度の向上と運用コストの削減が見込まれます}g;
    s{開発工数削減に直結する}{開発工数の削減が見込まれます}g;
    s{(<pre\b.*?</pre>)|`([^`<>]+)`}{$1 // "<code>$2</code>"}gse;
    s{\*\*(Automatic Clustering の課金・動作モデル刷新)\*\*}{<strong>$1</strong>}g;
    s{content="noindex, nofollow"}{content="index, follow"}g;
    s{Snowflake 監視ポータル}{Snowflake Doc Monitor}g;
    s{SNOWFLAKE MONITOR}{SNOWFLAKE DOC MONITOR}g;
  ' "$html_file"
done < <(find "$TARGET_DIR" -type f -name '*.html' -print0)

python3 "$REPO_ROOT/scripts/build_snowflake_monitor_summary.py" \
  "$TARGET_DIR/index.html" "$TARGET_DIR/summary.json"

echo "Processed Snowflake monitor HTML in $TARGET_DIR"
