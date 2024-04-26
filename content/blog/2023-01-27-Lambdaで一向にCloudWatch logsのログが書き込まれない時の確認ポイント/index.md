---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Lambdaで一向にCloudWatch logsのログが書き込まれない時の確認ポイント"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-lambda-cloudwatch-logs-not-write
date: 2023-01-27
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

こんなエラーが出て一向にログが書き込まれない

![image-20230127162101389](image-20230127162101389.png)

### 原因

他のLamdba関数のロールを使いまわしており、CloudWatch logsの書き込み先が特定のLamdba用になっていたため。IAMポリシーを書き換えるか、新規でポリシーを作ることで解決出来る。

