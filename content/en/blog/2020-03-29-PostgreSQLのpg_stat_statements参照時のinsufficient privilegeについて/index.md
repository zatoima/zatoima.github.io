---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "About <insufficient privilege> When Viewing pg_stat_statements in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg-stat-statements-insuffient-priviledge
date: 2020-03-29
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---



I noticed a few things worth noting. When viewing pg_stat_statements as a regular (non-superuser) user, `insufficient privilege` appears in the output.

For example, when trying to check queries **executed by user testA** from pg_stat_statements **as user testA**, the output is as follows:

```sh
pgtest=> \c - testa
You are now connected to database "pgtest" as user "testa".
pgtest=> \x
Expanded display is off.
pgtest=> SELECT query FROM pg_stat_statements WHERE dbid=16392 ORDER BY total_time DESC LIMIT 20;
                                                     query
---------------------------------------------------------------------------------------------------------------
 create table userA.pgtesttbl(id numeric primary key, name varchar)
 CREATE SCHEMA userA AUTHORIZATION userA
 SELECT query, calls, total_time, rows FROM pg_stat_statements WHERE dbid=$1 ORDER BY total_time DESC LIMIT $2
 insert into userA.pgtesttbl values($1,$2)
 select oid,datname from pg_database
(5 rows)
```

On the other hand, when **a different user (testB)** tries to get these queries, `insufficient privilege` is output.

```sh
pgtest=> \c - testb
You are now connected to database "pgtest" as user "testb".
pgtest=> SELECT query FROM pg_stat_statements WHERE dbid=16392 ORDER BY total_time DESC LIMIT 20;
          query           | calls | total_time | rows
--------------------------+-------+------------+------
 <insufficient privilege> |     1 |   5.340486 |    0
 <insufficient privilege> |     1 |    0.45077 |    0
 <insufficient privilege> |     3 |   0.288345 |   10
 <insufficient privilege> |     1 |   0.106162 |    1
 <insufficient privilege> |     1 |   0.016645 |    4
```

Unlike Oracle, PostgreSQL does not provide fine-grained access control for system catalogs (including operational statistics views), but I learned that it is implemented to not show queries to users other than the one who executed them.

> F.30. pg_stat_statements https://www.postgresql.jp/document/10/html/pgstatstatements.html
>
> For security reasons, only superusers and members of the `pg_read_all_stats` role are allowed to see the SQL text and `queryid` of queries executed by other users.

The manual above also states that without a specific role, you cannot see SQL text executed by other users. pg_monitor also includes pg_read_all_stats, so either a superuser, pg_read_all_stats, or pg_monitor is sufficient to see all text. Be careful when creating users for monitoring purposes.

For more details about roles, refer to:

> Default Monitoring Roles - Qiita https://qiita.com/nuko_yokohama/items/6debdd3291c8f27d1da8
