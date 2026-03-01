---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Trying QPM (Query Plan Management) in Aurora (PostgreSQL)"
subtitle: ""
summary: " "
tags: ["AWS", "RDS", "Aurora", "PostgreSQL"]
categories: ["AWS", "RDS", "Aurora", "PostgreSQL"]
url: aurora-postgresql-query-plan-management.html
date: 2019-11-13
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


### What is QPM (Query Plan Management)?

***

A feature that records execution plans for SQL, then either fixes those execution plans or migrates them to another environment for fixation. This is equivalent to Oracle's SPM (SQL Plan Management). Since Aurora (PostgreSQL) also supports this feature, let's actually try it.

##### How to Control Query Plan Management

```sql
rds.enable_plan_management = { 0,1} # Set in parameter group

apg_plan_mgmt.capture_plan_baselines = { manual, automatic, off }
# automatic : Automatic plan capture. Captures SQL executed one or more times
# manual    : Manually capture execution plans for individual SQL
# off       : Disable Query Plan capture

apg_plan_mgmt.use_plan_baselines = { true, false }
# true  : Use captured Query Plan to fix execution plan
# false : Do not use captured Query Plan
```

### Environment and Scenario Description

***

Assuming migration of execution plans from development environment to production environment.

- Production DB name: prod
- Development DB name: dev

Migrate the full scan (seq scan) execution plan from the development environment to the production environment to reproduce an inefficient execution plan.

### Modify Parameter Group (dev/prod environments)

***

Set `rds.enable_plan_management` in the cluster parameter group to `1`

### Enable Extension (dev/prod environments)

***

Install apg_plan_mgmt using the create extension command

##### Command

```sql
\dx
create extension apg_plan_mgmt;
\dx
```

##### Execution Result

```sql
# Execution result
dev=> \dx
                 List of installed extensions
  Name   | Version |   Schema   |         Description
---------+---------+------------+------------------------------
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(1 row)
dev=>
dev=> create extension apg_plan_mgmt;    # Enable extension
CREATE EXTENSION
dev=> \dx
                                        List of installed extensions
     Name      | Version |    Schema     |                            Description

---------------+---------+---------------+--------------------------------------------------
-----------------
 apg_plan_mgmt | 1.0.1   | apg_plan_mgmt | Amazon Aurora with PostgreSQL compatibility Query # ★← apg_plan_mgmt added
 Plan Management
 plpgsql       | 1.0     | pg_catalog    | PL/pgSQL procedural language
(2 rows)
dev=>
dev=>
```



### Pre-check dba_plans Table (dev/prod environments)

***

The apg_plan_mgmt.dba_plans table has nothing stored in it yet.

##### Command

```sql
SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
FROM   apg_plan_mgmt.dba_plans
ORDER BY sql_text, plan_created;
```

##### Execution Result

```sql
dev=> SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
dev-> FROM   apg_plan_mgmt.dba_plans
dev-> ORDER BY sql_text, plan_created;
 sql_hash | plan_hash | status | enabled | sql_text
----------+-----------+--------+---------+----------
(0 rows)
```



### Create Test Table (dev/prod environments)

***

Create a test table

##### Command

```sql
CREATE TABLE t1 AS
SELECT num                         a -- generated value
      ,'1'                         b -- constant
      ,to_char(num,'FM00000')      c -- use generated value (string like ID)
      ,current_timestamp      d
FROM   generate_series(1,10000) num
;

ALTER TABLE t1 ADD PRIMARY KEY(a);

\d t1
```

##### Execution Result

```sql
dev=> CREATE TABLE t1 AS
dev-> SELECT num                         a -- generated value
dev->       ,'1'                         b -- constant
dev->       ,to_char(num,'FM00000')      c -- use generated value (string like ID)
dev->       ,current_timestamp      d
dev-> FROM   generate_series(1,10000) num
dev-> ;
SELECT 10000
dev=>
dev=> ALTER TABLE t1 ADD PRIMARY KEY(a);
ALTER TABLE
dev=>
dev=> \d t1
                         Table "public.t1"
 Column |           Type           | Collation | Nullable | Default
--------+--------------------------+-----------+----------+---------
 a      | integer                  |           | not null |
 b      | text                     |           |          |
 c      | text                     |           |          |
 d      | timestamp with time zone |           |          |
Indexes:
    "t1_pkey" PRIMARY KEY, btree (a)
dev=>
```



### Execute SQL and Capture (dev environment)

***

