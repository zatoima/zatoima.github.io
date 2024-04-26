---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLで論理レプリケーションするテーブルを追加"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-addtable-logical-replication.html
date: 2019-12-26
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



#### はじめに

***

CREATE PUBLICATIONする時に「FOR ALL TABLES」を付与するとそれ以降CREATE TABLEしたテーブルは自動的にレプリケーション対象になると思い込んでいた。初歩的なのかもしれないがこの動作を知らなかったのでメモ。

結論を書くと「FOR ALL TABLES」を付与している場合でも「ALTER SUBSCRIPTION xxxxxxx REFRESH PUBLICATION」コマンドが必要となる。



#### 事前確認

***

Publisher側の設定確認。All tablesがTrueになっている。

```sql
repdb=> \dRp+
                Publication alltables
  Owner   | All tables | Inserts | Updates | Deletes 
----------+------------+---------+---------+---------
 postgres | t          | t       | t       | t
(1 row)
```

Subscriber側の設定確認。logicalreplicationtestが既にレプリケーション対象となっている。

```sql
repdb=> SELECT
repdb->     a3.subname,
repdb->     a2.relname,
repdb->     a1.srsubstate,
repdb->     a1.srsublsn
repdb-> FROM
repdb->     pg_subscription_rel AS a1
repdb->     LEFT OUTER JOIN
repdb->     pg_class AS a2 ON
repdb->     a1.srrelid = a2.oid
repdb->     LEFT OUTER JOIN
repdb->     pg_stat_subscription AS a3 ON
repdb->     a1.srsubid = a3.subid;
      subname       |        relname         | srsubstate | srsublsn  
--------------------+------------------------+------------+-----------
 auroratopostgresql | logicalreplicationtest | r          | 0/1220050
(1 row)
```



#### テーブルを追加

***

Publisher側、Subscriber側でテーブルを作成する。

```sql
repdb=> CREATE TABLE addtable1 (a int PRIMARY KEY);
CREATE TABLE
```

確認する。この時点でレプリケーション対象に追加されると思っていた。

```sql
repdb=> SELECT
repdb->     a3.subname,
repdb->     a2.relname,
repdb->     a1.srsubstate,
repdb->     a1.srsublsn
repdb-> FROM
repdb->     pg_subscription_rel AS a1
repdb->     LEFT OUTER JOIN
repdb->     pg_class AS a2 ON
repdb->     a1.srrelid = a2.oid
repdb->     LEFT OUTER JOIN
repdb->     pg_stat_subscription AS a3 ON
repdb->     a1.srsubid = a3.subid;
      subname       |        relname         | srsubstate | srsublsn  
--------------------+------------------------+------------+-----------
 auroratopostgresql | logicalreplicationtest | r          | 0/1220050
(1 row)

repdb=> 
```

ALTER SUBSCRIPTIONでREFRESHする。

```sql
repdb=> ALTER SUBSCRIPTION auroratopostgresql REFRESH PUBLICATION;
ALTER SUBSCRIPTION
```

> ALTER SUBSCRIPTION [https://www.postgresql.jp/document/10/html/sql-altersubscription.html](https://www.postgresql.jp/document/10/html/sql-altersubscription.html)
>
> REFRESH PUBLICATION
>
>  不足しているテーブル情報をパブリッシャーから取得します。 最後のREFRESH PUBLICATION、あるいはCREATE SUBSCRIPTIONの実行の後でサブスクライブ対象のパブリケーションに追加されたテーブルの複製が、これにより開始されます。

ここでようやくレプリケーション対象が増えた。

```sql
repdb=> SELECT
repdb->     a3.subname,
repdb->     a2.relname,
repdb->     a1.srsubstate,
repdb->     a1.srsublsn
repdb-> FROM
repdb->     pg_subscription_rel AS a1
repdb->     LEFT OUTER JOIN
repdb->     pg_class AS a2 ON
repdb->     a1.srrelid = a2.oid
repdb->     LEFT OUTER JOIN
repdb->     pg_stat_subscription AS a3 ON
repdb->     a1.srsubid = a3.subid;
      subname       |        relname         | srsubstate | srsublsn  
--------------------+------------------------+------------+-----------
 auroratopostgresql | logicalreplicationtest | r          | 0/1220050
 auroratopostgresql | addtable1              | r          | 0/5030740
(2 rows)

```

#### まとめ

***

CREATE PUBLICATION側のマニュアルには"そのデータベース内の全テーブルについての変更を複製するもの"という記載があるのでこれからテーブル追加時に自動的にレプリケーションされるものと思い込んでいた。

> https://www.postgresql.jp/document/10/html/sql-createpublication.html
>  > CREATE PUBLICATION
>  > FOR ALL TABLES
>  > そのパブリケーションでは、将来作成されるテーブルも含め、そのデータベース内の全テーブルについての変更を複製するものとして印をつけます。

レプリケーション対象のテーブルが増えたらALTER SUBSCRIPTION xxxxxxx REFRESH PUBLICATIONコマンドを実行しようという話。