---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ドキュメント系MCPサーバーのコンテキスト使用量を検証し改善した"
subtitle: ""
summary: " "
tags: ["MCP","Claude","LLM","Snowflake"]
categories: ["MCP","LLM"]
url: mcp-server-context-usage-optimization
date: 2026-02-25
featured: false
draft: false

# Featured image
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## はじめに

MCPサーバーはLLMエージェントに外部ツールを提供する仕組みだが、ツールのレスポンスはすべてLLMのコンテキストウィンドウに入る。つまりMCPツールが返すデータ量がそのままコンテキスト消費に直結する。

本記事では、自作のSnowflake Docs MCPサーバーのコンテキスト使用量を実測し、問題点を特定した上で改善を行った過程と結果をまとめる。

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}


## MCPツールのレスポンスとコンテキストの関係

MCPツールの呼び出し結果は、LLMへの入力としてコンテキストウィンドウに載る。

```text
[ユーザーメッセージ] + [システムプロンプト] + [MCPツール結果] + [過去の会話] = コンテキスト消費
```

ドキュメント取得系のMCPツールは、1回の呼び出しで数千〜数万文字を返すことがある。これを意識せずに設計すると、数回の呼び出しでコンテキストの大部分を消費し、会話の継続が困難になる。

### サブエージェント経由の場合

Claude Codeのサブエージェント（Task tool）経由でMCPツールを使う場合、ツールの生レスポンスはサブエージェントのコンテキスト内に留まり、メインには要約のみが返る。これによりメインコンテキストの消費を大幅に削減できる。

| 方式 | メインコンテキスト消費 |
|---|---|
| 直接呼び出し | ツール結果の全文 |
| サブエージェント経由 | 要約のみ（50-90%削減） |

ただしサブエージェントは合計トークン消費量が増え、レイテンシも大きくなるため、すべてをサブエージェント経由にするのは現実的ではない。MCPサーバー側でレスポンスサイズを適切に制御することが重要である。

## 改善前の状態

改善前のサーバーは2つのツールを提供していた。

| ツール | 機能 |
|---|---|
| `search_snowflake_docs` | キーワード検索（excerpt 200文字、最大20件） |
| `get_doc_content` | ページ全文取得（HTML→Markdown変換） |

### 実測結果

CREATE TABLE ページ（Snowflakeで最も大きいページの一つ）を対象に計測した。

**search_snowflake_docs:**

| max_results | レスポンス文字数 | 推定トークン数 |
|---|---|---|
| 3件 | ~850 | ~250 |
| 5件（デフォルト） | ~1,400 | ~400 |
| 10件 | ~2,800 | ~800 |
| 20件（最大） | ~5,500 | ~1,500 |

検索ツールは軽量で問題なし。

**get_doc_content:**

| max_length | レスポンス文字数 | 推定トークン数 | 備考 |
|---|---|---|---|
| 2,000 | ~2,200 | ~600 | |
| 4,000 | ~4,200 | ~1,100 | |
| 8,000（デフォルト） | ~8,200 | ~2,200 | |
| 0（無制限） | **102,079** | **~25,000+** | コンテキスト上限超過 |

### 発見された問題

**1. テキスト重複バグ**

HTML→Markdown変換に `descendants` イテレータを使っていたため、`<li>` 内の `<p>` で同じテキストが2回出力されていた。

```text
- Requires a value (NOT NULL).
Requires a value (NOT NULL).          ← 重複

- Has a default value.
Has a default value.                  ← 重複
```

リスト10項目が20行に膨張し、**コンテンツの30-40%が無駄な重複**に消費されていた。

**2. max_length=0 でコンテキスト破綻**

CREATE TABLEページを無制限取得すると102,079文字が返り、Claude Codeのトークン上限を超えてファイルに退避された。ファイル退避されるとコンテキスト内で直接参照できなくなり、実質的に使い物にならない。

**3. セクション指定取得ができない**

ページの先頭から `max_length` 分だけ切り取る方式のため、Usage NotesやExamplesなどページ後半にある重要情報に到達できなかった。

