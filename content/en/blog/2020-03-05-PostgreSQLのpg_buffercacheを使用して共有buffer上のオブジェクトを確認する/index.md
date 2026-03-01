---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Checking Objects on the Shared Buffer with PostgreSQL's pg_buffercache"
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



### Introduction

The contrib module includes an extension called pg_buffercache that lets you check the usage of PostgreSQL's buffer cache. I think it's similar to Oracle's x$bh table.

### Version

```sh
postgres=# select version();
                                                 version
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### Installing pg_buffercache

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

Since pg_buffercache is one of the contrib modules, you may need to install contrib as needed.

```sh
sudo yum -y install postgresql10-devel postgresql10-contrib
```

## Usage

pg_buffercache records information for each buffer per row. Since 1 buffer page is `8KB`, if `shared_buffers` is `128MB`, the number of pages is `16384`.

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

The description of each column in the pg_buffercache view is as follows:

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

| Name             | Type     | Reference            | Description                                                  |
| ---------------- | -------- | -------------------- | ------------------------------------------------------------ |
| bufferid         | integer  |                      | ID ranging from 1 to shared_buffers                          |
| relfilenode      | oid      | pg_class.relfilenode | File node number of the relation                             |
| reltablespace    | oid      | pg_tablespace.oid    | Tablespace OID of the relation                               |
| reldatabase      | oid      | pg_database.oid      | Database OID of the relation                                 |
| relforknumber    | smallint |                      | Fork number within the relation. See include/common/relpath.h |
| relblocknumber   | bigint   |                      | Page number within the relation                              |
| isdirty          | boolean  |                      | Whether the page is dirty                                    |
| usagecount       | smallint |                      | Clock-sweep access count                                     |
| pinning_backends | integer  |                      | Number of backends pinning this buffer                       |

##### Aggregate buffer page counts per table

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

##### Output

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

##### Aggregate buffer page counts per database and table

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

##### Output

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

##### Getting information about dirty buffers not yet written

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

##### Output

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

Issuing a checkpoint will naturally clear all dirty pages.

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

##### How much shared buffer is unused?

Unused buffers have null values, so you can check by changing the argument to count.

```sql
postgres=# select count(*) as shared_buffer_count, COUNT(relfilenode) as free_in_use_count, count(*) - COUNT(relfilenode) as free_buffer_count from pg_buffercache;
 shared_buffer_count | free_in_use_count | free_buffer_count
---------------------+-------------------+-------------------
               16384 |              7093 |              9291
(1 row)
```

### Reference

> F.25. pg_buffercache https://www.postgresql.jp/document/10/html/pgbuffercache.html

> PostgreSQL Deep Dive: Peeking at the Shared Buffer with pg_buffercache http://pgsqldeepdive.blogspot.com/2012/12/pgbuffercache.html
