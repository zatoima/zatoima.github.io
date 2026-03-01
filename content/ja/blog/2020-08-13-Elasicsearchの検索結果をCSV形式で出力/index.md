---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Amazon Elasicsearch Serviceの検索結果をCSV形式で出力"
subtitle: ""
summary: " "
tags: ["AWS","Elasicsearch"]
categories: ["AWS","Elasicsearch"]
url: aws-elasticsearch-csv-output.html
date: 2020-08-13
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

### 事前準備

jqコマンドとcsvkitに含まれるJSON形式の出力をCSVにするコマンドであるin2csvが必要となので事前にインストールする。Python環境も必要。

```sh
sudo yum -y install jq
pip install csvkit
```

### CSV形式でElasicsearchの結果を取得

```sh
curl https://vpc-xxxxxxx-xxxxxx.ap-northeast-1.es.amazonaws.com/xxxxxxx/_search?pretty | jq [.hits.hits[]._source] | in2csv -f json
```

