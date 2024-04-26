---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpgstattupleのインストールと使用方法"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-how-to-install-and-use-pgstattuple
date: 2020-03-04
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



pgstattupleでタプルレベルの統計情報を確認することが出来ます。タプル総数、テーブルの大きさ、デットタプルの総数や空き容量を知ることが出来ます。

## バージョン情報

```sh
pgbench=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

## インストール

```sh
pgbench=# CREATE EXTENSION pgstattuple;
CREATE EXTENSION
pgbench=# \dx
                   List of installed extensions
    Name     | Version |   Schema   |         Description          
-------------+---------+------------+------------------------------
 pgstattuple | 1.5     | public     | show tuple-level statistics
 plpgsql     | 1.0     | pg_catalog | PL/pgSQL procedural language
(2 rows)

pgbench=# 
pgbench=# 
pgbench=# \dx+
  Objects in extension "pgstattuple"
          Object description           
---------------------------------------
 function pg_relpages(regclass)
 function pg_relpages(text)
 function pgstatginindex(regclass)
 function pgstathashindex(regclass)
 function pgstatindex(regclass)
 function pgstatindex(text)
 function pgstattuple_approx(regclass)
 function pgstattuple(regclass)
 function pgstattuple(text)
(9 rows)
```

pgstattupleはcontribモジュールの一つなので必要に応じてcontribのインストールも実施が必要です。

```sh
sudo yum -y install postgresql10-devel postgresql10-contrib
```

## 使用方法

### 特定テーブルの情報取得

```sh
pgbench=# \dt
              List of relations
 Schema |       Name       | Type  |  Owner   
--------+------------------+-------+----------
 public | pgbench_accounts | table | postgres
 public | pgbench_branches | table | postgres
 public | pgbench_history  | table | postgres
 public | pgbench_tellers  | table | postgres
(4 rows)

pgbench=# SELECT * FROM pgstattuple('pgbench_accounts');
 table_len | tuple_count | tuple_len | tuple_percent | dead_tuple_count | dead_tuple_len | dead_tuple_percent | free_space | free_percent 
-----------+-------------+-----------+---------------+------------------+----------------+--------------------+------------+--------------
  14712832 |      100000 |  12100000 |         82.24 |             3488 |         422048 |               2.87 |     569468 |         3.87
(1 row)
```

#### 各列の説明

| 列                   | 型       | 説明                               |
| -------------------- | -------- | ---------------------------------- |
| `table_len`          | `bigint` | リレーションのバイト単位の物理長   |
| `tuple_count`        | `bigint` | 有効なタプル数                     |
| `tuple_len`          | `bigint` | 有効なタプルの物理長（バイト単位） |
| `tuple_percent`      | `float8` | 有効タプルの割合                   |
| `dead_tuple_count`   | `bigint` | 無効なタプル数                     |
| `dead_tuple_len`     | `bigint` | バイト単位の総不要タプル長         |
| `dead_tuple_percent` | `float8` | 不要タプルの割合                   |
| `free_space`         | `bigint` | バイト単位の総空き領域             |
| `free_percent`       | `float8` | 空き領域の割合                     |



### 特定インデックスの情報取得

```sh
pgbench=# \di
                          List of relations
 Schema |         Name          | Type  |  Owner   |      Table       
--------+-----------------------+-------+----------+------------------
 public | pgbench_accounts_pkey | index | postgres | pgbench_accounts
 public | pgbench_branches_pkey | index | postgres | pgbench_branches
 public | pgbench_tellers_pkey  | index | postgres | pgbench_tellers
(3 rows)

pgbench=# SELECT * FROM pgstatindex('pgbench_accounts_pkey');
 version | tree_level | index_size | root_block_no | internal_pages | leaf_pages | empty_pages | deleted_pages | avg_leaf_density | leaf_fragmentation 
---------+------------+------------+---------------+----------------+------------+-------------+---------------+------------------+--------------------
       2 |          1 |    2260992 |             3 |              1 |        274 |           0 |             0 |            94.57 |                  0
(1 row)
```

| 列                   | 型        | 説明                         |
| -------------------- | --------- | ---------------------------- |
| `version`            | `integer` | B-treeバージョン番号         |
| `tree_level`         | `integer` | ルートページのツリーレベル   |
| `index_size`         | `bigint`  | インデックス内の総ページ数   |
| `root_block_no`      | `bigint`  | ルートブロックの場所         |
| `internal_pages`     | `bigint`  | "内部"（上位レベル）ページ数 |
| `leaf_pages`         | `bigint`  | リーフページ数               |
| `empty_pages`        | `bigint`  | 空ページ数                   |
| `deleted_pages`      | `bigint`  | 削除ページ数                 |
| `avg_leaf_density`   | `float8`  | リーフページの平均密度       |
| `leaf_fragmentation` | `float8`  | リーフページの断片化         |

### その他

pgstattuple、pgstatindexは常に全件走査(Full Scan)を実行してテーブル、インデックスの情報を収集するためタイミングには注意が必要。全件走査(Full Scan)を避けたい場合はpgstattuple_approx関数を使う手もある。

### 参考

> F.31. pgstattuple https://www.postgresql.jp/document/10/html/pgstattuple.html