---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Outputting Execution Plans for Specific Queries with PostgreSQL's auto_explain"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-auto_explain.html
date: 2020-03-03
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



### Introduction

The contrib module includes an extension called auto_explain that outputs execution plans for queries matching specific conditions to the log. I think this is a useful extension for monitoring and improving slow queries.

Since auto_explain is one of the contrib modules, you may need to install contrib as needed.

```sh
sudo yum -y install postgresql10-devel postgresql10-contrib
```

### Version

```sh
postgres=# select version();
                                                 version
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### pg_buffercache Configuration

Set the following parameters in `postgresql.conf`. With `auto_explain.log_min_duration`, execution plans for queries taking longer than the specified number of milliseconds will be output to the server log. This setting value needs to be changed according to requirements. Here it is set to 1 millisecond or more.

```sh
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = '1'
auto_explain.log_analyze=on
auto_explain.log_buffers=on
auto_explain.log_verbose=on
```

#### Related Parameters

| Parameter                     | Description                                                  |
| ----------------------------- | ------------------------------------------------------------ |
| auto_explain.log_min_duration | The minimum statement execution time in milliseconds at which execution plans start to be logged. |
| auto_explain.log_analyze      | Outputs EXPLAIN ANALYZE output instead of EXPLAIN output. Can cause extremely significant performance degradation. |
| auto_explain.log_buffers      | Controls whether buffer usage statistics are output when logging execution plans. Same as EXPLAIN's BUFFERS option. |
| auto_explain.log_timing       | Controls whether per-node timing information is output when execution plans are logged. |
| auto_explain.log_triggers     | Includes trigger execution statistics when logging execution plans. |
| auto_explain.log_verbose      | Controls whether verbose details are output. Same as EXPLAIN's VERBOSE option. |

## Usage

Execute a query. This performs a cross join on a table with 10,000 rows and counts the results. The SQL must take longer than auto_explain.log_min_duration.

```
select count(*) from t1,t2;
```

Ran two patterns.

### Pattern 1.)

- shared_preload_libraries = 'auto_explain'
- auto_explain.log_min_duration = '1'

```sh
2020-03-02 09:22:53.837 UTC [27039] LOG:  duration: 6715.237 ms  plan:
	Query Text: select count(*) from t1,t2;
	Aggregate  (cost=1500353.00..1500353.01 rows=1 width=8)
	  ->  Nested Loop  (cost=0.00..1250353.00 rows=100000000 width=0)
	        ->  Seq Scan on t1  (cost=0.00..164.00 rows=10000 width=0)
	        ->  Materialize  (cost=0.00..214.00 rows=10000 width=0)
	              ->  Seq Scan on t2  (cost=0.00..164.00 rows=10000 width=0)
```

### Pattern 2.)

- shared_preload_libraries = 'auto_explain'
- auto_explain.log_min_duration = '1'
- auto_explain.log_analyze=on
- auto_explain.log_buffers=on
- auto_explain.log_verbose=on

```sh
2020-03-02 09:36:56.407 UTC [27217] LOG:  duration: 399369.613 ms  plan:
	Query Text: select count(*) from t1,t2;
	Aggregate  (cost=1500353.00..1500353.01 rows=1 width=8) (actual time=399369.587..399369.588 rows=1 loops=1)
	  Output: count(*)
	  Buffers: shared hit=128
	  ->  Nested Loop  (cost=0.00..1250353.00 rows=100000000 width=0) (actual time=0.020..297204.066 rows=100000000 loops=1)
	        Buffers: shared hit=128
	        ->  Seq Scan on public.t1  (cost=0.00..164.00 rows=10000 width=0) (actual time=0.007..18.548 rows=10000 loops=1)
	              Output: t1.a, t1.b, t1.c, t1.d
	              Buffers: shared hit=64
	        ->  Materialize  (cost=0.00..214.00 rows=10000 width=0) (actual time=0.002..10.057 rows=10000 loops=10000)
	              Buffers: shared hit=64
	              ->  Seq Scan on public.t2  (cost=0.00..164.00 rows=10000 width=0) (actual time=0.005..11.372 rows=10000 loops=1)
	                    Buffers: shared hit=64
```

Pattern 2 outputs more information. However, the manual states for auto_explain.log_analyze: `When this parameter is enabled, per-plan-node timing occurs for all statements executed, regardless of how long they take to be logged. This can have an extremely significant negative impact on performance.` In this case, a difference in execution time of "6715.237 ms" vs "399369.613 ms" occurred. It would be counterproductive to affect production queries due to log collection, so please be careful with the `auto_explain.log_analyze` setting.

### Reference

> F.4. auto_explain https://www.postgresql.jp/document/10/html/auto-explain.html