Execute SQL that results in **full scan (seq scan)** and SQL that results in **Index Scan**. At this time, manually capture only the execution plan for the SQL that results in **full scan (seq scan)**.

In this example, you can see that "Plan Hash: -52705300" has been captured in the `apg_plan_mgmt.dba_plans` table.

##### Command

```sql
SET apg_plan_mgmt.capture_plan_baselines = manual; # Enable manual execution plan capture

explain (hashes true) select count(*) from t1 where a > 1;

SET apg_plan_mgmt.capture_plan_baselines = off;  # Stop manual execution plan capture

explain (hashes true) select count(*) from t1 where a > 9999;

SET apg_plan_mgmt.capture_plan_baselines = off;

SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
FROM   apg_plan_mgmt.dba_plans
ORDER BY sql_text, plan_created;
```

##### Execution Result

```sql
# Execution log
dev=> SET apg_plan_mgmt.capture_plan_baselines = manual;
SET
dev=>
dev=> explain (hashes true) select count(*) from t1 where a > 1;
                          QUERY PLAN
--------------------------------------------------------------
 Aggregate  (cost=214.00..214.01 rows=1 width=8)
   ->  Seq Scan on t1  (cost=0.00..189.00 rows=10000 width=0)
         Filter: (a > 1)
 SQL Hash: -1895827505, Plan Hash: -52705300
(4 rows)
dev=>
dev=>
dev=> SET apg_plan_mgmt.capture_plan_baselines = off;
SET
dev=>
dev=>
dev=>
dev=> explain (hashes true) select count(*) from t1 where a > 9999;
                                 QUERY PLAN
-----------------------------------------------------------------------------
 Aggregate  (cost=8.30..8.31 rows=1 width=8)
   ->  Index Only Scan using t1_pkey on t1  (cost=0.29..8.30 rows=1 width=0)
         Index Cond: (a > 9999)
 Plan Hash: 1222455040
(4 rows)
dev=>
dev=> SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
dev-> FROM   apg_plan_mgmt.dba_plans
dev-> ORDER BY sql_text, plan_created;
  sql_hash   | plan_hash |  status  | enabled |               sql_text
-------------+-----------+----------+---------+--------------------------------------
 -1895827505 | -52705300 | Approved | t       | select count(*) from t1 where a > 1; # ★← execution plan has been captured
(1 row)
dev=>
dev=>
dev=>
```



### Create Export Table (dev)

***

```sql
CREATE TABLE plans_copy AS SELECT * FROM apg_plan_mgmt.plans;
```



### Export Using pg_dump (dev)

***

```sql
export PGPASSWORD=xxxxxx
pg_dump -U postgres -h aurora-postgres-cluster-dev.cluster-xxxxxxxx.ap-northeast-1.rds.amazonaws.com -t plans_copy -Ft dev > plans_copy.tar

# Delete the intermediate table if no longer needed
--DROP TABLE plans_copy;
```



### Import to Another DB (prod)

***

```sql
pg_restore -U postgres -h aurora-postgres-cluster-prod.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com -t plans_copy -Ft plans_copy.tar -d prod
```

### Verify Import and Merge (prod)

***

Perform execution plan merge with reference to this manual section.

> Maintaining Execution Plans - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Optimize.Maintenance.html#AuroraPostgreSQL.Optimize.Maintenance.ExportingImporting
>
> > Exporting and importing plans

##### Command

```sql
INSERT INTO apg_plan_mgmt.plans SELECT * FROM plans_copy
 ON CONFLICT ON CONSTRAINT plans_pkey
 DO UPDATE SET
 status = EXCLUDED.status,
 enabled = EXCLUDED.enabled,
 last_used = CASE WHEN EXCLUDED.last_used > plans.last_used
 THEN EXCLUDED.last_used ELSE plans.last_used END,
 estimated_startup_cost = EXCLUDED.estimated_startup_cost,
 estimated_total_cost = EXCLUDED.estimated_total_cost,
 planning_time_ms = EXCLUDED.planning_time_ms,
 execution_time_ms = EXCLUDED.execution_time_ms,
-- estimated_rows = EXCLUDED.estimated_rows,
-- actual_rows = EXCLUDED.actual_rows,
 total_time_benefit_ms = EXCLUDED.total_time_benefit_ms,
 execution_time_benefit_ms = EXCLUDED.execution_time_benefit_ms;

# Reload management plans to shared memory
SELECT apg_plan_mgmt.reload(); -- refresh shared memory
DROP TABLE plans_copy;

-- Verify
SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
FROM   apg_plan_mgmt.dba_plans
ORDER BY sql_text, plan_created;
```

