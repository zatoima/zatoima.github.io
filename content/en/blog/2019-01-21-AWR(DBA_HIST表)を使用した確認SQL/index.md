---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Useful SQL Queries Using AWR (DBA_HIST Tables)"
subtitle: ""
summary: " "
tags: ["Oracle","AWR"]
categories: ["Oracle","AWR"]
url: oracle-awr-checksql
date: 2019-01-21
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

AWR (Automatic Workload Repository) is a feature that automatically collects and manages snapshots of Oracle Database operational statistics and workload information.

Typically, AWR analysis is performed by outputting AWR reports in HTML or text format and then reviewing performance and operational statistics from those reports to analyze and formulate improvement plans.

Since AWR reports reference various data dictionaries (DBA_HIST tables), you can directly query those dictionaries for various types of analysis.

Note that using AWR requires an additional "Diagnostic Pack" license.

### Report Past SQL Monitoring Results Stored in AWR (Oracle 12c and Later)

```sql
SELECT report_id,
       GENERATION_TIME,
       key1
FROM dba_hist_reports
WHERE component_name='sqlmonitor'
  AND key1='5j5wp4d5s9pqz';
```

### Check SQL Stored in AWR

```sql
select
    a.begin_interval_time,
    b.sql_id,
    c.sql_text
from DBA_HIST_SNAPSHOT a, DBA_HIST_SQLSTAT st, DBA_HIST_SQLTEXT c
where a.dbid=b.dbid and a.instance_number=b.instance_number and a.snap_id=b.snap_id
      and b.dbid=c.dbid and b.sql_id=c.sql_id
      and c.sql_text like '%<search SQL>%';
```

### Report Past SQL Monitoring Results Stored in AWR (Oracle 12c and Later)

```sql
SELECT report_id,
       GENERATION_TIME,
       key1
FROM dba_hist_reports
WHERE component_name='sqlmonitor'
  AND key1='5j5wp4d5s9pqz';
```

### Check AWR Snapshots

```sql
SELECT DBID
     , SNAP_ID
     , MIN(TO_CHAR(BEGIN_INTERVAL_TIME, 'YYYY/MM/DD HH24:MI:SS')) AS BEGIN_INTERVAL_TIME
     , MIN(TO_CHAR(END_INTERVAL_TIME  , 'YYYY/MM/DD HH24:MI:SS')) AS END_INTERVAL_TIME
  FROM DBA_HIST_SNAPSHOT
 WHERE DBID = xxxxxxxxx
 GROUP BY DBID
        , SNAP_ID
 ORDER BY 1,2,3,4;
```

### Check Long-Running SQL from dba_undo_stat (Cumulative)

```sql
select MAXQUERYSQLID,sum(MAXQUERYLEN)
from dba_hist_undostat where dbid='xxxxxxxxx'
AND BEGIN_TIME >= TO_TIMESTAMP('2016/02/10 20:00:00', 'YYYY/MM/DD HH24:MI:SS')
AND END_TIME <=  TO_TIMESTAMP('2016/10/31 20:15:00', 'YYYY/MM/DD HH24:MI:SS')
group by MAXQUERYSQLID
order by 2;
```

### Check Long-Running SQL from dba_undo_stat (Individual)

```sql
select MAXQUERYSQLID,sum(MAXQUERYLEN)
from dba_hist_undostat where dbid='xxxxxxxxx'
AND BEGIN_TIME >= TO_TIMESTAMP('2016/02/10 20:00:00', 'YYYY/MM/DD HH24:MI:SS')
AND END_TIME <=  TO_TIMESTAMP('2016/10/31 20:15:00', 'YYYY/MM/DD HH24:MI:SS')
group by MAXQUERYSQLID
order by 2;
```

### Check Shared Pool Resize History from AWR

```sql
col CURRENT_SIZE for 999,999,999,999,999
col MIN_SIZE for 999,999,999,999,999
col MAX_SIZE for 999,999,999,999,999
col USER_SPECIFIED_SIZE for 999,999,999,999,999
col COMPONENT for a30
col diff for 999,999,999,999,999
set pages 20000
set lin 20000
alter session set NLS_DATE_FORMAT='YYYY/MM/DD HH24:MI:SS';

select * from DBA_HIST_MEM_DYNAMIC_COMP
where LAST_OPER_MODE = 'IMMEDIATE' and
dbid=xxxxxxxxx
order by LAST_OPER_TIME desc;

select * from DBA_HIST_MEM_DYNAMIC_COMP
where LAST_OPER_MODE = 'DEFERRED' and
dbid=xxxxxxxxx
order by LAST_OPER_TIME;
```

### Get Execution Time by SQL_ID

```sql
select sql_id,sum(EXECUTIONS_DELTA),sum(ELAPSED_TIME_DELTA) ,round(sum(ELAPSED_TIME_DELTA)/sum(EXECUTIONS_DELTA)/100000,0) sec
from dba_hist_sqlstat natural join dba_hist_snapshot
where sql_id in
(
  '2znznu2dkbjq1'
, '39up7r1bnk3mn'
, '5wna3gkz7wx7v'
)
AND begin_interval_time between to_timestamp('20160201:00','YYYYMMDD:HH24')
AND to_date('20160213:00','YYYYMMDD:HH24')
group by sql_id;
```

### Output Execution Plan from AWR Snapshot

```sql
select plan_table_output from table(DBMS_XPLAN.DISPLAY_AWR('ff6uqt4322h9'));
```

### Create/Delete AWR Snapshots

```sql
exec dbms_workload_repository.create_snapshot();

exec DBMS_WORKLOAD_REPOSITORY.DROP_SNAPSHOT_RANGE (low_snap_id => 1,high_snap_id => 9999999);
```
