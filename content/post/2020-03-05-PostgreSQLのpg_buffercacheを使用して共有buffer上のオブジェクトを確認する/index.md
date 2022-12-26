---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_buffercacheを使用して共有buffer上のオブジェクトを確認する"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-pg_buffercache.html
date: 2020-03-05
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



### はじめに

contribモジュールにpg_buffercacheというPostgreSQLのバッファ・キャッシュの使用状況を確認できる拡張機能がありますので使ってみます。Oracleでいうところのx$bh表かな、と思っています。

### バージョンについて

```sh
postgres=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### pg_buffercacheのインストール

```sh
postgres=# CREATE EXTENSION pg_buffercache;
CREATE EXTENSION
postgres=# \dx
                                     List of installed extensions
        Name        | Version |   Schema   |                        Description                        
--------------------+---------+------------+-----------------------------------------------------------
 pg_buffercache     | 1.3     | public     | examine the shared buffer cache
 pg_stat_statements | 1.6     | public     | track execution statistics of all SQL statements executed
 plpgsql            | 1.0     | pg_catalog | PL/pgSQL procedural language
(3 rows)

postgres=# 
postgres=# \dx+
Objects in extension "pg_buffercache"
       Object description        
---------------------------------
 function pg_buffercache_pages()
 view pg_buffercache
(2 rows)
```

pg_buffercacheはcontribモジュールの一つなので必要に応じてcontribのインストールも実施が必要です。

```sh
sudo yum -y install postgresql10-devel postgresql10-contrib
```

## 使用方法

pg_buffercacheは1行ごとに各バッファの情報が記載されます。したがって、1バッファページは`8KB単位`となるので、`shared_buffers`が`128MB`の場合はページ数は`16384`となります。

```sql
postgres=# show shared_buffers;
 shared_buffers 
----------------
 128MB
(1 row)
postgres=# SELECT count(*) FROM pg_buffercache;
 count 
-------
 16384
(1 row)
```

pg_buffercacheビューの各列の説明は次の通りです。

```sql
postgres=# \d pg_buffercache
                 View "public.pg_buffercache"
      Column      |   Type   | Collation | Nullable | Default 
------------------+----------+-----------+----------+---------
 bufferid         | integer  |           |          | 
 relfilenode      | oid      |           |          | 
 reltablespace    | oid      |           |          | 
 reldatabase      | oid      |           |          | 
 relforknumber    | smallint |           |          | 
 relblocknumber   | bigint   |           |          | 
 isdirty          | boolean  |           |          | 
 usagecount       | smallint |           |          | 
 pinning_backends | integer  |           |          | 
```

| 名前             | 型       | 参照                 | 説明                                                       |
| ---------------- | -------- | -------------------- | ---------------------------------------------------------- |
| bufferid         | integer  |                      | 1からshared_buffersまでの範囲で示されるID                  |
| relfilenode      | oid      | pg_class.relfilenode | リレーションのファイルノード番号                           |
| reltablespace    | oid      | pg_tablespace.oid    | リレーションのテーブル空間OID                              |
| reldatabase      | oid      | pg_database.oid      | リレーションのデータベースOID                              |
| relforknumber    | smallint |                      | リレーション内のフォーク番号。include/common/relpath.h参照 |
| relblocknumber   | bigint   |                      | リレーション内のページ番号                                 |
| isdirty          | boolean  |                      | ダーティページかどうか                                     |
| usagecount       | smallint |                      | Clock-sweepアクセスカウント                                |
| pinning_backends | integer  |                      | このバッファをピン留めしているバックエンドの数             |

##### テーブルごとのバッファページ数を集計

```sql
SELECT
    c.relname,
    COUNT(*) AS buffers
FROM
    pg_buffercache b
    INNER JOIN
        pg_class c
    ON  b.relfilenode = pg_relation_filenode(c.oid)
    AND b.reldatabase IN(0,(
                SELECT
                    oid
                FROM
                    pg_database
                WHERE
                    datname = current_database()
            ))
GROUP BY c.relname
ORDER BY 2 DESC
LIMIT 10
;
```

##### 出力結果

```sh
        relname        | buffers 
