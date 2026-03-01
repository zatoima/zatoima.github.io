---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Cannot Access pg_replication_origin_status in RDS (PostgreSQL) (permission denied)"
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


#### Version

***

```sql
rdbtest=> select version();
                                                 version
---------------------------------------------------------------------------------------
 PostgreSQL 10.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5
-11), 64-bit
```

#### Issue

***

When attempting to SELECT from pg_replication_origin_status, a permission denied error occurs. This happens even with the rds_superuser role. This view contains the mapping between the transaction log position (LSN) reflected on the subscriber side and the publisher-side LSN. Not being able to view this information causes operational difficulties during logical replication.

```sql
rdbtest=> SELECT * FROM pg_replication_origin_status;
ERROR:  permission denied for relation pg_replication_origin_status
```

#### Solution

***

Use pg_show_replication_origin_status() to retrieve the LSN information.

```sql
rdbtest=> select * from pg_show_replication_origin_status();
 local_id | external_id | remote_lsn | local_lsn
----------+-------------+------------+-----------
        1 | pg_43450    | 0/28D70910 | 0/0
(1 row)
```

#### References

***

> AWS Developer Forums: RDS Postgres Logical replication access ... [https://forums.aws.amazon.com/thread.jspa?threadID=301094](https://forums.aws.amazon.com/thread.jspa?threadID=301094)
