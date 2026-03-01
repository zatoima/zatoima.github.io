---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Hugo wowchemy（旧Academic）における記事幅の調整方法"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-wowchemy-academic-article-container
date: 2021-09-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: f
---



下記の通り行うことでカスタマイズが可能。

高度なスタイルのカスタマイズが必要な場合は、既存のスタイルをオーバーライドしたり、強化するための CSS コード を記述することが可能

1. `assets/scss/` フォルダがない場合は作成する。
2. `assets/scss/` フォルダの中に `custom.scss` という名前のファイルを作成する。
3. 作成したファイルにカスタムCSSコードを追加し、Hugoを再実行して変更を確認する。

適宜、こんな形で指定すれば良い。

```
.article-container {
    width: 100%;
    max-width: 1000px;
    min-width: 500px;
    margin-right: auto;
    margin-left: auto;
}
```

参考

[Extending Wowchemy \| Wowchemy: Free, No Code Website Builder for Hugo themes](https://wowchemy.com/docs/guide/extending-wowchemy/)

> ##### Customize style (CSS)
>
> To personalize Wowchemy, you can **choose a colour theme and font set** in `config/_default/params.yaml`.
>
> For further personalization, you can [**create your own colour theme and font theme**](https://wowchemy.com/docs/getting-started/customization/#custom-theme).
>
> If advanced style customization is required, **CSS code** can be written to override or enhance the existing styles:
>
> 1. Create the `assets/scss/` folder if it doesn’t exist
> 2. Create a file named `custom.scss` in the `assets/scss/` folder
> 3. Add your custom CSS code to the file you created and re-run Hugo to view changes
