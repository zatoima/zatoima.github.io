---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQL でリードレプリカかプライマリか見分ける方法"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-replica-master-check.html
date: 2020-04-25
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

`server_id` に `session_id='MASTER_SESSION_ID'` があればプライマリのインスタンス。

```sql
postgres=> select server_id,session_id,highest_lsn_rcvd,cur_replay_latency_in_usec,now(),last_update_timestamp from aurora_replica_status();
     server_id     |    session_id     | highest_lsn_rcvd | cur_replay_latency_in_usec |              now              | last_update_timestamp  
-------------------+-------------------+------------------+----------------------------+-------------------------------+------------------------
 aurorapostgresv11 | MASTER_SESSION_ID |                  |                            | 2020-04-24 13:44:30.808061+00 | 2020-04-24 13:44:29+00
(1 row)
```

> https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.BestPractices.html
>
> \> ホスト文字列を取得するそのほかのオプション
>
> アプリケーションは、DB クラスターのすべての DB インスタンスに接続でき、`aurora_replica_status` 関数を照会して、クラスターのライターを特定したり、クラスターのその他のリーダーノードを見つけたりできます。