Note that estimated_rows and actual_rows need to be commented out. It appears these columns don't actually exist. Manual error?

```sql
ERROR:  column excluded.actual_rows does not exist
LINE 13:  actual_rows = EXCLUDED.actual_rows,
```

##### Execution Result

```sql
prod=> INSERT INTO apg_plan_mgmt.plans SELECT * FROM plans_copy
prod->  ON CONFLICT ON CONSTRAINT plans_pkey
prod->  DO UPDATE SET
prod->  status = EXCLUDED.status,
prod->  enabled = EXCLUDED.enabled,
prod->  last_used = CASE WHEN EXCLUDED.last_used > plans.last_used
prod->  THEN EXCLUDED.last_used ELSE plans.last_used END,
prod->  estimated_startup_cost = EXCLUDED.estimated_startup_cost,
prod->  estimated_total_cost = EXCLUDED.estimated_total_cost,
prod->  planning_time_ms = EXCLUDED.planning_time_ms,
prod->  execution_time_ms = EXCLUDED.execution_time_ms,
prod-> -- estimated_rows = EXCLUDED.estimated_rows,
prod-> -- actual_rows = EXCLUDED.actual_rows,
prod->  total_time_benefit_ms = EXCLUDED.total_time_benefit_ms,
prod->  execution_time_benefit_ms = EXCLUDED.execution_time_benefit_ms;
INSERT 0 2
prod=>
prod=>
prod=> SELECT apg_plan_mgmt.reload();
 reload
--------
      0
(1 row)
prod=>
prod=>
prod=> DROP TABLE plans_copy;
DROP TABLE
prod=>
prod=>
prod=>
prod=>
prod=> SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
prod-> FROM   apg_plan_mgmt.dba_plans
prod-> ORDER BY sql_text, plan_created;
  sql_hash   | plan_hash  |   status   | enabled |                sql_text
-------------+------------+------------+---------+-----------------------------------------
 -1895827505 |  -52705300 | Approved   | t       | select count(*) from t1 where a > 1;
(2 rows)
prod=>
prod=>
prod=>

```

### Execute SQL

In this example, we are forcing a fullscan where an index scan would be selected.

##### Command

```sql
-- SQL test
SET apg_plan_mgmt.use_plan_baselines = true;
explain (hashes true) select count(*) from t1 where a > 9999;
SET apg_plan_mgmt.use_plan_baselines = false;
```

##### Execution Result

```sql
prod=> SET apg_plan_mgmt.use_plan_baselines = true;
prod=>
prod=> explain (hashes true) select count(*) from t1 where a > 9999;
                                   QUERY PLAN
---------------------------------------------------------------------------------
 Aggregate  (cost=189.00..189.01 rows=1 width=8)
   ->  Seq Scan on t1  (cost=0.00..189.00 rows=1 width=0)
         Filter: (a > 9999)
 Note: An Approved plan was used instead of the minimum cost plan.
 SQL Hash: -1895827505, Plan Hash: -52705300, Minimum Cost Plan Hash: 1222455040
(5 rows)
prod=> SET apg_plan_mgmt.use_plan_baselines = false;
SET

```

In this example, the WHERE clause is filtering down the data, so the index scan is the correct execution plan. However, QPM has captured the execution plan for `select count(*) from t1 where a > 1;`, which results in a Full scan (Seq Scan). This is a pattern where we deliberately selected an inefficient execution plan.

The log also indicates `Note: An Approved plan was used instead of the minimum cost plan.` - saying that there is a plan with better cost.

> prod=> explain (hashes true) select count(*) from t1 where a > 9999;
>
> QUERY PLAN
>
> Aggregate  (cost=189.00..189.01 rows=1 width=8)
> ->  Seq Scan on t1  (cost=0.00..189.00 rows=1 width=0)
>    Filter: (a > 9999)
> Note: An Approved plan was used instead of the minimum cost plan.
> SQL Hash: -1895827505, Plan Hash: -52705300, Minimum Cost Plan Hash: 1222455040

### References

***

> Maintaining Execution Plans - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Optimize.Maintenance.html
>
> Use Cases for Query Plan Management in Amazon Aurora PostgreSQL | Amazon Web Services Blog https://aws.amazon.com/jp/blogs/news/use-cases-for-query-plan-management-in-amazon-aurora-postgresql/
