---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Getting Exchange Rates and Stock Prices at a Specific Point in Time with Google Spreadsheet"
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

Using only the GOOGLEFINANCE function will return both a Date and Close price.

```
=GOOGLEFINANCE("CURRENCY:USDJPY", "price", "2019/8/1")
```

![image-20220930102716790](./image-20220930102716790.png)

Wrap the function with `index(..., 2, 2)` to get only the second cell in the second row.

```
=index(GOOGLEFINANCE("CURRENCY:USDJPY", "price", "2019/8/1"), 2, 2)
```

Getting a specific company's stock price. Also use the Index function to retrieve only the desired information.

```
=index(GOOGLEFINANCE("NASDAQ:AMZN", "price", "2019/8/1"), 2, 2)
```
