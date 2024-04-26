---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "OracleのパーティションテーブルをAurora(PostgreSQL)へSCT変換する場合の注意事項メモ"
subtitle: ""
summary: " "
tags: ["AWS", "DMS", "SCT"]
categories: ["AWS", "DMS", "SCT"]
url: oracle-to-aws-sct-partition-limit.html
date: 2019-11-15
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

こちらの記載に関する注意事項メモ。

> Oracle から Amazon RDS for PostgreSQL または Amazon Aurora (PostgreSQL) への変換 - AWS Schema Conversion Tool https://docs.aws.amazon.com/ja_jp/SchemaConversionTool/latest/userguide/CHAP_Source.Oracle.ToPostgreSQL.html#CHAP_Source.Oracle.ToPostgreSQL.PG10Partitioning
>
> \> 以下は、パーティションの PostgreSQL バージョン 10 への変換に関する既知の問題の一部です。
>
> \> NULL ではない列のみが列に分割することがでます。
>
> \> DEFAULT はパーティション値として使用できる値ではありません。

例えば、こういうレンジ・パーティションのテーブルがあったとして、`ORDER_DATE`をパーティション・キーとする。

```sql
drop table TAB_RANGE_PART;
CREATE TABLE TAB_RANGE_PART (
    ORDER_ID        NUMBER primary key,
    ORDER_DATE      DATE,
    BOOK_NO         VARCHAR(20) NOT NULL,
    BOOK_TYPE       VARCHAR(20) NOT NULL,    
    BOOK_CNT        NUMBER    NOT NULL,
    REMARKS         VARCHAR2(40))
    LOGGING
    PCTFREE    20
    PARTITION BY RANGE (ORDER_DATE) (    
        PARTITION TAB_RANGE_PART01    VALUES LESS THAN ( TO_DATE('20160101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART02    VALUES LESS THAN ( TO_DATE('20170101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART03    VALUES LESS THAN ( TO_DATE('20180101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART04    VALUES LESS THAN ( TO_DATE('20190101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART05    VALUES LESS THAN ( MAXVALUE ))
    ENABLE ROW MOVEMENT;
```

<u>**上記のDDLでは特に`ORDER_DATE`に制約を設定していない</u>**ので`ORDER_DATE`にNullが入る可能性がある。この場合、SCTで変換した場合、エラーにもならず、パーティション・テーブルとして作成されない模様。下記の制限に該当する。

> \> NULL ではない列のみが列に分割することがでます。

こうなる。

<img src="images/image-20191121221832169.png" alt="image-20191121221832169" style="zoom:50%;" />

既存のテーブルのパーティションキーに注意する必要あり。パーティションキーの`ORDER_DATE`にNot Null制約を付与すればこうなる。

```sql
drop table TAB_RANGE_PART;
CREATE TABLE TAB_RANGE_PART (
    ORDER_ID        NUMBER primary key,
    ORDER_DATE      DATE NOT NULL,
    BOOK_NO         VARCHAR(20) NOT NULL,
    BOOK_TYPE       VARCHAR(20) NOT NULL,    
    BOOK_CNT        NUMBER    NOT NULL,
    REMARKS         VARCHAR2(40))
    LOGGING
    PCTFREE    20
    PARTITION BY RANGE (ORDER_DATE) (    
        PARTITION TAB_RANGE_PART01    VALUES LESS THAN ( TO_DATE('20160101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART02    VALUES LESS THAN ( TO_DATE('20170101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART03    VALUES LESS THAN ( TO_DATE('20180101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART04    VALUES LESS THAN ( TO_DATE('20190101','YYYYMMDD')),
        PARTITION TAB_RANGE_PART05    VALUES LESS THAN ( MAXVALUE ))
    ENABLE ROW MOVEMENT;
```

<img src="images/image-20191121221844733.png" alt="image-20191121221844733" style="zoom: 50%;" />
