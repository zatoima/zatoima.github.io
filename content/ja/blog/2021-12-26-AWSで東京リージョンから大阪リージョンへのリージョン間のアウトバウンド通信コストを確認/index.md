---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWSで東京リージョンから大阪リージョンへのリージョン間のアウトバウンド通信コストを確認"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-tokyo-to-osaka-network-outbound-cost
date: 2021-12-26
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

Cost Explolerのレポートで確認出来る。右側のフィルターで`使用タイプ`で`APN1-APN3-AWS-Out-Bytes`を指定する。グループ化の条件として`サービス`を指定することでどのサービスの転送量が多いのかが分かる。

![image-20211219152740457](image-20211219152740457.png)

Cost Explorerをもっと使いこなしたい。

参考

> [【AWS CLI】Cost Explorer編 - サーバーワークスエンジニアブログ](https://blog.serverworks.co.jp/aws-cli-cost-explorer)
>
> https://d1.awsstatic.com/webinars/jp/pdf/services/20200129_BlackBelt_CostExplorer.pdf
