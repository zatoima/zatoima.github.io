---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS(PostgreSQL)にsysbenchを実行する"
subtitle: ""
summary: " "
tags: ["AWS", "RDS", "PostgreSQL"]
categories: ["AWS", "RDS", "PostgreSQL"]
url: aws-rds-postgresql-sysbench.html
date: 2019-10-28
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


### 前提事項

***

既に実行するOSにsysbenchがインストールされていることを前提とします。

> EC2(Amazon Linux)にRDBMSベンチマークツールのsysbenchをインストールする - zato logger https://www.zatolog.com/entry/aws-ec2-sysbench-install-howto

### 事前準備

***

```sh
-- 接続
[ec2-user@donald-dev-ec2-bastin ~]$ psql -h aurora-postgressql-dev.cluster-xxxxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postdb
Password for user postgres: 
psql (9.2.24, server 10.7)
WARNING: psql version 9.2, server version 10.0.
         Some psql features might not work.
SSL connection (cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256)
Type "help" for help.

postdb=> 
postdb=> 

-- ユーザ作成、権限付与、データベース作成

postdb=> CREATE USER sbtest WITH PASSWORD 'sbtest';
CREATE ROLE
postdb=> 
postdb=> 
postdb=> 
postdb=> CREATE DATABASE sbtest;
CREATE DATABASE
postdb=> 
postdb=> GRANT ALL PRIVILEGES ON DATABASE sbtest TO sbtest;
GRANT
postdb=> 
postdb=> 

-- 作成したユーザで接続確認
[ec2-user@donald-dev-ec2-bastin ~]$ psql -h aurora-postgressql-dev.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U sbtest -d sbtest
Password for user sbtest: 
psql (9.2.24, server 10.7)
WARNING: psql version 9.2, server version 10.0.
         Some psql features might not work.
SSL connection (cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256)
Type "help" for help.

sbtest=> 
sbtest=> 
```



### 測定用テーブルの作成

***

```sh
-- sysbench prepare

[ec2-user@donald-dev-ec2-bastin ~]$ sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=pgsql --table-size=1000 --pgsql-host=aurora-postgressql-dev.cluster-xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com --pgsql-user=sbtest --pgsql-password=sbtest --pgsql-db=sbtest --db-ps-mode=disable prepare
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Creating table 'sbtest1'...
Inserting 1000 records into 'sbtest1'
Creating a secondary index on 'sbtest1'...
[ec2-user@donald-dev-ec2-bastin ~]$ 
[ec2-user@donald-dev-ec2-bastin ~]$ 
```



### 性能測定

***

```sh
-- sysbench run
[ec2-user@donald-dev-ec2-bastin ~]$ sysbench /usr/share/sysbench/oltp_read_write.lua --db-driver=pgsql --table-size=1000 --pgsql-db=sbtest --pgsql-host=aurora-postgressql-dev.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com --pgsql-user=sbtest --pgsql-password=sbtest --time=300 --db-ps-mode=disable --threads=16 run
sysbench 1.0.17 (using system LuaJIT 2.0.4)

Running the test with following options:
Number of threads: 16
Initializing random number generator from current time


Initializing worker threads...

Threads started!

SQL statistics:
    queries performed:
        read:                            61096
        write:                           12922
        other:                           9695
        total:                           83713
    transactions:                        3125   (10.40 per sec.)
    queries:                             83713  (278.61 per sec.)
    ignored errors:                      1239   (4.12 per sec.)
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          300.4662s
    total number of events:              3125

Latency (ms):
         min:                                   10.53
         avg:                                 1538.24
         max:                                19170.98
         95th percentile:                     6026.41
         sum:                              4807006.80

Threads fairness:
    events (avg/stddev):           195.3125/8.45
    execution time (avg/stddev):   300.4379/0.02

[ec2-user@donald-dev-ec2-bastin ~]$ 

```