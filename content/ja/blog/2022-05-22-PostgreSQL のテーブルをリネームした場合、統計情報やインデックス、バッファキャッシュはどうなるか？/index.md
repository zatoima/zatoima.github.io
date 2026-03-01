---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQL のテーブルをリネームした場合、統計情報やインデックス、バッファキャッシュはどうなるか？"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: aws-postgresql-rename-table-index-analyze-buffer
date: 2022-05-22
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

### 結論

- バッファキャッシュ、インデックス、統計情報はリネーム先に引き継がれる

### コマンド

```sql
-- テーブル準備
create table t1_work(a numeric primary key,b varchar(20));
insert into t1_work values(1,'test');

-- pg_buffercacheの有効化
create extension pg_buffercache;

-- 統計情報の確認
analyze t1_work;
select * from pg_stat_user_tables where relname='t1_work';

-- インデックス情報の確認
select * from pg_indexes where tablename='t1_work';

-- キャッシュ情報の確認
select c.relname, count(*) as buffers
from pg_buffercache as b
inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
where c.relname='t1_work'
group by c.relname
order by 2 desc
LIMIT 30;

-- テーブル名の変更
ALTER TABLE t1_work RENAME TO t1;

-- 統計情報の確認
select * from pg_stat_user_tables where relname='t1';

-- インデックス情報の確認
select * from pg_indexes where tablename='t1';

-- キャッシュ確認
select c.relname, count(*) as buffers
from pg_buffercache as b
inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
where c.relname='t1'
group by c.relname
order by 2 desc
LIMIT 30;

-- テーブル削除
drop table t1;
drop table t1_work;
```

### バッファキャッシュ

##### リネーム前

```sql
postgres=> select c.relname, count(*) as buffers
postgres-> from pg_buffercache as b
postgres-> inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
postgres-> where c.relname='t1_work'
postgres-> group by c.relname
postgres-> order by 2 desc
postgres-> LIMIT 30;
 relname | buffers 
---------+---------
 t1_work |       1
(1 row)
```

##### リネーム後

```sql
postgres=> select c.relname, count(*) as buffers
postgres-> from pg_buffercache as b
postgres-> inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
postgres-> where c.relname='t1'
postgres-> group by c.relname
postgres-> order by 2 desc
postgres-> LIMIT 30;
 relname | buffers 
---------+---------
 t1      |       1
(1 row)
```

### 統計情報

##### リネーム前

```sql
postgres=> select * from pg_stat_user_tables where relname='t1_work';
 relid | schemaname | relname | seq_scan | seq_tup_read | idx_scan | idx_tup_fetch | n_tup_ins | n_tup_upd | n_tup_del | n_tup_hot_upd | n_live_tup | n_dead_tup | n_mod_since_analyze | n_ins_since_vacuum | last_vacuum | last_autovacuum |         last_analyze          | last_autoanalyze | vacuum_count | autovacuum_c
ount | analyze_count | autoanalyze_count 
-------+------------+---------+----------+--------------+----------+---------------+-----------+-----------+-----------+---------------+------------+------------+---------------------+--------------------+-------------+-----------------+-------------------------------+------------------+--------------+-------------
-----+---------------+-------------------
 24688 | public     | t1_work |        1 |            0 |        0 |             0 |         1 |         0 |         0 |             0 |          1 |          0 |                   0 |                  1 |             |                 | 2022-05-18 04:21:08.540609+00 |                  |            0 |             
   0 |             1 |                 0
(1 row)
```

##### リネーム後

```sql
postgres=> select * from pg_stat_user_tables where relname='t1';
 relid | schemaname | relname | seq_scan | seq_tup_read | idx_scan | idx_tup_fetch | n_tup_ins | n_tup_upd | n_tup_del | n_tup_hot_upd | n_live_tup | n_dead_tup | n_mod_since_analyze | n_ins_since_vacuum | last_vacuum | last_autovacuum |         last_analyze          | last_autoanalyze | vacuum_count | autovacuum_c
ount | analyze_count | autoanalyze_count 
-------+------------+---------+----------+--------------+----------+---------------+-----------+-----------+-----------+---------------+------------+------------+---------------------+--------------------+-------------+-----------------+-------------------------------+------------------+--------------+-------------
-----+---------------+-------------------
 24688 | public     | t1      |        1 |            0 |        0 |             0 |         1 |         0 |         0 |             0 |          1 |          0 |                   0 |                  1 |             |                 | 2022-05-18 04:21:08.540609+00 |                  |            0 |             
   0 |             1 |                 0
(1 row)
```

##### インデックス

##### リネーム前

```sql
postgres=> select * from pg_indexes where tablename='t1_work';
 schemaname | tablename |  indexname   | tablespace |                              indexdef                              
------------+-----------+--------------+------------+--------------------------------------------------------------------
 public     | t1_work   | t1_work_pkey |            | CREATE UNIQUE INDEX t1_work_pkey ON public.t1_work USING btree (a)
(1 row)
```

##### リネーム後

