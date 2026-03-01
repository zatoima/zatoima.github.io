---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQL上のnumeric型とint型の性能差"
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



PostgreSQLのマニュアルを見ていたらこんな記載が。

> 8.1. 数値データ型 https://www.postgresql.jp/document/11/html/datatype-numeric.html
>
> numericの値に対する計算は整数型、もしくは次節で説明する浮動小数点データ型に比較し非常に遅くなります。

どのくらいの差が生じるのか気になったので実機で確認してみた。

#### numericのテーブル作成

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

#### integerのテーブル作成

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

#### データの大量生成(5000万件)

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

余計な負荷が掛からないようにtimingで計測する。パラレルクエリで走らないようにパラメータを調整する。

```sql
\timing
SET max_parallel_workers_per_gather TO 0;

SELECT SUM(data) FROM t1;
SELECT AVG(data) FROM t1;
SELECT STDDEV(data) FROM t1;
```

キャッシュの影響を受けないように、念の為PostgreSQLの再起動とファイルシステム側のキャッシュのクリアをしている。

```sql
pg_ctl stop
sudo "echo 3 > /proc/sys/vm/drop_caches"
pg_ctl start
```

#### 結果

回数が少ないので何とも言えないがこんな結果に。データ型の検討時には注意をしよう。

|        | numeric   | integer  | 性能差   |
| ------ | --------- | -------- | -------- |
| SUM    | 9403.565  | 8508.652 | 0.904833 |
| AVG    | 8590.127  | 8886.078 | 1.034452 |
| STDDEV | 12419.859 | 8325.705 | 0.670354 |





