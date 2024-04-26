---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Amazon Elasticsearch Serviceでindex.max_result_windowの値を変更"
subtitle: ""
summary: " "
tags: ["AWS","Elasticsearch"]
categories: ["AWS","Elasticsearch"]
url: aws-elasticsearch-max_result_window_parameter.html
date: 2020-07-25
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

Amazon Elasticsearch Service で `index.max_result_window` を変更する方法と確認する方法をメモ。変更に伴いクラスターのレイテンシーとメモリへの注意が必要。

> Index modules | Elasticsearch Reference [7.8] | Elastic https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html
>
> **`index.max_result_window`**
>
> The maximum value of `from + size` for searches to this index. Defaults to `10000`. Search requests take heap memory and time proportional to `from + size` and this limits that memory. See [Scroll](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-scroll) or [Search After](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-search-after) for a more efficient alternative to raising this.

### 変更

```sh
curl -H "Content-Type: application/json" -XPUT 'https://vpc-xxx-xxxx.ap-northeast-1.es.amazonaws.com/xxxx/_settings' -d '
{
  "index": {
    "max_result_window" : "1000000"
  }
}'
```

### 確認

```sh
curl -X GET "https://vpc-xxx-xxx.ap-northeast-1.es.amazonaws.com/xxxx/_settings?pretty"
```

### 結果

```sh
[ec2-user@bastin ~]$ curl -H "Content-Type: application/json" -XPUT 'https://vpc-xxx-xxxxx.ap-northeast-1.es.amazonaws.com/xxxxx/_settings' -d '
> {
>   "index": {
>     "max_result_window" : "1000000"
>   }
> }'
[ec2-user@bastin ~]$ curl -X GET "https://vpc-xx-xx.ap-northeast-1.es.amazonaws.com/xxxxx/_settings?pretty"
{
  "amazon_neptune" : {
    "settings" : {
      "index" : {
        "number_of_shards" : "1",
        "provided_name" : "xxxxx",
        "max_result_window" : "1000000",
        "creation_date" : "1595601039642",
        "number_of_replicas" : "1",
        "uuid" : "05kXhekxQ5KUfqyI4_nABw",
        "version" : {
          "created" : "7040299"
        }
      }
    }
  }
```

