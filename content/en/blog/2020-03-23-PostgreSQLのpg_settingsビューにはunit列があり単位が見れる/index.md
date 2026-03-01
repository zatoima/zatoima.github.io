---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "The pg_settings View in PostgreSQL Has a Unit Column Showing Parameter Units"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg_setting-unit.html
date: 2020-03-23
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



The pg_settings view has a unit column where you can see the units of parameters. Very useful.

```sql
postgres=# select name,setting,unit from pg_settings where name like '%wal%';
             name             |  setting  | unit
------------------------------+-----------+------
 max_wal_senders              | 10        |
 max_wal_size                 | 1024      | MB
 min_wal_size                 | 80        | MB
 wal_block_size               | 8192      |
 wal_buffers                  | 512       | 8kB
 wal_compression              | off       |
 wal_consistency_checking     |           |
 wal_keep_segments            | 0         |
 wal_level                    | replica   |
 wal_log_hints                | off       |
 wal_receiver_status_interval | 10        | s
 wal_receiver_timeout         | 60000     | ms
 wal_retrieve_retry_interval  | 5000      | ms
 wal_segment_size             | 2048      | 8kB
 wal_sender_timeout           | 60000     | ms
 wal_sync_method              | fdatasync |
 wal_writer_delay             | 200       | ms
 wal_writer_flush_after       | 128       | 8kB
(18 rows)
```

> [Revised Edition] PostgreSQL Design and Operations Guide: Internal Structure: Book Information | Gijutsu-Hyoron-sha https://gihyo.jp/book/2018/978-4-297-10089-6
