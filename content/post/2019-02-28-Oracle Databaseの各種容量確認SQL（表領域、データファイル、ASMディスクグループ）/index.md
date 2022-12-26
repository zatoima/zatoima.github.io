---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Databaseの表領域使用率を確認するSQL"
subtitle: ""
summary: " "
tags: [Oracle, SQL]
categories: [Oracle, SQL]
url: oracle-tablespace-capacitycheck.html
date: 2019-02-28
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



**表領域使用率を確認するSQL**

```sql
set pages 2000 lin 2000
col name for a15
SELECT t.tablespace_name name
       , t.status
       , t.contents type
       , t.extent_management extmgt
       , t.allocation_type alloc
       , t.initial_extent/1024 init_kb
       , t.segment_space_management segmgt
       , TO_CHAR(NVL(d.bytes - NVL(f.bytes, 0), 0)/1024/1024,
'9,999,990.9') "USED(MB)"
       , TO_CHAR(NVL(d.bytes, 0)/1024/1024, '9,999,990.9') "TOTAL(MB)"
       , TO_CHAR(NVL(d.bytes - NVL(f.bytes, 0), 0)/(NVL(d.bytes, -1)/100),
'990.0') "USED(%)"
    FROM dba_tablespaces t
       , (SELECT tablespace_name, SUM(bytes) bytes FROM dba_data_files
GROUP BY tablespace_name) d
       , (SELECT tablespace_name, SUM(bytes) bytes FROM dba_free_space
GROUP BY tablespace_name) f
   WHERE t.tablespace_name = d.tablespace_name(+)
     AND t.tablespace_name = f.tablespace_name(+)
     AND NOT (t.extent_management = 'LOCAL' AND t.contents = 'TEMPORARY')
   UNION ALL
SELECT t.tablespace_name name
       , t.status
       , t.contents type
       , t.extent_management extmgt
       , t.allocation_type alloc
       , t.initial_extent/1024 init_kb
       , t.segment_space_management segmgt
       , TO_CHAR(NVL(f.bytes, 0)/1024/1024, '9,999,990.9') "USED(MB)"
       , TO_CHAR(NVL(d.bytes, 0)/1024/1024, '9,999,990.9') "TOTAL(MB)"
       , TO_CHAR(NVL(f.bytes/(d.bytes/100), 0), '990.0') "USED(%)"
    FROM dba_tablespaces t
       , (SELECT tablespace_name, SUM(bytes) bytes FROM dba_temp_files
GROUP BY tablespace_name) d
       , (SELECT tablespace_name, SUM(bytes_cached) bytes FROM
v$temp_extent_pool GROUP BY tablespace_name) f
   WHERE t.tablespace_name = d.tablespace_name(+)
     AND t.tablespace_name = f.tablespace_name(+)
     AND t.extent_management = 'LOCAL' AND t.contents = 'TEMPORARY'
   ORDER BY name
;
```

結果

```sql
NAME            STATUS    TYPE                  EXTMGT     ALLOC        INIT_KB SEGMGT USED(MB)     TOTAL(MB)    USED(%
--------------- --------- --------------------- ---------- --------- ---------- ------ ------------ ------------ ------
GG_DATA         ONLINE    PERMANENT             LOCAL      SYSTEM            64 AUTO            1.0      5,120.0    0.0
SYSAUX          ONLINE    PERMANENT             LOCAL      SYSTEM            64 AUTO        2,400.6      2,530.0   94.9
SYSTEM          ONLINE    PERMANENT             LOCAL      SYSTEM            64 MANUAL        897.4        900.0   99.7
TEMP            ONLINE    TEMPORARY             LOCAL      UNIFORM         1024 MANUAL        597.0        200.0  298.5
UNDOTBS1        ONLINE    UNDO                  LOCAL      SYSTEM            64 MANUAL         12.3        320.0    3.8
USERS           ONLINE    PERMANENT             LOCAL      SYSTEM            64 AUTO            1.0          5.0   20.0

6行が選択されました。

SQL>

```