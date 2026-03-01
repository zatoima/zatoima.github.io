---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQL InnoDB Buffer Pool Preloading"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-buffer-pool-load.html
date: 2019-07-19
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

Summarizing the MySQL buffer pool preloading feature. (This feature doesn't exist in Oracle, so I was curious about it)

### Related System Variables

```sql
mysql> select version();
+------------+
| version()  |
+------------+
| 5.7.26-log |
+------------+
1 row in set (0.00 sec)

mysql>

mysql> show variables like 'innodb_buffer_pool%';
+-------------------------------------+----------------+
| Variable_name                       | Value          |
+-------------------------------------+----------------+
| innodb_buffer_pool_chunk_size       | 134217728      |
| innodb_buffer_pool_dump_at_shutdown | ON             |
| innodb_buffer_pool_dump_now         | OFF            |
| innodb_buffer_pool_dump_pct         | 25             |
| innodb_buffer_pool_filename         | ib_buffer_pool |
| innodb_buffer_pool_instances        | 1              |
| innodb_buffer_pool_load_abort       | OFF            |
| innodb_buffer_pool_load_at_startup  | ON             |
| innodb_buffer_pool_load_now         | OFF            |
| innodb_buffer_pool_size             | 134217728      |
+-------------------------------------+----------------+
10 rows in set (0.00 sec)
```

##### innodb_buffer_pool_dump_at_shutdown

Whether to retain the cache in the buffer pool at shutdown.

> https://dev.mysql.com/doc/refman/5.6/ja/innodb-parameters.html#sysvar_innodb_buffer_pool_dump_at_shutdown
> Specifies whether to record the pages cached in the InnoDB buffer pool when the MySQL server is shut down, to shorten the warmup process at the next restart. Generally used together with innodb_buffer_pool_load_at_startup.

After shutdown, `ib_buffer_pool` is created.

```sql
[mysql@awsstg-db001 mysql]$ ls -l ib_buffer_pool
-rw-r----- 1 mysql mysql 3206 Jun 29 15:07 ib_buffer_pool
[mysql@awsstg-db001 mysql]$
```

Setting this parameter causes the following log to be output to the error log during the shutdown sequence:

```sql
2019-06-27T07:59:52.431613Z 0 [Note] InnoDB: Starting shutdown...
2019-06-27T07:59:52.531945Z 0 [Note] InnoDB: Dumping buffer pool(s) to /var/lib/mysql/ib_buffer_pool
2019-06-27T07:59:52.532242Z 0 [Note] InnoDB: Buffer pool(s) dump completed at 190627  7:59:52
2019-06-27T07:59:54.242932Z 0 [Note] InnoDB: Shutdown completed; log sequence number 616413821
```

##### innodb_buffer_pool_load_at_startup

At startup, reads `ib_buffer_pool` and preloads the buffer pool.

> https://dev.mysql.com/doc/refman/5.6/ja/innodb-parameters.html#sysvar_innodb_buffer_pool_load_at_startup
> Specifies that, on MySQL server startup, the InnoDB buffer pool is automatically warmed up by loading the same pages it held at an earlier time. Generally used together with innodb_buffer_pool_dump_at_shutdown.

##### innodb_buffer_pool_filename

Specifies the name of the file to record.

##### innodb_buffer_pool_dump_now/innodb_buffer_pool_load_at_startup

Performs immediate write and immediate read at any time while MySQL is online, rather than at shutdown or startup.

### Information Stored in ib_buffer_pool

`Required tablespace ID` and `page ID`

```sql
[mysql@awsstg-db001 mysql]$ head ib_buffer_pool
0,890
0,889
0,888
0,887
0,886
0,885
0,884
0,883
0,882
0,881
```

> Only the tablespace ID and page ID needed to find the relevant pages are saved to disk. This information is retrieved from the `INNODB_BUFFER_PAGE_LRU` `INFORMATION_SCHEMA` table. By default, the tablespace ID and page ID data is stored in a file named `ib_buffer_pool` in the `InnoDB` data directory. The file name can be changed using the `innodb_buffer_pool_filename` configuration parameter.

This information appears to be retrieved from `INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU`.

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU LIMIT 1\G
*************************** 1. row ***************************
            POOL_ID: 0
       LRU_POSITION: 0
              SPACE: 30
        PAGE_NUMBER: 11063
          PAGE_TYPE: INDEX
         FLUSH_TYPE: 0
          FIX_COUNT: 0
          IS_HASHED: NO
NEWEST_MODIFICATION: 0
OLDEST_MODIFICATION: 0
        ACCESS_TIME: 2747830684
         TABLE_NAME: `mydb`.`t1`
         INDEX_NAME: PRIMARY
     NUMBER_RECORDS: 648
          DATA_SIZE: 14904
    COMPRESSED_SIZE: 0
         COMPRESSED: NO
             IO_FIX: IO_NONE
             IS_OLD: YES
    FREE_PAGE_CLOCK: 0
1 row in set (0.01 sec)

```
