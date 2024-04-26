---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshift Spectrum用にテストデータの準備、及びクエリの実行"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-spectrum-data-prepare-query-execute
date: 2021-09-10
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



### はじめに

一定のテストデータ、及び多少の負荷が掛かるSQLをRedshift Spectrumに向けて実行したい場合の作業用メモ。

### データ確認

データは`s3://awssampledbuswest2/ssbgz/`から自バケットに予めコピーしている

```sql
aws s3 ls --human-readable --recursive s3://ssbgz-spectrum/
```

```sql
[ec2-user@bastin ~]$ aws s3 ls --human-readable --recursive s3://ssbgz-spectrum/
2021-06-15 16:10:10  100.5 MiB customer/customer0002_part_00.gz
2021-06-15 16:10:10   24.6 KiB dwdate/dwdate.tbl.gz
2021-06-15 16:10:10    3.1 GiB lineorder/lineorder0000_part_00.gz
2021-06-15 16:10:10    3.1 GiB lineorder/lineorder0001_part_00.gz
2021-06-15 16:10:11    3.1 GiB lineorder/lineorder0002_part_00.gz
2021-06-15 16:10:10    3.1 GiB lineorder/lineorder0003_part_00.gz
2021-06-15 16:10:14    3.1 GiB lineorder/lineorder0004_part_00.gz
2021-06-15 16:11:47    3.1 GiB lineorder/lineorder0005_part_00.gz
2021-06-15 16:12:16    3.1 GiB lineorder/lineorder0006_part_00.gz
2021-06-15 16:12:26    3.1 GiB lineorder/lineorder0007_part_00.gz
2021-06-15 16:12:35    8.3 MiB part/part0000_part_00.gz
2021-06-15 16:12:36    8.3 MiB part/part0001_part_00.gz
2021-06-15 16:12:38    8.3 MiB part/part0002_part_00.gz
2021-06-15 16:12:39    8.3 MiB part/part0003_part_00.gz
2021-06-15 16:12:40   32.5 MiB supplier/supplier.tbl_0000_part_00.gz
2021-06-15 16:12:42   20 Bytes supplier/supplier0001_part_00.gz
2021-06-15 16:12:42   20 Bytes supplier/supplier0002_part_00.gz
2021-06-15 16:12:42   20 Bytes supplier/supplier0003_part_00.gz

```

### 外部スキーマ定義

```sql
create external schema s3 from data catalog
database 's3_spectrum'
iam_role 'arn:aws:iam::xxxxxxxxxxx:role/myRedshiftRole'
create external database if not exists;
```

```sql
mydb=# create external schema s3 from data catalog
mydb-# database 's3_spectrum'
mydb-# iam_role 'arn:aws:iam::xxxxxxxxxxx:role/myRedshiftRole'
mydb-# create external database if not exists;
INFO:  External database "s3_spectrum" already exists
CREATE SCHEMA
```

### 外部表の定義

```sql
drop table s3.part;
CREATE EXTERNAL TABLE s3.part 
(
  p_partkey     INTEGER,
  p_name        VARCHAR(22),
  p_mfgr        VARCHAR(6),
  p_category    VARCHAR(7),
  p_brand1      VARCHAR(9),
  p_color       VARCHAR(11),
  p_type        VARCHAR(25),
  p_size        INTEGER,
  p_container   VARCHAR(10))
row format delimited
fields terminated by '|'
stored as textfile
LOCATION 's3://ssbgz-spectrum/part/';

drop table s3.supplier;
CREATE EXTERNAL TABLE s3.supplier 
(
  s_suppkey   INTEGER,
  s_name      VARCHAR(25),
  s_address   VARCHAR(25),
  s_city      VARCHAR(10),
  s_nation    VARCHAR(15),
  s_region    VARCHAR(12),
  s_phone     VARCHAR(15))
row format delimited
fields terminated by '|'
stored as textfile
LOCATION 's3://ssbgz-spectrum/supplier/';

drop table s3.customer;
CREATE EXTERNAL TABLE s3.customer 
(
  c_custkey      INTEGER,
  c_name         VARCHAR(25),
  c_address      VARCHAR(25),
  c_city         VARCHAR(10),
  c_nation       VARCHAR(15),
  c_region       VARCHAR(12),
  c_phone        VARCHAR(15),
  c_mktsegment   VARCHAR(10))
row format delimited
fields terminated by '|'
stored as textfile
LOCATION 's3://ssbgz-spectrum/customer/';

drop table s3.dwdate;
CREATE EXTERNAL TABLE s3.dwdate 
(
  d_datekey            INTEGER,
  d_date               VARCHAR(19),
  d_dayofweek          VARCHAR(10),
  d_month              VARCHAR(10),
  d_year               INTEGER,
  d_yearmonthnum       INTEGER,
  d_yearmonth          VARCHAR(8),
  d_daynuminweek       INTEGER,
  d_daynuminmonth      INTEGER,
  d_daynuminyear       INTEGER,
  d_monthnuminyear     INTEGER,
  d_weeknuminyear      INTEGER,
  d_sellingseason      VARCHAR(13),
  d_lastdayinweekfl    VARCHAR(1),
  d_lastdayinmonthfl   VARCHAR(1),
  d_holidayfl          VARCHAR(1),
  d_weekdayfl          VARCHAR(1))
row format delimited
fields terminated by '|'
stored as textfile
LOCATION 's3://ssbgz-spectrum/dwdate/';

drop table s3.lineorder;
CREATE EXTERNAL TABLE s3.lineorder 
(
  lo_orderkey          INTEGER,
  lo_linenumber        INTEGER,
  lo_custkey           INTEGER,
  lo_partkey           INTEGER,
  lo_suppkey           INTEGER,
  lo_orderdate         INTEGER,
  lo_orderpriority     VARCHAR(15),
  lo_shippriority      VARCHAR(1),
  lo_quantity          INTEGER,
  lo_extendedprice     INTEGER,
  lo_ordertotalprice   INTEGER,
  lo_discount          INTEGER,
  lo_revenue           INTEGER,
  lo_supplycost        INTEGER,
  lo_tax               INTEGER,
  lo_commitdate        INTEGER,
  lo_shipmode          VARCHAR(10))
row format delimited
fields terminated by '|'
stored as textfile
LOCATION 's3://ssbgz-spectrum/lineorder/';
```

### テストクエリ

```sql
SELECT
    c_city,
    s_city,
    d_year,
    SUM(lo_revenue) AS revenue
FROM
    s3.customer,
    s3.lineorder,
    s3.supplier,
    s3.dwdate
WHERE
    lo_custkey = c_custkey AND
    lo_suppkey = s_suppkey AND
    lo_orderdate = d_datekey AND
    (c_city='UNITED KI1' OR c_city='UNITED KI5') AND
    (s_city='UNITED KI1' OR s_city='UNITED KI5') AND
    d_yearmonth = 'Dec1997'
GROUP BY
    c_city,
    s_city,
    d_year
ORDER BY
    d_year ASC,
    revenue DESC;
```

