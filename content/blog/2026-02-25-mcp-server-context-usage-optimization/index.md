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

本記事では、自作のSnowflake Docs MCPサーバーのコンテキスト使用量を実測し、問題点を特定した上で、AWS公式のドキュメントMCPサーバーの実装を参考に改善を行った。改善前後の具体的な数値比較と、ドキュメント系MCPサーバー設計のポイントをまとめる。

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

## 改善前のSnowflake Docs MCPサーバー（v0.1.0）

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

#### 1. テキスト重複バグ

HTML→Markdown変換に `descendants` イテレータを使っていたため、`<li>` 内の `<p>` で同じテキストが2回出力されていた。

```text
- Requires a value (NOT NULL).
Requires a value (NOT NULL).          ← 重複

- Has a default value.
Has a default value.                  ← 重複
```

リスト10項目が20行に膨張し、**コンテンツの30-40%が無駄な重複**に消費されていた。

原因はBeautifulSoupの `descendants` が全ネスト要素を走査するため、`<li>` ハンドラと `<p>` ハンドラの両方が同じテキストに対して発火していたこと。

#### 2. max_length=0 でコンテキスト破綻

CREATE TABLEページを無制限取得すると102,079文字が返り、Claude Codeのトークン上限を超えてファイルに退避された。ファイル退避されるとコンテキスト内で直接参照できなくなり、実質的に使い物にならない。

#### 3. セクション指定取得ができない

ページの先頭から `max_length` 分だけ切り取る方式のため、Usage NotesやExamplesなどページ後半にある重要情報に到達できなかった。

#### 4. ページ構造の確認手段がない

どんなセクションがあるかを知るためにも `get_doc_content` で全文取得する必要があった。

## AWS Documentation MCPサーバーの実装調査

改善の参考として、AWSが公式に提供しているドキュメントMCPサーバーの実装を調査した。

### アーキテクチャ

AWSのサーバーは3つのツールを提供している。

| ツール | 機能 |
|---|---|
| `read_documentation` | ページ取得（ページネーション対応） |
| `search_documentation` | 検索（公式Search API使用） |
| `recommend` | 関連コンテンツ推薦 |

### 参考になった設計ポイント

**1. markdownifyライブラリの使用**

手書きのHTMLパーサーではなく、`markdownify` ライブラリでHTML→Markdown変換を行っている。これにより重複バグのような問題は構造的に発生しない。

```python
content = markdownify.markdownify(
    str(main_content),
    heading_style=markdownify.ATX,
    strip=tags_to_strip,
)
```

**2. start_indexによるページネーション**

長文ドキュメントを一度に全文返すのではなく、`start_index` パラメータで分割読み込みする設計。

```python
async def read_documentation(
    url: str,
    max_length: int = 5000,     # デフォルト5000
    start_index: int = 0,       # 読み込み開始位置
) -> str:
```

instructions には「30,000文字超のドキュメントは、必要な情報が見つかった時点で読み込みを止めること」と明記されている。

**3. max_lengthの安全な制約**

Pydantic Fieldで `gt=0, lt=1000000` の制約をかけ、0（無制限）を入力できないようにしている。

## 改善後のSnowflake Docs MCPサーバー（v0.2.0）

上記の調査を踏まえ、以下の改善を実施した。

### 変更一覧

| 変更 | 内容 |
|---|---|
| HTML→Markdown変換 | 手書き `descendants` ループ → `markdownify` ライブラリ |
| デフォルト max_length | 8000 → 5000（重複解消で情報密度向上） |
| max_length=0 | 無制限 → ハードキャップ(20000)まで |
| ページネーション | `start_index` パラメータ追加 |
| 新ツール: `get_doc_toc` | ページ見出し構造の軽量取得 |
| 新ツール: `get_doc_section` | 特定セクションのみ取得 |

### ツール構成

改善後は4つのツールを提供する。

```text
search_snowflake_docs  → ドキュメント検索
get_doc_toc            → ページの目次取得（軽量）
get_doc_section        → 特定セクションの取得
get_doc_content        → ページ全文の取得（ページネーション対応）
```

推奨される使い方は以下の流れ。

```text
1. search_snowflake_docs で検索
2. get_doc_toc でページ構造を確認（軽量）
3. get_doc_section で必要なセクションだけ取得
4. 全文が必要な場合のみ get_doc_content（start_index で分割読み込み）
```

### 主要な実装

**_clamp_max_length:**

