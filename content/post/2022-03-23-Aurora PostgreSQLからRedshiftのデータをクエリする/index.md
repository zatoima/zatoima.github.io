---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLからRedshiftのデータをクエリする"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-aurora-postgreSQL-data-from-redshift
date: 2022-03-23
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

## Aurora PostgreSQLからRedshiftのデータをクエリする

Redshift側の情報は下記となる。

- データベース名：`mydb`
- テーブル名：`testdata`
- ユーザ名：`awsuser`
- パスワード：`*******`
- ホスト名：`redshift-ra3.xxxx.ap-northeast-1.redshift.amazonaws.com:5439/mydb`

### Aurora側の事前準備

拡張機能の有効化

```sql
CREATE EXTENSION postgres_fdw;
```

外部サーバの定義

```sql
drop server fdw_app;
CREATE SERVER fdw_app FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'redshift-ra3.xxxx.ap-northeast-1.redshift.amazonaws.com', dbname 'mydb', port '5439');
```

外部サーバのユーザマップ定義

```sql
CREATE USER MAPPING FOR public SERVER fdw_app OPTIONS (user 'awsuser', password '*****');
```

外部テーブルの作成

```sql
CREATE FOREIGN TABLE testdata (id numeric, name varchar(30), comment text) SERVER fdw_app;
```

AuroraからRedshiftのテーブルをクエリする

```sql
select * from testdata;
```
