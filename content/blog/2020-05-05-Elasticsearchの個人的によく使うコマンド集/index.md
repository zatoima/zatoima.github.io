---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Elasticsearchの個人的によく使うコマンド集"
subtitle: ""
summary: " "
tags: ["AWS","Elasticsearch"]
categories: ["AWS","Elasticsearch"]
url: aws-elasticsearch-commands-lists.html
date: 2020-05-05
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

Amazon Elasticsearch Service 上でのコマンド実行を想定。適宜追加。

### インデックス作成

```sh
curl -X PUT "<Amazon Elasticsearch Serviceのエンドポイント>/<index_name>"
```

### インデックスの確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_aliases?pretty
```

### インデックスの詳細確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/<index_name>/_settings?pretty
```

### インデックス削除

```sh
curl -XDELETE <Amazon Elasticsearch Serviceのエンドポイント>/<index_name>?pretty=true
```

### データ検索（無条件）

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/<index_name>/_search?pretty
```

### index確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_cat/indices?v
```

### 件数確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_cat/count/<index_name>?v
curl <Amazon Elasticsearch Serviceのエンドポイント>/<index_name>/_count?pretty
```

### 統計情報

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/<index_name>/_stats?pretty
```

### エイリアスの確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_aliases?pretty
```

### エイリアスの作成

```sh
curl  -H "Content-Type: application/json" -XPOST '<Amazon Elasticsearch Serviceのエンドポイント>/_aliases' -d '
{
  "actions" : [
    { "add" : { "index" : "my_index1", "alias" : "my_ind1" } },
    { "add" : { "index" : "my_index2", "alias" : "my_ind2" } }
  ]
}'
```

### エイリアスの削除

```sh
curl  -H "Content-Type: application/json" -XPOST '<Amazon Elasticsearch Serviceのエンドポイント>/_aliases' -d '
{
  "actions" : [
    { "remove" : { "index" : "my_index1", "alias" : "my_ind1" } },
    { "remove" : { "index" : "my_index2", "alias" : "my_ind2" } }
  ]
}'
```

### catで確認が可能なもの一覧

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_cat
```

### マッピング確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/<index_name>/_mapping?pretty
```

### 各ノードの役割の確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_cat/nodes
```

### マスターノードの確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_cat/master
```

### どのノードがどのシャードを含んでいるか確認

```sh
curl <Amazon Elasticsearch Serviceのエンドポイント>/_cat/shards
```

### field-dataの確認

```sh
curl -XGET <Amazon Elasticsearch Serviceのエンドポイント>/_stats/fielddata?pretty
```