```python
def _clamp_max_length(max_length: int) -> int:
    if max_length < 0:
        return DEFAULT_MAX_CONTENT_LENGTH  # 5000
    if max_length == 0:
        return MAX_CONTENT_LENGTH_HARD_CAP  # 20000
    return min(max_length, MAX_CONTENT_LENGTH_HARD_CAP)
```

| max_length の値 | 挙動 |
|---|---|
| 0 | 全文取得の意図を尊重し、ハードキャップ(20,000)まで返す |
| 1〜20,000 | 指定値そのまま |
| 20,001以上 | 20,000にキャップ |
| 負値 | デフォルト(5,000)にフォールバック |

**get_doc_content のページネーション:**

```python
@mcp.tool()
async def get_doc_content(
    url: str,
    include_code_blocks: bool = True,
    max_length: int = 5000,
    start_index: int = 0,
) -> dict:
```

レスポンスに `total_length` と `next_start_index` を含め、続きの取得を容易にしている。

## 改善前後のコンテキスト使用量比較

### テキスト品質の改善

同じ `max_length=2000` で取得した CREATE TABLE ページのリスト部分：

**旧版（v0.1.0）— 20行:**

```text
- Requires a value (NOT NULL).
Requires a value (NOT NULL).

- Has a default value.
Has a default value.

- CREATE OR ALTER TABLE (creates a table if ...)
CREATE OR ALTER TABLE (creates a table if ...)
```

**新版（v0.2.0）— 10行:**

```text
* Requires a value (NOT NULL).
* Has a default value.
* CREATE OR ALTER TABLE (creates a table if ...)
```

同じ文字数でも、新版は重複がないため実効的に約1.5倍の情報量を含む。

### get_doc_content の比較

| 条件 | 旧版 JSON chars | 新版 JSON chars | 備考 |
|---|---|---|---|
| max_length=2000 | ~2,200 | 2,269 | 新版は重複なしで情報量2倍 |
| max_length=5000（新デフォルト） | — | 5,351 | 新デフォルト |
| max_length=8000（旧デフォルト） | ~8,200 | 8,450 | 旧版は30-40%が重複 |
| max_length=0 | **102,079（破綻）** | **20,000以下（安全）** | 95%以上削減 |

### 新ツールのコンテキスト消費

| ツール | JSON chars | ~tokens | 用途 |
|---|---|---|---|
| `get_doc_toc` (CREATE TABLE) | 2,114 | ~528 | 24見出しの目次 |
| `get_doc_toc` (SHOW TABLES) | 454 | ~113 | 6見出しの目次 |
| `get_doc_section` (syntax) | 3,883 | ~970 | Syntaxセクションのみ |
| `get_doc_section` (usage-notes) | 5,267 | ~1,316 | Usage Notesのみ |
| `get_doc_section` (required-parameters) | 2,585 | ~646 | 必須パラメータのみ |

`get_doc_toc` は500トークン前後で済むため、気軽に呼び出せる。

### 典型的な使用パターンの比較

| パターン | 旧版 chars | 新版 chars | 改善 |
|---|---|---|---|
| search + get_doc_content | ~9,600 | 7,378 | 23%削減 |
| search + 2x get_doc_content | ~17,800 | 12,714 | 29%削減 |
| search + TOC + 1 section | — | 9,408 | 新機能 |
| search + TOC + 2 sections | — | 13,291 | 新機能 |
| Usage Notes だけ欲しい | 不可能 | 5,267 | 新機能 |

特にページ後半のセクション（Usage Notes、Examples）だけが必要な場合、旧版では到達不可能だったが、新版では `get_doc_section` で直接取得できるようになった。

## さらなる最適化（v0.3.0）

v0.2.0で段階的な情報取得が可能になったが、実際にClaude Codeで使っていると、典型的な使用パターン（`search` → `get_doc_toc` → `get_doc_section`）で3回のツール呼び出しが必要であり、ツール呼び出し回数の多さとHTTPフェッチの重複が気になった。

v0.3.0ではコンテキスト消費をさらに削減するため、以下の4つの改善を実施した。

### 変更一覧

| 変更 | 内容 |
|---|---|
| レスポンスキャッシュ | `_fetch_and_parse_page` にTTL付きインメモリキャッシュ（5分）を追加 |
| 検索結果にheadings付与 | `search_snowflake_docs` に `include_headings` パラメータを追加 |
| コードブロックのデフォルトOFF | `include_code_blocks` のデフォルトを `True` → `False` に変更 |
| 新ツール: `search_in_doc` | ページ内キーワード検索で関連セクションを自動選択 |

