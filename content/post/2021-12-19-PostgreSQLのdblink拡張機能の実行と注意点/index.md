---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのdblink拡張機能の実行と注意点"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-extension-dblink-install-and-causion
date: 2021-12-19
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

postgres_fdwではなくdblinkの話。環境はAurora PostgreSQLで実行

> dblink https://www.postgresql.jp/document/13/html/contrib-dblink-function.html

## dblinkの実行

### dblinkのインストール

```sql
postgres=> \dx
                 List of installed extensions
  Name   | Version |   Schema   |         Description          
---------+---------+------------+------------------------------
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(1 row)

postgres=> create extension dblink;
CREATE EXTENSION
postgres=> \dx
                                 List of installed extensions
  Name   | Version |   Schema   |                         Description                          
---------+---------+------------+--------------------------------------------------------------
 dblink  | 1.2     | public     | connect to other PostgreSQL databases from within a database
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(2 rows)

postgres=> 
```

### 事前準備：データベースとテーブル作成

test1データベースのt1テーブルをdblinkで別データベースから取得する。そのためのデータベースとテーブル作成。

```sql
create database test1;
\c test1;
create table t1(a numeric primary key, b varchar(30));
insert into t1 values(1,'this data is at test1 database');
```

### 方法1:コネクションを生成して接続する方法

#### コネクションの生成

```sql
postgres=> select dblink_connect('dblink-test1','dbname=test1 user=postgres password=postgres');
 dblink_connect 
----------------
 OK
(1 row)
```

#### 検索

検索時にはリモートテーブル側のデータ型まで記載する必要がある

```sql
postgres=> select * from dblink('dblink-test1','select a,b from t1') as t1(a numeric, b varchar(30)) ;
 a |               b                
---+--------------------------------
 1 | this data is at test1 database
(1 row)
```

データ型がないと下記の通り、怒られる

```sql
postgres=> select * from dblink('dblink-test1','select a,b from t1');
ERROR:  a column definition list is required for functions returning "record"
LINE 1: select * from dblink('dblink-test1','select a,b from t1');
```

#### 切断

```sql
postgres=> select dblink_disconnect('dblink-test1');
 dblink_disconnect 
-------------------
 OK
(1 row)
```

切断後は当然エラーとなる

```sql
postgres=> select * from dblink('dblink-test1','select a,b from t1') as t1(a numeric, b varchar(30)) ;
ERROR:  password is required
DETAIL:  Non-superusers must provide a password in the connection string.
postgres=> 
```

### 方法2:コネクションを生成せずに接続する方法

```sql
postgres=> select * from dblink('dbname=test1 user=postgres password=postgres','select a,b from t1') as t1(a numeric, b varchar(30)) ;
 a |               b                
---+--------------------------------
 1 | this data is at test1 database
(1 row)
```

## 注意点

- 独特なdblink用のSQL構文

  - 上記で記載した通り、リモート側のデータ型を一つ一つ記載する必要がある。マニュアル的にはviewを使って簡単に記載してくださいとのこと。

  > https://www.postgresql.jp/document/13/html/contrib-dblink-function.html
  >
  > 前もって判明している問い合わせを`dblink`で使用する簡便な方法はビューを作成することです。 これにより問い合わせの度に列型の情報を記載することなく、ビュー内に隠すことができます。 以下に例を示します。
  >
  > ```sql
  > CREATE VIEW myremote_pg_proc AS
  > SELECT *
  >  FROM dblink('dbname=postgres options=-csearch_path=',
  >              'select proname, prosrc from pg_proc')
  >  AS t1(proname name, prosrc text);
  > 
  > SELECT * FROM myremote_pg_proc WHERE proname LIKE 'bytea%';
  > ```

- リモートテーブルとローカルテーブルを結合したりする際に全量をローカルに転送してから結合処理やWHERE句による絞り込みを行う必要があり、表によっては大量のデータを転送することになり、非効率な実行計画となる。インデックスを付けていても有無を言わさず全てを持ってくる。同じサーバ内の通信であればどうにかなるケースがあるかもしれないがネットワーク経由の通信の場合、帯域が気になる。同じサーバ内でも通信量次第でボトルネックになる可能性がある。単純に全件データを持ってくることがそもそも辛い。

  下記は、t1がローカルテーブル、t2がリモートテーブル。t2.a=10を指定しており、インデックスを貼っているので1件だけ取ってくれれば嬉しいが、そういう実行計画になっていない。実行時間も非常に時間がかかっている

  ```sql
  postgres=> explain analyze select t1.d from dblink('dbname=test1 user=postgres password=postgres','select a from t2') as t2(a integer), t1 where t1.a=t2.a and t2.a=10;
                                                        QUERY PLAN                                                       
  -----------------------------------------------------------------------------------------------------------------------
   Nested Loop  (cost=0.00..13.68 rows=5 width=8) (actual time=50611.640..58457.467 rows=1 loops=1)
     ->  Seq Scan on t1  (cost=0.00..1.12 rows=1 width=12) (actual time=1.910..1.914 rows=1 loops=1)
           Filter: (a = 10)
           Rows Removed by Filter: 9
     ->  Function Scan on dblink t2  (cost=0.00..12.50 rows=5 width=4) (actual time=50609.726..58455.547 rows=1 loops=1)
           Filter: (a = 10)
           Rows Removed by Filter: 99999999
   Planning time: 41.712 ms
   Execution time: 58712.667 ms
  (9 rows)
  ```

- dblink での問合せは、別のトランザクションとして扱われるので、実行中のトランザクションとの整合性を保証するには、[二相コミット](http://www.postgresql.jp/document/current/html/sql-prepare-transaction.html)の検討が必要

## まとめ

データベースリンク機能であれば後継的扱いのpostgres_fdwを使った方が良い。

> https://www.postgresql.jp/document/13/html/postgres-fdw.html
>
> 実質上、本モジュールの提供する機能は以前の[dblink](https://www.postgresql.jp/document/13/html/dblink.html)モジュールが提供する機能と重複していますが、`postgres_fdw`はリモートのテーブルにアクセスするためにより透過的で標準に準拠した構文を利用できるほか、多くの場合においてより良い性能を得る事ができます。

### 参考

> dblink https://www.postgresql.jp/document/13/html/contrib-dblink-function.html
>
> dblink | Let's POSTGRES https://lets.postgresql.jp/documents/technical/contrib/dblink
>
> PostgreSQL9.3 新機能を検証してみた Vol.2 | アシスト https://www.ashisuto.co.jp/corporate/column/technical-column/detail/1198469_2274.html
