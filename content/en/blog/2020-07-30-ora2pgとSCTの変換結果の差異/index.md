---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Differences in Conversion Results Between ora2pg and SCT"
subtitle: ""
summary: " "
tags: ["AWS","SCT","Oracle","PostgreSQL","DB Migration"]
categories: ["AWS","SCT","Oracle","PostgreSQL","DB Migration"]
url: aws-sct-ora2pg-conversion-compare.html
date: 2020-07-30
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

Out of curiosity, I compared the conversion results of `ora2pg` and `SCT (AWS Schema Conversion Tool)` — two commonly used tools for schema migration from Oracle to PostgreSQL. Both were run with default settings, and the results were compared using WinMerge. SCT is on the left side and ora2pg is on the right. I was surprised by how different the results were.

The source Oracle table used is as follows:

### CREATE Statement

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

### Table Definition

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

### Conversion Results

<img src="image-20200530231421545.png" alt="image-20200530231421545" style="zoom:150%;" />

In table form below. The SCT and ora2pg columns are the PostgreSQL results output via `\d`.

| No.  | Oracle (desc result)          | SCT (\d metacommand result)    | ora2pg (\d metacommand result) |
| ---- | ----------------------------- | ------------------------------ | ------------------------------ |
| 1    | BINARY FILE LOB               | character varying(255)         | bytea                          |
| 2    | BINARY_FLOAT                  | real                           | double precision               |
| 3    | BINARY_DOUBLE                 | double precision               | double precision               |
| 4    | BLOB                          | bytea                          | bytea                          |
| 5    | CHAR(10)                      | character(10)                  | character(10)                  |
| 6    | CHAR(10)                      | character(10)                  | character(10)                  |
| 7    | CLOB                          | text                           | text                           |
| 8    | NCLOB                         | text                           | text                           |
| 9    | DATE                          | timestamp(0) without time zone | timestamp without time zone    |
| 10   | NUMBER(3,2)                   | numeric(3,2)                   | real                           |
| 11   | NUMBER(3,2)                   | numeric(3,2)                   | real                           |
| 12   | FLOAT(126)                    | double precision               | double precision               |
| 13   | FLOAT(3)                      | double precision               | double precision               |
| 14   | NUMBER(38)                    | numeric(38,0)                  | numeric(38,0)                  |
| 15   | NUMBER(38)                    | numeric(38,0)                  | numeric(38,0)                  |
| 16   | INTERVAL YEAR(4) TO MONTH     | interval year to month         | interval year to month         |
| 17   | INTERVAL DAY(4) TO SECOND(4)  | interval day to second(4)      | interval day to second(4)      |
| 18   | LONG                          | text                           | text                           |
| 19   | NCHAR(10)                     | character(10)                  | character(10)                  |
| 20   | NVARCHAR2(10)                 | character varying(10)          | character varying(10)          |
| 21   | NUMBER(9,9)                   | numeric(9,9)                   | double precision               |
| 22   | NUMBER(9)                     | numeric(9,0)                   | integer                        |
| 23   | NUMBER                        | double precision               | bigint                         |
| 24   | NUMBER(9,9)                   | numeric(9,9)                   | double precision               |
| 25   | NVARCHAR2(10)                 | character varying(10)          | character varying(10)          |
| 26   | RAW(10)                       | bytea                          | bytea                          |
| 27   | FLOAT(63)                     | double precision               | double precision               |
| 28   | ROWID                         | character(255)                 | oid                            |
| 29   | NUMBER(38)                    | numeric(38,0)                  | numeric(38,0)                  |
| 30   | TIMESTAMP(5)                  | timestamp(5) without time zone | timestamp without time zone    |
| 31   | TIMESTAMP(5) WITH TIME ZONE   | timestamp(5) with time zone    | timestamp with time zone       |
| 32   | ROWID                         | character varying              | oid                            |
| 33   | VARCHAR2(10)                  | character varying(10)          | character varying(10)          |
| 34   | VARCHAR2(10)                  | character varying(10)          | character varying(10)          |
| 35   | PUBLIC.XMLTYPE STORAGE BINARY | xml                            | xml                            |
