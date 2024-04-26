---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "awsetsを使用してAWSリソース情報を出力する"
subtitle: ""
summary: " "
tags: ["AWS","EC2","awsets"]
categories: ["AWS","EC2","awsets"]
url: aws-awssets-list-resources.html
date: 2020-10-05
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

`A utility for crawling an AWS account and exporting all its resources for further analysis.`とあるようにAWSアカウントに紐づくAWSリソースをjson形式で出力してくれるツール。

> GitHub - trek10inc/awsets: A utility for crawling an AWS account and exporting all its resources for further analysis. https://github.com/trek10inc/awsets

現時点の最新のバージョンである`0.4.1`のバージョンでざっくりやってみたのでメモ。既にAWS CLIを実行出来る環境の場合はサクッとインストール、実行することが出来る。

#### インストール

```
cd /home/ec2-user
mkdir awsets
cd awsets
wget https://github.com/trek10inc/awsets/releases/download/v0.4.1/awsets_0.4.1_linux_x86_64.tar.gz
tar xvfz awsets_0.4.1_linux_x86_64.tar.gz

export PATH=PATH=$PATH:/home/ec2-user/awsets/
```

#### 実行

```
awsets list --regions ap-northeast-1 -o ec2.json --include ec2
awsets list --regions ap-northeast-1 -o elasticsearch.json --include elasticsearch
awsets list --regions ap-northeast-1 -o ecs.json --include ecs
```

他にも色々機能があるらしい。参考のリンク、公式githubを参照。

#### 参考

> AWSのリソース一覧を出力できるツール AWSets を試してみた - Qiita https://qiita.com/hayao_k/items/837e176e9d16101e09b1



