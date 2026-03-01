---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Setting Up Logical Replication Between Aurora (PostgreSQL) and RDS (PostgreSQL)"
subtitle: ""
summary: " "
tags: ["AWS", "Aurora", "RDS", "PostgreSQL"]
categories: ["AWS", "Aurora", "RDS", "PostgreSQL"]
url: aws-aurora-rds-postgresql-replication.html
date: 2019-12-25
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



#### Introduction

***

Logical replication became available in PostgreSQL 10. Since Aurora also supports this feature, let's try it. Following this documentation should work without issues.

> Using PostgreSQL Logical Replication with Aurora - Amazon Aurora [https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Replication.Logical.html](https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Replication.Logical.html)

#### Environment

***

Set up a replication environment between Aurora PostgreSQL 10.7 and RDS PostgreSQL 10.7.

#### Notes from the Manual

***

- Enabling the rds.logical_replication parameter affects the performance of the DB cluster.
- To run logical replication for a PostgreSQL database, the AWS user account requires the rds_superuser role.
- To use an existing Aurora PostgreSQL DB cluster as the publisher, the engine version must be 10.6 or later.

#### Prerequisites

***

- Set rds.logical_replication from "0" to "1"

  <img src="image-20191214172939865.png" alt="image-20191214172939865" style="zoom:50%;" />

- Allow communication from PostgreSQL to Aurora in security groups

<img src="image-20191214173509701.png" alt="image-20191214173509701" style="zoom:50%;" />

#### Environment Setup

***

Create the database for replication:

```sql
CREATE DATABASE repdb WITH OWNER postgres;
```

Prepare the table for replication. Since PostgreSQL 10 logical replication does not replicate DDL, this must be done on both Publisher and Subscriber sides.

```sql
\c repdb
CREATE TABLE LogicalReplicationTest (a int PRIMARY KEY);
```

Insert data only on the Publisher side:

```sql
INSERT INTO LogicalReplicationTest VALUES (generate_series(1,10000));
```

Execute "CREATE PUBLICATION" on the Publisher side. Here we chose the "FOR ALL TABLES" option to replicate the entire database.

> https://www.postgresql.jp/document/10/html/sql-createpublication.html
>
> CREATE PUBLICATION
> FOR ALL TABLES
> Marks the publication as one that replicates changes for all tables in the database, including tables created in the future.

```sql
# Connect to repdb
\c repdb

CREATE PUBLICATION alltables FOR ALL TABLES;
```

Execute "CREATE SUBSCRIPTION" on the Subscriber side:

```sql
# Connect to repdb
\c repdb

CREATE SUBSCRIPTION auroratopostgresql CONNECTION 'host=aurorapostgresqlv1.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com port=5432 dbname=repdb user=postgres password=postgres' PUBLICATION alltables;
```

Checking the logs confirms that replication has started (initial synchronization):

```sql
2019-12-14 09:25:49 UTC::@:[16112]:LOG:  logical replication table synchronization worker for subscription "auroratopostgresql", table "logicalreplicationtest" has started
2019-12-14 09:25:49 UTC::@:[16112]:LOG:  logical replication table synchronization worker for subscription "auroratopostgresql", table "logicalreplicationtest" has finished
```

Check pg_subscription_rel to see which tables are subject to logical replication:

```sql
SELECT * FROM pg_subscription_rel;

repdb=> SELECT * FROM pg_subscription_rel;
 srsubid | srrelid | srsubstate | srsublsn
---------+---------+------------+----------
   16425 |   16417 | d          |
(1 row)

repdb=> select relname from pg_class where oid=16417;
        relname
------------------------
 logicalreplicationtest
(1 row)

repdb=>
```

Replication settings can be confirmed from the pg_replication_slots view:

```sql
repdb=> select * from pg_replication_slots;
-[ RECORD 1 ]-------+-------------------
slot_name           | auroratopostgresql
plugin              | pgoutput
slot_type           | logical
datoid              | 24590
database            | repdb
temporary           | f
active              | t
active_pid          | 19407
xmin                |
catalog_xmin        | 23236
restart_lsn         | 0/4F8C710
confirmed_flush_lsn | 0/4F8CAE8

```

From pg_publication on the Publisher side, you can see the definition that was created. Since we chose to replicate all tables in the database, "puballtables" is set to "True":

```sql
repdb=> select * from pg_publication;
-[ RECORD 1 ]+----------
pubname      | alltables
pubowner     | 16393
puballtables | t
pubinsert    | t
pubupdate    | t
pubdelete    | t
```