### ツール構成

v0.3.0では5つのツールを提供する。

```text
search_snowflake_docs  → ドキュメント検索（include_headings=Trueで目次も同時取得可能）
search_in_doc          → ページ内キーワード検索（関連セクション自動選択）
get_doc_toc            → ページの目次取得（軽量）
get_doc_section        → 特定セクションの取得
get_doc_content        → ページ全文の取得（ページネーション対応）
```

### 改善1: レスポンスキャッシュ

同一URLへの重複HTTPフェッチを排除するため、パース済みHTMLのインメモリキャッシュを導入した。

```python
_CACHE_TTL = 300  # 5分
_page_cache: dict[str, tuple[float, str, Tag]] = {}

async def _fetch_and_parse_page(url: str) -> dict | tuple[str, Tag]:
    now = time.monotonic()
    if url in _page_cache:
        cached_at, cached_title, cached_content = _page_cache[url]
        if now - cached_at < _CACHE_TTL:
            return (cached_title, copy.copy(cached_content))
        else:
            del _page_cache[url]
    # ... HTTPフェッチ・パース処理 ...
    _page_cache[url] = (now, title, main_content)
    return (title, copy.copy(main_content))
```

BeautifulSoupの `Tag` オブジェクトは `decompose()` で破壊的に変更されるため、キャッシュから返す際は `copy.copy()` でコピーを返す点がポイントである。

これにより `search` → `get_doc_toc` → `get_doc_section` の流れで同じページを3回フェッチしていた問題が解消され、初回のみHTTPアクセスし、以降はキャッシュから返すようになった。

### 改善2: 検索結果にheadings付与

`search_snowflake_docs` に `include_headings` パラメータを追加し、検索と同時にページの見出し構造を取得できるようにした。

```python
@mcp.tool()
async def search_snowflake_docs(
    query: str,
    max_results: int = 5,
    language: str = "en",
    include_headings: bool = False,  # 追加
) -> dict:
```

`include_headings=True` を指定すると、各検索結果に `headings` フィールドが追加される。これにより `get_doc_toc` の呼び出しを省略でき、3ステップから2ステップに削減できる。

```text
改善前: search → get_doc_toc → get_doc_section  (3回)
改善後: search(include_headings=True) → get_doc_section  (2回)
```

heading抽出ロジックは `_extract_headings()` として共通関数化し、`get_doc_toc` からも利用するようにした。

### 改善3: コードブロックのデフォルトOFF

構文リファレンスページではコードブロックがコンテキストの大半を占める。CREATE TABLEページで計測した結果、コードブロックを除去すると **37.7%のコンテキスト削減** が得られた。

| モード | サイズ | 削減率 |
|---|---|---|
| コードブロックON | 52,694 chars | - |
| コードブロックOFF | 32,851 chars | 37.7% |

`get_doc_content`、`get_doc_section`、`search_in_doc` の `include_code_blocks` パラメータのデフォルト値を `True` → `False` に変更した。構文やコード例が必要な場合のみ `include_code_blocks=True` を明示的に指定する運用とした。

実装上の注意点として、`markdownify` の `strip` パラメータでは `pre` / `code` タグの書式を除去するだけでテキスト内容は残ってしまう。HTML段階で `decompose()` して要素ごと除去する必要がある。

```python
def _convert_to_markdown(tag: Tag, include_code_blocks: bool = True) -> str:
    if not include_code_blocks:
        tag = copy.copy(tag)
        for code_tag in tag.find_all(["pre", "code"]):
            code_tag.decompose()
    # ...
```

### 改善4: search_in_doc（ページ内キーワード検索）

新ツール `search_in_doc` を追加した。URLとキーワードを渡すと、ページ内の全セクションをスコアリングし、関連度の高いセクションだけを返す。

```python
@mcp.tool()
async def search_in_doc(
    url: str,
    query: str,
    max_sections: int = 3,
    include_code_blocks: bool = False,
    max_length: int = 5000,
) -> dict:
```

スコアリングロジックは以下の通り。

- クエリを空白で分割しキーワードリスト化
- 各セクションについて:
  - 見出しにキーワードが含まれる → +10点
  - 本文にキーワードが含まれる → 出現回数に応じて+1点ずつ
- 大文字小文字は区別しない
- スコア上位N件のセクション内容を合計 `max_length` 以内で返す

これにより `get_doc_toc` で目次を確認してセクションを選ぶ判断をMCPサーバー側で行い、1回の呼び出しで関連セクションだけを返せるようになった。

