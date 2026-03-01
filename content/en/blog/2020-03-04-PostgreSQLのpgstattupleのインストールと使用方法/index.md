---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Install and Use PostgreSQL's pgstattuple"
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



With pgstattuple, you can check tuple-level statistics. You can find out the total number of tuples, table size, total number of dead tuples, and free space.

## Version Information

```sh
pgbench=# select version();
                                                 version
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

## Installation

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

Since pgstattuple is one of the contrib modules, you may need to install contrib as needed.

```sh
sudo yum -y install postgresql10-devel postgresql10-contrib
```

## Usage

### Getting Information for a Specific Table

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

#### Description of Each Column

| Column               | Type     | Description                               |
| -------------------- | -------- | ----------------------------------------- |
| `table_len`          | `bigint` | Physical length of the relation in bytes  |
| `tuple_count`        | `bigint` | Number of live tuples                     |
| `tuple_len`          | `bigint` | Physical length of live tuples (in bytes) |
| `tuple_percent`      | `float8` | Percentage of live tuples                 |
| `dead_tuple_count`   | `bigint` | Number of dead tuples                     |
| `dead_tuple_len`     | `bigint` | Total dead tuple length in bytes          |
| `dead_tuple_percent` | `float8` | Percentage of dead tuples                 |
| `free_space`         | `bigint` | Total free space in bytes                 |
| `free_percent`       | `float8` | Percentage of free space                  |



### Getting Information for a Specific Index

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

| Column               | Type      | Description                               |
| -------------------- | --------- | ----------------------------------------- |
| `version`            | `integer` | B-tree version number                     |
| `tree_level`         | `integer` | Tree level of the root page               |
| `index_size`         | `bigint`  | Total number of pages in the index        |
| `root_block_no`      | `bigint`  | Location of the root block                |
| `internal_pages`     | `bigint`  | Number of "internal" (upper-level) pages  |
| `leaf_pages`         | `bigint`  | Number of leaf pages                      |
| `empty_pages`        | `bigint`  | Number of empty pages                     |
| `deleted_pages`      | `bigint`  | Number of deleted pages                   |
| `avg_leaf_density`   | `float8`  | Average density of leaf pages             |
| `leaf_fragmentation` | `float8`  | Fragmentation of leaf pages               |

### Other Notes

Since pgstattuple and pgstatindex always perform a full scan to collect table and index information, care must be taken regarding timing. If you want to avoid a full scan, you can also use the pgstattuple_approx function.

### Reference

> F.31. pgstattuple https://www.postgresql.jp/document/10/html/pgstattuple.html
