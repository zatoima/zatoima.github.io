---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Notes on Converting Oracle Partition Tables to Aurora (PostgreSQL) Using SCT"
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

Notes on the following documentation.

> Converting from Oracle to Amazon RDS for PostgreSQL or Amazon Aurora (PostgreSQL) - AWS Schema Conversion Tool https://docs.aws.amazon.com/ja_jp/SchemaConversionTool/latest/userguide/CHAP_Source.Oracle.ToPostgreSQL.html#CHAP_Source.Oracle.ToPostgreSQL.PG10Partitioning
>
> \> The following are some known issues with the conversion of partitions to PostgreSQL version 10.
>
> \> Only non-NULL columns can be used as partition column.
>
> \> DEFAULT cannot be used as a partition value.

For example, suppose you have a range-partitioned table like this, using `ORDER_DATE` as the partition key.

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

<u>**The above DDL does not set any constraint on `ORDER_DATE`**</u>, so there is a possibility that NULL values can be inserted into `ORDER_DATE`. In this case, when converting with SCT, it appears that no error occurs, but the table is not created as a partition table. This falls under the following restriction:

> \> Only non-NULL columns can be used as partition column.

This is what happens:

<img src="images/image-20191121221832169.png" alt="image-20191121221832169" style="zoom:50%;" />

Need to be careful about the partition key of existing tables. Adding a NOT NULL constraint to the partition key `ORDER_DATE` results in this:

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