## v0.2.0 → v0.3.0 のコンテキスト消費比較

CREATE TABLEページで、典型的な使用フローごとのコンテキスト消費を比較した。

### フロー別比較

| フロー | ツール回数 | HTTP回数 | コンテキスト | 削減率 |
|---|---|---|---|---|
| v0.2.0: search → toc → section(code=ON) | 3回 | 3回 | 7,407 chars | - |
| v0.3.0 A: search(1件,headings) → section(code=OFF) | 2回 | 1回+cache | 3,115 chars | **57.9%** |
| v0.3.0 B: search → search_in_doc | 2回 | 1回+cache | 7,133 chars | 3.7% |
| v0.3.0 C: search_in_doc のみ (URL既知) | 1回 | 1回 | 5,408 chars | **27.0%** |

最も効率的なのはフローA（`search(max_results=1, include_headings=True)` → `get_doc_section(code=OFF)`）で、約58%のコンテキスト削減を達成した。

`include_headings=True` で検索件数が多い場合（5件以上）は、全件のTOCを取得するためかえってレスポンスが膨張する点に注意が必要である。`max_results=1` と組み合わせるのが効果的。

## さらなる最適化（v0.4.0）— コンテキスト品質の改善

v0.3.0までは「返すデータ量をどう制御するか」が焦点だったが、v0.4.0では「返すデータの品質をどう高めるか」にフォーカスした。同じ文字数でもLLMにとって有用な情報の割合を上げることで、実効的なコンテキスト効率を改善する。

Claude Codeに包括的テストを実行させ、コンテキスト使用量を計測・分析した結果、以下の問題を特定した。

### 発見された問題

#### 1. Markdownの出力ノイズ

`markdownify` によるHTML→Markdown変換後に、LLMにとって不要なアーティファクトが多数残留していた。

```text
## Usage notes[¶](#usage-notes "Link to this heading")     ← pilcrowリンク（~40 chars/見出し）
Copy                                                        ← コピーボタンの残骸
[COPY INTO <table>](copy-into-table)                        ← 辿れない相対リンク
```

CREATE TABLEページ（24見出し）だけでpilcrowリンクに約960文字が消費されていた。

#### 2. include_headings=True のコンテキスト爆発

`search_snowflake_docs(query="CREATE TABLE", max_results=5, include_headings=True)` を実行すると、SnowConvertの移行ガイドページ（DB2、Sybase、BigQuery、PostgreSQL）が各100件以上の見出しを持っており、レスポンス全体が26,443文字以上に膨張していた。

#### 3. search_in_doc のスコアリング精度

`search_in_doc(url, "CTAS examples")` で「CTAS examples」セクションを探すと、親の「create-table」セクションが最高スコアになっていた。親セクションの `get_text()` が子セクションのテキストを全て含むため、常に親のスコアが高くなる構造的な問題があった。

#### 4. 文字列の途中切断

`max_length` での切断が文字位置ベースのため、単語やMarkdownの構造の途中で切れることがあった。

### 変更一覧

| 変更 | 内容 |
|---|---|
| Markdown出力クリーンアップ | pilcrowリンク除去、Copyボタン残骸除去、リンクURL除去（テキストのみ保持）、画像・SVG除去 |
| HTMLノイズ除去 | フィードバック・評価・アンケート・ページネーション・フォーム要素をパース段階で除去 |
| 見出し数キャップ | `include_headings=True` 時、1結果あたり30見出し上限（超過時はh1-h3のみ） |
| スコアリング改善 | 子セクションのテキストを親スコアから除外 + ネスト重複排除 |
| 境界切断 | 段落→行→文→単語の優先度で自然な位置で切断 |
| キャッシュLRU | 50エントリ上限で最古エントリを削除 |
| buildIdキャッシュ | 1時間TTLでbuildIdを保持、stale時は自動リトライ |
| 共有HTTPクライアント | コネクションプーリングによりTCPハンドシェイクを削減 |
| 並列headings取得 | `asyncio.gather` でinclude_headings時のページフェッチを並列化 |
| レスポンスメタデータ | `get_doc_section` に `content_length`、`search_in_doc` に `total_content_chars` 追加 |

### 主要な実装

**Markdown出力クリーンアップ:**

