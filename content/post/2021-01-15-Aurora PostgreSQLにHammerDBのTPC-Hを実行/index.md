---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLにHammerDBのTPC-Hを実行"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-hammerdb-benchmark-tpc-h.html
date: 2021-01-15
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

TPC-HをAurora PostgreSQLに対して実行する。

TPC-Cについては下記を参照。

> Aurora PostgreSQLにHammerDBのTPC-Cを実行 | my opinion is my own https://zatoima.github.io/aws-aurora-postgresql-hammerdb-benchmark.html

### はじめに

CLI実行とのことで、下記のHammerDBのドキュメントを参考

> Chapter 8. Command Line Interface (CLI) https://hammerdb.com/docs/ch08.html

### 事前準備

PostgreSQL関連のライブラリが既にインストールされていることを前提。無ければ下記でインストールしておく。

```sh
sudo yum -y install postgresql
sudo yum -y install postgresql-contrib
```

### HammerDBのインストーラーダウンロード

```sh
wget https://github.com/TPC-Council/HammerDB/releases/download/v3.3/HammerDB-3.3-Linux.tar.gz
tar xvzf HammerDB-3.3-Linux.tar.gz
cd HammerDB-3.3
```

> HammerDB https://hammerdb.com/download.html

### ライブラリ確認

PostgreSQLのライブラリのチェックのSuccessを確認する。

```
Checking database library for PostgreSQL
Success ... loaded library Pgtcl for PostgreSQL
```

```sh
[ec2-user@bastin HammerDB-3.3]$ ls -l
total 100
drwxr-xr-x  2 ec2-user ec2-user    19 Oct 18  2019 agent
drwxr-xr-x  2 ec2-user ec2-user    37 Oct 21  2019 bin
-rwxr-xr-x  1 ec2-user ec2-user 29218 Oct 16  2019 ChangeLog
drwxr-xr-x  2 ec2-user ec2-user   178 Oct 16  2019 config
-rwxr-xr-x  1 ec2-user ec2-user  7274 Oct 16  2019 hammerdb
-rwxr-xr-x  1 ec2-user ec2-user  3167 Oct 16  2019 hammerdbcli
-rwxr-xr-x  1 ec2-user ec2-user  2508 Oct 16  2019 hammerdbws
drwxr-xr-x  2 ec2-user ec2-user    39 Jul 19  2019 images
drwxr-xr-x  2 ec2-user ec2-user  4096 Oct 21  2019 include
drwxr-xr-x 21 ec2-user ec2-user  4096 Oct 21  2019 lib
-rwxr-xr-x  1 ec2-user ec2-user 34666 Jul 19  2019 license
drwxr-xr-x  2 ec2-user ec2-user  4096 Oct 16  2019 modules
-rwxr-xr-x  1 ec2-user ec2-user   116 Oct 16  2019 readme
drwxr-xr-x 10 ec2-user ec2-user   126 Jul 19  2019 src
[ec2-user@bastin HammerDB-3.3]$ ./hammerdbcli
HammerDB CLI v3.3
Copyright (C) 2003-2019 Steve Shaw
Type "help" for a list of commands
The xml is well-formed, applying configuration
hammerdb>librarycheck
Checking database library for Oracle
Error: failed to load Oratcl - can't read "env(ORACLE_HOME)": no such variable
Ensure that Oracle client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for MSSQLServer
Error: failed to load tdbc::odbc - couldn't load file "libiodbc.so": libiodbc.so: cannot open shared object file: No such file or directory
Ensure that MSSQLServer client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for Db2
Error: failed to load db2tcl - couldn't load file "/home/ec2-user/HammerDB-3.3/lib/db2tcl2.0.0/libdb2tcl.so.0.0.1": libdb2.so.1: cannot open shared object file: No such file or directory
Ensure that Db2 client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for MySQL
Error: failed to load mysqltcl - couldn't load file "/home/ec2-user/HammerDB-3.3/lib/mysqltcl-3.052/libmysqltcl3.052.so": libmysqlclient.so.21: cannot open shared object file: No such file or directory
Ensure that MySQL client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for PostgreSQL
Success ... loaded library Pgtcl for PostgreSQL
Checking database library for Redis
Success ... loaded library redis for Redis
```

