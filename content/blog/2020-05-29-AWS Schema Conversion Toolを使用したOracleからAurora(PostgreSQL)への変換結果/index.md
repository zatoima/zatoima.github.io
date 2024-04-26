---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS Schema Conversion Toolを使用したOracleからAurora(PostgreSQL)への変換結果"
subtitle: ""
summary: " "
tags: ["AWS","SCT","Oracle","PostgreSQL","DB Migration"]
categories: ["AWS","SCT","Oracle","PostgreSQL","DB Migration"]
url: aws-sct-oracle-to-aurora-postgresql-conversion.html
date: 2020-05-29
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

AWS Schema Conversion Toolでどのように変換されるかの確認。DDL定義についてはAWSのDatabase Migration Playbookから拝借致しました。なお、対象はAurora（PostgreSQL）で実施しましたが、RDS(PostgreSQL)でも結果は変わりませんでした。

### Oracle

#### CREATE文

```
CREATE TABLE "DATATYPES"(
 "BFILE" BFILE,
 "BINARY_FLOAT" BINARY_FLOAT,
 "BINARY_DOUBLE" BINARY_DOUBLE,
 "BLOB" BLOB,
 "CHAR" CHAR(10 BYTE),
 "CHARACTER" CHAR(10 BYTE),
 "CLOB" CLOB,
 "NCLOB" NCLOB,
 "DATE" DATE,
 "DECIMAL" NUMBER(3,2),
 "DEC" NUMBER(3,2),
 "DOUBLE_PRECISION" FLOAT(126),
 "FLOAT" FLOAT(3),
 "INTEGER" NUMBER(*,0),
 "INT" NUMBER(*,0),
 "INTERVAL_YEAR" INTERVAL YEAR(4) TO MONTH,
 "INTERVAL_DAY" INTERVAL DAY(4) TO SECOND(4),
 "LONG" LONG,
 "NCHAR" NCHAR(10),
 "NCHAR_VARYING" NVARCHAR2(10),
 "NUMBER" NUMBER(9,9),
 "NUMBER1" NUMBER(9,0),
 "NUMBER(*)" NUMBER,
 "NUMERIC" NUMBER(9,9),
 "NVARCHAR2" NVARCHAR2(10),
 "RAW" RAW(10),
 "REAL" FLOAT(63),
 "ROW_ID" ROWID,
 "SMALLINT" NUMBER(*,0),
 "TIMESTAMP" TIMESTAMP(5),
 "TIMESTAMP WITH TIME ZONE" TIMESTAMP(5) WITH TIME ZONE,
 "UROWID" UROWID(10),
 "VARCHAR" VARCHAR2(10 BYTE),
 "VARCHAR2" VARCHAR2(10 BYTE),
 "XMLTYPE" "PUBLIC"."XMLTYPE"
);
```

#### テーブル定義

```
SQL> desc DATATYPES;
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 BFILE						    BINARY FILE LOB
 BINARY_FLOAT					BINARY_FLOAT
 BINARY_DOUBLE					BINARY_DOUBLE
 BLOB						    BLOB
 CHAR						    CHAR(10)
 CHARACTER					    CHAR(10)
 CLOB						    CLOB
 NCLOB						    NCLOB
 DATE						    DATE
 DECIMAL					    NUMBER(3,2)
 DEC						    NUMBER(3,2)
 DOUBLE_PRECISION				FLOAT(126)
 FLOAT						    FLOAT(3)
 INTEGER					    NUMBER(38)
 INT						    NUMBER(38)
 INTERVAL_YEAR					INTERVAL YEAR(4) TO MONTH
 INTERVAL_DAY					INTERVAL DAY(4) TO SECOND(4)
 LONG						    LONG
 NCHAR						    NCHAR(10)
 NCHAR_VARYING					NVARCHAR2(10)
 NUMBER 					    NUMBER(9,9)
 NUMBER1					    NUMBER(9)
 NUMBER(* )					    NUMBER
 NUMERIC					    NUMBER(9,9)
 NVARCHAR2					    NVARCHAR2(10)
 RAW						    RAW(10)
 REAL						    FLOAT(63)
 ROW_ID 					    ROWID
 SMALLINT					    NUMBER(38)
 TIMESTAMP					    TIMESTAMP(5)
 TIMESTAMP WITH TIME ZONE		 TIMESTAMP(5) WITH TIME ZONE
 UROWID 					    ROWID
 VARCHAR					    VARCHAR2(10)
 VARCHAR2					    VARCHAR2(10)
 XMLTYPE					    PUBLIC.XMLTYPE STORAGE BINARY
```

### PostgreSQL

CREATE文

