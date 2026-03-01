---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "S3のパブリックアクセスに関するブロックパブリックアクセスとバケットポリシーの関係"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-s3-public-access-about-message-policy
date: 2022-04-10
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

### はじめに

S3のパブリックアクセスについて下記4つのステータスを確認したので整理してみる。

1. 非公開のバケットとオブジェクト
2. オブジェクトは公開することができます
3. 公開
4. このアカウントの認証ユーザのみ

### 1.非公開のバケットとオブジェクト

下記状態の場合、`非公開のバケットとオブジェクト`と表示される

- ブロックパブリックアクセスをオン
- バケットポリシーで明示的なアクセスを許可していない

![image-20220410113831656](image-20220410113831656.png)

![image-20220410113846723](image-20220410113846723.png)

![image-20220410113946431](image-20220410113946431.png)

### 2.オブジェクトは公開することができます

下記状態の場合、`オブジェクトは公開することができます`と表示される。当初、この表示の場合、パブリックアクセスが可能と思っていたが、明示的にバケットポリシーの変更が必要な模様。日本語的にもパブリックアクセス可能なように思えたが、実際にはアクセスできない。

- ブロックパブリックアクセスをオフ
- バケットポリシーで明示的なアクセスを許可していない

![image-20220410114103815](image-20220410114103815.png)

![image-20220410114139965](image-20220410114139965.png)

![image-20220410114043581](image-20220410114043581.png)

![image-20220410114335717](image-20220410114335717.png)

### 3.公開

下記状態の場合、`公開`と表示される。

- ブロックパブリックアクセスをオフ
- バケットポリシーで明示的なアクセスを許可を行う

例：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-public-test-1/*"
            ]
        }
    ]
}
```

![image-20220410115015587](image-20220410115015587.png)

![image-20220410115053992](image-20220410115053992.png)

![image-20220410115223332](image-20220410115223332.png)

### 4.このアカウントの認証ユーザのみ

下記状態の場合、`このアカウントの認証ユーザのみ`と表示される。

- ブロックパブリックアクセスをオン
- バケットポリシーで明示的なアクセスを許可を行う

![image-20220410115420705](image-20220410115420705.png)

![image-20220410115359315](image-20220410115359315.png)
