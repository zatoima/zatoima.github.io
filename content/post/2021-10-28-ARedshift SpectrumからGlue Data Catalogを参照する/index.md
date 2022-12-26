---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshift SpectrumからGlue Data Catalogのテーブルを参照する"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-spectrum-select-data-catalog
date: 2021-10-28
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

Athena側で作ったGlue Data Catalog側のデータベース名、テーブル名の前提は下記記事。

> [AthenaでParquetファイルのデータカタログ作成 \| my opinion is my own](https://zatoima.github.io/python-pyarrow-convert-csv-to-parquet-pandas/)

- データベース名：catalogtest
- テーブル名：testdata
- 外部スキーマ名：external_schema

### Redshift側で外部スキーマを定義

データカタログ側にデータベース、テーブルがある状態であれば外部スキーマ定義を行うだけで良い。S3やGlueの権限をiam_roleとしてRedshiftにアタッチしておく必要がある。

```sql
drop schema external_schema;
create external schema external_schema from data catalog
database 'catalogtest'
iam_role 'arn:aws:iam::xxxxxxx:role/myRedshiftRole'
create external database if not exists;
```

```sql
mydb=# create external schema external_schema from data catalog
mydb-# database 'catalogtest'
mydb-# iam_role 'arn:aws:iam::xxxxxxx:role/myRedshiftRole'
mydb-# create external database if not exists;
INFO:  External database "catalogtest" already exists
CREATE SCHEMA
```

### スキーマの確認

```sql
mydb=# select schemaname, databasename from svv_external_schemas where schemaname='external_schema';
   schemaname    | databasename 
-----------------+--------------
 external_schema | catalogtest
(1 row)
mydb=# select schemaname, tablename, location from SVV_EXTERNAL_TABLES where schemaname='external_schema';
   schemaname    | tablename |      location      
-----------------+-----------+--------------------
 external_schema | testdata  | s3://202110test/pq
(1 row)

mydb=# select * from SVV_EXTERNAL_COLUMNS where tablename = 'testdata';
   schemaname    | tablename | columnname | external_type | columnnum | part_key | is_nullable 
-----------------+-----------+------------+---------------+-----------+----------+-------------
 external_schema | testdata  | id         | string        |         1 |        0 | 
 external_schema | testdata  | name       | string        |         2 |        0 | 
 external_schema | testdata  | comment    | string        |         3 |        0 | 
(3 rows)

```

### クエリを行う

```sql
mydb=# select name,comment from external_schema.testdata;
 name  |       comment        
-------+----------------------
 test1 | ゎぶばあちあぬナクバ
 test2 | がマうひバぴじクハぺ
 test3 | スみでてゥあッあけげ
(3 rows)
```