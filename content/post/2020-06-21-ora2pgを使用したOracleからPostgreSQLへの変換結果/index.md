---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ora2pgを使用したOracleからPostgreSQLへの変換結果"
subtitle: ""
summary: " "
tags: ["AWS","SCT","Oracle","PostgreSQL","DB Migration"]
categories: ["AWS","SCT","Oracle","PostgreSQL","DB Migration"]
url: aws-ora2pg-oracle-to-aurora-postgresql-conversion.html
date: 2020-06-21
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

以前にAWS SCTで実施したOracleからAurora(PostgreSQL)への変換を今度はora2pgで実行してみた。

> AWS Schema Conversion Toolを使用したOracleからAurora(PostgreSQL)への変換結果 | my opinion is my own https://zatoima.github.io/aws-sct-oracle-to-aurora-postgresql-conversion.html

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
CREATE TABLE datatypes (
	bfile bytea,
	binary_float double precision,
	binary_double double precision,
	blob bytea,
	char char(10),
	character char(10),
	clob text,
	nclob text,
	date timestamp,
	decimal real,
	dec real,
	double_precision double precision,
	float double precision,
	integer numeric(38),
	int numeric(38),
	interval_year INTERVAL YEAR TO MONTH,
	interval_day INTERVAL DAY TO SECOND(4),
	long text,
	nchar char(10),
	nchar_varying varchar(10),
	number double precision,
	number1 integer,
	"number(*)" bigint,
	numeric double precision,
	nvarchar2 varchar(10),
	raw bytea,
	real double precision,
	row_id oid,
	smallint numeric(38),
	timestamp timestamp,
	"timestamp with time zone" timestamp with time zone,
	urowid oid,
	varchar varchar(10),
	varchar2 varchar(10),
	xmltype xml
) ;

```

#### テーブル定義

```
postgres> \d datatypes                                                                                                                                                                      
+--------------------------+-----------------------------+-------------+
| Column                   | Type                        | Modifiers   |
|--------------------------+-----------------------------+-------------|
| bfile                    | bytea                       |             |
| binary_float             | double precision            |             |
| binary_double            | double precision            |             |
| blob                     | bytea                       |             |
| char                     | character(10)               |             |
| character                | character(10)               |             |
| clob                     | text                        |             |
| nclob                    | text                        |             |
| date                     | timestamp without time zone |             |
| decimal                  | real                        |             |
| dec                      | real                        |             |
| double_precision         | double precision            |             |
| float                    | double precision            |             |
| integer                  | numeric(38,0)               |             |
| int                      | numeric(38,0)               |             |
| interval_year            | interval year to month      |             |
| interval_day             | interval day to second(4)   |             |
| long                     | text                        |             |
| nchar                    | character(10)               |             |
| nchar_varying            | character varying(10)       |             |
| number                   | double precision            |             |
| number1                  | integer                     |             |
| number(*)                | bigint                      |             |
| numeric                  | double precision            |             |
| nvarchar2                | character varying(10)       |             |
| raw                      | bytea                       |             |
| real                     | double precision            |             |
| row_id                   | oid                         |             |
| smallint                 | numeric(38,0)               |             |
| timestamp                | timestamp without time zone |             |
| timestamp with time zone | timestamp with time zone    |             |
| urowid                   | oid                         |             |
| varchar                  | character varying(10)       |             |
| varchar2                 | character varying(10)       |             |
| xmltype                  | xml                         |             |
+--------------------------+-----------------------------+-------------+

```

OracleとPostgreSQLを対比した結果は次の通り。一部SCTとora2pgで異なる結果が出た。SCTは下記を参照。

> AWS Schema Conversion Toolを使用したOracleからAurora(PostgreSQL)への変換結果 | my opinion is my own https://zatoima.github.io/aws-sct-oracle-to-aurora-postgresql-conversion.html

### OracleとPostgreSQLの対比一覧

| No.  | Oracle (※descの結果）         | PostgreSQL (\d メタコマンド結果） |
| ---- | ----------------------------- | --------------------------------- |
| 1    | BINARY FILE LOB               | bytea                             |
| 2    | BINARY_FLOAT                  | double precision                  |
| 3    | BINARY_DOUBLE                 | double precision                  |
| 4    | BLOB                          | bytea                             |
| 5    | CHAR(10)                      | character(10)                     |
| 6    | CHAR(10)                      | character(10)                     |
| 7    | CLOB                          | text                              |
| 8    | NCLOB                         | text                              |
| 9    | DATE                          | timestamp without time zone       |
| 10   | NUMBER(3,2)                   | real                              |
| 11   | NUMBER(3,2)                   | real                              |
| 12   | FLOAT(126)                    | double precision                  |
| 13   | FLOAT(3)                      | double precision                  |
| 14   | NUMBER(38)                    | numeric(38,0)                     |
| 15   | NUMBER(38)                    | numeric(38,0)                     |
| 16   | INTERVAL YEAR(4) TO MONTH     | interval year to month            |
| 17   | INTERVAL DAY(4) TO SECOND(4)  | interval day to second(4)         |
| 18   | LONG                          | text                              |
| 19   | NCHAR(10)                     | character(10)                     |
| 20   | NVARCHAR2(10)                 | character varying(10)             |
| 21   | NUMBER(9,9)                   | double precision                  |
| 22   | NUMBER(9)                     | integer                           |
| 23   | NUMBER                        | bigint                            |
| 24   | NUMBER(9,9)                   | double precision                  |
| 25   | NVARCHAR2(10)                 | character varying(10)             |
| 26   | RAW(10)                       | bytea                             |
| 27   | FLOAT(63)                     | double precision                  |
| 28   | ROWID                         | oid                               |
| 29   | NUMBER(38)                    | numeric(38,0)                     |
| 30   | TIMESTAMP(5)                  | timestamp without time zone       |
| 31   | TIMESTAMP(5) WITH TIME ZONE   | timestamp with time zone          |
| 32   | ROWID                         | oid                               |
| 33   | VARCHAR2(10)                  | character varying(10)             |
| 34   | VARCHAR2(10)                  | character varying(10)             |
| 35   | PUBLIC.XMLTYPE STORAGE BINARY | xml                               |



