---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS Oracleでロックされているテーブルのセッションをkill"
subtitle: ""
summary: " "
tags: ["Oracle","RDS"]
categories: ["Oracle","RDS"]
url: oracle-rds-for-oracle-kill-session.html
date: 2021-05-05
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



息をするように`alter system kill session`で殺していたセッションもRDSであれば専用のパッケージを使わないとダメで忘れがちなので備忘のためメモ。

```sql
SELECT
    X.SID
  , X.SERIAL#
  , TO_CHAR(
        X.SQL_EXEC_START
      , 'YYYY/MM/DD HH24:MI:SS'
    ) AS SQL_EXEC_START
  , Y.SQL_TEXT
FROM
    V$SESSION X
        INNER JOIN V$SQL Y
           ON Y.HASH_VALUE = X.SQL_HASH_VALUE
          AND Y.ADDRESS    = X.SQL_ADDRESS
WHERE
    X.STATUS = 'ACTIVE'
AND X.SID IN (
        SELECT
            Z.SID
        FROM
            V$LOCK Z
        WHERE
            Z.TYPE IN ('TM','TX')
    )
;
```

```sql
exec rdsadmin.rdsadmin_util.kill(SID,SERIAL#);
```

### 実行結果

```sql
SQL> SELECT
    X.SID
  , X.SERIAL#
  , TO_CHAR(
        X.SQL_EXEC_START
      , 'YYYY/MM/DD HH24:MI:SS'
    ) AS SQL_EXEC_START
  , Y.SQL_TEXT
FROM
    V$SESSION X
        INNER JOIN V$SQL Y
           ON Y.HASH_VALUE = X.SQL_HASH_VALUE
          AND Y.ADDRES  2    3    4    5    6    7    8    9   10   11   12   13  S    = X.SQL_ADDRESS
WHERE
    X.STATUS = 'ACTIVE'
AND X.SID IN (
        SELECT
            Z.SID
        FROM
            V$LOCK Z
        WHERE
            Z.TYPE IN ('TM','TX')
    )
; 14   15   16   17   18   19   20   21   22   23   24  

       SID    SERIAL# SQL_EXEC_START
---------- ---------- -------------------
SQL_TEXT
--------------------------------------------------------------------------------
      1292	50094 2021/04/23 06:41:41
insert into PARTTBL_MAIN_1 select * from PARTTBL_MAIN_1
```



```sql
SQL>  exec rdsadmin.rdsadmin_util.kill(1292,50094);

PL/SQL procedure successfully completed.
```

