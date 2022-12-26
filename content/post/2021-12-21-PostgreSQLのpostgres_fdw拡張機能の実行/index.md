---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpostgres_fdw拡張機能の実行"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-extension-fdw-install
date: 2021-12-21
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

## postgres_fdwの実行

### 拡張機能の有効化

```sql
CREATE EXTENSION postgres_fdw;
```

### 外部サーバの定義

`test1`データベースに対しての外部サーバを作成する

```sql
CREATE SERVER fdw_app FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'test1');
```

### 外部サーバのユーザーマップ定義

```sql
CREATE USER MAPPING FOR public SERVER fdw_app OPTIONS (user 'postgres', password 'postgres');
```

### 外部テーブルの作成

`fdw_app`外部サーバを使用して`t2`テーブルを外部テーブルとして作成する

```sql
CREATE FOREIGN TABLE t2 (a integer, b text,c text, d timestamp with time zone) SERVER fdw_app;
```

外部テーブルの場合はtypeが`foreign table`になる模様

```sql
postgres=> \d
                List of relations
 Schema |    Name     |     Type      |  Owner   
--------+-------------+---------------+----------
 public | t1          | table         | postgres
 public | t2          | foreign table | postgres
 public | v_dblink_t1 | view          | postgres
```

[IMPORT FOREIGN SCHEMA](https://www.postgresql.jp/document/13/html/sql-importforeignschema.html)を使用して外部テーブルの作成も可能。

### 検索

```sql
postgres=> select count(*) from t2;
   count   
-----------
 100000000
(1 row)
```

## postgres_fdwの特徴

- プッシュダウン機能
  - SQL文に含まれるWHERE句（絞り込み処理）、ORDER BY句（ソート処理）などをリモート側で実行される
    - dblinkと違う明確なメリット
- 更新が可能
  - ON CONFLICT DO UPDATE句のあるINSERT文をサポートしていない

## postgres_fdwの注意点

- トランザクションの制御
  - リモート側のCOMMITのタイミング、トランザクション分離レベルで注意が必要（詳細は参考のリンクを）
- 性能面
  - 通信量次第で遅くなる傾向にある
  - リモート実行オプションでfetch_sizeが100なので、必要に応じてチューニングする必要がある

### 参考

> F.33. postgres_fdw https://www.postgresql.jp/document/13/html/postgres-fdw.html
>
> PostgreSQL 9.6 の postgres_fdw について検証してみた | SIOS Tech. Lab https://tech-lab.sios.jp/archives/8641#i
>
> 外部データとの連携 ～FDWで様々なデータソースとつなぐ～｜PostgreSQLインサイド : 富士通 https://www.fujitsu.com/jp/products/software/resources/feature-stories/postgres/article-index/fdw-overview/
