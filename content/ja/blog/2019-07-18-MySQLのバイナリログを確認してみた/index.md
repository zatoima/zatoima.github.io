---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLのバイナリログを確認してみた"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-binlog-show.html
date: 2019-07-18
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



バイナリログを確認

### 実行コマンド

```sql
-- login
mysql -u myuser -pmysql

-- 既存のバイナリログを確認、及びバイナリログのスイッチ
show binary logs;
flush binary logs;
show binary logs;

-- バイナリログを確認
-- この時にはバイナリのログの中には何も更新情報はない
show binlog events in 'awsstg-db001-bin.000011';

show variables like 'binlog_format';

use mydb;
desc t1;
insert into t1 values(1,'1度目のInsert','testテスト',5555,now());

-- バイナリログを確認
-- 上記Insertが記録されている
show binlog events in 'awsstg-db001-bin.000011';

-- binlog_formatを変更した後に実行
show variables like 'binlog_format';
set session binlog_format='STATEMENT';
show variables like 'binlog_format';

insert into t1 values(2,'2度目のInsert','testテスト',5555,now());

show binlog events in 'awsstg-db001-bin.000011';
```

### 実行結果

```sql
[ec2-user@awsstg-db001 ~]$
[ec2-user@awsstg-db001 ~]$
[ec2-user@awsstg-db001 ~]$
[ec2-user@awsstg-db001 ~]$ mysql -u myuser -pmysql
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 5.7.26-log MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
mysql> show binary logs;
+-------------------------+-----------+
| Log_name                | File_size |
+-------------------------+-----------+
| awsstg-db001-bin.000001 |  42128655 |
| awsstg-db001-bin.000002 |       217 |
| awsstg-db001-bin.000003 |      3533 |
| awsstg-db001-bin.000004 |       217 |
| awsstg-db001-bin.000005 |       217 |
| awsstg-db001-bin.000006 |      1164 |
| awsstg-db001-bin.000007 |  84251908 |
| awsstg-db001-bin.000008 |      1270 |
| awsstg-db001-bin.000009 |       248 |
| awsstg-db001-bin.000010 |       194 |
+-------------------------+-----------+
10 rows in set (0.00 sec)

mysql> flush binary logs;
Query OK, 0 rows affected (0.01 sec)

mysql> show binary logs;
+-------------------------+-----------+
| Log_name                | File_size |
+-------------------------+-----------+
| awsstg-db001-bin.000001 |  42128655 |
| awsstg-db001-bin.000002 |       217 |
| awsstg-db001-bin.000003 |      3533 |
| awsstg-db001-bin.000004 |       217 |
| awsstg-db001-bin.000005 |       217 |
| awsstg-db001-bin.000006 |      1164 |
| awsstg-db001-bin.000007 |  84251908 |
| awsstg-db001-bin.000008 |      1270 |
| awsstg-db001-bin.000009 |       248 |
| awsstg-db001-bin.000010 |       248 |
| awsstg-db001-bin.000011 |       194 |
+-------------------------+-----------+
11 rows in set (0.00 sec)

mysql>
mysql> show binlog events in 'awsstg-db001-bin.000011';
+-------------------------+-----+----------------+-----------+-------------+-------------------------------------------+
| Log_name                | Pos | Event_type     | Server_id | End_log_pos | Info                                      |
+-------------------------+-----+----------------+-----------+-------------+-------------------------------------------+
| awsstg-db001-bin.000011 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.26-log, Binlog ver: 4     |
| awsstg-db001-bin.000011 | 123 | Previous_gtids |         1 |         194 | 86a2b2da-9683-11e9-9dd6-067b425ce144:1-72 |
+-------------------------+-----+----------------+-----------+-------------+-------------------------------------------+
2 rows in set (0.00 sec)

mysql> show variables like 'binlog_format';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | ROW   |
+---------------+-------+
1 row in set (0.00 sec)

mysql>
mysql> use mydb;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> desc t1
    -> ;
+-------+------------------+------+-----+---------+----------------+
| Field | Type             | Null | Key | Default | Extra          |
+-------+------------------+------+-----+---------+----------------+
| a     | int(11)          | NO   | PRI | NULL    | auto_increment |
| b     | varchar(10)      | YES  |     | NULL    |                |
| c     | varchar(30)      | YES  |     | NULL    |                |
| d     | int(10) unsigned | YES  |     | NULL    |                |
| e     | datetime         | YES  |     | NULL    |                |
+-------+------------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)

mysql>
mysql> insert into t1 values(1,'1度目のInsert','testテスト',5555,now());
Query OK, 1 row affected (0.00 sec)

mysql>
mysql> show binlog events in 'awsstg-db001-bin.000011';
+-------------------------+-----+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name                | Pos | Event_type     | Server_id | End_log_pos | Info            |
+-------------------------+-----+----------------+-----------+-------------+--------------------------------------------------------------------+
| awsstg-db001-bin.000011 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.26-log, Binlog ver: 4            |
| awsstg-db001-bin.000011 | 123 | Previous_gtids |         1 |         194 | 86a2b2da-9683-11e9-9dd6-067b425ce144:1-72            |
| awsstg-db001-bin.000011 | 194 | Gtid           |         1 |         259 | SET @@SESSION.GTID_NEXT= '86a2b2da-9683-11e9-9dd6-067b425ce144:73' |
| awsstg-db001-bin.000011 | 259 | Query          |         1 |         339 | BEGIN            |
| awsstg-db001-bin.000011 | 339 | Table_map      |         1 |         393 | table_id: 110 (mydb.t1)            |
| awsstg-db001-bin.000011 | 393 | Write_rows     |         1 |         473 | table_id: 110 flags: STMT_END_F            |
| awsstg-db001-bin.000011 | 473 | Xid            |         1 |         504 | COMMIT /* xid=178 */            |
+-------------------------+-----+----------------+-----------+-------------+--------------------------------------------------------------------+
7 rows in set (0.00 sec)

mysql> show variables like 'binlog_format';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | ROW   |
+---------------+-------+
1 row in set (0.01 sec)

mysql> set session binlog_format='STATEMENT';
Query OK, 0 rows affected (0.00 sec)

mysql> show variables like 'binlog_format';
+---------------+-----------+
| Variable_name | Value     |
+---------------+-----------+
| binlog_format | STATEMENT |
+---------------+-----------+
1 row in set (0.01 sec)

mysql> insert into t1 values(2,'2度目のInsert','testテスト',5555,now());
Query OK, 1 row affected (0.00 sec)

mysql>
mysql>
mysql> show binlog events in 'awsstg-db001-bin.000011';
+-------------------------+-----+----------------+-----------+-------------+------------------------------------------------------------------------------------+
| Log_name                | Pos | Event_type     | Server_id | End_log_pos | Info                            |
+-------------------------+-----+----------------+-----------+-------------+------------------------------------------------------------------------------------+
| awsstg-db001-bin.000011 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.26-log, Binlog ver: 4                            |
| awsstg-db001-bin.000011 | 123 | Previous_gtids |         1 |         194 | 86a2b2da-9683-11e9-9dd6-067b425ce144:1-72                            |
| awsstg-db001-bin.000011 | 194 | Gtid           |         1 |         259 | SET @@SESSION.GTID_NEXT= '86a2b2da-9683-11e9-9dd6-067b425ce144:73'                 |
| awsstg-db001-bin.000011 | 259 | Query          |         1 |         339 | BEGIN                            |
| awsstg-db001-bin.000011 | 339 | Table_map      |         1 |         393 | table_id: 110 (mydb.t1)                            |
| awsstg-db001-bin.000011 | 393 | Write_rows     |         1 |         473 | table_id: 110 flags: STMT_END_F                            |
| awsstg-db001-bin.000011 | 473 | Xid            |         1 |         504 | COMMIT /* xid=178 */                            |
| awsstg-db001-bin.000011 | 504 | Gtid           |         1 |         569 | SET @@SESSION.GTID_NEXT= '86a2b2da-9683-11e9-9dd6-067b425ce144:74'                 |
| awsstg-db001-bin.000011 | 569 | Query          |         1 |         656 | BEGIN                            |
| awsstg-db001-bin.000011 | 656 | Query          |         1 |         808 | use `mydb`; insert into t1 values(2,'2度目のInsert','testテスト',5555,now())       |
| awsstg-db001-bin.000011 | 808 | Xid            |         1 |         839 | COMMIT /* xid=183 */                            |
+-------------------------+-----+----------------+-----------+-------------+------------------------------------------------------------------------------------+
11 rows in set (0.00 sec)

mysql>
```