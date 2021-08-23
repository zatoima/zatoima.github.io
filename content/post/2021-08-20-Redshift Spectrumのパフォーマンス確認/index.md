---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshift Spectrumのパフォーマンス確認"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-spectrum-performance-check
date: 2021-08-20
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



### テストクエリ

```sql
\timing
SET enable_result_cache_for_session = off;

select d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit
from s3.dwdate, s3.customer, s3.supplier, s3.part, s3.lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = 'AMERICA'
and s_nation = 'UNITED STATES'
and (d_year = 1997 or d_year = 1998)
and p_category = 'MFGR#14'
group by d_year, s_city, p_brand1 order by d_year, s_city, p_brand1
LIMIT 10;
```

### 実行時間、実行結果

1分20秒程度掛かった

```sql
mydb=# select d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit
mydb-# from s3.dwdate, s3.customer, s3.supplier, s3.part, s3.lineorder
mydb-# where lo_custkey = c_custkey
mydb-# and lo_suppkey = s_suppkey
mydb-# and lo_partkey = p_partkey
mydb-# and lo_orderdate = d_datekey
mydb-# and c_region = 'AMERICA'
mydb-# and s_nation = 'UNITED STATES'
mydb-# and (d_year = 1997 or d_year = 1998)
mydb-# and p_category = 'MFGR#14'
mydb-# group by d_year, s_city, p_brand1 order by d_year, s_city, p_brand1
mydb-# LIMIT 10;
 d_year |   s_city   | p_brand1  |  profit   
--------+------------+-----------+-----------
   1997 | UNITED ST0 | MFGR#141  | 262922467
   1997 | UNITED ST0 | MFGR#1410 | 179590048
   1997 | UNITED ST0 | MFGR#1411 | 215249314
   1997 | UNITED ST0 | MFGR#1412 | 164321123
   1997 | UNITED ST0 | MFGR#1413 | 175368488
   1997 | UNITED ST0 | MFGR#1414 | 215494333
   1997 | UNITED ST0 | MFGR#1415 | 148209735
   1997 | UNITED ST0 | MFGR#1416 | 198091798
   1997 | UNITED ST0 | MFGR#1417 | 176595141
   1997 | UNITED ST0 | MFGR#1418 | 194768567
(10 rows)

Time: 80526.072 ms (01:20.526)
mydb=# 
```

### SVL_S3QUERY_SUMMARY テーブルの確認

テーブルには過去のクエリ実行の実際の統計が格納されるので、そこで時間が掛かったのかを知ることが出来る

```sql
select elapsed, s3_scanned_rows, s3_scanned_bytes,
  s3query_returned_rows, s3query_returned_bytes, files, avg_request_parallelism
from svl_s3query_summary
where query = pg_last_query_id()
order by query,segment;
```

```sql
mydb=# select elapsed, s3_scanned_rows, s3_scanned_bytes,
mydb-#   s3query_returned_rows, s3query_returned_bytes, files, avg_request_parallelism
mydb-# from svl_s3query_summary
mydb-# where query = pg_last_query_id()
mydb-# order by query,segment;
 elapsed  | s3_scanned_rows | s3_scanned_bytes | s3query_returned_rows | s3query_returned_bytes | files | avg_request_parallelism 
----------+-----------------+------------------+-----------------------+------------------------+-------+-------------------------
   269908 |            2556 |            25239 |                   729 |                   1830 |     1 |                     0.1
  1272336 |         1000000 |         34110277 |                 39991 |                 141551 |     4 |                     0.5
  2847076 |         3000000 |        105338147 |                599689 |                1748517 |     1 |                     0.1
   800323 |         1400000 |         34724133 |                 55855 |                 266349 |     4 |                     0.4
 73152028 |       600037902 |      26972503425 |                234982 |                3906264 |     8 |                     0.8
(5 rows)

Time: 558.935 ms
```

