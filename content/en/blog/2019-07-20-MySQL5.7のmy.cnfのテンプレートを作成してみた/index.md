---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Creating a my.cnf Template for MySQL 5.7"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-myconf-setting-template.html
date: 2019-07-20
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



I created a template to make explicit which MySQL system variables to specify in my.cnf.

Note that there are many parts that need to be adjusted based on requirements and environment (memory values, directory structure, disk performance (HDD or SSD)).

*Will be updated and revised as needed.*

### Assumed Version

This assumes `MySQL 5.7`.

```sql
mysql> select version();
+------------+
| version()  |
+------------+
| 5.7.26-log |
+------------+
1 row in set (0.00 sec)
```

### my.cnf Template

```sql
[mysqld]
# Tuning required based on environment

# #################
# Common
# #################

# Disable autocommit
# SQL statements specified in init_connect are not executed for users with SUPER privilege
init_connect='SET AUTOCOMMIT=0'

# Disable password validation
validate-password=OFF

# Enable binary logging
log-bin

# Server ID
server_id=1

# Data directory
datadir=/var/lib/mysql

# Socket file
socket=/var/lib/mysql/mysql.sock

# Character set specification
character_set_server=utf8mb4

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

# mysqld.log file specification
log-error=/var/log/mysqld.log

# mysqld.pid file specification
pid-file=/var/run/mysqld/mysqld.pid


# #################
# innodb
# #################

# InnoDB data file path
innodb_data_file_path = ibdata1:1G:autoextend

# InnoDB tablespace auto-extension size
innodb_autoextend_increment = 64

# Size of the buffer that caches InnoDB data and indexes (recommended: 80% of physical memory)
innodb_buffer_pool_size=300M

# Buffer size for uncommitted transactions. About 25% of innodb_buffer_pool_size (max 64MB)
# Set to 32M or similar during data import or data replacement operations
innodb_log_buffer_size=8M

# Number of instances to divide innodb_buffer_pool_size into. Recommended to split when buffer size is large
# innodb_buffer_pool_instances=8

# Size of the disk file that records InnoDB update logs (about 1/4 of innodb_buffer_pool_size)
innodb_log_file_size=1G

# Store data and indexes in individual table files rather than shared
innodb_file_per_table=1

# Controls whether to bypass OS cache
# Use O_DIRECT to prevent "double buffering" where data exists in both InnoDB and OS filesystem cache
innodb_flush_method=O_DIRECT

# Mechanism to write neighboring pages together in a single I/O when writing changed data from buffer pool to disk (disabling recommended for SSD)
innodb_flush_neighbors=0

# Memory area for caching uncommitted transaction information. Effective for tuning when large transactions overflow cache and create temporary tables
binlog_cache_size=32768

# Controls timing of synchronizing changes to REDO log. Set to 0 or 2 for faster performance when ACID is not required
innodb_flush_log_at_trx_commit=1

# Disable doublewrite buffer
# Specify only during data import (do not specify normally)
# skip_innodb_doublewrite

# Number of background threads used for InnoDB write requests
innodb_write_io_threads = 8

# Number of background threads used for InnoDB read requests
innodb_read_io_threads = 8

# Overall I/O capacity available to InnoDB (IOPS value is appropriate). Should be changed for SSD vs HDD
innodb_io_capacity=200

# Change in accordance with innodb_io_capacity change (default is 2x innodb_io_capacity if not set; minimum 2000)
innodb_io_capacity_max=2000


# #################
# query cache
# #################

# Query cache block size
query_cache_min_res_unit=4096

# Query cache maximum size
query_cache_limit=16M

# Memory size used for query cache
query_cache_size=128M

# Query cache type (0:off, 1:ON except SELECT SQL_NO_CACHE, 2:DEMAND SELECT SQL_CACHE only)
query_cache_type=2

# #################
# slow query log
# #################

# Slow query output setting
slow_query_log=ON

# Seconds to determine as slow query
long_query_time=3

# Location of slow query log (must be created in advance)
slow_query_log_file=/var/log/slow.log

# #################
# replication
# #################

# Enable GTID
gtid_mode=on

# Required setting when using GTID (prohibits SQL execution that cannot guarantee GTID consistency)
enforce_gtid_consistency=on

# #################
# thread buffer
# #################

# Buffer used for JOINs without index
join_buffer_size=256K

# Record buffer for full scans
read_buffer_size=1M

# Buffer used during sorting
sort_buffer_size=4M

# Buffer that caches rows read in key-based sorting
read_rnd_buffer_size=2M


# #################
# etc
# #################

# Maximum length of packets that can be sent from client to server
max_allowed_packet=8M

# Maximum size of MEMORY tables. MEMORY tables exceeding this size are created on disk
max_heap_table_size=16M

# Maximum size of temporary tables created per thread. Thread buffer
tmp_table_size=16M

# Maximum number of threads to keep in cache
thread_cache_size=100

# Connection timeout period
wait_timeout=30

# Table cache value. When changing this value, open_files_limit must also be increased.
# open_files_limit controls the upper limit of file descriptors the OS allows for the mysqld process.
table_open_cache=2000

# Table definition cache. Caches table definitions (.frm files) for faster table opening
table_definition_cache=1400

# Initial value of packet message buffer size for storing sent/received packets
net_buffer_length=16384

```

### References

##### Reference Blog 1

> (Back Again) Basics of InnoDB Performance Optimization | Yakst https://yakst.com/ja/posts/65

##### Reference Blog 2

> 10 Settings to Check After Installing MySQL | Yakst https://yakst.com/ja/posts/200

##### Reference Blog 3

> About MySQL-related parameters (mainly InnoDB) - hiroi10's Blog http://hiroi10.hatenablog.com/entry/20151210/1449731029

##### Reference Book 1

[asin:4774170208:detail]

##### Reference Book 2

[asin:B01N0R2BL2:detail]




