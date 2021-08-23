---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGateのコマンドを使用してオープントランザクションを特定する"
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



#### showtransオプションを使用するとオープントランザクションの情報が出力される

XIDを把握します。

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



#### 稼動しているトランザクションを見る方法

SES_ADDRが判明します。

```sql
SQL> select SES_ADDR,XIDUSN, XIDSLOT, XIDSQN, START_SCN from v$transaction;
SES_ADDR          XIDUSN  XIDSLOT  XIDSQN  START_SCN
000000010868F4E0  5       15       930     1124828
SQL>

```



#### 特定のトランザクションが動いているセッションを知る方法

SES_ADDRをv$sessionのsaddrに指定します。

```sql
SQL> select sid,serial#,username,logon_time,status
  2  from v$session
  3  where saddr='000000010868F4E0';
SID  SERIAL#  USERNAME  LOGON_TIME  STATUS
18   1117     GGTEST    19-03-29    INACTIVE

```



#### SQL_ID、SQL_TEXTを確認する方法

sid,serial#を基にSQL_TEXTを確認します。

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



マニュアルはこちらです。send extractには便利なオプションがたくさんありますのでご確認ください。

> https://docs.oracle.com/cd/E51849_01/gg-winux/GWURF/ggsci_commands014.htm
>
> SEND EXTRACT
>
> SHOWTRANS 
>
> オープンしているトランザクションに関する情報を表示します。`SHOWTRANS`は、データベース・タイプに応じて次のいずれかを表示します。
>
> - プロセス・チェックポイント(Extractが再起動する場合に、トランザクション処理を継続する必要がある最も古いログを示します)。チェックポイントの詳細は、*Oracle GoldenGateの管理for Windows and UNIX*を参照してください。
> - トランザクションID
> - Extractグループ名
> - REDOスレッド番号
> - (トランザクションの実際の開始時刻でなく)Oracle GoldenGateがトランザクションから抽出した最初の操作のタイムスタンプ
> - システム変更番号(SCN)
> - REDOログ番号とRBA
> - ステータス(`Pending COMMIT`または`Running`)。`Pending COMMIT`は、`FORCETRANS`発行後のトランザクション書込み中に表示されます。
>
> オプションを指定しない場合`SHOWTRANS`では、使用可能なバッファに収まるオープンしているすべてのトランザクションが表示されます。[SHOWTRANS](https://docs.oracle.com/cd/E51849_01/gg-winux/GWURF/ggsci_commands014.htm#CHDBIDFA)のサンプル出力は、`例1-0`を参照してください。出力をさらに制御するには、次のオプションを参照してください。