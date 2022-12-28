---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Hugo wowchemy（旧Academic）のcustom.scssのカスタマイズ"
subtitle: ""
summary: " "
tags: ["その他"]
categories: ["その他"]
url: other-hugo-wowchemy-academic-custome
date: 2022-04-22
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

> 高度なスタイルのカスタマイズが必要な場合は、既存のスタイルをオーバーライドしたり、強化するための CSS コード を記述することが可能
>
> 1. `assets/scss/` フォルダがない場合は作成する。
> 2. `assets/scss/` フォルダの中に `custom.scss` という名前のファイルを作成する。
> 3. 作成したファイルにカスタムCSSコードを追加し、Hugoを再実行して変更を確認する。

```python

.article-container {
    width: 100%;
    max-width: 1000px;
    min-width: 500px;
    margin-right: auto;
    margin-left: auto;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 1.7rem;
    margin-bottom: 0.3rem;
    font-weight: 700;

}


img {
	max-width: 100%;
	height: auto;
	vertical-align: bottom;
}

body, h1, h2, h3, h4, h5, h6, .navbar-custom { 
    font-family: Helvetica,"Sawarabi Gothic",Meiryo,"メイリオ","Hiragino Kaku Gothic ProN", "ヒラギノ角ゴ ProN",YuGothic,"游ゴシック",Arial,sans-serif; 
}


article h2 {
    padding: .5em .75em;
    border-left: 14px solid #E5E5E5;
    background-color: #f6f6f6;
  }
  
article h3 {
  position: relative;
  padding: .25em 0 .5em .75em;
  border-left: 12px solid #E5E5E5;
}
article h3::after {
  position: absolute;
  left: 0;
  bottom: 0;
  content: '';
  width: 100%;
  height: 0;
  border-bottom: 1px solid #E5E5E5;
}


article h4 {
    padding: .25em 0 .25em .75em;
    border-left: 10px solid #E5E5E5;
  }
```

[Extending Wowchemy | Wowchemy: Free, No Code Website Builder for Hugo themes](https://wowchemy.com/docs/guide/extending-wowchemy/)

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
