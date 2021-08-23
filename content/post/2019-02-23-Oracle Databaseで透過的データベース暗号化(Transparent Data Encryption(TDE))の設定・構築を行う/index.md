---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Databaseで透過的データベース暗号化(Transparent Data Encryption(TDE))の設定・構築を行う"
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


今回は、Oracle Database 12cR1 において設定を行います。

透過的データベース暗号化(Transparent Data Encryption(TDE))は、データベース内の保存データを暗号化することによって、機密データを保護します。

データベースの物理ファイルを暗号化することにより、保存データを暗号化します。

データはストレージに書き込まれる前に自動的に暗号化され、ストレージから読み込まれる時に自動的に複合化されます。

マニュアルはこちら

> Oracle® Database Advanced Securityガイド 12cリリース1 (12.1) 
> https://docs.oracle.com/cd/E57425_01/121/ASOAG/toc.htm

概要説明はこちら

> Transparent Data Encryption https://www.oracle.com/technetwork/jp/database/security/index-099011-ja.html
>
> [Oracle Advanced Security](https://www.oracle.com/technetwork/jp/database/options/advanced-security/index.html)の透過的データベース暗号化（Transparent Data Encryption（TDE））は、保存されているデータをデータベース・レイヤーで暗号化することで、潜在的な攻撃者がデータベースをバイパスしてストレージから機密情報を読み取ることを阻止します。
>
> データベース認証が済んだアプリケーションおよびユーザーは、（アプリケーション・コードまたは構成変更なしで）透過的にアプリケーション・データへのアクセスを維持することができますが、表領域ファイルから機密データを読み取ろうとするOSユーザーによる攻撃や、盗み取ったディスクまたはバックアップから情報を読み取ろうとする窃盗犯の攻撃によるクリアテキスト・データへのアクセスは拒否されます。  
>
> 暗号化鍵アーキテクチャは2層に分かれているため、鍵の管理が容易で、鍵と暗号化データの明確な分離が可能です。また、アシスト付き鍵ローテーション機能があり、データを再暗号化する必要はありません。キーストアの管理には、Oracle Enterprise Managerの便利なWebコンソールまたはコマンドラインを使用できます。



#### **keystoreを格納するディレクトリ作成**

今回は同サーバ上にディレクトリを作成します。

```bash
su -
mkdir -p /keystore/dbvms
chown -R oracle:oinstall /keystore
chmod -R 755 /keystore
```

#### **sqlnet.oraに記載する**

ENCRYPTION_WALLET_LOCATIONを記載します。

```bash
vi $ORACLE_HOME/network/admin/sqlnet.ora

ENCRYPTION_WALLET_LOCATION=
  (SOURCE=
    (METHOD=FILE)
    (METHOD_DATA=
      (DIRECTORY=/keystore/$ORACLE_UNQNAME)))
```

#### **環境変数に ORACLE_UNQNAME を記載する。**

  ※ $ORACLE_UNQNAMEをENCRYPTION_WALLET_LOCATIONに使用しているため設定しています。

```bash
vi .oraenv_dbvms

export ORACLE_UNQNAME=dbvms
```

#### **TDEキーストアの作成**

```sql
. /home/oracle/.oraenv_dbvms
sqlplus / as sysdba
administer key management create keystore '/keystore/dbvms' identified by "oracle";

【コマンド結果】
SQL> administer key management create keystore '/keystore/dbvms' identified by "oracle";

キーストアが変更されました。

SQL>
```

#### **TDEキーストアのオープン**

```sql
administer key management set keystore open identified by "oracle";

【コマンド結果】
SQL> administer key management set keystore open identified by "oracle";

キーストアが変更されました。

```

#### **TDEキーストアのオープン確認**

```sql
set pages 2000 lin 2000
col WRL_TYPE      for a8
col WRL_PARAMETER for a30
col STATUS        for a30
col WALLET_TYPE   for a30

select INST_ID, WRL_TYPE, WRL_PARAMETER, STATUS, WALLET_TYPE from GV$ENCRYPTION_WALLET order by 1;

【コマンド結果】

   INST_ID WRL_TYPE WRL_PARAMETER                  STATUS                         WALLET_TYPE
---------- -------- ------------------------------ ------------------------------ ------------------------------
         1 FILE     /keystore/dbvms/             OPEN_NO_MASTER_KEY             PASSWORD

SQL>
```

#### **TDEマスター暗号化鍵の作成**

```sql
administer key management set key identified by "oracle" with backup using 'deploy';

【コマンド結果】
SQL> administer key management set key identified by "oracle" with backup using 'deploy';

キーストアが変更されました。

SQL>
```

#### **TDEマスター暗号化鍵の確認**

```sql
alter session set nls_timestamp_tz_format = 'yyyy/mm/dd hh24:mi:ss';
col CREATOR_DBNAME  for a15
col KEY_ID          for a60
col CREATION_TIME   for a20
col ACTIVATION_TIME for a20

select CREATOR_DBNAME, KEY_ID, CREATION_TIME, ACTIVATION_TIME from V$ENCRYPTION_KEYS order by 1,2;

【コマンド結果】
CREATOR_DBNAME  KEY_ID                                                       CREATION_TIME        ACTIVATION_TIME
--------------- ------------------------------------------------------------ -------------------- --------------------
dbvms         AccLZFJI/U95v/XKfMIdMWIAAAAAAAAAAAAAAAAAAAAAAAAAAAAA         2019/03/08 07:52:37  2019/03/08 07:52:37

SQL>
```

#### **自動ログイン・キーストア作成**

```sql
administer key management create auto_login keystore from keystore '/keystore/dbvms' identified by "oracle";
```

#### **DB再起動**

```sql
shutdown immediate
startup
exit
```

#### **自動ログインキーストアのオープン状態確認**

   列 STATUS が "OPEN"、列 WALLET_TYPE が "AUTOLOGIN" となっていること

```sql
sqlplus / as sysdba
set lines 200
col WRL_TYPE      for a8
col WRL_PARAMETER for a60
col STATUS        for a6
col WALLET_TYPE   for a15
select INST_ID, WRL_TYPE, WRL_PARAMETER, STATUS, WALLET_TYPE from GV$ENCRYPTION_WALLET order by 1;
exit

【コマンド結果】
   INST_ID WRL_TYPE WRL_PARAMETER                                                STATUS WALLET_TYPE
---------- -------- ------------------------------------------------------------ ------ ---------------
         1 FILE     /keystore/dbvms/                                           OPEN   AUTOLOGIN
```

#### **暗号化表領域の作成**

```sql
CREATE TABLESPACE dbdata
    DATAFILE '/u01/app/oracle/oradata/dbvms/dbdata.dbf' SIZE 3000M
    EXTENT MANAGEMENT LOCAL UNIFORM SIZE 1M
    SEGMENT SPACE MANAGEMENT AUTO
    ENCRYPTION USING 'AES256'
    DEFAULT STORAGE (ENCRYPT);
```

#### **表領域の確認**

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

【コマンド結果】
TABLESPACE_NAME INITIAL_EXTENT   MAX_SIZE STATUS EXTENT_MANAGEMENT ALLOCATION_TYPE SEGMENT_SPACE_MANAGEMENT  BIGFIL ENCRYPTED
--------------- -------------- ---------- ------ ----------------- --------------- ------------------------- ------ ---------
dbdata                1048576 2147483645 ONLINE LOCAL             UNIFORM         AUTO                      NO     YES
SYSAUX                   65536 2147483645 ONLINE LOCAL             SYSTEM          AUTO                      NO     NO
SYSTEM                   65536 2147483645 ONLINE LOCAL             SYSTEM          MANUAL                    NO     NO
TEMP                   1048576 2147483645 ONLINE LOCAL             UNIFORM         MANUAL                    NO     NO
UNDOTBS1                 65536 2147483645 ONLINE LOCAL             SYSTEM          MANUAL                    NO     NO
USERS                    65536 2147483645 ONLINE LOCAL             SYSTEM          AUTO                      NO     NO

```

#### **データ・ファイルの確認**

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

#### **物理的な暗号化表領域の確認**

テーブルを作成する

```sql
create table CHECK_ENCRYPT_TABLE(COL1 number, COL2 VARCHAR2(40)) tablespace dbdata;
insert into CHECK_ENCRYPT_TABLE values (1,'CHECK_ENCRYPT_VALUE');
commit;
```

#### **データファイルに反映されるように複数回ログスイッチを行う**

```sql
alter system switch logfile;
exit
```

#### **物理的な暗号化を確認する。CHECK_ENCRYPT_VALUEという文言がないかどうか確認する**

```m
strings '/u01/app/oracle/oradata/dbvms/dbdata.dbf' | grep CHECK_ENCRYPT_VALUE
```