---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS(PostgreSQL)でpg_replication_origin_statusにアクセス出来ない(permission denied)"
subtitle: ""
summary: " "
tags: ["AWS","RDS","PostgreSQL"]
categories: ["AWS","RDS","PostgreSQL"]
url: aws-rds-pg-replication-origin-status-error.html
date: 2019-12-10
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


#### バージョン

***

```sql
rdbtest=> select version();
                                                 version                                    
---------------------------------------------------------------------------------------
 PostgreSQL 10.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5
-11), 64-bit
```

#### 事象

***

pg_replication_origin_statusの情報をselectしようとするとpermission deniedでエラーが発生する。rds_superuserロールだとしても同様。この情報はsubscriber に反映されている変更のトランザクションログの位置(LSN)の位置とpublisher側のLSNの対応関係が記載されているので、この情報が見れないと論理レプリケーション時の運用時に困る。

```sql
rdbtest=> SELECT * FROM pg_replication_origin_status;
ERROR:  permission denied for relation pg_replication_origin_status
```

#### 対応策

***

pg_show_replication_origin_status()にアクセスしてLSNを取得する。

```sql
rdbtest=> select * from pg_show_replication_origin_status();
 local_id | external_id | remote_lsn | local_lsn 
----------+-------------+------------+-----------
        1 | pg_43450    | 0/28D70910 | 0/0
(1 row)
```

#### 参考

***

> AWS Developer Forums: RDS Postgres Logical replication access ... [https://forums.aws.amazon.com/thread.jspa?threadID=301094](https://forums.aws.amazon.com/thread.jspa?threadID=301094)