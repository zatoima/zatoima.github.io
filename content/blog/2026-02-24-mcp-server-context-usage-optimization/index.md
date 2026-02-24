---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ドキュメント系MCPサーバーのコンテキスト使用量を検証し改善した"
subtitle: ""
summary: " "
tags: ["MCP","Claude","LLM","Snowflake"]
categories: ["MCP","LLM"]
url: mcp-server-context-usage-optimization
date: 2026-02-24
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

```
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

```
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

```
search_snowflake_docs  → ドキュメント検索
get_doc_toc            → ページの目次取得（軽量）
get_doc_section        → 特定セクションの取得
get_doc_content        → ページ全文の取得（ページネーション対応）
```

推奨される使い方は以下の流れ。

```
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
```
- Requires a value (NOT NULL).
Requires a value (NOT NULL).

- Has a default value.
Has a default value.

- CREATE OR ALTER TABLE (creates a table if ...)
CREATE OR ALTER TABLE (creates a table if ...)
```

**新版（v0.2.0）— 10行:**
```
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

## ドキュメント系MCPサーバー設計のポイント

今回の検証で得られた知見をまとめる。

### 1. レスポンスサイズにハードキャップを設ける

無制限取得はコンテキスト破綻のリスクがある。LLMのコンテキストウィンドウは有限なので、MCPサーバー側で上限を設けるべきである。

### 2. ページネーションを提供する

長文ドキュメントを一度に返すのではなく、`start_index` + `max_length` で分割読み込みできるようにする。AWS版の設計が参考になる。

### 3. 段階的な情報取得を可能にする

```
検索 → 目次確認（軽量） → セクション取得（必要な部分だけ）
```

この段階的アプローチにより、不要な情報をコンテキストに載せずに済む。

### 4. HTML→Markdown変換にはライブラリを使う

手書きのHTMLパーサーはバグの温床になる。`markdownify` のような実績あるライブラリを使えば、重複出力やネスト構造のハンドリングミスを避けられる。

### 5. instructions にベストプラクティスを記載する

AWS版では FastMCP の `instructions` パラメータに「長文は分割読み込みすること」「見つかったら止めること」と明記している。LLMがツールをどう使うべきかのガイドをサーバー側から提供する設計は有効である。

## まとめ

ドキュメント系MCPサーバーのコンテキスト使用量を検証し、以下の改善を実施した。

- `markdownify` ライブラリ導入でテキスト重複バグを解消（同じ文字数で実効情報量1.5倍）
- `start_index` ページネーションで長文ドキュメントの分割読み込みに対応
- `get_doc_toc`（目次取得）と `get_doc_section`（セクション取得）で段階的な情報取得を実現
- `max_length` のハードキャップ設定でコンテキスト破綻を防止

MCPサーバーを設計する際は、レスポンスのサイズ = LLMのコンテキスト消費であることを意識し、「必要な情報だけを、必要な分だけ返す」設計にすることが重要である。

## 参考資料

{{< linkcard "https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server" >}}

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}

{{< linkcard "https://pypi.org/project/markdownify/" >}}
