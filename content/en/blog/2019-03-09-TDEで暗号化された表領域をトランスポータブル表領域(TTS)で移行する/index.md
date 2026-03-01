---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Migrating TDE-Encrypted Tablespaces Using Transportable Tablespace (TTS)"
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



#### **Create Encrypted Tablespace**

```sql
CREATE TABLESPACE tdedata
    DATAFILE '/u01/app/oracle/oradata/db121s/tdedata.dbf' SIZE 1000M
    EXTENT MANAGEMENT LOCAL UNIFORM SIZE 1M
    SEGMENT SPACE MANAGEMENT AUTO
    ENCRYPTION USING 'AES256'
    DEFAULT STORAGE (ENCRYPT);
```

#### **Verify Tablespace Encryption**

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

#### **Create User for Data Migration**

```sql
create user iko identified by oracle DEFAULT TABLESPACE TDEDATA;
grant dba to iko;
```

#### **Create Test Table for Migration** and Insert Test Data

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

#### **Export Master Encryption Key**

```sql
sqlplus / as sysdba
select * from v$encryption_wallet;
select ACTIVATING_PDBNAME,tag,key_id,con_id,CREATION_TIME,ACTIVATION_TIME from v$encryption_keys;
administer key management export encryption keys with secret "my_secret" to '/home/oracle/export_TDE.exp' identified by oracle;
```

#### **Set Migration Tablespace to Read Only**

```sql
alter tablespace tdedata read only;
exit
```

#### **Run expdp with transport_tablespaces (Export Metadata)**

```sql
expdp system/oracle DUMPFILE=tdedata_tts.dmp DIRECTORY=homedir transport_tablespaces=tdedata
```

#### **Copy TDE Keystore and Data Files to Target Database**

```sql
cp /u01/app/oracle/oradata/db121s/tdedata.dbf /u01/app/oracle/oradata/db121t/
cp /keystore/db121s/ewallet.p12 /keystore/db121t
```

#### **Import Master Encryption Key (Target DB)**

```sql
sqlplus / as sysdba
select INST_ID, WRL_TYPE, WRL_PARAMETER, STATUS, WALLET_TYPE from GV$ENCRYPTION_WALLET order by 1;
select * from v$encryption_wallet;

administer key management import keys with secret "my_secret" from '/home/oracle/export_TDE.exp' identified  by oracle with backup;

select ACTIVATING_PDBNAME,tag,key_id,con_id,CREATION_TIME,ACTIVATION_TIME from v$encryption_keys;
select * from v$encryption_wallet;

```

#### **Create Master Encryption Key**

```sql
administer key management set key identified by "oracle" with backup;
select ACTIVATING_PDBNAME,tag,key_id,con_id,CREATION_TIME,ACTIVATION_TIME from v$encryption_keys;
```

#### **Create User for Data Migration (Target)**

```sql
create user iko identified by oracle;
grant dba to iko;
```

#### **Import Metadata on Target Side**

```sql
impdp system/oracle dumpfile=tdedata_tts.dmp directory=homedir transport_datafiles=/u01/app/oracle/oradata/db121t/tdedata.dbf
```

#### **Set Tablespace Back to Read Write**

```sql
conn / as sysdba
alter tablespace tdedata read write;
```

#### **Verify Test Data**

```sql
select count(*) from iko.t1;
```
