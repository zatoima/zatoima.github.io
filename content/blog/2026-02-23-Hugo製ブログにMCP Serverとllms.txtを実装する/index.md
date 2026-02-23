---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Hugo製ブログにMCP Serverとllms.txtを実装する"
subtitle: ""
summary: " "
tags: ["Hugo","Claude Code"]
categories: ["Hugo","Claude Code"]
url: hugo-blog-mcp-server-llms-txt
date: 2026-02-23
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

自分のHugoブログ（GitHub Pages）に対して、以下2つのアプローチでAI/LLM向けのインターフェースを実装した。

1. **ローカルMCP Server** - Claude Codeから記事の検索・閲覧ができるMCPサーバー
2. **llms.txt** - Webサイト上でLLM向けにコンテンツを公開する標準フォーマット

## MCP（Model Context Protocol）とは

MCPはAnthropicが提唱するプロトコルで、AIモデルが外部のデータソースやツールと連携するための標準的な仕組みである。MCP Serverを作ることで、Claude CodeなどのAIツールからブログの記事検索・閲覧が可能になる。

## ローカルMCP Serverの実装

### 構成

```
mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   └── index.ts
└── dist/
    └── index.js
```

使用したライブラリは以下の通り。

| パッケージ | 用途 |
|-----------|------|
| `@modelcontextprotocol/sdk` | MCP Server SDK |
| `gray-matter` | Markdownのフロントマター解析 |
| `zod` | スキーマバリデーション（SDK内蔵） |

### 提供ツール

MCP Serverでは5つのツールを実装した。

| ツール名 | 説明 |
|---------|------|
| `search_posts` | キーワードでタイトル・本文・タグを全文検索 |
| `read_post` | slugまたはタイトルの一部から記事全文を取得 |
| `list_posts` | 記事一覧の取得（タグ・カテゴリ・年でフィルタ可） |
| `list_tags` | 全タグと記事数の一覧 |
| `blog_stats` | ブログの統計情報（記事数、年別投稿数、人気タグ） |

### 実装のポイント

記事データの読み込みは、Hugoの`content/blog/`配下のMarkdownファイルを直接パースする方式を採用した。

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import matter from "gray-matter";

const server = new McpServer({
  name: "zatoima-blog",
  version: "1.0.0",
});

// ツール登録の例: 記事検索
server.tool(
  "search_posts",
  "ブログ記事をキーワードで検索する",
  {
    query: z.string().describe("検索キーワード"),
    limit: z.number().optional().default(10),
  },
  async ({ query, limit }) => {
    const q = query.toLowerCase();
    const results = getPosts()
      .filter(
        (p) =>
          p.title.toLowerCase().includes(q) ||
          p.content.toLowerCase().includes(q) ||
          p.tags.some((t) => t.toLowerCase().includes(q))
      )
      .slice(0, limit);
    // ... 結果を返す
  }
);
```

起動時に全記事を一括読み込みし、メモリ上に保持する。395記事程度であれば問題ない。

### Claude Codeへの登録

以下のコマンドでMCP Serverを登録する。

```bash
# ビルド
cd mcp-server && npm install && npx tsc

# Claude Codeに登録
claude mcp add zatoima-blog node /path/to/mcp-server/dist/index.js
```

登録後、Claude Codeのセッション内で以下のように使用できる。

```
# 記事検索
mcp__zatoima-blog__search_posts(query="Aurora")

# 統計情報
mcp__zatoima-blog__blog_stats()
```

## llms.txtの実装

### llms.txtとは

`llms.txt`はWebサイトの内容をLLMに理解させるためのフォーマットである。`robots.txt`のAI版のようなもので、サイトの概要と記事一覧をプレーンテキストで提供する。

- `/llms.txt` - 記事タイトル・URL・タグの一覧（軽量版）
- `/llms-full.txt` - 全記事の本文を含む完全版

### Hugoでの生成方法

#### 1. hugo.tomlにカスタム出力フォーマットを定義

```toml
[mediaTypes]
  [mediaTypes."text/llms"]
    suffixes = ["txt"]
  [mediaTypes."text/llms-full"]
    suffixes = ["txt"]

[outputFormats]
  [outputFormats.llms]
    mediaType = "text/llms"
    baseName = "llms"
    isPlainText = true
    notAlternative = true
  [outputFormats.llms-full]
    mediaType = "text/llms-full"
    baseName = "llms-full"
    isPlainText = true
    notAlternative = true

[outputs]
  home = ["HTML", "RSS", "JSON", "llms", "llms-full"]
```

#### 2. テンプレートファイルの作成

`layouts/_default/index.llms.txt`（軽量版）:

```
# {{ .Site.Title }}

> {{ .Site.Params.description }}

author: zatoima
url: {{ .Site.BaseURL }}

## Blog Posts

{{- $pages := where .Site.RegularPages "Section" "blog" }}
{{ range $pages }}
- [{{ .Title }}]({{ .Permalink }}) ({{ .Date.Format "2006-01-02" }}){{ with .Params.tags }} [{{ delimit . ", " }}]{{ end }}
{{- end }}
```

`layouts/_default/index.llms-full.txt`（完全版）:

```
{{- $pages := where .Site.RegularPages "Section" "blog" }}
{{ range $pages }}
---
### {{ .Title }}
date: {{ .Date.Format "2006-01-02" }}
url: {{ .Permalink }}
{{ .Plain }}
{{ end }}
```

#### 3. HTMLヘッダーへのリンク追加

`layouts/_default/baseof.html`の`<head>`内に以下を追加する。

```html
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt" />
<link rel="alternate" type="text/plain" href="/llms-full.txt" title="LLMs-full.txt" />
```

ナビゲーションにもリンクを追加した。

```html
<a href="/llms.txt" title="LLMs.txt - AI/LLM向けサイト情報">llms.txt</a>
```

### 生成結果

| ファイル | 行数 | 内容 |
|---------|------|------|
| `llms.txt` | 414行 | 記事タイトル・URL・タグの一覧 |
| `llms-full.txt` | 7,448行 | 全記事の本文を含む完全版 |

## まとめ

Hugo製の静的ブログに対して、2つの異なるアプローチでAI/LLMとの連携を実装した。

| 方式 | 用途 | 動作環境 |
|------|------|---------|
| ローカルMCP Server | Claude Codeからの記事操作 | ローカル（Node.js） |
| llms.txt | Web上でのLLM向けコンテンツ公開 | GitHub Pages（静的ファイル） |

ローカルMCP Serverはリアルタイムな検索・操作に優れ、llms.txtはデプロイするだけで誰でもアクセスできる手軽さがある。静的サイトでも工夫次第でAIフレンドリーな対応が可能である。

## 参考資料

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [llms.txt proposal](https://llmstxt.org/)
- [Hugo Custom Output Formats](https://gohugo.io/templates/output-formats/)