-----------------------+---------
 pgbench_accounts      |    1644
 pgbench_accounts_pkey |     276
 pg_proc               |      78
 pg_depend             |      59
 pg_toast_2618         |      56
 pg_attribute          |      53
 pg_collation          |      53
 pg_description        |      43
 test                  |      35
 pg_statistic          |      35
(10 rows)
```

##### データベース、テーブルごとのバッファページ数を集計

```sql
SELECT
    d.datname,
    c.relname,
    count(*)
FROM
    pg_buffercache b
    LEFT OUTER JOIN
        (
            SELECT
                oid,
                *
            FROM
                pg_database
            WHERE
                oid = 0
            OR  datname = current_database()
        ) AS d
    ON  b.reldatabase = d.oid
    LEFT OUTER JOIN
        pg_class c
    ON  b.relfilenode = c.relfilenode
GROUP BY
    d.datname,
    c.relname
ORDER BY
    d.datname,
    c.relname
;
```

##### 出力結果

```sh
 datname  |                 relname                  | count 
----------+------------------------------------------+-------
 postgres | pg_aggregate                             |     6
 postgres | pg_aggregate_fnoid_index                 |     2
 postgres | pg_am                                    |     5
 postgres | pg_amop                                  |    10
 postgres | pg_amop_fam_strat_index                  |     4
 postgres | pg_amop_opr_fam_index                    |     4
 postgres | pg_amproc                                |     8
 postgres | pg_amproc_fam_proc_index                 |     4
 postgres | pg_amproc_oid_index                      |     3
 postgres | pg_attrdef_adrelid_adnum_index           |     1
```

##### ダーティー状態でまだ書き込まれていないバッファ情報を取得

```sql
SELECT c.relname, count(*) AS buffers
    FROM pg_buffercache b INNER JOIN pg_class c
    ON b.relfilenode = pg_relation_filenode(c.oid) AND
          b.reldatabase IN (0, (SELECT oid FROM pg_database WHERE datname = current_database()))
          AND
          b.isdirty = true
             GROUP BY c.relname
             ORDER BY 2 DESC
             LIMIT 100;
```

##### 出力結果

```sh
              relname              | buffers 
-----------------------------------+---------
 pgbench_accounts                  |    1645
 pgbench_accounts_pkey             |     274
 pgbench_history                   |      51
 pgbench_branches                  |      13
 pgbench_tellers                   |      10
 pg_class                          |       1
 pgbench_tellers_pkey              |       1
 pg_class_oid_index                |       1
 pg_class_relname_nsp_index        |       1
 pg_class_tblspc_relfilenode_index |       1
 pgbench_branches_pkey             |       1
(11 rows)
```

checkpoint を発行すると当然ダーティーページはなくなります。

```sql
postgres=# checkpoint;
CHECKPOINT
postgres=# 
postgres=# SELECT c.relname, count(*) AS buffers
    FROM pg_buffercache b INNER JOIN pg_class c
    ON b.relfilenode = pg_relation_filenode(c.oid) AND
          b.reldatabase IN (0, (SELECT oid FROM pg_database WHERE datname = current_database()))
          AND
          b.isdirty = true
             GROUP BY c.relname
             ORDER BY 2 DESC
             LIMIT 100;
 relname | buffers 
---------+---------
(0 rows)

postgres=# 
```

##### どのくらいの共有バッファが未使用か

未使用のバッファはnullなのでcountの引数を変えることで確認可能なはず。

```sql
postgres=# select count(*) as shared_buffer_count, COUNT(relfilenode) as free_in_use_count, count(*) - COUNT(relfilenode) as free_buffer_count from pg_buffercache;
 shared_buffer_count | free_in_use_count | free_buffer_count 
---------------------+-------------------+-------------------
               16384 |              7093 |              9291
(1 row)
```

### 参考

> F.25. pg_buffercache https://www.postgresql.jp/document/10/html/pgbuffercache.html

> PostgreSQL Deep Dive: pg_buffercacheで共有バッファを覗いてみる http://pgsqldeepdive.blogspot.com/2012/12/pgbuffercache.html