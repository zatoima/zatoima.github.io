---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "HugoブログにOGP自動取得のリンクカードshortcodeを実装する"
subtitle: ""
summary: " "
tags: ["Hugo", "ブログ"]
categories: ["Hugo", "ブログ"]
url: hugo-linkcard-shortcode
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

ブログ記事の参考資料セクションにURLを並べるとき、箇条書きのプレーンリンクでは味気ない。Zennやはてなブログのようなリンクカード表示を実現するため、HugoのカスタムshortcodeとOGPメタデータの自動取得を組み合わせた `linkcard` shortcodeを作成した。

## 完成イメージ

### ライトモード

![リンクカード（ライトモード）](linkcard-light.png)

### ダークモード

![リンクカード（ダークモード）](linkcard-dark.png)

## 実装方針

リンクカードの実装にはいくつかのアプローチがある。

| 方式 | メリット | デメリット |
|------|----------|------------|
| JavaScript（クライアント側） | 動的にOGP取得 | CORS制限、表示遅延 |
| 手動パラメータ指定 | 確実に動作 | 毎回手入力が必要 |
| **ビルド時OGP取得（採用）** | **自動取得、JS不要** | **ビルド時間が若干増加** |

Hugoの `resources.GetRemote` を使い、ビルド時にリンク先のHTMLを取得してOGPメタデータを抽出する方式を採用した。手動パラメータによる上書きも可能なハイブリッド型とした。

## 実装

### Hugo設定の追加

`resources.GetRemote` でHTTPリクエストを発行するには、`hugo.toml` にセキュリティ設定を追加する必要がある。

```toml
[security]
  [security.http]
    methods = ['(?i)GET']
    urls = ['.*']
```

### shortcodeテンプレート

`layouts/shortcodes/linkcard.html` を作成する。

