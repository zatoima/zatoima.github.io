---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Elasticsearchのエイリアス設定方法"
subtitle: ""
summary: " "
tags: ["AWS","Elasticsearch"]
categories: ["AWS","Elasticsearch"]
url: aws-elasticsearch-alias-setting.html
date: 2020-05-04
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

AWS上のAmazon Elasticsearch Serviceで実施しています。

エイリアスとは名前の通り、インデックスに対して別名をつけることが可能になる。エイリアスとインデックスは1対1の関係ではなく、一つのエイリアスに複数のインデックスを紐付けることが出来る。

#### インデックスの作成

まずは事前準備としてインデックスを作成。

```sh
curl -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index1"
curl -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index2"
```

#### データ登録(my_index1用)

後ほどエイリアスを使用した検索を実施するのでテスト用のデータを挿入

```sh
curl -H "Content-Type: application/json" -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index1/_doc/1" -d '
{
  "title": "my_index1",
  "comments": {
    "name": "my_index1",
    "comment": "my_index1用のデータ"
  }
}'
```

#### データ登録(my_index2用)

```sh
curl -H "Content-Type: application/json" -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index2/_doc/1" -d '
{
  "title": "my_index2",
  "comments": {
    "name": "my_index2",
    "comment": "my_index2のデータ"
  }
}'
```

#### エイリアスの確認

```sh
cu
```

初期状態なので特にエイリアスは設定されていない

```sh
{
  "amazon_neptune" : {
    "aliases" : { }
  },
  ".kibana_1" : {
    "aliases" : {
      ".kibana" : { }
    }
  },
  "my_index2" : {
    "aliases" : { }
  },
  "my_index1" : {
    "aliases" : { }
  }
}
```

#### エイリアスの作成

`my_index1`のエイリアスである`my_ind`を作成してみる

```sh
curl  -H "Content-Type: application/json" -XPOST 'https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases' -d '
{
  "actions" : [
    { "add" : { "index" : "my_index1", "alias" : "my_ind" } }
  ]
}'
```

#### エイリアスの確認

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases?pretty
```

my_indが作成されている

```sh
  "my_index2" : {
    "aliases" : { }
  },
  "my_index1" : {
    "aliases" : {
      "my_ind" : { }
    }
```

この状態で検索をしてみると`my_index1`用のデータが出力される。

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_ind/_search?pretty
```

#### エイリアスの変更

次にエイリアスの設定変更をすることでインデックスの切替を実施する

```sh
curl  -H "Content-Type: application/json" -XPOST 'https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases' -d '
{
  "actions" : [
    { "remove" : { "index" : "my_index1", "alias" : "my_ind" } },
    { "add"    : { "index" : "my_index2", "alias" : "my_ind" } }
  ]
}'
```

#### エイリアスの確認

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases?pretty
```

先程とは異なり`my_index2`用のエイリアスが作成されている。`my_index1`のエイリアスは削除され存在しない。

```sh
  "my_index2" : {
    "aliases" : {
      "my_ind" : { }
    }
  },
  "my_index1" : {
    "aliases" : { }
  }

```

#### エイリアスを使用した検索

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_ind/_search?pretty
```

このエイリアス機能を使用することでダウンタイムを無くしてインデックスの切替が実施出来る。

> Changing Mapping with Zero Downtime | Elastic Blog https://www.elastic.co/jp/blog/changing-mapping-with-zero-downtime/
>
> Elasticsearch のインデックスを無停止で再構築する - クックパッド開発者ブログ https://techlife.cookpad.com/entry/2015/09/25/170000

