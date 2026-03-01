---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Resolving Logical Replication Conflict Errors in RDS (PostgreSQL)"
subtitle: " "
summary: " "
tags: ["AWS", "RDS", "PostgreSQL"]
categories: ["AWS", "RDS", "PostgreSQL"]
url: aws-rds-repllication-error-conflict.html
date: 2019-12-13T20:00:00+09:00
lastmod: 2019-12-13T20:00:10+09:00
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



### Causing a Conflict

***

```sql
# Pre-insert a record on the subscriber side
insert into LogicalReplicationTest values (1);

# Insert on the publisher side and let it propagate
insert into LogicalReplicationTest values (1);
```

### Error Confirmation

***

```
2019-11-30 15:13:26 UTC::@:[29680]:ERROR: duplicate key value violates unique constraint "logicalreplicationtest_pkey"
2019-11-30 15:13:26 UTC::@:[29680]:DETAIL: Key (a)=(1) already exists.
2019-11-30 15:13:26 UTC::@:[12125]:LOG: worker process: logical replication worker for subscription 110499 (PID 29680) exited with exit code 1
```

There are two main approaches for handling this:

1. Remove the cause of the conflict
   - In this case, data already existed on the subscriber side, so the solution is to perform maintenance on the subscriber side.
2. Change the LSN apply position on the subscriber side

Here we'll try approach "2. Change the LSN apply position on the subscriber side." The correct approach should be "1. Remove the cause of the conflict."

### Check Current LSN Position

***

```sql
select * from pg_show_replication_origin_status();

rdb=> select * from pg_show_replication_origin_status();
 local_id | external_id | remote_lsn | local_lsn
----------+-------------+------------+------------
        1 | pg_110499   | 0/306DC150 | B/E103DA48
(1 row)
```

### Check WAL LSN Position on Publisher Side

***

```sql
SELECT pg_current_wal_lsn();

rdb=> SELECT pg_current_wal_lsn();
 pg_current_wal_lsn
--------------------
 0/306E3BF8
(1 row)
```

### Change LSN Position on Subscriber Side

***

```sql
SELECT pg_replication_origin_advance('pg_110499', '0/306E3BF8');

rdb=> select * from pg_show_replication_origin_status();
 local_id | external_id | remote_lsn | local_lsn
----------+-------------+------------+-----------
        1 | pg_43450    | 0/3006B190 | 0/0
(1 row)
```

By changing the read position, the conflict no longer occurs.
