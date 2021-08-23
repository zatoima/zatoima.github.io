---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MERGE文のGoldenGateによる伝搬"
subtitle: " "
summary: " "
tags: ["Oracle", "GoldenGate"]
categories: ["Oracle", "GoldenGate"]
url: goldengate-merge-replication.html
date: 2019-03-10
lastmod: 2019-03-10
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false
---


### はじめに

MERGE文による更新をソース側DBで実施した場合、GoldenGateでどのように実行されるかを確認。

当初の推察通りだったが、REDOログ・ファイルから更新情報を読み込むアーキテクチャ上、MERGE文でINSERTが使用された場合は、INSERT文をキャプチャするし、UPDATE文だった場合は当然UPDATE文で伝搬される。

### テストデータ作成

```sql
drop table t1;
create table t1(a number primary key,b number,c varchar(30),d number);
insert into t1 values (1,dbms_flashback.get_system_change_number,'test',TO_NUMBER(TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS')));
commit;

drop table t2;
create table t2(a number primary key,b number,c varchar(30),d number);
insert into t2 values (1,dbms_flashback.get_system_change_number,'test',TO_NUMBER(TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS')));
insert into t2 values (2,dbms_flashback.get_system_change_number,'test',TO_NUMBER(TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS')));
insert into t2 values (3,dbms_flashback.get_system_change_number,'test',TO_NUMBER(TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS')));
insert into t2 values (4,dbms_flashback.get_system_change_number,'test',TO_NUMBER(TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS')));
commit;
```

### テストデータの確認

```
SQL> select * from t1;
A  B        C     D               
1  1202613  test  20190610133851  

SQL> select * from t2;
A  B        C     D               
1  1202715  test  20190610133852  
2  1202726  test  20190610133852  
3  1202726  test  20190610133852  
4  1202726  test  20190610133852  
```

### MERGE文の実行

```sql
MERGE INTO t1
  USING t2
  ON (t1.a = t2.a) 
  WHEN MATCHED THEN
    UPDATE SET
      t1.b = t2.b
  WHEN NOT MATCHED THEN
    INSERT (a, b, c, d)
    VALUES (t2.a,t2.b,t2.c,t2.d)
/
```

### MERGE後のテストデータ確認

```
SQL> select * from t1;
A  B        C     D               
1  1202715  test  20190610133851  
2  1202726  test  20190610133852  
3  1202726  test  20190610133852  
4  1202726  test  20190610133852  


SQL> select * from t2;
A  B        C     D               
1  1202715  test  20190610133852  
2  1202726  test  20190610133852  
3  1202726  test  20190610133852  
4  1202726  test  20190610133852  
```

### GoldenGateの伝搬結果

```
	      A 	      B C					     D
--------------- --------------- ------------------------------ ---------------
	      1 	1202715 test				20190610133851
	      2 	1202726 test				20190610133852
	      3 	1202726 test				20190610133852
	      4 	1202726 test				20190610133852

SQL> 
	      A 	      B C					     D
--------------- --------------- ------------------------------ ---------------
	      1 	1202715 test				20190610133852
	      2 	1202726 test				20190610133852
	      3 	1202726 test				20190610133852
	      4 	1202726 test				20190610133852

```

### ターゲット側の共有プール（v$sql)から実行されたSQLを確認

```sql
SELECT sql_id,
       plan_hash_value,
       sql_text,
       module,
       fetches,
       command_type,
       executions,
       first_load_time,
       last_active_time,
       action,
       service,
       is_bind_aware
FROM V$SQL
WHERE module='GoldenGate'
and   action like '%Apply Server';
```

### 実行結果

少し見にくいが、INSERT文とUPDATE文がGGTESTスキーマのT1テーブルに実行されていることがわかる。

```sql
SQL> SELECT sql_id,
  2         plan_hash_value,
  3         sql_text,
  4         module,
  5         fetches,
  6         command_type,
  7         executions,
  8         first_load_time,
  9         last_active_time,
 10         action,
 11         service,
 12         is_bind_aware
 13  FROM V$SQL
 14  WHERE module='GoldenGate'
 15  and   action like '%Apply Server';
"SQL_ID","PLAN_HASH_VALUE","SQL_TEXT","MODULE","FETCHES","COMMAND_TYPE","EXECUTIONS","FIRST_LOAD_TIME","LAST_ACTIVE_TIME","ACTION","SERVICE","IS_BIND_AWARE"
"6j3z4vh2pudfs",0," INSERT /*+ restrict_all_ref_cons */ INTO ""GGTEST"".""T1"" (""A"",""B"",""C"",""D"") VALUES (:1   ,:2   ,:3   ,:4   )","GoldenGate",0,2,2,"2019-06-10/12:25:03",19-06-10,"OGG$R11 - Apply Server","db18p1","N"
"g92sukn9vaduv",0,"INSERT INTO sys.streams$_apply_progress (apply#, source_db_name, xidusn, xidslt, xidsqn, commit_scn, commit_position, transaction_id) VALUES (1, 'NULL', :1, :2, :3, :4, :5, :6)","GoldenGate",0,2,119,"2019-06-10/12:23:53",19-06-10,"OGG$R11 - Apply Server","db18p1","N"
"9vyxjaht16r7v",0," INSERT /*+ restrict_all_ref_cons */ INTO ""GGTEST"".""T2"" (""A"",""B"",""C"",""D"") VALUES (:1   ,:2   ,:3   ,:4   )","GoldenGate",0,2,1,"2019-06-10/12:27:25",19-06-10,"OGG$R11 - Apply Server","db18p1","N"
"ghjk279rcm16p",3903122721,"UPDATE SYS.STREAMS$_APPLY_MILESTONE SET OLDEST_SCN=:1, COMMIT_SCN=:2,SYNCH_SCN=:3, SPARE1=:4, EPOCH=:5, PROCESSED_SCN=:6, APPLY_TIME=:7,APPLIED_MESSAGE_CREATE_TIME=:8, START_SCN=:9, OLDEST_TRANSACTION_ID=:10,LWM_EXTERNAL_POS=:11, OLDEST_POSITION=:12, PROCESSED_POSITION=:13,START_POSITION=:14, OLDEST_CREATE_TIME=:15, XOUT_PROCESSED_POSITION=:16,XOUT_PROCESSED_CREATE_TIME=:17, XOUT_PROCESSED_TID=:18,APPLIED_HIGH_POSITION=:19, XOUT_PROCESSED_TIME=:20, SPARE5=:21, PTO_RECOVERY_SCN=:22,PTO_RECOVERY_INCARNATION=DECODE(:23,PTO_RECOVERY_SCN,                                 PTO_RECOVERY_INCARNATION,                                (select incarnation# from                                  v$database_incarnation                                  where status = 'CURRENT'))  WHERE APPLY#=:24","GoldenGate",0,6,4,"2019-06-10/12:23:54",19-06-10,"OGG$R11 - Apply Server","db18p1","N"
"0913ps7wxvf0h",559339712," UPDATE /*+ restrict_all_ref_cons */ ""GGTEST"".""T1"" SET ""B""=:1    WHERE ""A""=:2   ","GoldenGate",0,6,1,"2019-06-10/12:55:15",19-06-10,"OGG$R11 - Apply Server","db18p1","N"
"0913ps7wxvf0h",1027040727," UPDATE /*+ restrict_all_ref_cons */ ""GGTEST"".""T1"" SET ""B""=:1    WHERE ""A""=:2   ","GoldenGate",0,6,1,"2019-06-10/12:55:15",19-06-10,"OGG$R11 - Apply Server","db18p1","N"

6行が選択されました。 

```