**4. ページ構造の確認手段がない**

どんなセクションがあるかを知るためにも `get_doc_content` で全文取得する必要があった。

**5. Markdown出力のノイズ**

HTML→Markdown変換後に、LLMにとって不要なアーティファクトが多数残留していた。

```text
## Usage notes[¶](#usage-notes "Link to this heading")     ← pilcrowリンク（~40 chars/見出し）
Copy                                                        ← コピーボタンの残骸
[COPY INTO <table>](copy-into-table)                        ← 辿れない相対リンク
```

CREATE TABLEページ（24見出し）だけでpilcrowリンクに約960文字が消費されていた。

## 改善の過程

### AWS公式MCPサーバーの調査

改善の参考として、AWSが公式に提供しているドキュメントMCPサーバーの実装を調査した。参考になった設計ポイントは以下の通り。

- **markdownifyライブラリの使用**: 手書きのHTMLパーサーではなく `markdownify` ライブラリでHTML→Markdown変換を行っており、重複バグのような問題は構造的に発生しない
- **start_indexによるページネーション**: 長文ドキュメントを `start_index` パラメータで分割読み込みする設計
- **max_lengthの安全な制約**: Pydantic Fieldで `gt=0, lt=1000000` の制約をかけ、0（無制限）を入力できないようにしている
- **instructionsへのベストプラクティス記載**: 「30,000文字超のドキュメントは、必要な情報が見つかった時点で読み込みを止めること」と明記

### 取り組み1: HTML→Markdown変換の品質改善

手書きの `descendants` ループを `markdownify` ライブラリに置き換えた。これによりテキスト重複バグが解消され、同じ文字数でも実効的に約1.5倍の情報量を含むようになった。

さらに、Markdown変換後のノイズ除去を実装した。

- pilcrowリンク（`[¶](...)`）の除去
- コピーボタンの残骸（`Copy`）の除去
- リンクURLの除去（テキストのみ保持）
- 画像・SVGタグの除去
- フィードバック・評価・アンケート・フォーム要素の除去

ポイントは除去の段階を分けている点。ボタンや画像はHTML段階で `decompose()` し、pilcrowやCopyの残骸はMarkdown変換後にテキストレベルで除去する。`<a>` タグは `unwrap()` でタグだけ除去しテキストは保持する。

### 取り組み2: 段階的な情報取得の導入

2つだったツールを5つに増やし、段階的な情報取得を可能にした。

```text
search_snowflake_docs  → ドキュメント検索（include_headings=Trueで目次も同時取得可能）
search_in_doc          → ページ内キーワード検索（関連セクション自動選択）
get_doc_toc            → ページの目次取得（軽量）
get_doc_section        → 特定セクションの取得
get_doc_content        → ページ全文の取得（ページネーション対応）
```

推奨される使い方の流れ。

```text
1. search_snowflake_docs(include_headings=True) で検索+目次を1回で取得
2. search_in_doc で関連セクションだけ自動抽出
3. コード例が必要な場合のみ include_code_blocks=True を指定
```

### 取り組み3: レスポンスサイズの制御

`max_length` のハードキャップを設け、コンテキスト破綻を防止した。

| max_length の値 | 挙動 |
|---|---|
| 0 | 全文取得の意図を尊重し、ハードキャップ(20,000)まで返す |
| 1〜20,000 | 指定値そのまま |
| 20,001以上 | 20,000にキャップ |
| 負値 | デフォルト(5,000)にフォールバック |

加えて `start_index` パラメータによるページネーション、自然な位置での境界切断（段落→行→文→単語の優先度）を導入した。

### 取り組み4: コードブロックのデフォルトOFF

構文リファレンスページではコードブロックがコンテキストの大半を占める。CREATE TABLEページで計測した結果、コードブロックを除去すると **37.7%のコンテキスト削減** が得られた。

| モード | サイズ | 削減率 |
|---|---|---|
| コードブロックON | 52,694 chars | - |
| コードブロックOFF | 32,851 chars | 37.7% |

