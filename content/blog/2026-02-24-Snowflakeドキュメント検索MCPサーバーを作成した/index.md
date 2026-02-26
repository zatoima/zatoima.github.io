---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflakeドキュメント検索MCPサーバーを作成した"
subtitle: ""
summary: " "
tags: ["Snowflake","MCP","Claude Code"]
categories: ["Snowflake","AI"]
url: snowflake-docs-mcp-server-architecture
date: 2026-02-24
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## はじめに

Claude CodeからSnowflake公式ドキュメントを検索・取得できるMCPサーバーを作成した。APIキーや認証は不要で、docs.snowflake.comの内部構造を利用して動作する。

本記事では、このMCPサーバーの技術的な仕組みについて記載する。

- GitHub: https://github.com/zatoima/snowflake-docs-mcp-server

## MCPサーバーの概要

提供するツールは2つ。

| ツール名 | 機能 |
|---|---|
| `search_snowflake_docs` | キーワードでドキュメントを全文検索 |
| `get_doc_content` | 指定URLのページ本文をMarkdown形式で取得 |

Claude Codeへの登録は以下のコマンドで行う。

```bash
claude mcp add snowflake-docs -- uv run --directory /path/to/snowflake-docs-mcp-server python server.py
```

## Next.jsの内部データ取得の仕組みを利用

このMCPサーバーの実装の肝は、docs.snowflake.comがNext.jsで構築されている点にある。Next.jsには`getServerSideProps`で取得したデータをJSONとして返す内部エンドポイントが存在し、これを利用している。

### 処理フロー

```
1. docs.snowflake.com のHTMLを取得
2. HTMLから Next.js の buildId を正規表現で抽出
3. _next/data/{buildId}/{lang}/search.json?q=... にリクエスト
4. 返却されたJSONから検索結果を抽出
```

### buildIdの取得

Next.jsアプリケーションはビルド時に一意の`buildId`を生成する。この値はページのHTMLソース内に埋め込まれている。

```python
async def _get_build_id() -> str:
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        resp = await client.get("https://docs.snowflake.com")
        resp.raise_for_status()
    m = re.search(r'"buildId":"([^"]+)"', resp.text)
    if not m:
        raise ValueError("Could not extract buildId from docs.snowflake.com")
    return m.group(1)
```

取得されるbuildIdは例えば `4Vr4FcaZt5TNi0rcHXIGK` のようなランダムな文字列である。サイトが再デプロイされるたびにこの値は変わる。

### 検索APIへのリクエスト

buildIdを使って以下のURLにリクエストを送る。

```
https://docs.snowflake.com/_next/data/{buildId}/en/search.json?q=Dynamic+Tables
```

レスポンスはJSON形式で、`pageProps.searchResults.results`に検索結果の配列が含まれる。各結果には`title`、`href`、`description`、`category`などのフィールドがある。

### ドキュメント本文の取得

`get_doc_content`ツールでは、指定URLのHTMLページをBeautifulSoupでパースし、本文をMarkdown風に整形して返す。

処理の流れは以下の通り。

1. HTMLを取得し、`<article>`または`role="main"`の要素を抽出
2. `nav`、`footer`、`aside`、sidebar、toc等の不要な要素を除去
3. 見出し、段落、コードブロック、リスト、テーブルをMarkdown形式に変換
4. `max_length`を超えた場合は切り捨て

セキュリティのため、`docs.snowflake.com`以外のURLは拒否する設計としている。

## 制限事項

- docs.snowflake.comの構造変更（Next.jsのbuildId体系の変更等）により動作しなくなる可能性がある
- 公式APIではなく、サイト内部の非公開の挙動に依存しているため、予告なく動作しなくなるリスクがある
- 日本語ドキュメント（`language: "ja"`）の検索精度は英語に比べて低い場合がある

## まとめ

Snowflakeドキュメント検索MCPサーバーは、docs.snowflake.comのNext.js内部エンドポイントを利用して検索・取得を行っている。公式APIに依存しないためAPIキーが不要だが、サイト構造の変更には弱いというトレードオフがある。

## 関連記事

{{< linkcard url="https://zatoima.github.io/mcp-server-context-usage-optimization/" title="ドキュメント系MCPサーバーのコンテキスト使用量を検証し改善した" description="本記事で作成したMCPサーバーのコンテキスト使用量を実測し、改善した過程と結果" >}}

{{< linkcard url="https://zatoima.github.io/snowflake-mcp-documentation-server-benchmark/" title="Snowflake MCPドキュメントサーバー2種のベンチマーク比較" description="本MCPサーバーとCortex Agent + CKEベースのMCPサーバーを20クエリ・5評価軸で比較" >}}

## 参考資料

{{< linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" >}}

{{< linkcard "https://modelcontextprotocol.io/" >}}

{{< linkcard "https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props" >}}
