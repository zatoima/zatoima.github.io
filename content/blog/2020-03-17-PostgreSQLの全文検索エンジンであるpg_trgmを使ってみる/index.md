---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLの全文検索エンジンであるpg_trgmを使ってみる"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg_trgm-about.html
date: 2020-03-17
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

PostgreSQLでIndexを利用した「中間一致検索」を行うケース。通常のB-Treeインデックスの場合、中間一致検索時は使用できない。pg_trgmというPostgreSQLの全文検索エンジンを使用することによって中間一致検索を手軽に行うことが出来る。pg_bigmやPGroongaもあるが、今回はcontribに含まれているpg_trgmを試してみる。

#### バージョン

```
postgres=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
```

#### pg_trgmの有効化

```sh
postgres=# CREATE EXTENSION pg_trgm;
CREATE EXTENSION
postgres=# \dx
                                    List of installed extensions
  Name   | Version |   Schema   |                            Description                            
---------+---------+------------+-------------------------------------------------------------------
 pg_trgm | 1.3     | public     | text similarity measurement and index searching based on trigrams
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(2 rows)
```

##### テストデータを適当に作る（1億件のテキストデータ）

```sql
CREATE TABLE t1 AS
SELECT to_char(num,'FM0000000000000000') textdata
FROM   generate_series(1,10000000) num
;
```

##### 検索対象のテキストデータを挿入

```sql
insert into t1 values('test1test2test3');
insert into t1 values('メロスは激怒した。必ず、かの 邪智暴虐 （ じゃちぼうぎゃく ） の王を除かなければならぬと決意した。');
```

ここまでで1億2件のデータがテーブルに格納されている。

```sql
select count(*) from t1;

postgres=# select count(*) from t1;
   count   
-----------
 100000002
(1 row)
```

##### "test2"が含まれる中間検索

```sql
explain analyze select * from t1 where textdata like '%test2%';
```

##### explain analyze結果

`Execution time: 10061.160 ms`ほど時間が掛かっている。約10秒。テーブルのフルスキャンとなるので遅い。

```sql
postgres=# explain analyze select * from t1 where textdata like '%test2%';
                                                         QUERY PLAN                                                          
-----------------------------------------------------------------------------------------------------------------------------
 Gather  (cost=1000.00..1159776.58 rows=10000 width=17) (actual time=10059.633..10061.097 rows=1 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on t1  (cost=0.00..1157776.58 rows=4167 width=17) (actual time=10053.097..10053.098 rows=0 loops=3)
         Filter: (textdata ~~ '%test2%'::text)
         Rows Removed by Filter: 33333334
 Planning time: 0.938 ms
 Execution time: 10061.160 ms
(8 rows)
```

##### ""邪智暴虐""が含まれる中間検索

```sql
explain analyze select * from t1 where textdata like '%邪智暴虐%';
```

##### explain analyze結果

`Execution time: 9982.465 ms`ほど時間が掛かっている。こちらも同じく約10秒。

```sql
postgres=# explain analyze select * from t1 where textdata like '%邪智暴虐%';
                                                        QUERY PLAN                                                         
---------------------------------------------------------------------------------------------------------------------------
 Gather  (cost=1000.00..1159776.58 rows=10000 width=17) (actual time=9982.347..9982.403 rows=1 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on t1  (cost=0.00..1157776.58 rows=4167 width=17) (actual time=9977.282..9977.282 rows=0 loops=3)
         Filter: (textdata ~~ '%邪智暴虐%'::text)
         Rows Removed by Filter: 33333334
 Planning time: 0.052 ms
 Execution time: 9982.465 ms
(8 rows)
```

全文検索用のインデックスの作成

```sql
create index pg_trgm_idx on t1 USING gin(textdata gin_trgm_ops);
```

作成完了まで約300秒掛かっている。

```sh
[2020-03-16 21:27:36 JST]postgres postgres 4539[53] LOG:  statement: create index pg_trgm_idx on t1 USING gin(textdata gin_trgm_ops);
[2020-03-16 21:32:39 JST]postgres postgres 4539[54] LOG:  duration: 303535.309 ms
```

テーブルのサイズは約5217.8MB=約5GB程度。インデックスのサイズは約1,461MB=約1GB。全文検索用のインデックスの場合はテーブルサイズ＜インデックスサイズとなると思ってた。テスト用データが原因かもしれない。

```sql
SELECT
    objectname,
    TO_CHAR(pg_relation_size(objectname::regclass),'999,999,999,999') AS bytes
FROM
    (
    SELECT
        tablename AS objectname
    FROM
        pg_tables
    WHERE
        schemaname = 'public'
    UNION
    SELECT
        indexname AS objectname
    FROM
        pg_indexes
    WHERE
        schemaname = 'public'
    ) AS objectlist
ORDER BY
    bytes DESC;
    
 objectname  |      bytes       
-------------+------------------
 t1          |    5,217,837,056
 pg_trgm_idx |    1,461,542,912
(2 rows)

```

##### test2が含まれる中間検索