`include_code_blocks` パラメータのデフォルト値を `False` に変更し、構文やコード例が必要な場合のみ明示的に指定する運用にした。

### 取り組み5: ツール呼び出し回数の削減

`search_snowflake_docs` に `include_headings` パラメータを追加し、検索と同時にページの見出し構造を取得できるようにした。

```text
改善前: search → get_doc_toc → get_doc_section  (3回)
改善後: search(include_headings=True) → get_doc_section  (2回)
```

ただし見出しの多いページ（120件以上の見出しを持つDB2移行ガイド等）でレスポンスが膨張する問題があったため、1結果あたり30見出し上限のキャップを設けた。超過時はh1-h3のみに絞り込む。

### 取り組み6: ページ内キーワード検索

`search_in_doc` ツールを追加した。URLとキーワードを渡すと、ページ内の全セクションをスコアリングし、関連度の高いセクションだけを返す。これにより目次確認→セクション選択の判断をMCPサーバー側で行えるようになった。

スコアリング精度の問題として、親セクションの `get_text()` が子セクションのテキストを全て含むため常に親のスコアが高くなる問題があった。子セクションのテキストを親スコアから除外し、ネスト重複排除を行うことで解決した。

### 取り組み7: キャッシュとパフォーマンス改善

- 同一URLへの重複HTTPフェッチを排除するTTL付きインメモリキャッシュ（5分、LRU 50エントリ上限）
- buildIdキャッシュ（1時間TTL）
- 共有HTTPクライアントによるコネクションプーリング
- `asyncio.gather` による並列headings取得

## 改善結果

### get_doc_content 全文取得の比較

CREATE TABLEページを `get_doc_content(include_code_blocks=False)` で全文取得した比較。

| 条件 | 改善前 | 改善後 | 備考 |
|---|---|---|---|
| max_length=2000 | ~2,200 chars（30-40%が重複） | 2,269 chars（重複なし） | 同文字数で情報量約1.5倍 |
| max_length=5000 | — | 5,351 chars | 改善後のデフォルト |
| max_length=8000 | ~8,200 chars（30-40%が重複） | 8,450 chars（重複なし） | 改善前のデフォルト |
| max_length=0 | **102,079 chars（破綻）** | **20,000以下（安全）** | 95%以上削減 |

### 複数ページでの全文取得比較

CREATE TABLE以外のページでも同様の効果があるかを検証した。

| ページ | 改善前 | 改善後 | 削減率 |
|---|---|---|---|
| CREATE TABLE（大規模SQLリファレンス） | 70,948 chars | 44,503 chars | **37.3%** |
| SELECT（大規模SQLリファレンス） | 25,068 chars | 10,538 chars | **58.0%** |
| Dynamic Tables（中規模ガイド） | 5,409 chars | 4,529 chars | **16.3%** |
| **合計** | **101,425 chars** | **59,570 chars** | **41.3%** |

リンクの多いリファレンスページほど効果が大きく、SELECTページでは58%の大幅な削減を達成した。小規模ガイドページでは削減率が比較的小さいが、元々のサイズが小さいため実用上の影響は少ない。

### 典型的な使用パターンの比較

| パターン | 改善前 | 改善後 | 改善 |
|---|---|---|---|
| search + get_doc_content | ~9,600 chars | 7,378 chars | 23%削減 |
| search + 2x get_doc_content | ~17,800 chars | 12,714 chars | 29%削減 |
| search + TOC + 1 section | 不可能 | 9,408 chars | 新機能 |
| search(headings) + section(code=OFF) | 不可能 | 3,115 chars | **最適フロー** |
| Usage Notes だけ欲しい | 不可能（到達できない） | 5,267 chars | 新機能 |

最も効率的なフロー（`search(max_results=1, include_headings=True)` → `get_doc_section(code=OFF)`）で、改善前の典型フローと比べて約58%のコンテキスト削減を達成した。

### 新ツールのコンテキスト消費