```python
def _convert_to_markdown(tag: Tag, include_code_blocks: bool = True) -> str:
    tag = copy.copy(tag)

    # コピーボタンのアーティファクトを除去
    for btn in tag.find_all("button", class_=re.compile(r"(copy|clipboard)", re.I)):
        btn.decompose()

    # リンクURLを除去してテキストのみ保持（トークン節約）
    for a_tag in tag.find_all("a"):
        a_tag.unwrap()

    # 画像・SVGを除去（LLMには不要）
    for img_tag in tag.find_all(["img", "svg"]):
        img_tag.decompose()

    content = markdownify.markdownify(str(tag), ...)

    # pilcrowリンクを除去
    content = re.sub(r'\[¶\]\([^)]*\)', '', content)
    content = re.sub(r'\s*¶', '', content)
    content = content.replace('\nCopy\n', '\n')
    # ...
```

ポイントは除去の段階を分けている点。ボタンや画像はHTML段階で `decompose()` し、pilcrowやCopyの残骸はMarkdown変換後にテキストレベルで除去する。`<a>` タグは `unwrap()` でタグだけ除去しテキストは保持する。

**見出し数キャップ:**

```python
_MAX_HEADINGS_PER_RESULT = 30

async def _fetch_headings_for_result(url: str) -> list[dict]:
    headings = _extract_headings(main_content)
    if len(headings) > _MAX_HEADINGS_PER_RESULT:
        headings = [h for h in headings if h["level"] <= 3][:_MAX_HEADINGS_PER_RESULT]
    return headings
```

30件以内のページはそのまま全見出しを返し、超過する巨大ページではh1-h3に絞り込む。これにより主要セクションの目次は維持しつつ、DB2ページのような120件超の見出しによる爆発を防止する。

**スコアリング改善（子セクション除外 + 重複排除）:**

```python
def _score_section(section_tag: Tag, keywords: list[str]) -> tuple[int, str]:
    # ネストされた子sectionのテキストを除外して、直接コンテンツのみ取得
    direct_parts: list[str] = []
    for child in section_tag.children:
        if isinstance(child, Tag) and child.name == "section":
            continue  # 子セクションはスキップ
        text = child.get_text(separator=" ", strip=True) if isinstance(child, Tag) else str(child).strip()
        if text:
            direct_parts.append(text)
    section_text = " ".join(direct_parts).lower()
    # ...
```

加えて `_deduplicate_sections` で親子両方がスコア上位に入った場合の重複も排除する。

**境界切断:**

```python
def _truncate_at_boundary(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    search_start = max(0, max_length - 200)
    region = text[search_start:max_length]

    # 優先度1: 段落区切り（\n\n）
    pos = region.rfind('\n\n')
    if pos != -1:
        return text[:search_start + pos].rstrip()
    # 優先度2: 行区切り → 優先度3: 文末 → 優先度4: スペース → フォールバック
```

末尾200文字以内で最も自然な切断点を探す。Markdownの段落境界を最優先とし、それがなければ行→文→単語の順で切断位置を決定する。

### 計測結果

CREATE TABLEページで計測した。

**Markdown出力サイズの比較（コードブロック除外時）:**

| バージョン | 文字数 | v0.3.0比 |
|---|---|---|
| v0.3.0 | 52,694 chars | - |
| v0.4.0 | 44,503 chars | **-15.5%** |

同じページ、同じ条件（コードブロック除外）でも、ノイズ除去により約8,200文字（15.5%）の削減が得られた。これはpilcrowリンク、コピーボタン、リンクURL、画像タグ、フィードバックフォームなど、LLMにとって価値のない要素を除去した結果である。

**include_headings のコンテキスト消費:**

| 条件 | v0.3.0 | v0.4.0 | 改善 |
|---|---|---|---|
| `search(5件, headings=True)` "CREATE TABLE" | 26,443+ chars | 10,853 chars | **59%削減** |
| DB2ページの見出し数 | 120+件 | 30件（h1-h3のみ） | **75%削減** |
| `search(2件, headings=True)` | — | 4,628 chars | 安全な範囲 |

5件検索+見出し付きという最悪ケースでも、キャップにより10,853文字に収まるようになった。

**search_in_doc のスコアリング精度:**

| クエリ | v0.3.0 トップマッチ | v0.4.0 トップマッチ |
|---|---|---|
| "CTAS examples" | `create-table`（親セクション全体） | `ctas-examples`（正確なサブセクション） |
| "usage notes" | `usage-notes` | `usage-notes`（変化なし） |

子セクション除外とネスト重複排除により、具体的なクエリが適切なサブセクションにマッチするようになった。

**ツール別コンテキスト消費（v0.4.0）:**

