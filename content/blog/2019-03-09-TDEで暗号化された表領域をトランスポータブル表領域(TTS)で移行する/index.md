---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "TDEで暗号化された表領域をトランスポータブル表領域(TTS)で移行する"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-migration-tde-tts.html
date: 2019-03-09
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



#### **暗号化表領域の作成**

```sql
CREATE TABLESPACE tdedata
    DATAFILE '/u01/app/oracle/oradata/db121s/tdedata.dbf' SIZE 1000M
    EXTENT MANAGEMENT LOCAL UNIFORM SIZE 1M
    SEGMENT SPACE MANAGEMENT AUTO
    ENCRYPTION USING 'AES256'
    DEFAULT STORAGE (ENCRYPT);
```

#### **表領域の暗号化確認**

```sql
set pages 2000 lin 2000
col TABLESPACE_NAME           for a15
col EXTENT_MANAGEMENT         for a17
col ALLOCATION_TYPE           for a15
col SEGMENT_SPACE_MANAGEMENT  for a25
col BIGFILE                   for a6
col ENCRYPTED                 for a9
SELECT
  TABLESPACE_NAME
  ,INITIAL_EXTENT
  ,MAX_SIZE
  ,STATUS
  ,EXTENT_MANAGEMENT
  ,ALLOCATION_TYPE
  ,SEGMENT_SPACE_MANAGEMENT
  ,BIGFILE
  ,ENCRYPTED
FROM DBA_TABLESPACES
where TABLESPACE_NAME='TDEDATA'
ORDER BY 1;
```

#### **データ移行用のユーザを作成する**

```sql
create user iko identified by oracle DEFAULT TABLESPACE TDEDATA;
grant dba to iko;
```

#### **移行用のテストテーブルを作成**&テストデータを挿入

```sql
conn iko/oracle
create table t1(a number primary key,b number ,c varchar2(30));

declare
   v_c1   number;
   v_c2   number;
   v_c3   varchar2(30);
begin
   dbms_random.seed(uid);
   for i in 1..1000
   loop
           v_c1 := i;
           v_c2 := i;
           v_c3 := dbms_random.string('x', 16);
           insert into t1 (a, b, c) values (v_c1, v_c2, v_c3);
           if (mod(i, 100) = 0) then
                   commit;
           end if;
   end loop;
   commit;
end;
/

select count(*) from iko.t1;
exit
```

#### **マスター暗号化鍵のエクスポート**

```sql
sqlplus / as sysdba
select * from v$encryption_wallet;
select ACTIVATING_PDBNAME,tag,key_id,con_id,CREATION_TIME,ACTIVATION_TIME from v$encryption_keys;
administer key management export encryption keys with secret "my_secret" to '/home/oracle/export_TDE.exp' identified by oracle;
```

#### 移行する表領域をread onlyに変更する

```sql
alter tablespace tdedata read only;
exit
```

#### **transport_tablespaces付きでexpdpする（メタデータをエクスポート）**

```sql
expdp system/oracle DUMPFILE=tdedata_tts.dmp DIRECTORY=homedir transport_tablespaces=tdedata
```

#### **TDE用のキーストアとデータファイルをターゲット側のデータベースにコピーする**

```sql
cp /u01/app/oracle/oradata/db121s/tdedata.dbf /u01/app/oracle/oradata/db121t/
cp /keystore/db121s/ewallet.p12 /keystore/db121t
```

#### **マスター暗号化鍵のインポート（ターゲットDB）**

```sql
sqlplus / as sysdba
select INST_ID, WRL_TYPE, WRL_PARAMETER, STATUS, WALLET_TYPE from GV$ENCRYPTION_WALLET order by 1;
select * from v$encryption_wallet;

administer key management import keys with secret "my_secret" from '/home/oracle/export_TDE.exp' identified  by oracle with backup;

select ACTIVATING_PDBNAME,tag,key_id,con_id,CREATION_TIME,ACTIVATION_TIME from v$encryption_keys;
select * from v$encryption_wallet;

```

#### **マスター暗号化鍵を作成**

```sql
administer key management set key identified by "oracle" with backup;
select ACTIVATING_PDBNAME,tag,key_id,con_id,CREATION_TIME,ACTIVATION_TIME from v$encryption_keys;
```

#### **データ移行用のユーザを作成する**

```sql
create user iko identified by oracle;
grant dba to iko;
```

#### **ターゲット側で、メタデータをインポート**

```sql
impdp system/oracle dumpfile=tdedata_tts.dmp directory=homedir transport_datafiles=/u01/app/oracle/oradata/db121t/tdedata.dbf
```

#### **transport_tablespaces付きでexpdpする（メタデータをエクスポート）**

```sql
conn / as sysdba
alter tablespace tdedata read write;
```

#### **テストデータの確認**

```sql
select count(*) from iko.t1;
```