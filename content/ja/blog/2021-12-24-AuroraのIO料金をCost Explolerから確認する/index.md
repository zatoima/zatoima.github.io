---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AuroraのIO料金をCost Explolerから確認する"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-aurora-io-cost-exploler-check
date: 2021-12-24
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

Cost Explolerのレポートを開く

> https://console.aws.amazon.com/cost-management/home#/dashboard

![image-20211219151527819](image-20211219151527819.png)

右側のフィルター部分で下記の通り指定する。適宜集計する期間も変更する。左上部分。

1. サービスで`RDS`を選択する
2. `Aurora:StorageIOUsage (IOs)`を使用タイプで検索して該当する使用タイプを全部選択する

![image-20211219151029956](image-20211219151029956.png)

カーソルをグラフにあてるとIO数とコストが確認可能。

![image-20211219151631348](image-20211219151631348.png)