| ツール | 消費量 | 用途 |
|---|---|---|
| `search_snowflake_docs`（3件） | ~850 chars | 検索結果のみ |
| `get_doc_toc` | ~600 chars | ページ構造の確認 |
| `get_doc_section`（1セクション） | ~528 chars | 特定セクションの取得 |
| `search_in_doc`（3セクション） | ~2,400 chars | 関連セクション自動抽出 |
| `get_doc_content`（全文、code=OFF） | ~44,503 chars | ページ全体 |

`search_in_doc` で必要なセクションだけ取得すれば、`get_doc_content` 全文の約9分の1のコンテキストで済む。

### include_headings の影響

| パターン | 推定文字数 |
|---|---|
| search（5件、headings=false） | ~500文字 |
| search（5件、headings=true） | ~3,500〜5,000文字 |

`include_headings=true` にすると約7〜10倍のコンテキストを消費するが、`get_doc_toc` の呼び出しを省略できる。見出しキャップ導入前は見出しの多いページで26,443文字以上に膨張していたが、導入後は10,853文字以内に収まるようになった（**59%削減**）。

## ドキュメント系MCPサーバー設計のポイント

今回の改善で得られた知見をまとめる。

1. **レスポンスサイズにハードキャップを設ける** — 無制限取得はコンテキスト破綻のリスクがある
2. **ページネーションを提供する** — `start_index` + `max_length` で分割読み込みできるようにする
3. **段階的な情報取得を可能にする** — 検索 → 目次確認（軽量） → セクション取得（必要な部分だけ）
4. **HTML→Markdown変換にはライブラリを使う** — 手書きのHTMLパーサーはバグの温床になる
5. **instructionsにベストプラクティスを記載する** — LLMがツールをどう使うべきかのガイドをサーバー側から提供する
6. **ツール呼び出し回数を削減する** — 複数のツール呼び出しを1回にまとめるオプションを提供する
7. **コードブロックをデフォルトで除外する** — 構文リファレンスではコードブロックがレスポンスの30〜40%を占める
8. **HTTP重複フェッチをキャッシュで排除する** — 同一URLへの連続アクセスは頻発する
9. **Markdown出力のノイズを除去する** — pilcrowリンク、コピーボタン、リンクURL、画像タグ等を除去する
10. **大量データを返すパラメータに安全弁を設ける** — 見出しキャップのような上限を設ける

## まとめ

自作のSnowflake Docs MCPサーバーのコンテキスト使用量を実測し、以下の改善を行った。

| 改善 | 効果 |
|---|---|
| HTML→Markdown変換の品質改善 | テキスト重複解消、ノイズ除去で全文取得時 **平均41.3%削減** |
| 段階的な情報取得の導入 | 必要なセクションだけ取得で全文の **約9分の1** |
| コードブロックのデフォルトOFF | **37.7%削減** |
| ツール呼び出し回数の削減 | 3ステップ → 2ステップ |
| レスポンスサイズの制御 | 102,079 chars → **20,000以下**（破綻防止） |
| 最適フロー全体 | **約58%のコンテキスト削減** |

MCPサーバーを設計する際は、レスポンスのサイズ = LLMのコンテキスト消費であることを意識し、「必要な情報だけを、必要な分だけ、ノイズなく返す」設計にすることが重要である。

## 関連記事

{{< linkcard url="https://zatoima.github.io/snowflake-docs-mcp-server-architecture/" title="Snowflakeドキュメント検索MCPサーバーを作成した" description="MCPサーバーの技術的な仕組み（Next.jsのbuildId取得、検索API、HTML→Markdown変換）" >}}

{{< linkcard url="https://zatoima.github.io/snowflake-mcp-documentation-server-benchmark/" title="Snowflake MCPドキュメントサーバー2種のベンチマーク比較" description="本MCPサーバーとCortex Agent + CKEベースのMCPサーバーを20クエリ・5評価軸で比較" >}}

## 参考資料

{{< linkcard "https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server" >}}

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}

{{< linkcard "https://pypi.org/project/markdownify/" >}}