| ツール | 文字数 | 用途 |
|---|---|---|
| `search_snowflake_docs(3件)` | ~850 | 検索結果のみ |
| `get_doc_toc` | 2,114 | 24見出しの目次 |
| `get_doc_section(usage-notes)` | 4,913 | 特定セクション |
| `search_in_doc(usage notes)` | 4,913 | 自動セクション選択 |
| `get_doc_content(code=OFF)` | 44,503（全文） | ページ全体 |
| `get_doc_content(code=ON)` | 64,413（全文） | コード含むページ全体 |

`search_in_doc` で必要なセクションだけ取得すれば `get_doc_content` 全文の **約9分の1** のコンテキストで済む。

### 複数ページでのコンテキスト節約（v0.3.0比）

CREATE TABLE以外のページでも同様の効果があるかを検証するため、3つの異なるタイプのページで `get_doc_content(include_code_blocks=False)` の全文取得を比較した。

| ページ | v0.3.0相当 | v0.4.0 | 節約 | 削減率 |
|---|---|---|---|---|
| CREATE TABLE（大規模SQLリファレンス） | 70,948 chars | 44,503 chars | 26,445 chars | **37.3%** |
| Dynamic Tables（中規模ガイド） | 5,409 chars | 4,529 chars | 880 chars | **16.3%** |
| SELECT（大規模SQLリファレンス） | 25,068 chars | 10,538 chars | 14,530 chars | **58.0%** |
| **合計** | **101,425 chars** | **59,570 chars** | **41,855 chars** | **41.3%** |

ページの種類やサイズに関わらず、一貫してコンテキスト削減が得られた。特にSELECTページでは58%の大幅な削減を達成している。これはリンクURLやナビゲーション要素の比率がページによって異なるためで、リンクの多いリファレンスページほど効果が大きい。

Dynamic Tablesのような小規模ガイドページでは削減率が16.3%と比較的小さいが、元々のサイズが小さいため実用上の影響は少ない。

### テスト結果

ユニットテスト（59件）と統合テスト（96件）の合計156テストが全合格。

| カテゴリ | テスト数 | 結果 |
|---|---|---|
| **Part A: ユニットテスト（ネットワーク不要）** | | |
| _clamp_max_length | 7 | 全合格 |
| _truncate_at_boundary（段落/行/文/スペース/フォールバック） | 9 | 全合格 |
| _is_valid_snowflake_url | 9 | 全合格 |
| _strip_noise_elements（nav/footer/aside/feedback/form等） | 13 | 全合格 |
| _convert_to_markdown（リンク/画像/SVG/pilcrow/コード除去） | 11 | 全合格 |
| _score_section（直接テキストスコアリング） | 4 | 全合格 |
| _deduplicate_sections（親子重複排除） | 6 | 全合格 |
| _has_ancestor_in_set | 5 | 全合格 |
| _extract_headings | 5 | 全合格 |
| **Part B: 統合テスト（実ネットワーク使用）** | | |
| buildIdキャッシュ（TTL/ヒット/日本語） | 7 | 全合格 |
| httpx.AsyncClient再利用 | 3 | 全合格 |
| コンテキスト節約の定量検証（3ページ × 7項目） | 23 | 全合格 |
| ページネーション連続性 | 4 | 全合格 |
| search_snowflake_docs（英語/日本語/headings） | 10 | 全合格 |
| get_doc_content（基本/max_length=0/start_index超過/エラー） | 9 | 全合格 |
| get_doc_toc（3ページ × 構造検証） | 6 | 全合格 |
| get_doc_section（基本/max_length制限/コードON/OFF/エラー） | 6 | 全合格 |
| search_in_doc（基本/構造/スコア/max_length/空クエリ/マッチなし） | 7 | 全合格 |
| ネスト重複排除（実ページ） | 2 | 全合格 |
| 並列ヘッダフェッチ性能 | 3 | 全合格 |
| キャッシュ動作検証（ヒット/高速化/破壊耐性） | 4 | 全合格 |
| キャッシュエビクション（LRU上限） | 3 | 全合格 |
| buildIdリトライ | 2 | 全合格 |
| **Part C: コンテキスト節約サマリー** | 1 | 全合格 |
| **合計** | **156** | **全合格** |

## 実際の検索シナリオでのコンテキスト消費検証（v0.4.0）

v0.4.0の改善を踏まえ、実際のSnowflake関連の検索シナリオでツールごとのコンテキスト消費を検証した。キーワード検索（「マイクロパーティション」）と文章形式の検索（「ウェアハウスのスケールアップの基準は？」）の2パターンで実施した。

