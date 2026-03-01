---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWR(DBA_HIST表)を使用した確認SQL"
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



### はじめに

AWR（Automatic Workload Repository）とはOracle Databaseの稼働統計とワークロード情報のスナップショットを自動的に収集・管理する機能です。

一般的にAWRを使用した分析はAWRレポートをhtml形式、text形式で出力してレポートからパフォーマンスや稼働統計を確認して分析、改善案を整理します。

AWRレポートを出力する際には各種ディクショナリ(DBA_HIST表)を参照することからそのディクショナリを直接見て色々な分析を行うことが出来ます。

AWR利用には「Diagnostic Pack」のライセンスが追加で必要になります。

### AWRに格納された過去のSQL監視結果をレポートする（Oracle 12c～）

```sql
SELECT report_id,
       GENERATION_TIME,
       key1
FROM dba_hist_reports
WHERE component_name='sqlmonitor'
  AND key1='5j5wp4d5s9pqz';
```

### AWRに格納されているSQLを確認する

```sql
select
    a.begin_interval_time,
    b.sql_id,
    c.sql_text
from DBA_HIST_SNAPSHOT a, DBA_HIST_SQLSTAT st, DBA_HIST_SQLTEXT c
where a.dbid=b.dbid and a.instance_number=b.instance_number and a.snap_id=b.snap_id
      and b.dbid=c.dbid and b.sql_id=c.sql_id
      and c.sql_text like '%<検索SQL>%';
```

### AWRに格納された過去のSQL監視結果をレポートする（Oracle 12c～）

```sql
SELECT report_id,
       GENERATION_TIME,
       key1
FROM dba_hist_reports
WHERE component_name='sqlmonitor'
  AND key1='5j5wp4d5s9pqz';
```

### AWR snapshotの確認

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

### dba_undo_statから長時間実行されているSQL等の確認（累積）

```sql
select MAXQUERYSQLID,sum(MAXQUERYLEN)
from dba_hist_undostat where dbid='xxxxxxxxx'
AND BEGIN_TIME >= TO_TIMESTAMP('2016/02/10 20:00:00', 'YYYY/MM/DD HH24:MI:SS')
AND END_TIME <=  TO_TIMESTAMP('2016/10/31 20:15:00', 'YYYY/MM/DD HH24:MI:SS')
group by MAXQUERYSQLID
order by 2;
```

### dba_undo_statから長時間実行されているSQL等の確認（個別）

```sql
select MAXQUERYSQLID,sum(MAXQUERYLEN)
from dba_hist_undostat where dbid='xxxxxxxxx'
AND BEGIN_TIME >= TO_TIMESTAMP('2016/02/10 20:00:00', 'YYYY/MM/DD HH24:MI:SS')
AND END_TIME <=  TO_TIMESTAMP('2016/10/31 20:15:00', 'YYYY/MM/DD HH24:MI:SS')
group by MAXQUERYSQLID
order by 2;
```

### AWRから共有プールの拡張履歴を確認する

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

### SQL_IDを指定し、実行時間を取得するSQL

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

### AWRスナップショットから実行計画を出力

```sql
select plan_table_output from table(DBMS_XPLAN.DISPLAY_AWR('ff6uqt4322h9'));
```

### AWRの取得・削除

```sql
exec dbms_workload_repository.create_snapshot();

exec DBMS_WORKLOAD_REPOSITORY.DROP_SNAPSHOT_RANGE (low_snap_id => 1,high_snap_id => 9999999);
```