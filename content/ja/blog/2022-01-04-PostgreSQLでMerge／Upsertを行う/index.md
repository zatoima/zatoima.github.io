---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでMerge／Upsertを行う"
subtitle: ""
summary: " "
tags: [PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-merge-upsert
date: 2022-01-04
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

PostgreSQLの場合はMerge文というものはなくInsert on conflictを使うことになる。昔はCTE（共通テーブル式）を使ってUPSERT処理を行っていた模様。注意点としてはon conflictのところで制約が必要なくらい。

### テーブル作成

```sql
drop table PRODUCT;
CREATE TABLE PRODUCT (
    product_name   CHARACTER VARYING(50),
    product_type   CHARACTER VARYING (10),
    unit_price     DOUBLE PRECISION, 
    modified_date  TIMESTAMP
);

ALTER TABLE PRODUCT 
    ADD CONSTRAINT PRODUCT_PKEY PRIMARY KEY(product_name, product_type);
    
drop table PRODUCT;
CREATE TABLE PRODUCT_DELTA (
    product_name   CHARACTER VARYING (50),
    product_type   CHARACTER VARYING (10),
    unit_price     DOUBLE PRECISION, 
    status         CHAR(1)
);
```

### データ準備

```sql
--Insert into PRODUCT table
INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR1',  'A', 10, '2020-01-01');
INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR2',  'C', 10, '2020-01-01');
INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR3',  'B', 10, '2020-01-01');
INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR4',  'B', 10, '2020-01-01');
INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR10', 'A', 10, '2020-01-01');

-- insert into PRODUCT_DELTA table
INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR1', 'A', 20, 'Y');
INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR2', 'C', 20, 'N');
INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR5', 'F', 20, 'N');
INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR6', 'B', 20, 'N');
```

### upsert/merge

```sql
INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date)
  SELECT   src.product_name,
         src.product_type,
         src.unit_price,
         now() modified_date
  FROM ( SELECT
         		product_name,
           	product_type,
           	unit_price
        	FROM PRODUCT_DELTA
  ) src
ON CONFLICT(product_name, product_type)
DO UPDATE
       SET
         unit_price   = excluded.unit_price,
         modified_date = excluded.modified_date;
```

### 実行ログ

```sql
postgres=> CREATE TABLE PRODUCT (
postgres(>     product_name   CHARACTER VARYING(50),
postgres(>     product_type   CHARACTER VARYING (10),
postgres(>     unit_price     DOUBLE PRECISION, 
postgres(>     modified_date  TIMESTAMP
postgres(> );
CREATE TABLE
postgres=> ALTER TABLE PRODUCT 
postgres->     ADD CONSTRAINT PRODUCT_PKEY PRIMARY KEY(product_name, product_type);
ALTER TABLE
postgres=> CREATE TABLE PRODUCT_DELTA (
postgres(>     product_name   CHARACTER VARYING (50),
postgres(>     product_type   CHARACTER VARYING (10),
postgres(>     unit_price     DOUBLE PRECISION, 
postgres(>     status         CHAR(1)
postgres(> );
CREATE TABLE
postgres=> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR1',  'A', 10, '2020-01-01');
ce, modified_date) VALUES('PR10', 'A', 10, '2020-01-01');INSERT 0 1
postgres=> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR2',  'C', 10, '2020-01-01');
INSERT 0 1
postgres=> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR3',  'B', 10, '2020-01-01');
INSERT 0 1
postgres=> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR4',  'B', 10, '2020-01-01');
INSERT 0 1
postgres=> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date) VALUES('PR10', 'A', 10, '2020-01-01');
INSERT 0 1
postgres=> 
postgres=> INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR1', 'A', 20, 'Y');
INSERT 0 1
postgres=> INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR2', 'C', 20, 'N');
INSERT 0 1
postgres=> INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR5', 'F', 20, 'N');
INSERT 0 1
postgres=> INSERT INTO PRODUCT_DELTA(product_name, product_type, unit_price, status) VALUES('PR6', 'B', 20, 'N');
INSERT 0 1
postgres=> 
postgres=> 
postgres=> select * from PRODUCT;
 product_name | product_type | unit_price |    modified_date    
--------------+--------------+------------+---------------------
 PR1          | A            |         10 | 2020-01-01 00:00:00
 PR2          | C            |         10 | 2020-01-01 00:00:00
 PR3          | B            |         10 | 2020-01-01 00:00:00
 PR4          | B            |         10 | 2020-01-01 00:00:00
 PR10         | A            |         10 | 2020-01-01 00:00:00
(5 rows)

postgres=> select * from PRODUCT_DELTA;
 product_name | product_type | unit_price | status 
--------------+--------------+------------+--------
 PR1          | A            |         20 | Y
 PR2          | C            |         20 | N
 PR5          | F            |         20 | N
 PR6          | B            |         20 | N
(4 rows)

postgres=> 
postgres=> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date)
postgres->   SELECT   src.product_name,
postgres->          src.product_type,
postgres->          src.unit_price,
postgres->          now() modified_date
postgres->   FROM ( SELECT
postgres(>          

postgres(>          product_name,
postgres(>            product_type,
postgres(>            unit_price
postgres(>         FROM PRODUCT_DELTA
postgres(>   ) src
postgres-> ON CONFLICT(product_name, product_type)
postgres-> DO UPDATE
postgres->        SET
postgres->          unit_price   = excluded.unit_price,
postgres->          modified_date = excluded.modified_date;
INSERT 0 4
postgres=> 
postgres=> select * from PRODUCT
postgres-> ;
 product_name | product_type | unit_price |       modified_date        
--------------+--------------+------------+----------------------------
 PR3          | B            |         10 | 2020-01-01 00:00:00
 PR4          | B            |         10 | 2020-01-01 00:00:00
 PR10         | A            |         10 | 2020-01-01 00:00:00
 PR1          | A            |         20 | 2021-12-23 05:42:30.980878
 PR2          | C            |         20 | 2021-12-23 05:42:30.980878
 PR5          | F            |         20 | 2021-12-23 05:42:30.980878
 PR6          | B            |         20 | 2021-12-23 05:42:30.980878
(7 rows)

postgres=> 
postgres=> explain analyze
postgres-> INSERT INTO PRODUCT(product_name, product_type, unit_price, modified_date)
postgres->   SELECT   src.product_name,
postgres->          src.product_type,
postgres->          src.unit_price,
postgres->          now() modified_date
postgres->   FROM ( SELECT
postgres(>          

postgres(>          product_name,
postgres(>            product_type,
postgres(>            unit_price
postgres(>         FROM PRODUCT_DELTA
postgres(>   ) src
postgres-> ON CONFLICT(product_name, product_type)
postgres-> DO UPDATE
postgres->        SET
postgres->          unit_price   = excluded.unit_price,
postgres->          modified_date = excluded.modified_date;
                                                    QUERY PLAN                                                    
------------------------------------------------------------------------------------------------------------------
 Insert on product  (cost=0.00..16.00 rows=400 width=172) (actual time=0.115..0.116 rows=0 loops=1)
   Conflict Resolution: UPDATE
   Conflict Arbiter Indexes: product_pkey
   Tuples Inserted: 0
   Conflicting Tuples: 4
   ->  Seq Scan on product_delta  (cost=0.00..16.00 rows=400 width=172) (actual time=0.014..0.016 rows=4 loops=1)
 Planning time: 0.056 ms
 Execution time: 0.142 ms
(8 rows)
```

参考

> [Best practices for migrating Oracle database MERGE statements to Amazon Aurora PostgreSQL and Amazon RDS PostgreSQL \| AWS Database Blog](https://aws.amazon.com/jp/blogs/database/best-practices-for-migrating-oracle-database-merge-statements-to-amazon-aurora-postgresql-and-amazon-rds-postgresql/?utm_source=pocket_mylist)