```sql
explain analyze select * from t1 where textdata like '%test2%';
```

##### explain analyze結果

`Execution time: 10061.160 ms`ほど時間が掛かっていた検索が`0.090 ms`で完了。

```sql
postgres=# explain analyze select * from t1 where textdata like '%test2%';
                                                        QUERY PLAN                                                        
--------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on t1  (cost=285.50..36386.84 rows=10000 width=17) (actual time=0.021..0.022 rows=1 loops=1)
   Recheck Cond: (textdata ~~ '%test2%'::text)
   Heap Blocks: exact=1
   ->  Bitmap Index Scan on pg_trgm_idx  (cost=0.00..283.00 rows=10000 width=0) (actual time=0.016..0.016 rows=1 loops=1)
         Index Cond: (textdata ~~ '%test2%'::text)
 Planning time: 1.148 ms
 Execution time: 0.090 ms
(7 rows)
```

##### 邪智暴虐が含まれる中間検索

```sql
explain analyze select * from t1 where textdata like '%邪智暴虐%';
```

##### explain analyze結果

`Execution time: 9982.465 ms`ほど時間が掛かっていた検索が`0.044 ms`で完了。

```sql
postgres=# explain analyze select * from t1 where textdata like '%邪智暴虐%';
                                                        QUERY PLAN                                                        
--------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on t1  (cost=217.50..36318.84 rows=10000 width=17) (actual time=0.022..0.022 rows=1 loops=1)
   Recheck Cond: (textdata ~~ '%邪智暴虐%'::text)
   Heap Blocks: exact=1
   ->  Bitmap Index Scan on pg_trgm_idx  (cost=0.00..215.00 rows=10000 width=0) (actual time=0.017..0.017 rows=1 loops=1)
         Index Cond: (textdata ~~ '%邪智暴虐%'::text)
 Planning time: 0.107 ms
 Execution time: 0.044 ms
(7 rows)
```

なお、トライグラム（tri-gram）の性質上、致し方ないが、2文字以下の検索は激遅になるので注意。

```sql
postgres=# explain analyze select * from t1 where textdata like '%邪智%';
                                                                 QUERY PLAN                                                                  
------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on t1  (cost=758005.50..794106.84 rows=10000 width=17) (actual time=169524.760..169524.761 rows=1 loops=1)
   Recheck Cond: (textdata ~~ '%邪智%'::text)
   Rows Removed by Index Recheck: 100000001
   Heap Blocks: exact=636943
   ->  Bitmap Index Scan on pg_trgm_idx  (cost=0.00..758003.00 rows=10000 width=0) (actual time=26370.882..26370.882 rows=100000002 loops=1)
         Index Cond: (textdata ~~ '%邪智%'::text)
 Planning time: 0.261 ms
 Execution time: 169524.849 ms
(8 rows)

postgres=# 

```

#### Recheck Cond について

下記の記事がすごくわかりやすかった。

> Bitmap Index Scan の後の Bitmap Heap Scan でRecheck処理が行われることの解説 - ぱと隊長日誌 https://taityo-diary.hatenablog.jp/entry/2018/07/07/071928

> postgresql - What does "Recheck Cond" in Explain result mean? - Stack Overflow https://stackoverflow.com/questions/50959814/what-does-recheck-cond-in-explain-result-mean/50961326#50961326

### 追記

データを青空文庫のテキストデータに変更してみたらこうなった。想定通り、テーブルサイズよりインデックスサイズの方が大きくなった。

```sql
postgres=# SELECT * FROM pgstattuple('aozoradata');
-[ RECORD 1 ]------+----------
table_len          | 807690240
tuple_count        | 3533485
tuple_len          | 774167704
tuple_percent      | 95.85
dead_tuple_count   | 0
dead_tuple_len     | 0
dead_tuple_percent | 0
free_space         | 3066496
free_percent       | 0.38

postgres=# \d aozoradata
                            Table "public.aozoradata"
 Column |  Type   | Collation | Nullable |                Default                 
--------+---------+-----------+----------+----------------------------------------
 id     | integer |           | not null | nextval('aozoradata_id_seq'::regclass)
 data   | text    |           | not null | 
```

```sql
postgres=# SELECT
postgres-#     objectname,
postgres-#     TO_CHAR(pg_relation_size(objectname::regclass),'999,999,999,999') AS bytes
postgres-# FROM
postgres-#     (
postgres(#     SELECT
postgres(#         tablename AS objectname
postgres(#     FROM
postgres(#         pg_tables
postgres(#     WHERE
postgres(#         schemaname = 'public'
postgres(#     UNION
postgres(#     SELECT
postgres(#         indexname AS objectname
postgres(#     FROM
postgres(#         pg_indexes
postgres(#     WHERE
postgres(#         schemaname = 'public'
postgres(#     ) AS objectlist
postgres-# ORDER BY
postgres-#     bytes DESC;
   objectname   |      bytes       
----------------+------------------
 aozoradata     |      807,690,240
 aozoradata_idx |    1,156,775,936
(2 rows)
```

