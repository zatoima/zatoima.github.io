---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_stat_statementsのインストール、設定方法"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg-stat-statements-install.html
date: 2020-01-30
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



contrib拡張モジュールの中にpg_stat_statementsが含まれており、このモジュールをインストールし設定することで下記のようなSQLを特定することが出来る。Oracle Databaseのv$sqlのような使い方が出来る。

- 実行されたSQL
- 実行時間が長いSQL
- 実行回数が多いSQL
- キャッシュヒット率が低いSQL

### バージョン

```sh
-bash-4.2$ psql
psql (10.11)
Type "help" for help.

postgres=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### 前提条件

#### postgresql-contribがインストールされていること

```sh
-bash-4.2$ rpm -qa | grep contrib
postgresql10-contrib-10.11-2PGDG.rhel7.x86_64
```

#### ライブラリの確認

```sh
-bash-4.2$ pg_config --libdir
/usr/pgsql-10/lib
-bash-4.2$ find /usr/pgsql-10/lib -name pg_stat_statements.so
/usr/pgsql-10/lib/pg_stat_statements.so
```

### pg_stat_statementsの設定方法

前提条件としてpostgresql-contrib パッケージ（pg_stat_statementsモジュールの中に含まれる）がインストールされていることが必要。

```sh
vi /var/lib/pgsql/10/data/postgresql.conf
```

下記パラメータを修正する。

```sh
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 1000
pg_stat_statements.track = top
pg_stat_statements.save = on
```

※custom_variable_classesの設定は不要。9.2のバージョンまで必要だった。

各パラメータの説明は下記の通り。調整すべきはpg_stat_statements.maxで保存/格納するSQL数を増やす減らすのと、pg_stat_statements.trackで再帰的なSQLも含めて保存するかどうか。

| パラメータ                       | 説明                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| shared_preload_libraries         | サーバが稼働する時点で事前に読み込まれなければならない1つ以上の共有ライブラリを指定。今回の場合はpg_stat_statementsライブラリ（/usr/pgsql-10/lib/pg_stat_statements.so）を読みこむ必要があるのでpg_stat_statementsを指定。 |
| pg_stat_statements.max           | デフォルトは1000のSQLが記録される。記録されるSQL文の最大数を指定する。これを超えて異なるSQL文を検出した場合は、最も実行回数の低いSQL文の情報が切り捨てられる。 |
| pg_stat_statements.track         | どのSQL文をモジュールによって計測するかを制御          top：（直接クライアントによって発行された）最上層のSQL文を記録（デフォルト）     all：（関数の中から呼び出された文などの）入れ子になった文も記録     none：文に関する統計情報収集を無効 |
| pg_stat_statements.track_utility | このモジュールがユーティリティコマンドを記録するかどうかを指定。  ユーティリティコマンドとは、 SELECT、INSERT、UPDATEおよびDELETE以外のすべて。 デフォルトはon。  この設定はスーパーユーザのみが変更可。 |
| pg_stat_statements.save          | サーバを終了させる際に文の統計情報を保存するかどうかを指定。  offの場合、統計情報は終了時に保存されず、サーバ開始時に再読み込みもされない。 デフォルト値はon |

パラメータ設定後にはサーバ再起動が必要。

```sh
/usr/pgsql-10/bin/pg_ctl stop --pgdata=/var/lib/pgsql/10/data
/usr/pgsql-10/bin/pg_ctl start --pgdata=/var/lib/pgsql/10/data
```

### pg_stat_statementsの有効化

```sh
postgres=> \dx
                 List of installed extensions
  Name   | Version |   Schema   |         Description          
---------+---------+------------+------------------------------
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(1 row)

postgres=> CREATE EXTENSION pg_stat_statements;
CREATE EXTENSION
postgres=> \dx
                                     List of installed extensions
        Name        | Version |   Schema   |                        Description                        
--------------------+---------+------------+-----------------------------------------------------------
 pg_stat_statements | 1.6     | public     | track execution statistics of all SQL statements executed
 plpgsql            | 1.0     | pg_catalog | PL/pgSQL procedural language
(2 rows)
postgres=> 
pgtest=> SELECT * FROM pg_available_extensions WHERE name = 'pg_stat_statements';
        name        | default_version | installed_version |                          comment                          
--------------------+-----------------+-------------------+-----------------------------------------------------------
 pg_stat_statements | 1.6             | 1.6               | track execution statistics of all SQL statements executed
(1 row)
```

### パラメータ値の確認

```sh
select name, setting, unit from pg_settings where name like 'pg_stat_statements%';

postgres=> select name, setting, unit from pg_settings where name like 'pg_stat_statements%';
               name               | setting | unit 
----------------------------------+---------+------
 pg_stat_statements.max           | 5000    | 
 pg_stat_statements.save          | on      | 
 pg_stat_statements.track         | top     | 
 pg_stat_statements.track_utility | on      | 
(4 rows)
```

### pg_stat_statementsを実際に使ってみる

##### pg_stat_statements_reset()関数を使用してリセットする

```sh
postgres=# SELECT pg_stat_statements_reset();
 pg_stat_statements_reset 
--------------------------
```

##### pgbenchでサンプルクエリを実行

```sh
-bash-4.2$ pgbench -i postgres
NOTICE:  table "pgbench_history" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_branches" does not exist, skipping
creating tables...
100000 of 100000 tuples (100%) done (elapsed 0.10 s, remaining 0.00 s)
vacuum...
set primary keys...
done.
```

##### 結果確認

```sh
postgres=# SELECT query, calls, total_time, rows, 100.0 * shared_blks_hit /
postgres-#                nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
postgres-#           FROM pg_stat_statements ORDER BY total_time DESC LIMIT 5;
-[ RECORD 1 ]---------------------------------------------------
query       | copy pgbench_accounts from stdin
calls       | 1
total_time  | 107.231306
rows        | 100000
hit_percent | 0.36452004860267314702
-[ RECORD 2 ]---------------------------------------------------
query       | alter table pgbench_accounts add primary key (aid)
calls       | 1
total_time  | 57.199683
rows        | 0
hit_percent | 99.9425947187141217
-[ RECORD 3 ]---------------------------------------------------
query       | vacuum analyze pgbench_accounts
calls       | 1
total_time  | 41.366501
rows        | 0
hit_percent | 99.9199679871948780
-[ RECORD 4 ]---------------------------------------------------
query       | vacuum analyze pgbench_branches
calls       | 1
total_time  | 13.070895
rows        | 0
hit_percent | 93.0107526881720430
-[ RECORD 5 ]---------------------------------------------------
query       | alter table pgbench_branches add primary key (bid)
calls       | 1
total_time  | 1.957248
rows        | 0
hit_percent | 86.6197183098591549

```

### 補足

RDSやAuroraの場合は、ライブラリやパラメータの設定は特に不要で、` CREATE EXTENSION pg_stat_statements; `を実行するだけで良い。

> https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html
>
>  \> パフォーマンスメトリクス – pg_stat_statements モジュールは、デフォルトで shared_preload_libraries に含まれています。そのため、作成後すぐにインスタンスを再起動する必要はありません。ただし、この機能を使用する場合は、ステートメント CREATE EXTENSION pg_stat_statements; を実行する必要があります。また、詳細なデータを pg_stat_statements に追加できるように、track_io_timing はデフォルトで有効になっています。






