---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Configuring Transparent Data Encryption (TDE) in Oracle Database"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-tde-implement.html
date: 2019-02-23
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


This article covers the setup process for Oracle Database 12cR1.

Transparent Data Encryption (TDE) protects sensitive data by encrypting data at rest within the database.

Data is encrypted by encrypting the physical files of the database.

Data is automatically encrypted before being written to storage and automatically decrypted when read from storage.

Manual reference:

> Oracle® Database Advanced Security Guide 12c Release 1 (12.1)
> https://docs.oracle.com/cd/E57425_01/121/ASOAG/toc.htm

Overview reference:

> Transparent Data Encryption https://www.oracle.com/technetwork/jp/database/security/index-099011-ja.html
>
> [Oracle Advanced Security](https://www.oracle.com/technetwork/jp/database/options/advanced-security/index.html)'s Transparent Data Encryption (TDE) encrypts data stored at the database layer, preventing potential attackers from bypassing the database and reading sensitive information from storage.
>
> Applications and users that have been authenticated to the database can continue to transparently access application data (without application code or configuration changes), while access to cleartext data by OS users trying to read sensitive data from tablespace files, or by thieves attempting to read information from stolen disks or backups, is denied.
>
> The encryption key architecture is divided into two layers, making key management easy and enabling a clear separation of keys and encrypted data. There is also an assisted key rotation function that does not require data re-encryption. The Oracle Enterprise Manager convenient web console or command line can be used for keystore management.



#### **Create Directory for Storing the Keystore**

In this example, we create the directory on the same server.

```bash
su -
mkdir -p /keystore/dbvms
chown -R oracle:oinstall /keystore
chmod -R 755 /keystore
```

#### **Update sqlnet.ora**

Add the ENCRYPTION_WALLET_LOCATION parameter.

```bash
vi $ORACLE_HOME/network/admin/sqlnet.ora

ENCRYPTION_WALLET_LOCATION=
  (SOURCE=
    (METHOD=FILE)
    (METHOD_DATA=
      (DIRECTORY=/keystore/$ORACLE_UNQNAME)))
```

#### **Add ORACLE_UNQNAME to Environment Variables**

  * Since $ORACLE_UNQNAME is used in ENCRYPTION_WALLET_LOCATION, it needs to be set.

```bash
vi .oraenv_dbvms

export ORACLE_UNQNAME=dbvms
```

#### **Create TDE Keystore**

```sql
. /home/oracle/.oraenv_dbvms
sqlplus / as sysdba
administer key management create keystore '/keystore/dbvms' identified by "oracle";

[Command result]
SQL> administer key management create keystore '/keystore/dbvms' identified by "oracle";

Keystore altered.

SQL>
```

#### **Open TDE Keystore**

```sql
administer key management set keystore open identified by "oracle";

[Command result]
SQL> administer key management set keystore open identified by "oracle";

Keystore altered.

```

#### **Verify TDE Keystore is Open**

```sql
set pages 2000 lin 2000
col WRL_TYPE      for a8
col WRL_PARAMETER for a30
col STATUS        for a30
col WALLET_TYPE   for a30

select INST_ID, WRL_TYPE, WRL_PARAMETER, STATUS, WALLET_TYPE from GV$ENCRYPTION_WALLET order by 1;

[Command result]

   INST_ID WRL_TYPE WRL_PARAMETER                  STATUS                         WALLET_TYPE
---------- -------- ------------------------------ ------------------------------ ------------------------------
         1 FILE     /keystore/dbvms/             OPEN_NO_MASTER_KEY             PASSWORD

SQL>
```

#### **Create TDE Master Encryption Key**

```sql
administer key management set key identified by "oracle" with backup using 'deploy';

[Command result]
SQL> administer key management set key identified by "oracle" with backup using 'deploy';

Keystore altered.

SQL>
```

#### **Verify TDE Master Encryption Key**

```sql
alter session set nls_timestamp_tz_format = 'yyyy/mm/dd hh24:mi:ss';
col CREATOR_DBNAME  for a15
col KEY_ID          for a60
col CREATION_TIME   for a20
col ACTIVATION_TIME for a20

select CREATOR_DBNAME, KEY_ID, CREATION_TIME, ACTIVATION_TIME from V$ENCRYPTION_KEYS order by 1,2;

[Command result]
CREATOR_DBNAME  KEY_ID                                                       CREATION_TIME        ACTIVATION_TIME
--------------- ------------------------------------------------------------ -------------------- --------------------
dbvms         AccLZFJI/U95v/XKfMIdMWIAAAAAAAAAAAAAAAAAAAAAAAAAAAAA         2019/03/08 07:52:37  2019/03/08 07:52:37

SQL>
```

#### **Create Auto-Login Keystore**

```sql
administer key management create auto_login keystore from keystore '/keystore/dbvms' identified by "oracle";
```

#### **Restart DB**

```sql
shutdown immediate
startup
exit
```

#### **Verify Auto-Login Keystore Open State**

   The STATUS column should be "OPEN" and the WALLET_TYPE column should be "AUTOLOGIN".

```sql
sqlplus / as sysdba
set lines 200
col WRL_TYPE      for a8
col WRL_PARAMETER for a60
col STATUS        for a6
col WALLET_TYPE   for a15
select INST_ID, WRL_TYPE, WRL_PARAMETER, STATUS, WALLET_TYPE from GV$ENCRYPTION_WALLET order by 1;
exit

[Command result]
   INST_ID WRL_TYPE WRL_PARAMETER                                                STATUS WALLET_TYPE
---------- -------- ------------------------------------------------------------ ------ ---------------
         1 FILE     /keystore/dbvms/                                           OPEN   AUTOLOGIN
```

#### **Create Encrypted Tablespace**

```sql
CREATE TABLESPACE dbdata
    DATAFILE '/u01/app/oracle/oradata/dbvms/dbdata.dbf' SIZE 3000M
    EXTENT MANAGEMENT LOCAL UNIFORM SIZE 1M
    SEGMENT SPACE MANAGEMENT AUTO
    ENCRYPTION USING 'AES256'
    DEFAULT STORAGE (ENCRYPT);
```

#### **Verify Tablespace**

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
ORDER BY 1;

[Command result]
TABLESPACE_NAME INITIAL_EXTENT   MAX_SIZE STATUS EXTENT_MANAGEMENT ALLOCATION_TYPE SEGMENT_SPACE_MANAGEMENT  BIGFIL ENCRYPTED
--------------- -------------- ---------- ------ ----------------- --------------- ------------------------- ------ ---------
dbdata                1048576 2147483645 ONLINE LOCAL             UNIFORM         AUTO                      NO     YES
SYSAUX                   65536 2147483645 ONLINE LOCAL             SYSTEM          AUTO                      NO     NO
SYSTEM                   65536 2147483645 ONLINE LOCAL             SYSTEM          MANUAL                    NO     NO
TEMP                   1048576 2147483645 ONLINE LOCAL             UNIFORM         MANUAL                    NO     NO
UNDOTBS1                 65536 2147483645 ONLINE LOCAL             SYSTEM          MANUAL                    NO     NO
USERS                    65536 2147483645 ONLINE LOCAL             SYSTEM          AUTO                      NO     NO

```

#### **Verify Data Files**

```sql
col TABLESPACE_NAME   for a15
col FILE_NAME         for a70
col AUTOEXTENSIBLE    for a15
col ONLINE_STATUS     for a15
SELECT
  TABLESPACE_NAME
  ,FILE_NAME
  ,BYTES/1024/1024 MB
  ,AUTOEXTENSIBLE
  ,STATUS
  ,ONLINE_STATUS
FROM DBA_DATA_FILES
ORDER BY 1;
```

#### **Physically Verify Encrypted Tablespace**

Create a table:

```sql
create table CHECK_ENCRYPT_TABLE(COL1 number, COL2 VARCHAR2(40)) tablespace dbdata;
insert into CHECK_ENCRYPT_TABLE values (1,'CHECK_ENCRYPT_VALUE');
commit;
```

#### **Perform Multiple Log Switches to Flush to Data File**

```sql
alter system switch logfile;
exit
```

#### **Physically Verify Encryption - Check That "CHECK_ENCRYPT_VALUE" Is Not Present**

```m
strings '/u01/app/oracle/oradata/dbvms/dbdata.dbf' | grep CHECK_ENCRYPT_VALUE
```