### HammerDBのパラメータ設定

##### 接続DBをPostgreSQL 指定

```sh
hammerdb> dbset db pg
```

##### 対象ベンチマークをTPC-Cに設定する

```sh
hammerdb> dbset bm TPC-H
```

##### 接続先ホスト名の設定

```sh
hammerdb> diset connection pg_host aurorav1.cluster-cm678nkt5thr.ap-northeast-1.rds.amazonaws.com
```

##### superuserのユーザ名、パスワードの設定

```sh
hammerdb> diset tpch pg_tpch_superuser postgres
hammerdb> diset tpch pg_tpch_superuserpass postgres
```

##### pg_count_ware（スケールファクター）の設定

データ容量を調整する。

```sh
hammerdb> diset tpch pg_scale_fact 1
```

##### テストスキーマ構築を実行するユーザー数の設定

```sh
hammerdb> diset tpch pg_num_tpch_threads 4
```

##### 設定値を確認

```sh
hammerdb>print dict
Dictionary Settings for PostgreSQL
connection {
 pg_host = aurorav1.cluster-cm678nkt5thr.ap-northeast-1.rds.amazonaws.com
 pg_port = 5432
}
tpch       {
 pg_scale_fact         = 1
 pg_tpch_superuser     = postgres
 pg_tpch_superuserpass = postgres
 pg_tpch_defaultdbase  = postgres
 pg_tpch_user          = tpch
 pg_tpch_pass          = tpch
 pg_tpch_dbase         = tpch
 pg_tpch_gpcompat      = false
 pg_tpch_gpcompress    = false
 pg_num_tpch_threads   = 4
 pg_total_querysets    = 1
 pg_raise_query_error  = false
 pg_verbose            = false
 pg_refresh_on         = false
 pg_degree_of_parallel = 2
 pg_update_sets        = 1
 pg_trickle_refresh    = 1000
 pg_refresh_verbose    = false
 pg_cloud_query        = false
 pg_rs_compat          = false
}

```

### スキーマ作成

##### スキーマ作成、及び、テストデータの投入

データロードが走るので時間が掛かる。

```sh
hammerdb>buildschema
Script cleared
Building 1 Warehouses(s) with 1 Virtual User
Ready to create a 1 Warehouse PostgreSQL TPC-C schema
in host xxxxxx.CLUSTER-xxxxxxxx.AP-NORTHEAST-1.RDS.AMAZONAWS.COM:5432 under user TPCC in database TPCC?
Enter yes or no: replied yes
Vuser 1 created - WAIT IDLE
RUNNING - TPC-C creation
Vuser 1:RUNNING
Vuser 1:CREATING TPCC SCHEMA
Vuser 1:CREATING DATABASE tpcc under OWNER tpcc

～省略～
Vuser 1:GATHERING SCHEMA STATISTICS
Vuser 1:TPCC SCHEMA COMPLETE
Vuser 1:FINISHED SUCCESS
ALL VIRTUAL USERS COMPLETE
                          TPC-C Driver Script
hammerdb>
```

スケールファクタを10倍に設定して、完了後にPostgreSQL側のtpccデータベースにログインして確認すれば9つのテーブルが作成されていることがわかる。

```sh
postgres@aurorapgsqlv1:tpcc> \dt+                                                                                                   
+----------+------------+--------+---------+---------+---------------+
| Schema   | Name       | Type   | Owner   | Size    | Description   |
|----------+------------+--------+---------+---------+---------------|
| public   | customer   | table  | tpcc    | 371 MB  | <null>        |
| public   | district   | table  | tpcc    | 168 kB  | <null>        |
| public   | history    | table  | tpcc    | 56 MB   | <null>        |
| public   | item       | table  | tpcc    | 21 MB   | <null>        |
| public   | new_order  | table  | tpcc    | 7864 kB | <null>        |
| public   | order_line | table  | tpcc    | 656 MB  | <null>        |
| public   | orders     | table  | tpcc    | 43 MB   | <null>        |
| public   | stock      | table  | tpcc    | 710 MB  | <null>        |
| public   | warehouse  | table  | tpcc    | 40 kB   | <null>        |
+----------+------------+--------+---------+---------+---------------+
SELECT 9
Time: 0.021s
```

