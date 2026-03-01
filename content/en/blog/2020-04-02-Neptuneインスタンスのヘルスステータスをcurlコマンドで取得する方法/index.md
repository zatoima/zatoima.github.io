---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Get Neptune Instance Health Status with the curl Command"
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



While you can check the instance status from CloudWatch or the Management Console, you can also verify it using the curl command.

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

| Field                           | Description                                                         |
| ------------------------------- | ------------------------------------------------------------------- |
| status                          | Instance state. "healthy" when normal. Set to "recovery" if the instance is recovering from a crash or restart and there are active transactions from the last server shutdown. |
| version                         | Neptune engine version.                                             |
| startTime                       | Instance startup time in UTC.                                       |
| role                            | Whether the instance is a writer or reader instance.                |
| gremlin                         | Set to the current TinkerPop version used by the engine.            |
| sparql                          | The latest version of SPARQL used by the engine.                    |
| labMode                         | Lists the Lab Mode settings.                                        |
| rollingBackTrxCount             | The number of transactions being rolled back.                       |
| rollingBackTrxEarliestStartTime | The start time of the earliest transaction being rolled back.       |

If the instance is not running, the curl command will simply time out.

```sh
[ec2-user@bastin ~]$ curl -G https://neptestdb.xxxxxxxx.ap-northeast-1.neptune.amazonaws.com:8182/status
curl: (7) Failed to connect to neptestdb.xxxxxxxx.ap-northeast-1.neptune.amazonaws.com port 8182: Connection timed out
[ec2-user@bastin ~]$
```
