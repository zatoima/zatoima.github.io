---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLにHammerDBのTPC-Cを実行"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-hammerdb-benchmark.html
date: 2020-11-13
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



Auroraを対象にHammerDBのTPC-Cを使ってみましたが、（当然ですが、）ほぼ普通のPostgreSQL と同じ手順。

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
hammerdb> dbset bm TPC-C
```

##### 接続先ホスト名の設定

```sh
hammerdb> diset connection pg_host aurorapgsqlv1.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com		
```

##### superuserのユーザ名、パスワードの設定

```sh
hammerdb> diset tpcc pg_superuser postgres
hammerdb> diset tpcc pg_superuserpass postgres
```

##### pg_driverの変更

環境整整備、動作検証までは「test」を、実計測時は「timed」を指定

```sh
hammerdb> diset tpcc pg_driver timed
```

##### pg_timeprofileの変更

trueにすると、10秒間隔での応答時間のパーセンタイル、完了時の累積値がレポート

```sh
hammerdb> diset tpcc pg_timeprofile true
```

##### pg_total_iterationsの変更

トランザクションの実行回数を指定（デフォルト 1000000)

```sh
hammerdb> diset tpcc pg_total_iterations 100000
```

##### pg_count_ware（スケールファクター）の設定

データ容量を調整する。

```sh
hammerdb> diset tpcc pg_count_ware 10
```

##### pg_num_vu（同時実行ユーザ）の設定

データ容量を調整する。

```sh
hammerdb> diset tpcc pg_num_vu 4
```

##### 設定値を確認

```sh
hammerdb> print dict
hammerdb>print dict
Dictionary Settings for PostgreSQL
connection {
 pg_host = aurorapgsqlv1.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com
 pg_port = 5432
}
tpcc       {
 pg_count_ware       = 10
 pg_num_vu           = 1
 pg_superuser        = postgres
 pg_superuserpass    = postgres
 pg_defaultdbase     = postgres
 pg_user             = tpcc
 pg_pass             = tpcc
 pg_dbase            = tpcc
 pg_vacuum           = false
 pg_dritasnap        = false
 pg_oracompat        = false
 pg_storedprocs      = false
 pg_total_iterations = 100000
 pg_raiseerror       = false
 pg_keyandthink      = false
 pg_driver           = timed
 pg_rampup           = 2
 pg_duration         = 5
 pg_allwarehouse     = false
 pg_timeprofile      = true
 pg_async_scale      = false
 pg_async_client     = 10
 pg_async_verbose    = false
 pg_async_delay      = 1000
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

### HammerDBの実行

```sh
hammerdb> vurun
```

##### 実行結果

```sh
～省略～
Vuser 1:TEST RESULT : System achieved 14999 PostgreSQL TPM at 6461 NOPM
～省略～
```

> TPM = Transactions Per Minute=トランザクション数／分
>
> NOPM = New Order Per Minute=TPC-Cのシナリオにおける新規オーダー（注文）数／分

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

> HammerDBを使用してPostgreSQLのベンチマークを実施する - Qiita https://qiita.com/mkyz08/items/a9f224dbf4ea7b83e2e9
>
> HammerDBをCLIで使うなど（３）：PostgreSQLにTPC-Cを実行してみる - なからなLife https://atsuizo.hatenadiary.jp/entry/2019/08/28/090000