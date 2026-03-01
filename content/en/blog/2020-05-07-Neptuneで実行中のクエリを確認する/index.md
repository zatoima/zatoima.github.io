---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Checking Running Queries in Neptune"
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



When executing certain queries, the following error may occur. The cause is a processing conflict.

```sh
{
	"requestId": "c4b8f484-2de1-b8a4-81dd-6b225981653f",
	"code": "ConcurrentModificationException",
	"detailedMessage": "Operation failed due to conflicting concurrent operations (please retry), 0 transactions are currently rolling back."
}
```

To check what other queries are running, use the SPARQL Query Status API. The `queryString` field contains the actual SPARQL query being executed.

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

Reference

> SPARQL Query Status API - Amazon Neptune https://docs.aws.amazon.com/ja_jp/neptune/latest/userguide/sparql-api-status.html
