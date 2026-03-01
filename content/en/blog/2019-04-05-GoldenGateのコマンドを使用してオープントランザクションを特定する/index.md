---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Identifying Open Transactions Using GoldenGate Commands"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-opentransaction-getinfo.html
date: 2019-04-05
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



#### Using the showtrans option to output open transaction information

Obtain the XID.

```sql
GGSCI (dbvgg.jp.oracle.com) 2> send c11,showtrans

Sending SHOWTRANS request to EXTRACT C11 ...

------------------------------------------------------------
XID:                  5.15.930
Items:                1
Extract:              C11
Redo Thread:          1
Start Time:           2019-03-29:22:00:35
SCN:                  0.1124828 (1124828)
Redo Seq:             10
Redo RBA:             122960912
Status:               Running


```



#### How to View Running Transactions

The SES_ADDR can be obtained.

```sql
SQL> select SES_ADDR,XIDUSN, XIDSLOT, XIDSQN, START_SCN from v$transaction;
SES_ADDR          XIDUSN  XIDSLOT  XIDSQN  START_SCN
000000010868F4E0  5       15       930     1124828
SQL>

```



#### How to Find the Session Running a Specific Transaction

Specify SES_ADDR in the saddr column of v$session.

```sql
SQL> select sid,serial#,username,logon_time,status
  2  from v$session
  3  where saddr='000000010868F4E0';
SID  SERIAL#  USERNAME  LOGON_TIME  STATUS
18   1117     GGTEST    19-03-29    INACTIVE

```



#### How to Check SQL_ID and SQL_TEXT

Check SQL_TEXT based on sid and serial#.

```sql
SQL> SELECT
  2    s.sid,
  3    s.serial#,
  4    s.status,
  5    s.machine,
  6    s.osuser,
  7    s.module,
  8    s.username,
  9    s.process,
 10    p.program,
 11    a.sql_text
 12  FROM v$session s,
 13       v$sqlarea a,
 14       v$process p
 15  WHERE s.PREV_HASH_VALUE = a.hash_value
 16    AND s.PREV_SQL_ADDR = a.address
 17    AND s.paddr = p.addr
 18    AND s.SID = 18;
SID  SERIAL#  STATUS    MACHINE              OSUSER  MODULE    USERNAME  PROCESS  PROGRAM                              SQL_TEXT
18   1117     INACTIVE  dbvgg.jp.oracle.com  oracle  SQL*Plus  GGTEST    11342    oracle@dbvgg.jp.oracle.com (TNS V1-V3)  insert into t1 values (TO_NUMBER(TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISSFF4')),dbms_flashback.get_system_change_number,'test',sysdate)


```



Here is the manual reference. The SEND EXTRACT command has many useful options, so please review them.

> https://docs.oracle.com/cd/E51849_01/gg-winux/GWURF/ggsci_commands014.htm
>
> SEND EXTRACT
>
> SHOWTRANS
>
> Displays information about open transactions. `SHOWTRANS` displays one of the following depending on the database type:
>
> - Process checkpoint (indicates the oldest log from which transaction processing needs to continue if Extract restarts). For details on checkpoints, see *Administering Oracle GoldenGate for Windows and UNIX*.
> - Transaction ID
> - Extract group name
> - REDO thread number
> - Timestamp of the first operation extracted from the transaction by Oracle GoldenGate (not the actual start time of the transaction)
> - System Change Number (SCN)
> - REDO log number and RBA
> - Status (`Pending COMMIT` or `Running`). `Pending COMMIT` appears while writing a transaction after issuing `FORCETRANS`.
>
> Without options, `SHOWTRANS` displays all open transactions that fit in the available buffer. For sample output of [SHOWTRANS](https://docs.oracle.com/cd/E51849_01/gg-winux/GWURF/ggsci_commands014.htm#CHDBIDFA), see `Example 1-0`. For further control of output, see the following options.