```
CREATE TABLE IF NOT EXISTS datatypes(
    bfile CHARACTER VARYING(255),
    binary_float REAL,
    binary_double DOUBLE PRECISION,
    blob BYTEA,
    char CHARACTER(10),
    character CHARACTER(10),
    clob TEXT,
    nclob TEXT,
    date TIMESTAMP(0) WITHOUT TIME ZONE,
    decimal NUMERIC(3,2),
    dec NUMERIC(3,2),
    double_precision DOUBLE PRECISION,
    float DOUBLE PRECISION,
    integer NUMERIC(38,0),
    int NUMERIC(38,0),
    interval_year INTERVAL YEAR TO MONTH,
    interval_day INTERVAL DAY TO SECOND(4),
    long TEXT,
    nchar CHARACTER(10),
    nchar_varying CHARACTER VARYING(10),
    number NUMERIC(9,9),
    number1 NUMERIC(9,0),
    "NUMBER(*)" DOUBLE PRECISION,
    numeric NUMERIC(9,9),
    nvarchar2 CHARACTER VARYING(10),
    raw BYTEA,
    real DOUBLE PRECISION,
    row_id CHARACTER(255),
    smallint NUMERIC(38,0),
    timestamp TIMESTAMP(5) WITHOUT TIME ZONE,
    "TIMESTAMP WITH TIME ZONE" TIMESTAMP(5) WITH TIME ZONE,
    urowid CHARACTER VARYING,
    varchar CHARACTER VARYING(10),
    varchar2 CHARACTER VARYING(10),
    xmltype XML
);
```

#### テーブル定義

```
postgres> \d datatypes;                                                                                                                                                                     
+--------------------------+--------------------------------+-------------+
| Column                   | Type                           | Modifiers   |
|--------------------------+--------------------------------+-------------|
| bfile                    | character varying(255)         |             |
| binary_float             | real                           |             |
| binary_double            | double precision               |             |
| blob                     | bytea                          |             |
| char                     | character(10)                  |             |
| character                | character(10)                  |             |
| clob                     | text                           |             |
| nclob                    | text                           |             |
| date                     | timestamp(0) without time zone |             |
| decimal                  | numeric(3,2)                   |             |
| dec                      | numeric(3,2)                   |             |
| double_precision         | double precision               |             |
| float                    | double precision               |             |
| integer                  | numeric(38,0)                  |             |
| int                      | numeric(38,0)                  |             |
| interval_year            | interval year to month         |             |
| interval_day             | interval day to second(4)      |             |
| long                     | text                           |             |
| nchar                    | character(10)                  |             |
| nchar_varying            | character varying(10)          |             |
| number                   | numeric(9,9)                   |             |
| number1                  | numeric(9,0)                   |             |
| NUMBER(*)                | double precision               |             |
| numeric                  | numeric(9,9)                   |             |
| nvarchar2                | character varying(10)          |             |
| raw                      | bytea                          |             |
| real                     | double precision               |             |
| row_id                   | character(255)                 |             |
| smallint                 | numeric(38,0)                  |             |
| timestamp                | timestamp(5) without time zone |             |
| TIMESTAMP WITH TIME ZONE | timestamp(5) with time zone    |             |
| urowid                   | character varying              |             |
| varchar                  | character varying(10)          |             |
| varchar2                 | character varying(10)          |             |
| xmltype                  | xml                            |             |
+--------------------------+--------------------------------+-------------+

```

OracleとPostgreSQLを対比した結果は次の通りです。

### OracleとPostgreSQLの対比一覧

| No.  | Oracle (※descの結果）         | PostgreSQL (\d メタコマンド結果） |
| ---- | ----------------------------- | --------------------------------- |
| 1    | BINARY FILE LOB               | character varying(255)            |
| 2    | BINARY_FLOAT                  | real                              |
| 3    | BINARY_DOUBLE                 | double precision                  |
| 4    | BLOB                          | bytea                             |
| 5    | CHAR(10)                      | character(10)                     |
| 6    | CHAR(10)                      | character(10)                     |
| 7    | CLOB                          | text                              |
| 8    | NCLOB                         | text                              |
| 9    | DATE                          | timestamp(0) without time zone    |
| 10   | NUMBER(3,2)                   | numeric(3,2)                      |
| 11   | NUMBER(3,2)                   | numeric(3,2)                      |
| 12   | FLOAT(126)                    | double precision                  |
| 13   | FLOAT(3)                      | double precision                  |
| 14   | NUMBER(38)                    | numeric(38,0)                     |
| 15   | NUMBER(38)                    | numeric(38,0)                     |
| 16   | INTERVAL YEAR(4) TO MONTH     | interval year to month            |
| 17   | INTERVAL DAY(4) TO SECOND(4)  | interval day to second(4)         |
| 18   | LONG                          | text                              |
| 19   | NCHAR(10)                     | character(10)                     |
| 20   | NVARCHAR2(10)                 | character varying(10)             |
| 21   | NUMBER(9,9)                   | numeric(9,9)                      |
| 22   | NUMBER(9)                     | numeric(9,0)                      |
| 23   | NUMBER                        | double precision                  |
| 24   | NUMBER(9,9)                   | numeric(9,9)                      |
| 25   | NVARCHAR2(10)                 | character varying(10)             |
| 26   | RAW(10)                       | bytea                             |
| 27   | FLOAT(63)                     | double precision                  |
| 28   | ROWID                         | character(255)                    |
| 29   | NUMBER(38)                    | numeric(38,0)                     |
| 30   | TIMESTAMP(5)                  | timestamp(5) without time zone    |
| 31   | TIMESTAMP(5) WITH TIME ZONE   | timestamp(5) with time zone       |
| 32   | ROWID                         | character varying                 |
| 33   | VARCHAR2(10)                  | character varying(10)             |
| 34   | VARCHAR2(10)                  | character varying(10)             |
| 35   | PUBLIC.XMLTYPE STORAGE BINARY | xml                               |