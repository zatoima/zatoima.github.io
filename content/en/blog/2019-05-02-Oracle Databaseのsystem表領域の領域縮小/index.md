---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Shrinking the Oracle Database SYSTEM Tablespace"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-system-tablespace-shrink.html
date: 2019-05-02
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



#### **Introduction**

Verifying whether shrink operations or datafile drops are possible after expanding not user tablespaces, but the SYSTEM and SYSAUX tablespaces. Since the SYSTEM tablespace has many restrictions and is essential for DB operation, I investigated how it behaves.

#### **Checking Datafiles and Capacity**

```sql
SELECT
    tablespace_name,
    file_name,
    status,
    bytes/1024/1024 mbytes,
    increment_by,
    autoextensible,
    online_status
FROM
    dba_data_files
WHERE
    tablespace_name = 'SYSTEM';
```

#### **SQL Execution Result**

```sql
SQL> SELECT
  2      tablespace_name,
  3      file_name,
  4      status,
  5      bytes/1024/1024 mbytes,
  6      increment_by,
  7      autoextensible,
  8      online_status
  9  FROM
 10      dba_data_files
 11  WHERE
 12      tablespace_name = 'SYSTEM';
TABLESPACE_NAME  FILE_NAME                                                           STATUS     MBYTES  INCREMENT_BY  AUTOEXTENSIBLE  ONLINE_STATUS
SYSTEM           /u01/app/oracle/oradata/DB112S/datafile/o1_mf_system_g97nco87_.dbf  AVAILABLE  770     1280          YES             SYSTEM
```

#### **Checking Tablespace Capacity**

```sql
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

#### **SQL Execution Result**

```sql
NAME      STATUS  TYPE       EXTMGT  ALLOC    INIT_KB  SEGMGT  USED(MB)      TOTAL(MB)     USED(%)
GGDATA    ONLINE  PERMANENT  LOCAL   SYSTEM   64       AUTO             2.8       5,120.0     0.1
SYSAUX    ONLINE  PERMANENT  LOCAL   SYSTEM   64       AUTO           534.1         570.0    93.7
SYSTEM    ONLINE  PERMANENT  LOCAL   SYSTEM   64       MANUAL         752.4         770.0    97.7
TEMP      ONLINE  TEMPORARY  LOCAL   UNIFORM  1024     MANUAL          28.0          29.0    96.6
UNDOTBS1  ONLINE  UNDO       LOCAL   SYSTEM   64       MANUAL          32.6          70.0    46.5
USERS     ONLINE  PERMANENT  LOCAL   SYSTEM   64       AUTO             1.3           5.0    26.3
```

#### **Expanding the Tablespace (Adding a Datafile)**

```sql
alter tablespace SYSTEM add datafile '/u01/app/oracle/oradata/DB112S/datafile/system01.dbf' size 1G autoextend on next 100M;
```

#### **Tablespace Shrink Operations**

#### **Tablespace Shrink (Dropping a Datafile)**

An error occurs when trying to drop the newly added datafile above.

```sql
ALTER TABLESPACE SYSTEM DROP DATAFILE '/u01/app/oracle/oradata/DB112S/datafile/system01.dbf';
```

#### **SQL Execution Result**

```sql
SQL> ALTER TABLESPACE SYSTEM DROP DATAFILE '/u01/app/oracle/oradata/DB112S/datafile/system01.dbf';

Error starting at line : 1 -
ALTER TABLESPACE SYSTEM DROP DATAFILE '/u01/app/oracle/oradata/DB112S/datafile/system01.dbf'
Error report -
ORA-01541: SYSTEM tablespace cannot be brought offline; shut down if necessary
01541. 00000 -  "system tablespace cannot be brought offline; shut down if necessary"
*Cause:    Tried to bring system tablespace offline
*Action:   Shutdown if necessary to do recovery
SQL>
```

#### **Tablespace Shrink (Resize)**

Resizing the existing datafile.

```sql
ALTER DATABASE DATAFILE '/u01/app/oracle/oradata/DB112S/datafile/o1_mf_system_g97nco87_.dbf' RESIZE 800M;
```

#### **SQL Execution Result**

```sql
SQL> ALTER DATABASE DATAFILE '/u01/app/oracle/oradata/DB112S/datafile/o1_mf_system_g97nco87_.dbf' RESIZE 800M;

Database altered.
```

**Tablespace Shrink (Resize)**

An error occurs because the datafile composing the SYSTEM tablespace is a smallfile tablespace.

```sql
alter tablespace SYSTEM resize 800M ;
```

#### **SQL Execution Result**

```sql
SQL> alter tablespace SYSTEM resize 800M ;

Error starting at line : 1 -
alter tablespace SYSTEM resize 800M
Error report -
ORA-32773: operation not supported for smallfile tablespace SYSTEM
32773. 00000 -  "operation not supported for smallfile tablespace %s"
*Cause:    An attempt was made to perform an operation which is supported
           only for bigfile tablespaces, e.g. resize tablespace.
*Action:   Use the appropriate clause of the ALTER DATABASE DATAFILE
           command instead.
SQL>
```