##### ロード用のクライアントプロセスをkillする

```sh
hammerdb>vudestroy
Destroying Virtual Users
Virtual Users Destroyed
vudestroy success
```

##### スクリプトのロード

```sh
hammerdb>loadscript
TPC-C Driver Script
Script loaded, Type "print script" to view
```

#### テスト実行用クライアント（Virtual User）の設定、作成

```sh
hammerdb>vuset vu 4
hammerdb>vuset logtotemp 1
hammerdb>vuset showoutput 1
hammerdb>vuset unique 1
hammerdb>vuset timestamps 1
hammerdb>print vuconf
Virtual Users = 4
User Delay(ms) = 500
Repeat Delay(ms) = 500
Iterations = 1
Show Output = 1
Log Output = 1
Unique Log Name = 1
No Log Buffer = 0
Log Timestamps = 1

hammerdb>
hammerdb> vucreate
Vuser 1 created MONITOR - WAIT IDLE
Vuser 2 created - WAIT IDLE
Vuser 3 created - WAIT IDLE
Vuser 4 created - WAIT IDLE
Vuser 5 created - WAIT IDLE
Logging activated
to /tmp/hammerdb_5FADF0FE5B3F03E293835333.log
5 Virtual Users Created with Monitor VU

hammerdb>vustatus
1 = WAIT IDLE
2 = WAIT IDLE
3 = WAIT IDLE
4 = WAIT IDLE
5 = WAIT IDLE
```

### HammerDBの実行前の準備

下記のような理由からこの状態でHammerDBを実行していくと中々終わらないみたいなので、ひと手間加えていく。

