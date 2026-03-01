---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_stat_statements参照時の<insufficient privilege>について"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg-stat-statements-insuffient-priviledge
date: 2020-03-29
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



いくつか気付きがあったのでメモ。superuserではない一般ユーザでpg_stat_statementsを参照した場合に`insufficient privilege`という出力があったことに気が付いた。

例えば**<u>testAユーザで実行したクエリ</u>**を**<u>testAユーザで</u>**pg_stat_statementsから確認しようとした場合、下記出力となる。

```sh
pgtest=> \c - testa
You are now connected to database "pgtest" as user "testa".
pgtest=> \x
Expanded display is off.
pgtest=> SELECT query FROM pg_stat_statements WHERE dbid=16392 ORDER BY total_time DESC LIMIT 20;
                                                     query                                                     
---------------------------------------------------------------------------------------------------------------
 create table userA.pgtesttbl(id numeric primary key, name varchar)                                            
 CREATE SCHEMA userA AUTHORIZATION userA                                                                       
 SELECT query, calls, total_time, rows FROM pg_stat_statements WHERE dbid=$1 ORDER BY total_time DESC LIMIT $2 
 insert into userA.pgtesttbl values($1,$2)                                                                     
 select oid,datname from pg_database                                                                           
(5 rows)
```

一方、**<u>別ユーザ(testB)</u>**からこのクエリを取得しようとすると、`insufficient privilege`と出力される。

```sh
pgtest=> \c - testb
You are now connected to database "pgtest" as user "testb".
pgtest=> SELECT query FROM pg_stat_statements WHERE dbid=16392 ORDER BY total_time DESC LIMIT 20;
          query           | calls | total_time | rows 
--------------------------+-------+------------+------
 <insufficient privilege> |     1 |   5.340486 |    0
 <insufficient privilege> |     1 |    0.45077 |    0
 <insufficient privilege> |     3 |   0.288345 |   10
 <insufficient privilege> |     1 |   0.106162 |    1
 <insufficient privilege> |     1 |   0.016645 |    4
```

Oracleと違い、PostgreSQLはシステムカタログ（稼働統計ビュー含む）に対する細かい権限制御が出来ない一方、こういった実行したユーザ以外にはクエリを見せないような実装になっていることを知った。

> F.30. pg_stat_statements https://www.postgresql.jp/document/10/html/pgstatstatements.html
>
> セキュリティ上の理由から、スーパーユーザと`pg_read_all_stats`ロールのメンバだけが、他のユーザによって実行されたSQLテキストや問い合わせの`queryid`を見ることができます。

上記のマニュアルにも特定のロールがないと他のユーザによって実行されたSQLテキストは見れないよ、と記載がある。pg_monitorにpg_read_all_statsも内包されているのでスーパーユーザかpg_read_all_statsかpg_monitorさえあれば全てのテキストを見れる。監視用のユーザを作成する際には注意。

ロールについてはこちらに詳しく書いてあったので合わせてどうぞ。

> 監視用デフォルトロール - Qiita https://qiita.com/nuko_yokohama/items/6debdd3291c8f27d1da8



