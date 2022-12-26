---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Neptuneで実行中のクエリを確認する"
subtitle: ""
summary: " "
tags: ["Neptune"]
categories: ["Neptune"]
url: aws-neptune-execute-query-check.html
date: 2020-05-07
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



特定のクエリを実行した場合に下記のようなエラーが発生する場合がある。原因は処理の競合。

```sh
{
	"requestId": "c4b8f484-2de1-b8a4-81dd-6b225981653f",
	"code": "ConcurrentModificationException",
	"detailedMessage": "Operation failed due to conflicting concurrent operations (please retry), 0 transactions are currently rolling back."
}
```

他にどんなクエリが流れているか確認したい場合にはSPARQL クエリステータス APIを使用。queryStringが実際に流れているSPARQLクエリとなる。

```sh
[ec2-user@bastin ~]$ curl https://xxxxxxxx.xxxxxx.ap-northeast-1.neptune.amazonaws.com:8182/sparql/status | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   205    0   205    0     0   9318      0 --:--:-- --:--:-- --:--:--  9318
{
  "acceptedQueryCount": 8,
  "runningQueryCount": 1,
  "queries": [
    {
      "queryId": "372954e5-f674-497e-ae1f-0d772e636e41",
      "queryEvalStats": {
        "subqueries": 0,
        "elapsed": 1034223,
        "cancelled": false
      },
      "queryString": "clear all"
    }
  ]
}
```

参考

> SPARQL クエリステータス API - Amazon Neptune https://docs.aws.amazon.com/ja_jp/neptune/latest/userguide/sparql-api-status.html