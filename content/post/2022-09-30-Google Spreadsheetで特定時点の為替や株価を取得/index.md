---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Google Spreadsheetで特定時点の為替や株価を取得"
subtitle: ""
summary: " "
tags: ["その他"]
categories: ["その他"]
url: google-spreadsheet-googlefinance-currency
date: 2022-09-30
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

GOOGLEFINANCE関数だけを使用するとDateとClose時点のPriceを指定してしまう。

```
=GOOGLEFINANCE("CURRENCY:USDJPY", "price", "2019/8/1")
```

![image-20220930102716790](./image-20220930102716790.png)

関数を`index(..., 2, 2)`でラップして、2行目の2番目のセルだけを取得

```
=index(GOOGLEFINANCE("CURRENCY:USDJPY", "price", "2019/8/1"), 2, 2)
```

特定企業の株価を取得。こちらもIndex関数を使用してほしい情報のみを取得

```
=index(GOOGLEFINANCE("NASDAQ:AMZN", "price", "2019/8/1"), 2, 2)
```

