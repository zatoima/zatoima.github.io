---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでソートをメモリでは無く敢えてディスクで発生させる方法"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-disk-external-merge-sort
date: 2022-01-20
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

### pgbenchでデータ生成

適宜スケールファクターの数値を設定する

```sql
create database pgbench;
pgbench -i -s 100 -U postgres -h  aurorapgsqlv1.cluster-xxx.ap-northeast-1.rds.amazonaws.com
```

### work_memを低い数値に設定してSQLを実行

```sql
SET work_mem=1024;
EXPLAIN (ANALYZE,BUFFERS) SELECT t1.aid,t1.bid,t1.abalance,t2.bbalance FROM pgbench_accounts t1, pgbench_branches t2 where t1.bid=t2.bid ORDER BY t1.abalance DESC;
```

### 実行ログ

external merge Diskが発生していて147秒もかかっている。大部分がSort部分。

```sql

pgbench=> SET work_mem=1024;
SET
pgbench=> 
pgbench=> EXPLAIN (ANALYZE,BUFFERS) SELECT t1.aid,t1.bid,t1.abalance,t2.bbalance FROM pgbench_accounts t1, pgbench_branches t2 where t1.bid=t2.bid ORDER BY t1.abalance DESC;
                                                                           QUERY PLAN                                                                           
----------------------------------------------------------------------------------------------------------------------------------------------------------------
 Gather Merge  (cost=11000684.94..20723586.06 rows=83333334 width=16) (actual time=110248.334..141130.354 rows=100000000 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   Buffers: shared hit=1639508, temp read=1828307 written=1835749
   ->  Sort  (cost=10999684.91..11103851.58 rows=41666667 width=16) (actual time=109509.807..113561.825 rows=33333333 loops=3)
         Sort Key: t1.abalance DESC
         Sort Method: external merge  Disk: 852192kB
         Worker 0:  Sort Method: external merge  Disk: 855776kB
         Worker 1:  Sort Method: external merge  Disk: 836160kB
         Buffers: shared hit=1639508, temp read=1828307 written=1835749
         ->  Hash Join  (cost=27.50..2165877.71 rows=41666667 width=16) (actual time=0.328..10296.741 rows=33333333 loops=3)
               Hash Cond: (t1.bid = t2.bid)
               Buffers: shared hit=1639414
               ->  Parallel Seq Scan on pgbench_accounts t1  (cost=0.00..2056011.67 rows=41666667 width=12) (actual time=0.004..4573.584 rows=33333333 loops=3)
                     Buffers: shared hit=1639345
               ->  Hash  (cost=15.00..15.00 rows=1000 width=8) (actual time=0.272..0.273 rows=1000 loops=3)
                     Buckets: 1024  Batches: 1  Memory Usage: 48kB
                     Buffers: shared hit=15
                     ->  Seq Scan on pgbench_branches t2  (cost=0.00..15.00 rows=1000 width=8) (actual time=0.005..0.107 rows=1000 loops=3)
                           Buffers: shared hit=15
 Planning Time: 0.386 ms
 Execution Time: 147284.085 ms
(22 rows)

```

