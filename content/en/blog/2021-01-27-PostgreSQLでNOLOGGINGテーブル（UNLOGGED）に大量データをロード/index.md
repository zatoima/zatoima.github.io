---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Loading Large Amounts of Data into NOLOGGING (UNLOGGED) Tables in PostgreSQL"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-postgresql-nologging-load.html
date: 2021-01-27
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

# What are UNLOGGED Tables?

UNLOGGED tables are the equivalent of NOLOGGING tables in Oracle Database - they are tables that do not write to WAL, which enables faster performance. However, since there is no WAL data in the event of a crash, recovery is not possible.

That said, they are effective for retryable operations such as data loading, so I'll verify that along with the performance impact.

# How to Configure

Either add an option during table creation or use an ALTER TABLE statement. This time I'll use ALTER TABLE.

```
ALTER TABLE aozora SET UNLOGGED;
ALTER TABLE aozora SET LOGGED;
```

> CREATE TABLE https://www.postgresql.jp/document/12/html/sql-createtable.html
>
> ALTER TABLE https://www.postgresql.jp/document/12/html/sql-altertable.html

# Table Creation

Prepare a table to load text data from the Aozora Bunko (Japanese literary database).

```
CREATE TABLE aozora(file VARCHAR(30),num INT,row INT,word TEXT,subtype1 VARCHAR(30),subtype2 VARCHAR(30),subtype3 VARCHAR(30),subtype4 VARCHAR(10),conjtype VARCHAR(15),conjugation VARCHAR(15),basic TEXT,ruby TEXT,pronunce TEXT );
ALTER TABLE aozora SET UNLOGGED;
```

After creation, checking the table definition shows `Unlogged table "public.aozora"`.

```
postgres=> \d aozora
                    Unlogged table "public.aozora"
   Column    |         Type          | Collation | Nullable | Default
-------------+-----------------------+-----------+----------+---------
 file        | character varying(30) |           |          |
 num         | integer               |           |          |
 row         | integer               |           |          |
 word        | text                  |           |          |
 subtype1    | character varying(30) |           |          |
 subtype2    | character varying(30) |           |          |
 subtype3    | character varying(30) |           |          |
 subtype4    | character varying(10) |           |          |
 conjtype    | character varying(15) |           |          |
 conjugation | character varying(15) |           |          |
 basic       | text                  |           |          |
 ruby        | text                  |           |          |
 pronunce    | text                  |           |          |
```

# Results

The UNLOGGED table was about 30% faster.

| Table Type     | Time    |
| -------------- | ------- |
| UNLOGGED table | 0:04:41 |
| LOGGED table   | 0:06:11 |

#### UNLOGGED Table

```
[ec2-user@bastin ~]$ time psql -h aurorav1.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "COPY aozora(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < /home/ec2-user/utf8_all.csv
COPY 87701673

real	4m41.921s
user	0m19.347s
sys	0m6.618s
```

#### LOGGED Table

```
[ec2-user@bastin ~]$ time psql -h aurorav1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "COPY aozora(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < /home/ec2-user/utf8_all.csv
COPY 87701673

real	6m11.123s
user	0m18.744s
sys	0m6.738s
```
