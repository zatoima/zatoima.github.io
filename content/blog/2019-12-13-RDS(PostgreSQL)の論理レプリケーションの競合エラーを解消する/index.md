---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS(PostgreSQL)の論理レプリケーションの競合エラーを解消する"
subtitle: " "
summary: " "
tags: ["AWS", "RDS", "PostgreSQL"]
categories: ["AWS", "RDS", "PostgreSQL"]
url: aws-rds-repllication-error-conflict.html
date: 2019-12-13T20:00:00+09:00
lastmod: 2019-12-13T20:00:00:10+09:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---



### 競合を発生させる

***

```sql
#subscribe側のテーブルに事前にINSERTする
insert into LogicalReplicationTest values (1);

#publisher側のテーブルにINSERTして伝搬させる
insert into LogicalReplicationTest values (1);
```

### エラー確認

***

```
2019-11-30 15:13:26 UTC::@:[29680]:ERROR: duplicate key value violates unique constraint "logicalreplicationtest_pkey"
2019-11-30 15:13:26 UTC::@:[29680]:DETAIL: Key (a)=(1) already exists.
2019-11-30 15:13:26 UTC::@:[12125]:LOG: worker process: logical replication worker for subscription 110499 (PID 29680) exited with exit code 1
```

この時の方針としては大きく２つある。

1. 競合が発生した原因を取り除く
   - 上記の場合は、publisher側のテーブルに既にデータが入っていることが原因なので、publisher側をメンテナンスする。
2. publisher側のLSNの適用位置を変更する

今回は上記の「2.publisher側のLSNの適用位置を変更する」をやってみる。あるべき姿は「1.競合が発生した原因を取り除く」

### 現時点のLSNの位置を確認

***

```sql
select * from pg_show_replication_origin_status();

rdb=> select * from pg_show_replication_origin_status();
 local_id | external_id | remote_lsn | local_lsn  
----------+-------------+------------+------------
        1 | pg_110499   | 0/306DC150 | B/E103DA48
(1 row)
```

### Publisher側のWALのLSNの位置を確認

***

```sql
SELECT pg_current_wal_lsn();

rdb=> SELECT pg_current_wal_lsn();
 pg_current_wal_lsn 
--------------------
 0/306E3BF8
(1 row)
```

### Subscribe側のLSNの位置を変更

***

```sql
SELECT pg_replication_origin_advance('pg_110499', '0/306E3BF8');

rdb=> select * from pg_show_replication_origin_status();
 local_id | external_id | remote_lsn | local_lsn 
----------+-------------+------------+-----------
        1 | pg_43450    | 0/3006B190 | 0/0
(1 row)
```

読み取り位置が変更されることにより、競合が発生しなくなる。