### search_snowflake_docs: include_headings の影響

同じ検索（5件取得）でも `include_headings` のON/OFFでコンテキスト消費が大きく変わる。

| パターン | 推定文字数 |
|---|---|
| キーワード（headings=false） | ~500文字 |
| キーワード（headings=true） | ~3,500文字 |
| 文章形式（headings=false） | ~500文字 |
| 文章形式（headings=true） | ~5,000文字 |

`include_headings=true` にすると約 **7〜10倍** のコンテキストを消費する。ただし `get_doc_toc` の呼び出しを省略できるため、2ステップを1ステップに短縮できる。見出しの多いページ（ウェアハウス関連ページ等）ほど膨張が大きい。

### 全ツール横断比較（マイクロパーティションページ）

「マイクロパーティションとデータクラスタリング」ページ（total_length: 4,835文字）を対象に、全5ツールのコンテキスト消費を比較した。

| 順位 | ツール | 消費量 | ユースケース |
|---|---|---|---|
| 1 | `get_doc_toc` | ~600文字 | ページ構造の確認のみ |
| 2 | `get_doc_section`（1セクション） | ~528文字 | 特定セクションの詳細取得 |
| 3 | `search_snowflake_docs`（headings=false） | ~500文字/5件 | ドキュメント発見（概要のみ） |
| 4 | `search_in_doc`（3セクション） | ~2,400文字 | ページ内の関連情報を自動抽出 |
| 5 | `search_snowflake_docs`（headings=true） | ~3,500文字/5件 | ドキュメント発見+構造把握を一括 |
| 6 | `get_doc_content`（全文） | ~4,835文字 | ページ全体の読み込み |

小〜中規模ページでは `get_doc_content` の全文取得でも5,000文字以内に収まるため、段階的取得のメリットは相対的に小さい。CREATE TABLEのような大規模ページ（44,503文字〜）こそ、`search_in_doc` や `get_doc_section` による部分取得が効果を発揮する。

### search_in_doc のページ間比較

`search_in_doc` のコンテキスト消費はページとクエリの関連度によって大きく変動する。

| 対象ページ | クエリ | マッチセクション数 | total_content_chars |
|---|---|---|---|
| マイクロパーティション | 「マイクロパーティション 利点」 | 3件 | ~2,400文字 |
| ウェアハウス考慮事項 | 「スケールアップ スケールアウト 基準」 | 2件 | ~4,900文字 |
| ウェアハウスサイズ拡大 | 「スケールアップ サイズ変更 基準」 | 1件 | ~460文字 |

スコアリングで関連セクションを自動選択するため、必要な情報だけ効率的に取得できる。「ウェアハウス考慮事項」ページでは「スケールアップとスケールアウト」セクションが高スコア（24点）で正確にマッチし、スケールアップの判断基準やマルチクラスターウェアハウスとの使い分けに関する情報を返していた。

### 推奨ワークフロー

検証結果を踏まえた、コンテキスト効率の良いワークフローは以下の通り。

```text
1. search_snowflake_docs(include_headings=True) で検索+目次を1回で取得
2. search_in_doc で関連セクションだけ自動抽出（TOC確認→セクション選択を省略）
3. コード例が必要な場合のみ include_code_blocks=True を指定
```

これにより従来の `search` → `get_doc_toc` → `get_doc_section` の3ステップを最大1〜2ステップに短縮でき、ツール呼び出し回数とコンテキスト消費の両方を最適化できる。

## ドキュメント系MCPサーバー設計のポイント

今回の検証で得られた知見をまとめる。

### 1. レスポンスサイズにハードキャップを設ける

無制限取得はコンテキスト破綻のリスクがある。LLMのコンテキストウィンドウは有限なので、MCPサーバー側で上限を設けるべきである。

### 2. ページネーションを提供する

長文ドキュメントを一度に返すのではなく、`start_index` + `max_length` で分割読み込みできるようにする。AWS版の設計が参考になる。

### 3. 段階的な情報取得を可能にする

```text
検索 → 目次確認（軽量） → セクション取得（必要な部分だけ）
```

この段階的アプローチにより、不要な情報をコンテキストに載せずに済む。

### 4. HTML→Markdown変換にはライブラリを使う

手書きのHTMLパーサーはバグの温床になる。`markdownify` のような実績あるライブラリを使えば、重複出力やネスト構造のハンドリングミスを避けられる。

### 5. instructions にベストプラクティスを記載する