> HammerDBをCLIで使うなど（８）：PostgreSQLにTPC-Hを実行してみる - なからなLife https://atsuizo.hatenadiary.jp/entry/2019/09/04/090000
>
> 作成されるインデックスが、[MySQL](http://d.hatena.ne.jp/keyword/MySQL)用と異なっているからー！
>
> 例えば、[TPC](http://d.hatena.ne.jp/keyword/TPC)-Hで一番大きいテーブル「LINEITEM」には、以下のようにPARTSUPPテーブルを参照する外部キー制約が付与されています。
>
> ```
> CONSTRAINT lineitem_partsupp_fk FOREIGN KEY (l_partkey, l_suppkey)
>         REFERENCES public.partsupp (ps_partkey, ps_suppkey)
> ```
>
>
> [PostgreSQL](http://d.hatena.ne.jp/keyword/PostgreSQL)では
>
> > 外部キーは主キーであるかまたは一意性制約を構成する列を参照しなければなりません。 これは、被参照列は常に(主キーまたは一意性制約の基礎となる)インデックスを持つことを意味します。 このため、参照行に一致する行があるかどうかのチェックは効率的です。 被参照テーブルからの行のDELETEや被参照行のUPDATEは、古い値と一致する行に対して参照テーブルのスキャンが必要となるので、参照行にもインデックスを付けるのは大抵は良い考えです。 これは常に必要という訳ではなく、また、インデックスの方法には多くの選択肢がありますので、**外部キー制約の宣言では参照列のインデックスが自動的に作られるということはありません。**
> > [5.3. 制約](https://www.postgresql.jp/document/10/html/ddl-constraints.html#DDL-CONSTRAINTS-FK)
>
> ということで、PARTSUPPテーブルの(ps_partkey, ps_suppkey列には主キー制約が適用されている＝インデックスも存在するものの、LINEITEMのl_partkey, l_suppkey列には、インデックスがない状態です。
>
> [SQL](http://d.hatena.ne.jp/keyword/SQL)-20では、LINEITEMテーブルのl_partkey, l_suppkeyついて、PARTSUPPテーブルのps_partkey, ps_suppkeyに対するFKが張ってあり、これを使って結合されているのですが、l_partkey, l_suppkeyに自体にはインデックスが張ってないんで、フルスキャン（SeqScan）になっています。
>
> そして、この外部参照の関係にある列で結合して絞り込んだ結果を集約関数で処理するサブクエリの実行コストが異常に大きな値となります。

というわけで、実行前にtpchユーザでtpchデータベースにログインして、下記のインデックスを作成する。

```
CREATE INDEX ON customer (C_NATIONKEY);
CREATE INDEX ON lineitem (L_ORDERKEY);
CREATE INDEX ON lineitem (L_SUPPKEY);
CREATE INDEX ON lineitem (L_PARTKEY,L_SUPPKEY);
CREATE INDEX ON nation (N_REGIONKEY);
CREATE INDEX ON orders (O_CUSTKEY);
CREATE INDEX ON partsupp (PS_PARTKEY);
CREATE INDEX ON partsupp (PS_SUPPKEY);
CREATE INDEX ON supplier (S_NATIONKEY);
CREATE INDEX ON lineitem (L_SHIPDATE);
CREATE INDEX ON lineitem (L_COMMITDATE);
CREATE INDEX ON lineitem (L_RECEIPTDATE);
CREATE INDEX ON orders (O_ORDERDATE);
```

### HammerDBの実行

```sh
hammerdb> vurun
```

##### 実行結果

```sh
hammerdb>vurun
RUNNING - PostgreSQL TPC-H
Vuser 1:RUNNING
Vuser 1:Executing Query 21 (1 of 22)
Vuser 2:RUNNING
Vuser 2:Executing Query 6 (1 of 22)
Vuser 3:RUNNING
Vuser 3:Executing Query 8 (1 of 22)
Vuser 4:RUNNING
Vuser 4:Executing Query 5 (1 of 22)
Vuser 2:query 6 completed in 3.016 seconds
Vuser 2:Executing Query 17 (2 of 22)
Vuser 4:query 5 completed in 2.78 seconds
Vuser 4:Executing Query 21 (2 of 22)
Vuser 1:query 21 completed in 5.485 seconds
Vuser 1:Executing Query 3 (2 of 22)
Vuser 1:query 3 completed in 2.953 seconds
Vuser 1:Executing Query 18 (3 of 22)
Vuser 4:query 21 completed in 5.661 seconds
Vuser 4:Executing Query 14 (3 of 22)
Vuser 3:query 8 completed in 9.447 seconds
Vuser 3:Executing Query 5 (2 of 22)
Vuser 4:query 14 completed in 1.777 seconds
Vuser 4:Executing Query 19 (4 of 22)
Vuser 4:query 19 completed in 0.348 seconds
Vuser 4:Executing Query 15 (5 of 22)
Vuser 3:query 5 completed in 2.148 seconds
Vuser 3:Executing Query 4 (3 of 22)
Vuser 2:query 17 completed in 9.567 seconds
Vuser 2:Executing Query 14 (3 of 22)
Vuser 3:query 4 completed in 0.81 seconds
Vuser 3:Executing Query 6 (4 of 22)
Vuser 2:query 14 completed in 1.566 seconds
Vuser 2:Executing Query 16 (4 of 22)
Vuser 3:query 6 completed in 2.785 seconds
Vuser 3:Executing Query 17 (5 of 22)
Vuser 2:query 16 completed in 7.821 seconds
Vuser 2:Executing Query 19 (5 of 22)
Vuser 2:query 19 completed in 0.243 seconds
Vuser 2:Executing Query 10 (6 of 22)
Vuser 3:query 17 completed in 8.858 seconds
Vuser 3:Executing Query 7 (6 of 22)
Vuser 3:query 7 completed in 3.284 seconds
Vuser 3:Executing Query 1 (7 of 22)
Vuser 4:query 15 completed in 17.023 seconds
Vuser 4:Executing Query 17 (6 of 22)
Vuser 2:query 10 completed in 6.98 seconds
Vuser 2:Executing Query 9 (7 of 22)
Vuser 1:query 18 completed in 26.544 seconds
Vuser 1:Executing Query 5 (4 of 22)
Vuser 1:query 5 completed in 2.252 seconds
Vuser 1:Executing Query 11 (5 of 22)
Vuser 1:query 11 completed in 0.781 seconds
Vuser 1:Executing Query 7 (6 of 22)
Vuser 2:query 9 completed in 9.707 seconds
Vuser 2:Executing Query 2 (8 of 22)
Vuser 1:query 7 completed in 2.585 seconds
Vuser 1:Executing Query 6 (7 of 22)
Vuser 4:query 17 completed in 13.075 seconds
Vuser 4:Executing Query 12 (7 of 22)
Vuser 1:query 6 completed in 2.757 seconds
Vuser 1:Executing Query 20 (8 of 22)
Vuser 1:query 20 completed in 0.943 seconds
Vuser 1:Executing Query 17 (9 of 22)
Vuser 2:query 2 completed in 5.946 seconds
Vuser 2:Executing Query 15 (9 of 22)
Vuser 4:query 12 completed in 3.236 seconds
Vuser 4:Executing Query 6 (8 of 22)
Vuser 4:query 6 completed in 2.542 seconds
Vuser 4:Executing Query 4 (9 of 22)
Vuser 3:query 1 completed in 20.678 seconds
Vuser 3:Executing Query 18 (8 of 22)
Vuser 4:query 4 completed in 0.767 seconds
Vuser 4:Executing Query 9 (10 of 22)
Vuser 1:query 17 completed in 13.149 seconds
Vuser 1:Executing Query 12 (10 of 22)
Vuser 1:query 12 completed in 3.912 seconds
Vuser 1:Executing Query 16 (11 of 22)
Vuser 4:query 9 completed in 13.335 seconds
Vuser 4:Executing Query 8 (11 of 22)
Vuser 4:query 8 completed in 1.575 seconds
Vuser 4:Executing Query 16 (12 of 22)
Vuser 2:query 15 completed in 18.843 seconds
Vuser 2:Executing Query 8 (10 of 22)
Vuser 2:query 8 completed in 0.921 seconds
Vuser 2:Executing Query 5 (11 of 22)
Vuser 2:query 5 completed in 1.495 seconds
Vuser 2:Executing Query 22 (12 of 22)
Vuser 2:query 22 completed in 0.785 seconds
Vuser 2:Executing Query 12 (13 of 22)
Vuser 1:query 16 completed in 9.12 seconds
Vuser 1:Executing Query 15 (12 of 22)
Vuser 2:query 12 completed in 3.083 seconds
Vuser 2:Executing Query 7 (14 of 22)
Vuser 4:query 16 completed in 8.094 seconds
Vuser 4:Executing Query 11 (13 of 22)
Vuser 4:query 11 completed in 0.576 seconds
Vuser 4:Executing Query 2 (14 of 22)
Vuser 2:query 7 completed in 2.229 seconds
Vuser 2:Executing Query 13 (15 of 22)
Vuser 3:query 18 completed in 26.223 seconds
Vuser 3:Executing Query 22 (9 of 22)
Vuser 3:query 22 completed in 0.718 seconds
Vuser 3:Executing Query 14 (10 of 22)
Vuser 4:query 2 completed in 4.166 seconds
Vuser 4:Executing Query 10 (15 of 22)
Vuser 3:query 14 completed in 1.276 seconds
Vuser 3:Executing Query 9 (11 of 22)
Vuser 2:query 13 completed in 6.832 seconds
Vuser 2:Executing Query 18 (16 of 22)
Vuser 4:query 10 completed in 7.385 seconds
Vuser 4:Executing Query 18 (16 of 22)
Vuser 3:query 9 completed in 11.277 seconds
Vuser 3:Executing Query 10 (12 of 22)
Vuser 1:query 15 completed in 18.736 seconds
Vuser 1:Executing Query 13 (13 of 22)
Vuser 3:query 10 completed in 7.917 seconds
Vuser 3:Executing Query 15 (13 of 22)
Vuser 1:query 13 completed in 13.717 seconds
Vuser 1:Executing Query 10 (14 of 22)
Vuser 1:query 10 completed in 7.634 seconds
Vuser 1:Executing Query 2 (15 of 22)
Vuser 2:query 18 completed in 33.341 seconds
Vuser 2:Executing Query 1 (17 of 22)
Vuser 1:query 2 completed in 4.614 seconds
Vuser 1:Executing Query 8 (16 of 22)
Vuser 1:query 8 completed in 1.044 seconds
Vuser 1:Executing Query 14 (17 of 22)
Vuser 4:query 18 completed in 33.215 seconds
Vuser 4:Executing Query 1 (17 of 22)
Vuser 1:query 14 completed in 1.698 seconds
Vuser 1:Executing Query 19 (18 of 22)
Vuser 1:query 19 completed in 0.303 seconds
Vuser 1:Executing Query 9 (19 of 22)
Vuser 3:query 15 completed in 26.017 seconds
Vuser 3:Executing Query 11 (14 of 22)
Vuser 3:query 11 completed in 1.312 seconds
Vuser 3:Executing Query 20 (15 of 22)
Vuser 3:query 20 completed in 1.176 seconds
Vuser 3:Executing Query 2 (16 of 22)
Vuser 1:query 9 completed in 11.02 seconds
Vuser 1:Executing Query 22 (20 of 22)
Vuser 1:query 22 completed in 1.261 seconds
Vuser 1:Executing Query 1 (21 of 22)
Vuser 3:query 2 completed in 6.488 seconds
Vuser 3:Executing Query 21 (17 of 22)
Vuser 3:query 21 completed in 9.238 seconds
Vuser 3:Executing Query 19 (18 of 22)
Vuser 3:query 19 completed in 0.417 seconds
Vuser 3:Executing Query 13 (19 of 22)
Vuser 2:query 1 completed in 28.195 seconds
Vuser 2:Executing Query 4 (18 of 22)
Vuser 2:query 4 completed in 1.517 seconds
Vuser 2:Executing Query 20 (19 of 22)
Vuser 2:query 20 completed in 1.775 seconds
Vuser 2:Executing Query 3 (20 of 22)
Vuser 4:query 1 completed in 27.942 seconds
Vuser 4:Executing Query 13 (18 of 22)
Vuser 2:query 3 completed in 5.823 seconds
Vuser 2:Executing Query 11 (21 of 22)
Vuser 2:query 11 completed in 0.55 seconds
Vuser 2:Executing Query 21 (22 of 22)
Vuser 3:query 13 completed in 10.16 seconds
Vuser 3:Executing Query 16 (20 of 22)
Vuser 4:query 13 completed in 9.648 seconds
Vuser 4:Executing Query 7 (19 of 22)
Vuser 4:query 7 completed in 2.796 seconds
Vuser 4:Executing Query 22 (20 of 22)
Vuser 2:query 21 completed in 7.339 seconds
Vuser 2:Completed 1 query set(s) in 157 seconds
Vuser 2:FINISHED SUCCESS
Vuser 1:query 1 completed in 27.607 seconds
Vuser 1:Executing Query 4 (22 of 22)
Vuser 4:query 22 completed in 0.616 seconds
Vuser 4:Executing Query 3 (21 of 22)
Vuser 1:query 4 completed in 0.512 seconds
Vuser 1:Completed 1 query set(s) in 159 seconds
Vuser 1:FINISHED SUCCESS
Vuser 3:query 16 completed in 8.796 seconds
Vuser 3:Executing Query 12 (21 of 22)
Vuser 4:query 3 completed in 1.766 seconds
Vuser 4:Executing Query 20 (22 of 22)
Vuser 4:query 20 completed in 0.292 seconds
Vuser 4:Completed 1 query set(s) in 158 seconds
Vuser 4:FINISHED SUCCESS
Vuser 3:query 12 completed in 1.208 seconds
Vuser 3:Executing Query 3 (22 of 22)
Vuser 3:query 3 completed in 0.941 seconds
Vuser 3:Completed 1 query set(s) in 161 seconds
Vuser 3:FINISHED SUCCESS
ALL VIRTUAL USERS COMPLETE
                          TPC-H Driver Script
hammerdb>

```

### クリーンアップ

```sh
hammerdb>vucomplete
true
hammerdb>vudestroy
Destroying Virtual Users
Virtual Users Destroyed
vudestroy success

hammerdb>clearscript
Script cleared
```

### 参考

> HammerDBをCLIで使うなど（８）：PostgreSQLにTPC-Hを実行してみる - なからなLife https://atsuizo.hatenadiary.jp/entry/2019/09/04/090000
>
> Chapter 8. Command Line Interface (CLI) https://hammerdb.com/docs/ch08.html