```sql
postgres=> select * from pg_indexes where tablename='t1';
 schemaname | tablename |  indexname   | tablespace |                           indexdef                            
------------+-----------+--------------+------------+---------------------------------------------------------------
 public     | t1        | t1_work_pkey |            | CREATE UNIQUE INDEX t1_work_pkey ON public.t1 USING btree (a)
(1 row)
```

### 実行ログ

```sh
postgres=> create table t1_work(a numeric primary key,b varchar(20));
CREATE TABLE
postgres=> insert into t1_work values(1,'test');
INSERT 0 1
postgres=> create extension pg_buffercache;
ERROR:  extension "pg_buffercache" already exists
postgres=> \dx
                            List of installed extensions
      Name      | Version |   Schema   |                 Description                 
----------------+---------+------------+---------------------------------------------
 aws_commons    | 1.2     | public     | Common data types across AWS services
 aws_s3         | 1.1     | public     | AWS S3 extension for importing data from S3
 pg_buffercache | 1.3     | public     | examine the shared buffer cache
 plpgsql        | 1.0     | pg_catalog | PL/pgSQL procedural language
(4 rows)

postgres=> analyze t1_work;
ANALYZE
postgres=> select * from pg_stat_user_tables where relname='t1_work';
 relid | schemaname | relname | seq_scan | seq_tup_read | idx_scan | idx_tup_fetch | n_tup_ins | n_tup_upd | n_tup_del | n_tup_hot_upd | n_live_tup | n_dead_tup | n_mod_since_analyze | n_ins_since_vacuum | last_vacuum | last_autovacuum |         last_analyze          | last_autoanalyze | vacuum_count | autovacuum_c
ount | analyze_count | autoanalyze_count 
-------+------------+---------+----------+--------------+----------+---------------+-----------+-----------+-----------+---------------+------------+------------+---------------------+--------------------+-------------+-----------------+-------------------------------+------------------+--------------+-------------
-----+---------------+-------------------
 24688 | public     | t1_work |        1 |            0 |        0 |             0 |         1 |         0 |         0 |             0 |          1 |          0 |                   0 |                  1 |             |                 | 2022-05-18 04:21:08.540609+00 |                  |            0 |             
   0 |             1 |                 0
(1 row)

postgres=> select * from pg_indexes where tablename='t1_work';
 schemaname | tablename |  indexname   | tablespace |                              indexdef                              
------------+-----------+--------------+------------+--------------------------------------------------------------------
 public     | t1_work   | t1_work_pkey |            | CREATE UNIQUE INDEX t1_work_pkey ON public.t1_work USING btree (a)
(1 row)

postgres=> select c.relname, count(*) as buffers
postgres-> from pg_buffercache as b
postgres-> inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
postgres-> where c.relname='t1_work'
postgres-> group by c.relname
postgres-> order by 2 desc
postgres-> LIMIT 30;
 relname | buffers 
---------+---------
 t1_work |       1
(1 row)

postgres=> ALTER TABLE t1_work RENAME TO t1;
ALTER TABLE
postgres=> select * from pg_stat_user_tables where relname='t1';
 relid | schemaname | relname | seq_scan | seq_tup_read | idx_scan | idx_tup_fetch | n_tup_ins | n_tup_upd | n_tup_del | n_tup_hot_upd | n_live_tup | n_dead_tup | n_mod_since_analyze | n_ins_since_vacuum | last_vacuum | last_autovacuum |         last_analyze          | last_autoanalyze | vacuum_count | autovacuum_c
ount | analyze_count | autoanalyze_count 
-------+------------+---------+----------+--------------+----------+---------------+-----------+-----------+-----------+---------------+------------+------------+---------------------+--------------------+-------------+-----------------+-------------------------------+------------------+--------------+-------------
-----+---------------+-------------------
 24688 | public     | t1      |        1 |            0 |        0 |             0 |         1 |         0 |         0 |             0 |          1 |          0 |                   0 |                  1 |             |                 | 2022-05-18 04:21:08.540609+00 |                  |            0 |             
   0 |             1 |                 0
(1 row)

postgres=> select * from pg_indexes where tablename='t1';
 schemaname | tablename |  indexname   | tablespace |                           indexdef                            
------------+-----------+--------------+------------+---------------------------------------------------------------
 public     | t1        | t1_work_pkey |            | CREATE UNIQUE INDEX t1_work_pkey ON public.t1 USING btree (a)
(1 row)

postgres=> select c.relname, count(*) as buffers
postgres-> from pg_buffercache as b
postgres-> inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
postgres-> where c.relname='t1'
postgres-> group by c.relname
postgres-> order by 2 desc
postgres-> LIMIT 30;
 relname | buffers 
---------+---------
 t1      |       1
(1 row)

postgres=> 
postgres=> 
postgres=> select c.relname, count(*) as buffers
postgres-> from pg_buffercache as b
postgres-> inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
postgres-> where c.relname like 't1%'
postgres-> group by c.relname
postgres-> order by 2 desc
postgres-> LIMIT 30;
   relname    | buffers 
--------------+---------
 t1_work_pkey |       2
 t1           |       1
(2 rows)

postgres=> 
postgres=> drop table t1;
DROP TABLE
postgres=> drop table t1_work;
ERROR:  table "t1_work" does not exist
postgres=> 
```