AWS版では FastMCP の `instructions` パラメータに「長文は分割読み込みすること」「見つかったら止めること」と明記している。LLMがツールをどう使うべきかのガイドをサーバー側から提供する設計は有効である。

### 6. ツール呼び出し回数を削減する

複数のツール呼び出しを1回にまとめられるオプション（`include_headings` のような）を提供することで、往復のオーバーヘッドとコンテキスト消費の両方を削減できる。ただし、1回のレスポンスが膨張しないようパラメータの組み合わせに注意が必要。

### 7. コードブロックをデフォルトで除外する

構文リファレンスのようなドキュメントでは、コードブロックがレスポンスの30〜40%を占めることがある。説明文だけで十分な場合が多いため、デフォルトOFFにしてオンデマンドで取得する設計が有効。

### 8. HTTP重複フェッチをキャッシュで排除する

同一URLへの連続アクセス（TOC確認→セクション取得）は頻発する。TTL付きインメモリキャッシュでHTTPフェッチを排除することで、レイテンシとサーバー負荷の両方を改善できる。

### 9. Markdown出力のノイズを除去する

HTML→Markdown変換は万能ではなく、LLMにとって無意味な要素が混入しやすい。パーマリンクアンカー（`[¶](...)`）、コピーボタンの残骸、辿れない相対リンクURL、画像タグ、フィードバックフォームなど、トークンを消費するだけの要素はHTML段階とテキスト段階の両方で除去すべきである。

### 10. 大量データを返すパラメータに安全弁を設ける

`include_headings=True` のようにレスポンスが膨張しうるパラメータには、上限キャップを設けるべきである。1ページ120件の見出しを全て返す必要はなく、h1-h3に絞って30件以内にするだけで59%の削減になる。

## まとめ

ドキュメント系MCPサーバーのコンテキスト使用量を検証し、3段階の改善を実施した。

**v0.2.0の改善:**
- `markdownify` ライブラリ導入でテキスト重複バグを解消（同じ文字数で実効情報量1.5倍）
- `start_index` ページネーションで長文ドキュメントの分割読み込みに対応
- `get_doc_toc`（目次取得）と `get_doc_section`（セクション取得）で段階的な情報取得を実現
- `max_length` のハードキャップ設定でコンテキスト破綻を防止

**v0.3.0の改善:**
- インメモリキャッシュでHTTP重複フェッチを排除
- `include_headings` で検索と目次取得を1回に統合（ツール呼び出し回数削減）
- コードブロックのデフォルトOFFで37.7%のコンテキスト削減
- `search_in_doc` で関連セクションの自動選択（TOC確認不要）
- 最適なフローで**約58%のコンテキスト削減**を達成

**v0.4.0の改善:**
- Markdown出力のノイズ除去（pilcrow、コピーボタン、リンクURL、画像）で同一ページ **15.5%削減**
- 複数ページでの検証で平均 **41.3%のコンテキスト削減** を確認（CREATE TABLE 37.3%、SELECT 58.0%、Dynamic Tables 16.3%）
- `include_headings` の見出しキャップ（30件上限）でコンテキスト爆発を防止（最悪ケース **59%削減**）
- `search_in_doc` のスコアリング精度向上（子セクションテキストの二重カウント排除 + ネスト重複排除）
- 境界切断の導入（段落→行→文→単語の優先度で自然な位置で切断）
- buildIdキャッシュ・共有HTTPクライアント・並列headings取得によるパフォーマンス改善
- 156テスト（ユニット59件 + 統合96件 + サマリー1件）全合格

**実際の検索シナリオでの検証:**
- 「マイクロパーティション」「ウェアハウスのスケールアップ」等の実際のSnowflakeトピックで全5ツールのコンテキスト消費を横断比較
- `include_headings=true` は headings=false の **7〜10倍** のコンテキストを消費（見出しの多いページほど膨張）
- `search_in_doc` のスコアリングが実際の検索シナリオでも正確に機能（スケールアップ関連セクションを高スコアで正確にマッチ）
- 小〜中規模ページでは `get_doc_content` 全文でも5,000文字以内に収まるため、段階的取得は大規模ページで効果大

MCPサーバーを設計する際は、レスポンスのサイズ = LLMのコンテキスト消費であることを意識し、「必要な情報だけを、必要な分だけ、ノイズなく返す」設計にすることが重要である。

## 参考資料

{{< linkcard "https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server" >}}

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}

{{< linkcard "https://pypi.org/project/markdownify/" >}}
