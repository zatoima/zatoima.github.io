---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Google カスタム検索エンジンでHugoのサイト内検索を行う"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-google-custom-search-engine
date: 2021-06-27
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





### 前提条件

- カスタムエンジン側の設定が完了済なこと

![image-20210626223508573](image-20210626223508573.png)

### config.tomlの編集

メニューバーに追加したいので、下記を追加する

```
[[Menus.main]]
  Name = "search"
  URL = "/search/"
```

### content/search配下にindex.htmlを追加

```html
---
title: "Search"
---

<form action="https://cse.google.com/cse">
  <div class="searchBox">
    <input type="hidden" name="cx" value="1ef1df26a465b967e" />
    <input type="hidden" name="ie" value="UTF-8" />
    <input type="search" name="q" placeholder="Googleカスタム検索" size="30" autocomplete="off" />
    <input type="submit" value="検索" />
  </div>
</form>
```

### 結果

メニューバー、及び検索ボックスが準備できた

![image-20210626223725020](image-20210626223725020.png)

このようなURL形式になるのでコマンドラインランチャー等から検索できるのも良い

```html
https://cse.google.com/cse?cx=<検索エンジンID>=UTF-8&q=<検索文字列>
```