```html
{{- $url := .Get 0 | default (.Get "url") -}}
{{- $title := .Get "title" | default "" -}}
{{- $description := .Get "description" | default "" -}}
{{- $image := .Get "image" | default "" -}}

{{- if $url -}}
  {{- $domain := replaceRE `^https?://([^/]+).*` "$1" $url -}}
  {{- $favicon := printf "https://www.google.com/s2/favicons?sz=32&domain=%s" $domain -}}

  {{- if not $title -}}
    {{- with resources.GetRemote $url -}}
      {{- with .Err -}}
        {{- warnf "linkcard: failed to fetch %s" $url -}}
      {{- else -}}
        {{- $body := .Content -}}

        {{/* og:title */}}
        {{- range findRE `<meta[^>]*property="og:title"[^>]*>` $body 1 -}}
          {{- $title = replaceRE `.*content="([^"]*)".*` "$1" . -}}
        {{- end -}}

        {{/* og:description */}}
        {{- if not $description -}}
          {{- range findRE `<meta[^>]*property="og:description"[^>]*>` $body 1 -}}
            {{- $description = replaceRE `.*content="([^"]*)".*` "$1" . -}}
          {{- end -}}
        {{- end -}}

        {{/* og:image */}}
        {{- if not $image -}}
          {{- range findRE `<meta[^>]*property="og:image"[^>]*>` $body 1 -}}
            {{- $image = replaceRE `.*content="([^"]*)".*` "$1" . -}}
          {{- end -}}
        {{- end -}}

        {{/* fallback: <title> tag */}}
        {{- if not $title -}}
          {{- range findRE `<title[^>]*>[^<]+</title>` $body 1 -}}
            {{- $title = replaceRE `<title[^>]*>([^<]+)</title>` "$1" . -}}
          {{- end -}}
        {{- end -}}

        {{/* fallback: meta name="description" */}}
        {{- if not $description -}}
          {{- range findRE `<meta[^>]*name="description"[^>]*>` $body 1 -}}
            {{- $description = replaceRE `.*content="([^"]*)".*` "$1" . -}}
          {{- end -}}
        {{- end -}}

        {{/* resolve relative og:image */}}
        {{- if and $image (hasPrefix $image "/") -}}
          {{- $baseURL := replaceRE `^(https?://[^/]+).*` "$1" $url -}}
          {{- $image = printf "%s%s" $baseURL $image -}}
        {{- end -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}

  {{/* final fallback for title */}}
  {{- if not $title -}}
    {{- $title = $url -}}
  {{- end -}}

  <div class="link-card">
    <a href="{{ $url }}" target="_blank" rel="noopener noreferrer">
      <div class="link-card-body">
        <div class="link-card-text">
          <div class="link-card-title">{{ $title }}</div>
          {{- if $description -}}
            <div class="link-card-description">{{ $description }}</div>
          {{- end -}}
          <div class="link-card-meta">
            <img class="link-card-favicon" src="{{ $favicon }}" alt=""
                 loading="lazy" width="16" height="16">
            <span class="link-card-domain">{{ $domain }}</span>
          </div>
        </div>
        {{- if $image -}}
          <div class="link-card-image">
            <img src="{{ $image }}" alt="" loading="lazy">
          </div>
        {{- end -}}
      </div>
    </a>
  </div>
{{- end -}}
```

処理の流れは以下の通り。

1. 第1引数またはnamed parameterの `url` からURLを取得
2. `resources.GetRemote` でHTMLを取得
3. 正規表現でOGPメタタグ（`og:title`、`og:description`、`og:image`）を抽出
4. OGPがない場合は `<title>` タグや `meta name="description"` にフォールバック
5. 相対パスのOG画像はベースURLを付与して絶対パスに変換
6. Google Favicons APIでファビコンを取得

### CSS

`static/css/zenn.css` にリンクカード用のスタイルを追加する。

```css
/* --- Link Card --- */
.link-card {
  margin: 1.5rem 0;
}

.link-card a {
  display: block;
  text-decoration: none;
  color: inherit;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
  background: var(--bg-card);
}

.link-card a:hover {
  box-shadow: var(--shadow-card-hover);
  border-color: var(--accent);
}

.link-card-body {
  display: flex;
  align-items: stretch;
}

.link-card-text {
  flex: 1;
  min-width: 0;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.35rem;
}

.link-card-title {
  font-size: 0.95rem;
  font-weight: 700;
  line-height: 1.5;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.link-card-description {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.link-card-image {
  width: 230px;
  min-width: 230px;
  max-height: 130px;
  overflow: hidden;
}

.link-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

既存のCSS変数（`--border-color`、`--bg-card`、`--accent` など）を活用しているため、ダークモードは自動的に対応される。

外部リンクに付与される `↗` アイコンがカード内に表示されないよう、以下のルールも追加する。

```css
.article-content .link-card a[href]::after {
  content: none;
}
```

## 使い方

### 基本（OGP自動取得）

URLを渡すだけで、ビルド時にタイトル・説明・画像を自動取得する。

```
{{</* linkcard "https://github.com/zatoima/snowflake-docs-mcp-server" */>}}
```

### 手動指定

OGPが取得できないサイトやカスタマイズしたい場合は、named parameterで指定する。

```
{{</* linkcard url="https://example.com" title="タイトル" description="説明文" image="https://example.com/og.png" */>}}
```

## 技術的なポイント

### OGPメタタグの抽出

HTMLの `<meta>` タグは `property` と `content` 属性の出現順序がサイトによって異なる。`findRE` で `<meta[^>]*property="og:title"[^>]*>` とマッチさせることで、属性順序に依存しない抽出を実現している。

### ビルドキャッシュ

`resources.GetRemote` の結果はHugoのリソースキャッシュに保存される。2回目以降のビルドでは再取得が発生しないため、ビルド時間への影響は初回のみである。

### フォールバック戦略

OGPメタデータが存在しないサイトへの対応として、3段階のフォールバックを実装した。

```
og:title → <title>タグ → URL文字列
og:description → meta name="description" → （表示なし）
og:image → （表示なし）
```

## まとめ

Hugoの `resources.GetRemote` と正規表現によるOGPメタデータ抽出を組み合わせることで、ビルド時に自動でリンクカードを生成するshortcodeを実装した。JavaScriptを使わないため表示が速く、CORSの制限も受けない。既存のCSS変数を活用してダークモードにも対応している。
