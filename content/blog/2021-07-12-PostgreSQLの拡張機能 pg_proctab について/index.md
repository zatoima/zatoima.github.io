---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLの拡張機能 pg_proctab をAurora/RDSから触ってみる"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-postgresql-pg_proctab-extention
date: 2021-07-12
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

Aurora、及びRDS PostgreSQLでサポートされたpg_proctabについてざっと触ってみる。

開発側のリポジトリはこちら。

> pg_proctab / pg_proctab · GitLab https://gitlab.com/pg_proctab/pg_proctab

`PostgreSQL extension to access the operating system process table.`とあるようにPostgreSQLからOS関連の情報を取得出来る関数が提供される模様。

AuroraやRDSの場合、従来であればモニタリングのOSプロセスリストから確認が可能だったが、PostgreSQL側のSQLベースでも確認が可能になった。

![image-20210619221023004](image-20210619221023004.png)

### pg_proctab

```sql
create extension pg_proctab;
\dx
```

### 追加されるファンクション

```sql
select * from pg_cputime();
select * from pg_loadavg();
select * from pg_memusage();
select * from pg_proctab();
```

### 実行結果

```sql
postgres=> create extension pg_proctab;
CREATE EXTENSION
postgres=> 
postgres=> \dx
                       List of installed extensions
    Name    | Version |   Schema   |              Description              
------------+---------+------------+---------------------------------------
 pg_proctab | 0.0.9   | public     | Access operating system process table
 plpgsql    | 1.0     | pg_catalog | PL/pgSQL procedural language
(2 rows)
```

### pg_cputime

```sql
postgres=> select * from pg_cputime();
 user  | nice | system |  idle  | iowait 
-------+------+--------+--------+--------
 28387 | 5841 |  14782 | 362592 |   3942
(1 row)

```

> user: normal processes executing in user mode
>
> nice: niced processes executing in user mode
>
> system: processes executing in kernel mode
>
> idle: processes twiddling thumbs
>
> iowait: waiting for I/O to complete

### pg_loadavg

```sql
postgres=> select * from pg_loadavg();
 load1 | load5 | load15 | last_pid 
-------+-------+--------+----------
 23.92 |  5.71 |   2.02 |    30030
(1 row)
```

> load1: load average of last minute
>
> load5: load average of last 5 minutes
>
> load15: load average of last 15 minutes
>
> last pid: last pid running

### pg_memusage

```sql
postgres=> select * from pg_memusage();
 memused  | memfree | memshared | membuffers | memcached | swapused | swapfree | swapcached 
----------+---------+-----------+------------+-----------+----------+----------+------------
 12767552 | 3357416 |         0 |      62624 |    476284 |        0 |  8384508 |          0
(1 row)
```

> memused: Total physical RAM used
>
> memfree: Total physical RAM not used
>
> memshared: Not used, always 0. (For Solaris.)
>
> membuffers: Temporary storage for raw disk blocks
>
> memcached: In-memory cache for files read from disk
>
> swapused: Total swap space used
>
> swapfree: Memory evicted from RAM that is now temporary on disk
>
> swapcached: Memory that was swapped out, now swapped in but still in swap

### pg_proctab

