---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Performance Difference Between numeric and int Types in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-compare-performance-numeric-integer.html
date: 2020-05-02
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



While reading the PostgreSQL manual, I found this note:

> 8.1. Numeric Types https://www.postgresql.jp/document/11/html/datatype-numeric.html
>
> Calculations on numeric values are very slow compared to integer types or floating-point data types described in the next section.

I was curious how much of a difference there actually is, so I tested it on a real machine.

#### Create Table with numeric Type

```sql
CREATE TABLE t1(id numeric primary key,num text,data numeric,date timestamp with time zone);
```

```sql
postgres=> \d t1;
                         Table "public.t1"
 Column |           Type           | Collation | Nullable | Default
--------+--------------------------+-----------+----------+---------
 id     | numeric                  |           | not null |
 num    | text                     |           |          |
 data   | numeric                  |           |          |
 date   | timestamp with time zone |           |          |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (id)
```

#### Create Table with integer Type

```sql
CREATE TABLE t1(id numeric primary key,num text,data integer,date timestamp with time zone);
```

```sql
postgres=# \d t1;
                         Table "public.t1"
 Column |           Type           | Collation | Nullable | Default
--------+--------------------------+-----------+----------+---------
 id     | numeric                  |           | not null |
 num    | text                     |           |          |
 data   | integer                  |           |          |
 date   | timestamp with time zone |           |          |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (id)

```

#### Generate Large Dataset (50 Million Rows)

```sql
truncate table t1;
insert into t1
SELECT num                         a
      ,'1'                         b
      ,floor(random() * 1000000)   c
      ,current_timestamp           d
FROM   generate_series(1,50000000) num
;
```

Measure using `\timing` to avoid extra overhead. Also adjust parameters to prevent parallel query execution.

```sql
\timing
SET max_parallel_workers_per_gather TO 0;

SELECT SUM(data) FROM t1;
SELECT AVG(data) FROM t1;
SELECT STDDEV(data) FROM t1;
```

To avoid cache effects, restart PostgreSQL and clear the filesystem cache as a precaution.

```sql
pg_ctl stop
sudo "echo 3 > /proc/sys/vm/drop_caches"
pg_ctl start
```

#### Results

The number of runs is small so it's hard to draw firm conclusions, but here are the results. Keep data type choice in mind when designing schemas.

|        | numeric (ms) | integer (ms) | Ratio    |
| ------ | ------------ | ------------ | -------- |
| SUM    | 9403.565     | 8508.652     | 0.904833 |
| AVG    | 8590.127     | 8886.078     | 1.034452 |
| STDDEV | 12419.859    | 8325.705     | 0.670354 |
