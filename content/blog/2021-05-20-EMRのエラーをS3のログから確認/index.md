---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EMRのエラーをS3のログから確認"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","EMR"]
url: aws-emr-error-log-s3-command.html
date: 2021-05-20
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



### ログダウンロード用のディレクトリを作成、及び移動

```csharp
mkdir j-3PS6MU0W27GMG
cd j-3PS6MU0W27GMG
```

### ログのダウンロード

※`j-3PS6MU0W27GMG`はCluster ID

```sh
aws s3 sync s3://aws-logs-xxx-ap-northeast-1/elasticmapreduce/j-3PS6MU0W27GMG .
```

### 解凍

```sh
find . -type f -exec gunzip {} \;
```

### エラーとワーニングを検索

時系列に並ぶようにsort

```sh
find . | grep log | xargs egrep "WARN|ERROR" | sort -k2
```

