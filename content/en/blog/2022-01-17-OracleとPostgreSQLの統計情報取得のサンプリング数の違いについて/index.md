---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Differences in Sampling Count for Statistics Collection Between Oracle and PostgreSQL"
subtitle: ""
summary: " "
tags: ["Oracle","PostgreSQL"]
categories: ["Oracle","PostgreSQL"]
url: oracle-postgresql-dbms-stats-analyze-sampling
date: 2022-01-17
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

Statistics collection is an essential mechanism for the optimizer (planner) to generate appropriate execution plans, regardless of the database engine. However, there is a trade-off between sampling count and accuracy. A higher sampling count means more time is spent collecting statistics, while too few samples relative to the total population reduces statistical accuracy and may result in suboptimal execution plans.

When comparing Oracle and PostgreSQL statistics collection, I found that PostgreSQL's collection time was overwhelmingly shorter. Here are brief notes on why. The conclusion is that in default settings, PostgreSQL's sampling count is relatively fixed, whereas Oracle uses AUTO_SAMPLE_SIZE to increase or decrease the sampling count based on table size. This difference appears to be a major factor in the difference in collection time.

### Oracle's Case

Specified by the ESTIMATE_PERCENT parameter of the DBMS_STATS package. The default is AUTO_SAMPLE_SIZE, which lets Oracle automatically determine the optimal sample size. Larger tables get more samples, smaller tables get fewer. It claims "100% sampling accuracy at the cost of 10% sampling time," which is a remarkable feature. Statistically, that many samples should be sufficient for accuracy.

- PL/SQL Packages and Types Reference

> https://docs.oracle.com/cd/F19136_01/arpls/DBMS_STATS.html#GUID-7D7442B5-B060-40E9-AA18-2085E527C3B1
>
> Determines the percentage of rows to sample.
>
> The valid range is 0.000001 to 100. Using the constant DBMS_STATS.AUTO_SAMPLE_SIZE allows the database to determine an appropriate sample size for generating optimal statistics. This is the default.

- Best Practices for Gathering Optimizer Statistics with Oracle Database 19c

> https://www.oracle.com/technetwork/jp/database/bi-datawarehousing/twp-bp-for-stats-gather-19c-5324205-ja.pdf
>
> The ESTIMATE_PERCENT parameter determines the fraction of rows used to compute statistics. The most accurate statistics are collected when all rows in a table are processed (i.e., 100% sample), commonly referred to as computed statistics. Oracle Database 11g introduced a new hash-based sampling algorithm that achieves near 100% sample accuracy at a maximum cost of a 10% sample.

### PostgreSQL's Case

The sampling amount defaults to 30,000 records (MAX(column STATISTICS value) × 300 records).

The STATISTICS value is determined by:

- default_statistics_target parameter (default: 100)
- SET STATISTICS clause of the ALTER TABLE command for each column of a table
- SET STATISTICS clause of the ALTER INDEX command for expression-defined index columns

Running the analyze command with the verbose option on a large table shows `30000 rows in sample` and `scanned 30000 of 163935 pages`.

```sql
postgres=> show default_statistics_target;
 default_statistics_target
---------------------------
 100
(1 row)

postgres=> select count(*) from pgbench_accounts;
  count
----------
 10000000
(1 row)

postgres=>
postgres=> analyze verbose pgbench_accounts;
INFO:  analyzing "public.pgbench_accounts"
INFO:  "pgbench_accounts": scanned 30000 of 163935 pages, containing 1830000 live rows and 0 dead rows; 30000 rows in sample, 10000035 estimated total rows
ANALYZE
postgres=>
postgres=> select count(*) from pgbench_branches;
 count
-------
   100
(1 row)

postgres=> analyze verbose pgbench_branches;
INFO:  analyzing "public.pgbench_branches"
INFO:  "pgbench_branches": scanned 1 of 1 pages, containing 100 live rows and 0 dead rows; 100 rows in sample, 100 estimated total rows
ANALYZE
```

Of course, for tables with hundreds of millions of rows and high column value variety, this sample count may not lead to an appropriate execution plan. In such cases, you need to increase the sample count by adjusting the default_statistics_target parameter (or setting per-column statistics targets for more precise tuning). Be aware of the trade-off, as increasing the sample count takes more time.

The relevant manual section is here.

> ANALYZE https://www.postgresql.jp/document/13/html/sql-analyze.html
>
> For large tables, `ANALYZE` takes a random sample of the table contents, rather than examining every row. This allows even very large tables to be analyzed in a small amount of time. Note, however, that the statistics are only approximations, and will change slightly each time `ANALYZE` is run, even if the actual table contents did not change. This might result in small changes in the planner's estimated costs shown by `EXPLAIN`. In rare situations, this non-determinism will cause the planner to choose a different query plan between runs of `ANALYZE`. To avoid this, raise the amount of statistics collected by `ANALYZE`, as described below.

### References

- Best Practices for Gathering Optimizer Statistics with Oracle Database 19c https://www.oracle.com/technetwork/jp/database/bi-datawarehousing/twp-bp-for-stats-gather-19c-5324205-ja.pdf?utm_source=pocket_mylist
- Oracle Statistics Concepts https://www.oracle.com/technetwork/jp/database/bi-datawarehousing/twp-stats-concepts-19c-5324209-ja.pdf?utm_source=pocket_mylist
- Book: PostgreSQL Internal Structure Design and Operations Best Practices
