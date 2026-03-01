---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Neptuneインスタンスのヘルスステータスをcurlコマンドで取得する方法"
subtitle: ""
summary: " "
tags: ["AWS","Neptune"]
categories: ["AWS","Neptune"]
url: aws-neptune-health-status.html
date: 2020-04-02
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

CloudWatchやマネージメントコンソール上からもインスタンスステータスは当然分かるが、curlコマンドでも確認可能。

```sh
[ec2-user@bastin ~]$ curl -G https://neptestdb.xxxxxxxx.ap-northeast-1.neptune.amazonaws.com:8182/status | jq
{
  "status": "healthy",
  "startTime": "Sat Mar 21 03:06:07 UTC 2020",
  "dbEngineVersion": "1.0.2.1.R4",
  "role": "writer",
  "gremlin": {
    "version": "tinkerpop-3.4.1"
  },
  "sparql": {
    "version": "sparql-1.1"
  },
  "labMode": {
    "ObjectIndex": "disabled",
    "Streams": "enabled",
    "ReadWriteConflictDetection": "enabled"
  }
}

```

| 項目                            | 説明                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| status                          | インスタンスの状態。正常な場合はhealthy。インスタンスがクラッシュまたは再起動から回復中で、最新のサーバーのシャットダウンからアクティブなトランザクションが実行されている場合、ステータスは  "recovery" に設定 |
| version                         | Neptune エンジンバージョン。                                 |
| startTime                       | UTC時間でのインスタンスの起動時間                            |
| role                            | writerインスタンスかReaderインスタンスか                     |
| gremlin                         | エンジンで使用されている現在の TinkerPop バージョンに設定    |
| sparql                          | エンジンで使用されている SPARQL の最新バージョン             |
| labMode                         | ラボモード 設定が一覧表示                                    |
| rollingBackTrxCount             | ロールバックされるトランザクションの数                       |
| rollingBackTrxEarliestStartTime | ロールバックされる最も早いトランザクションの開始時刻         |

起動していない場合は、そもそもcurlコマンドがタイムアウト。

```sh
[ec2-user@bastin ~]$ curl -G https://neptestdb.xxxxxxxx.ap-northeast-1.neptune.amazonaws.com:8182/status
curl: (7) Failed to connect to neptestdb.xxxxxxxx.ap-northeast-1.neptune.amazonaws.com port 8182: Connection timed out
[ec2-user@bastin ~]$ 
```

