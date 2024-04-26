---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでNOLOGGINGテーブル（UNLOGGED）に大量データをロード"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-postgresql-nologging-load.html
date: 2021-01-27
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

# UNLOGGEDテーブルとは

UNLOGGEDテーブルはOracle Databaseで言うところのUNLOGGINGテーブルでWALに書き出さないテーブルとなり、高速化が見込める。一方、クラッシュ時には当然WALにデータがないので、リカバリが出来ない。

とは言え、データロード等のリトライ可能な処理には有効なので、効果含めて確認してみる

# 設定方法

テーブル作成時にオプションを付けるかALTER TABLE文を使用するか。今回はALTER TABLEで実施してみる

```
ALTER TABLE aozora SET UNLOGGED;
ALTER TABLE aozora SET LOGGED;
```

> CREATE TABLE https://www.postgresql.jp/document/12/html/sql-createtable.html
>
> ALTER TABLE https://www.postgresql.jp/document/12/html/sql-altertable.html

# テーブル作成

青空文庫のテキストデータをロード出来るようにテーブルを準備

```
CREATE TABLE aozora(file VARCHAR(30),num INT,row INT,word TEXT,subtype1 VARCHAR(30),subtype2 VARCHAR(30),subtype3 VARCHAR(30),subtype4 VARCHAR(10),conjtype VARCHAR(15),conjugation VARCHAR(15),basic TEXT,ruby TEXT,pronunce TEXT );
ALTER TABLE aozora SET UNLOGGED;
```

作成後にテーブル定義を確認すると`Unlogged table "public.aozora"`と表示されるようになっている。

```
postgres=> \d aozora
                    Unlogged table "public.aozora"
   Column    |         Type          | Collation | Nullable | Default 
-------------+-----------------------+-----------+----------+---------
 file        | character varying(30) |           |          | 
 num         | integer               |           |          | 
 row         | integer               |           |          | 
 word        | text                  |           |          | 
 subtype1    | character varying(30) |           |          | 
 subtype2    | character varying(30) |           |          | 
 subtype3    | character varying(30) |           |          | 
 subtype4    | character varying(10) |           |          | 
 conjtype    | character varying(15) |           |          | 
 conjugation | character varying(15) |           |          | 
 basic       | text                  |           |          | 
 ruby        | text                  |           |          | 
 pronunce    | text                  |           |          | 
```

# 結果

約3割ほどUNLOGGEDテーブルの方が早い結果に。

| テーブル種別     | 時間    |
| ---------------- | ------- |
| UNLOGGEDテーブル | 0:04:41 |
| LOGGEDテーブル   | 0:06:11 |

#### UNLOGGEDテーブルの場合

```
[ec2-user@bastin ~]$ time psql -h aurorav1.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "COPY aozora(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < /home/ec2-user/utf8_all.csv
COPY 87701673

real	4m41.921s
user	0m19.347s
sys	0m6.618s
```

#### LOGGEDテーブルの場合

```
[ec2-user@bastin ~]$ time psql -h aurorav1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "COPY aozora(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < /home/ec2-user/utf8_all.csv
COPY 87701673

real	6m11.123s
user	0m18.744s
sys	0m6.738s
```