```sql
postgres=> select * from pg_proctab();
  pid  | comm |                             fullcomm                             | state | ppid | pgrp | session | tty_nr | tpgid | flags | minflt | cminflt | majflt | cmajflt | utime | stime | cutime | cstime | priority | nice | num_threads | itrealvalue | starttime |    vsize    |  rss   | exit_signal | processor
 | rt_priority | policy | delayacct_blkio_ticks | uid | username |  rchar  | wchar | syscr | syscw | reads  | writes | cwrites 
-------+------+------------------------------------------------------------------+-------+------+------+---------+--------+-------+-------+--------+---------+--------+---------+-------+-------+--------+--------+----------+------+-------------+-------------+-----------+-------------+--------+-------------+----------
-+-------------+--------+-----------------------+-----+----------+---------+-------+-------+-------+--------+--------+---------
  9811 |      | postgres: autovacuum launcher                                    | S     | 9657 |      |    9811 |      0 |    -1 |       |   4253 |       0 |      2 |       0 |    10 |    20 |      0 |      0 |       39 |   19 |           1 |           0 |     18573 | 22007947264 |  11400 |          17 |          
 |           0 |      0 |                     0 |     |          | 5641788 |  3309 |  6468 |  2592 | 172032 |      0 |       0
  9813 |      | postgres: logical replication launcher                           | S     | 9657 |      |    9813 |      0 |    -1 |       |    368 |       0 |      2 |       0 |     0 |     0 |      0 |      0 |       39 |   19 |           1 |           0 |     18573 | 22003752960 |  11380 |          17 |          
 |           0 |      0 |                     0 |     |          |   95979 |   726 |    37 |     9 | 454656 |      0 |       0
 15233 |      | postgres: rdsadmin rdsadmin [local] idle                         | S     | 9657 |      |   15233 |      0 |    -1 |       |    638 |       0 |      0 |       0 |    10 |     3 |      0 |      0 |       39 |   19 |           1 |           0 |     28599 | 22114021376 |  17424 |          17 |          
 |           0 |      0 |                     0 |     |          |  237463 |     3 |    71 |     3 |      0 |      0 |       0
 15237 |      | postgres: rdsadmin rdsadmin [local] idle                         | S     | 9657 |      |   15237 |      0 |    -1 |       |    851 |       0 |      0 |       0 |    53 |    10 |      0 |      0 |       39 |   19 |           1 |           0 |     28630 | 22114021376 |  24048 |          17 |          
 |           0 |      0 |                     0 |     |          |  237463 |   323 |    71 |     6 |      0 |      0 |       0
 15757 |      | postgres: rdsadmin rdsadmin [local] idle                         | S     | 9657 |      |   15757 |      0 |    -1 |       |  19169 |       0 |      0 |       0 |    17 |     6 |      0 |      0 |       39 |   19 |           1 |           0 |     30067 | 22126604288 |  23096 |          17 |          
 |           0 |      0 |                     0 |     |          | 2345107 | 13309 |   685 |   413 |  57344 | 110592 |       0
 17262 |      | postgres: rdsadmin rdsadmin [local] idle                         | S     | 9657 |      |   17262 |      0 |    -1 |       |   1940 |       0 |      0 |       0 |    15 |     2 |      0 |      0 |       39 |   19 |           1 |           0 |     33822 | 22122409984 |  19852 |          17 |          
 |           0 |      0 |                     0 |     |          | 2407474 |  1764 |   829 |     9 |      0 |  12288 |       0
  1595 |      | postgres: postgres pgbench 10.0.1.123(40590) idle                | R     | 9657 |      |    1595 |      0 |    -1 |       |    950 |       0 |      0 |       0 |   122 |    34 |      0 |      0 |       39 |   19 |           1 |           0 |    215465 | 22114021376 |  24360 |          17 |          
 |           0 |      0 |                     0 |     |          |  173522 |   350 |   100 |    55 |      0 |      0 |       0
 12743 |      | postgres: postgres postgres 10.0.1.123(40258) SELECT             | R     | 9657 |      |   12743 |      0 |    -1 |       |   2432 |       0 |      0 |       0 |     1 |     1 |      0 |      0 |       39 |   19 |           1 |           0 |    168728 | 22122459136 |  24668 |          17 |          
 |           0 |      0 |                     0 |     |          |  272234 |  1181 |   556 |     9 |      0 |   4096 |       0
  1599 |      | postgres: postgres pgbench 10.0.1.123(40598) idle in transaction | R     | 9657 |      |    1599 |      0 |    -1 |       |    981 |       0 |      0 |       0 |   124 |    34 |      0 |      0 |       39 |   19 |           1 |           0 |    215465 | 22114021376 |  24636 |          17 |          
 |           0 |      0 |                     0 |     |          |  173515 |    47 |    93 |    47 |      0 |      0 |       0
  1596 |      | postgres: postgres pgbench 10.0.1.123(40592) UPDATE              | R     | 9657 |      |    1596 |      0 |    -1 |       |    941 |       0 |      0 |       0 |   119 |    38 |      0 |      0 |       39 |   19 |           1 |           0 |    215465 | 22114021376 |  24688 |          17 |          
 |           0 |      0 |                     0 |     |          |  173522 |    54 |   100 |    54 |      0 |      0 |       0
  1597 |      | postgres: postgres pgbench 10.0.1.123(40594) COMMIT              | S     | 9657 |      |    1597 |      0 |    -1 |       |    940 |       0 |      0 |       0 |   123 |    39 |      0 |      0 |       39 |   19 |           1 |           0 |    215465 | 22114021376 |  24452 |          17 |          
 |           0 |      0 |                     0 |     |          |  173512 |   340 |    90 |    45 |      0 |      0 |       0
  1598 |      | postgres: postgres pgbench 10.0.1.123(40596) idle in transaction | R     | 9657 |      |    1598 |      0 |    -1 |       |    948 |       0 |      0 |       0 |   124 |    36 |      0 |      0 |       39 |   19 |           1 |           0 |    215465 | 22114021376 |  24628 |          17 |          
 |           0 |      0 |                     0 |     |          |  173512 |    44 |    90 |    44 |      0 |      0 |       0
  9809 |      | postgres: background writer                                      | S     | 9657 |      |    9809 |      0 |    -1 |       |    230 |       0 |      0 |       0 |     1 |     2 |      0 |      0 |       39 |   19 |           1 |           0 |     18573 | 22003752960 |   7892 |          17 |          
 |           0 |      0 |                     0 |     |          |   96446 |  1193 |   504 |   476 |      0 |      0 |       0
  9808 |      | postgres: checkpointer                                           | S     | 9657 |      |    9808 |      0 |    -1 |       |    341 |       0 |      0 |       0 |     0 |     0 |      0 |      0 |       39 |   19 |           1 |           0 |     18573 | 22003752960 |  10144 |          17 |          
 |           0 |      0 |                     0 |     |          |   95981 | 10792 |    39 |    45 |      0 |      0 |       0
  9810 |      | postgres: walwriter                                              | S     | 9657 |      |    9810 |      0 |    -1 |       |    210 |       0 |      0 |       0 |     5 |    16 |      0 |      0 |       39 |   19 |           1 |           0 |     18573 | 22003752960 |   7408 |          17 |          
 |           0 |      0 |                     0 |     |          |   96014 |   761 |    72 |    44 |      0 |      0 |       0
  9741 |      | postgres: aurora runtime process                                 | S     | 9657 |      |    9741 |      0 |    -1 |       |   7252 |       0 |      2 |       0 |   300 |   166 |      0 |      0 |       20 |    0 |          12 |           0 |     18453 | 22072946688 | 183176 |          17 |          
 |           0 |      0 |                     0 |     |          |  130184 |   845 |  2023 |    11 | 266240 |      0 |       0
  9815 |      | postgres: aurora resource monitoring process                     | S     | 9657 |      |    9815 |      0 |    -1 |       |   1826 |       0 |      0 |       0 |     7 |     3 |      0 |      0 |       39 |   19 |           1 |           0 |     18573 | 22003752960 |  12252 |          17 |          
 |           0 |      0 |                     0 |     |          |  922456 |   726 |  2021 |     9 |      0 |      0 |       0
(17 rows)


```



### 参考

[pg_proctab: Accessing System Stats in PostgreSQL](https://www.slideshare.net/markwkm/pgproctab-accessing-system-stats-in-postgresql-3573304?from_action=save)