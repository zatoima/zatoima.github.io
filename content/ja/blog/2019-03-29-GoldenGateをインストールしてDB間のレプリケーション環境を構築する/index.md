---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGateをインストールしてDB間のレプリケーション環境を構築する"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-12c-18c-install-implement.html
date: 2019-03-29
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



GoldenGateを使用してOracle Database間のレプリケーションを構築します。

レプリケーションまでのステップは下記の通りですが、本記事だと「1.」と「2.」を対象にしています。

1. GoldenGateインストール

2. GoldenGate環境設定

3. データ伝搬
   

#### **環境構成**

マシンスペックの関係で同一マシン内に2DBを作成しています。この2DBをGoldenGateを使用してレプリケーション環境を作成します。

|                          | ソース                               | ターゲット                            |
| ------------------------ | ------------------------------------ | ------------------------------------- |
| DBバージョン             | 11.2.0.4                             | 18c                                   |
| GoldenGateバージョン     | 12.2.0.1                             | 18.1.0.0.0                            |
| DB名                     | db112s                               | db18s                                 |
| PDB名                    | -                                    | db18p1                                |
| GoldenGate用DBユーザ     | ggs                                  | c##ggs                                |
| 伝搬用ユーザ             | ggtest                               | ggtest                                |
| GoldenGateインストール先 | /gg/gg1                              | /gg/gg2                               |
| Captureプロセス          | c11                                  | -                                     |
| Data Pumpプロセス        | d11                                  | -                                     |
| Replicatプロセス         | -                                    | r11                                   |
| Captureプロセスのモード  | 統合モード<br />(Integrated Capture) | -                                     |
| Replicatプロセスのモード | -                                    | 統合モード<br />(Integrated Replicat) |
| その他                   | シングル構成                         |                                       |



#### **前提事項**

1. 既にソースDBとターゲットDBがインストールされていること
2. GoldenGateのメディアファイルを事前にダウンロードしていること



#### **GoldenGateインストール**

#### **GG_HOMEの作成**

今回はCUIベースでのインストールを行います。GUIでインストールしたい場合は下記qiitaの記事をご参照ください。

> GoldenGate布教活動②　～GoldenGateのインストール～ - Qiita https://qiita.com/ch0c0bana0/items/a57debf29a8d907e9feb

```sh
su -
mkdir -p /gg/gg1
mkdir -p /gg/gg2
chmod -R 755 /gg
chown -R oracle:oinstall /gg
exit
```



#### **GoldenGate12cR2(12.2.0.1)のインストール**

#### **メディア・ファイルの解凍**

```sh
#コマンド
cd /home/oracle/software/goldengate/12.2.0.1/V100692-01
ls -l
unzip V100692-01.zip
```

```sh
#実行結果
[oracle@dbvgg V100692-01]$
[oracle@dbvgg V100692-01]$ cd /home/oracle/software/goldengate/12.2.0.1/V100692-01
[oracle@dbvgg V100692-01]$ ls -l
合計 464468
-rwxr-xr-x 1 oracle oinstall 475611228  7月  7 19:15 2017 V100692-01.zip
[oracle@dbvgg V100692-01]$ unzip V100692-01.zip
Archive:  V100692-01.zip
   creating: fbo_ggs_Linux_x64_shiphome/
   creating: fbo_ggs_Linux_x64_shiphome/Disk1/
～中略～
   creating: fbo_ggs_Linux_x64_shiphome/Disk1/response/
  inflating: fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
  inflating: OGG-12.2.0.1-README.txt
  inflating: OGG-12.2.0.1.1-ReleaseNotes.pdf
[oracle@dbvgg V100692-01]$
```



#### **サイレントインストール用のレスポンスファイルの修正**

★部分が修正箇所になります。環境に合わせて修正する必要があります。

```sh
cd ./fbo_ggs_Linux_x64_shiphome/Disk1/response
ls -l
vi oggcore.rsp
```

```sh
#oggcore.rspの修正内容
####################################################################
## Copyright(c) Oracle Corporation 2014. All rights reserved.     ##
##                                                                ##
## Specify values for the variables listed below to customize     ##
## your installation.                                             ##
##                                                                ##
## Each variable is associated with a comment. The comment        ##
## can help to populate the variables with the appropriate        ##
## values.                                                        ##
##                                                                ##
## IMPORTANT NOTE: This file should be secured to have read       ##
## permission only by the oracle user or an administrator who     ##
## own this installation to protect any sensitive input values.   ##
##                                                                ##
####################################################################

#-------------------------------------------------------------------------------
# Do not change the following system generated value.
#-------------------------------------------------------------------------------
oracle.install.responseFileVersion=/oracle/install/rspfmt_ogginstall_response_schema_v12_1_2


################################################################################
##                                                                            ##
## Oracle GoldenGate installation option and details                          ##
##                                                                            ##
################################################################################

#-------------------------------------------------------------------------------
# Specify the installation option.
# Specify ORA12c for installing Oracle GoldenGate for Oracle Database 12c and
#         ORA11g for installing Oracle GoldenGate for Oracle Database 11g
#-------------------------------------------------------------------------------
INSTALL_OPTION=ORA11g ★←

#-------------------------------------------------------------------------------
# Specify a location to install Oracle GoldenGate
#-------------------------------------------------------------------------------
SOFTWARE_LOCATION=/gg/gg1 ★←

#-------------------------------------------------------------------------------
# Specify true to start the manager after installation.
#-------------------------------------------------------------------------------
START_MANAGER=false ★←

#-------------------------------------------------------------------------------
# Specify a free port within the valid range for the manager process.
# Required only if START_MANAGER is true.
#-------------------------------------------------------------------------------
MANAGER_PORT=

#-------------------------------------------------------------------------------
# Specify the location of the Oracle Database.
# Required only if START_MANAGER is true.
#-------------------------------------------------------------------------------
DATABASE_LOCATION=


################################################################################
##                                                                            ##
## Specify details to Create inventory for Oracle installs                    ##
## Required only for the first Oracle product install on a system.            ##
##                                                                            ##
################################################################################

#-------------------------------------------------------------------------------
# Specify the location which holds the install inventory files.
# This is an optional parameter if installing on
# Windows based Operating System.
#-------------------------------------------------------------------------------
INVENTORY_LOCATION=

#-------------------------------------------------------------------------------
# Unix group to be set for the inventory directory.
# This parameter is not applicable if installing on
# Windows based Operating System.
#-------------------------------------------------------------------------------
UNIX_GROUP_NAME=

```



#### **GoldenGateインストール**

```sh
cd /home/oracle/software/goldengate/12.2.0.1/V100692-01/fbo_ggs_Linux_x64_shiphome/Disk1
./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/12.2.0.1/V100692-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
```

```sh
#実行結果
[oracle@dbvgg Disk1]$ ./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/12.2.0.1/V100692-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
Oracle Universal Installerを起動中です...

一時領域の確認中: 120MBを超えている必要があります.   実際 28028MB    問題なし
スワップ領域の確認中: 150MBを超えている必要があります.   実際 7855MB    問題なし
Oracle Universal Installerの起動を準備中 /tmp/OraInstall2019-03-29_05-24-01PM. お待ちください...
このインストール・セッションのログは次の場所にあります:
 /u01/app/oraInventory/logs/installActions2019-03-29_05-24-01PM.log
Oracle GoldenGate Coreのインストールが成功しました。
詳細は'/u01/app/oraInventory/logs/silentInstall2019-03-29_05-24-01PM.log'を確認してください。
Successfully Setup Software.

[oracle@dbvgg Disk1]$
```



#### **OPatch更新**

```sh
#OPatch更新
cd /home/oracle/software/goldengate/12.2.0.1/p6880880
unzip p6880880_112000_Linux-x86-64.zip
cp -Rp ./OPatch/* /gg/gg1/OPatch/
/gg/gg1/OPatch/opatch version
```

```sh
#実行結果
[oracle@dbvgg p6880880]$ /gg/gg1/OPatch/opatch version
OPatch Version: 11.2.0.3.19

OPatch succeeded.
[oracle@dbvgg p6880880]$
```



#### **GoldenGate用のPatch更新**

```sh
#OPatch更新
export ORACLE_HOME=/gg/gg1
export PATH=$ORACLE_HOME/OPatch:$PATH

cd /home/oracle/software/goldengate/12.2.0.1/p26849940
unzip p26849940_12201170919_Linux-x86-64.zip
cd 26849940/
/gg/gg1/OPatch/opatch prereq CheckConflictAgainstOHWithDetail -ph ./
$ORACLE_HOME/OPatch/opatch apply -oh $ORACLE_HOME
$ORACLE_HOME/OPatch/opatch lspatches
$ORACLE_HOME/OPatch/opatch lsinventory

```

```sh
#実行結果
[oracle@dbvgg 26849940]$ $ORACLE_HOME/OPatch/opatch apply -oh $ORACLE_HOME

Oracle Interim Patch Installerバージョン11.2.0.3.19
Copyright (c) 2019, Oracle Corporation.  All rights reserved。


Oracle Home       : /gg/gg1
Central Inventory : /u01/app/oraInventory
   from           : /gg/gg1/oraInst.loc
OPatch version    : 11.2.0.3.19
OUI version       : 11.2.0.3.0
Log file location : /gg/gg1/cfgtoollogs/opatch/opatch2019-03-29_17-36-23午後_1.log

Verifying environment and performing prerequisite checks...
OPatch continues with these patches:   26849940

続行しますか。[y|n]
y
User Responded with: Y
All checks passed.
セキュリティの問題について通知を受ける電子メール・アドレスを指定し、Oracle Configuration
Managerをインストールして開始してください。My Oracle Supportの電子メール・アドレス/ユーザー名を使用すればより簡単です。
詳細はhttp://www.oracle.com/support/policies.htmlにアクセスしてください。
電子メール・アドレス/ユーザー名:

セキュリティの問題について通知を受け取るための電子メール・アドレスが指定されていません。
セキュリティの問題に関する通知を今後も受け取りませんか([Y]はい, [N]いいえ) [N]:  y



ローカル・システムのこのORACLE_HOME以外で実行しているOracleインスタンスを停止してください。
(Oracleホーム = '/gg/gg1')


ローカル・システムにパッチを適用する準備ができましたか。 [y|n]
y
User Responded with: Y
Backing up files...
Applying interim patch '26849940' to OH '/gg/gg1'

コンポーネントoracle.oggcore.ora11g, 12.2.0.0.0にパッチを適用中...
Patch 26849940 successfully applied.
Log file location: /gg/gg1/cfgtoollogs/opatch/opatch2019-03-29_17-36-23午後_1.log

OPatch succeeded.
[oracle@dbvgg 26849940]$
[oracle@dbvgg 26849940]$ $ORACLE_HOME/OPatch/opatch lspatches
26849940;

OPatch succeeded.
[oracle@dbvgg 26849940]$
[oracle@dbvgg 26849940]$ $ORACLE_HOME/OPatch/opatch lsinventory

Oracle Interim Patch Installerバージョン11.2.0.3.19
Copyright (c) 2019, Oracle Corporation.  All rights reserved。


Oracle Home       : /gg/gg1
Central Inventory : /u01/app/oraInventory
   from           : /gg/gg1/oraInst.loc
OPatch version    : 11.2.0.3.19
OUI version       : 11.2.0.3.0
Log file location : /gg/gg1/cfgtoollogs/opatch/opatch2019-03-29_17-38-37午後_1.log

Lsinventory Output file location : /gg/gg1/cfgtoollogs/opatch/lsinv/lsinventory2019-03-29_17-38-37午後.txt

--------------------------------------------------------------------------------
Local Machine Information::
Hostname: dbvgg.jp.oracle.com
ARU platform id: 226
ARU platform description:: Linux x86-64

インストールされた最上位製品(1):

Oracle GoldenGate Core                                               12.2.0.0.0
このOracleホームには1の製品がインストールされています。


仮パッチ(1) :

Patch  26849940     : applied on Fri Mar 29 17:37:09 JST 2019
Unique Patch ID:  21947835
   Created on 13 Feb 2018, 15:29:18 hrs PST8PDT
   Bugs fixed:
     26112114, 21254311, 22628312, 25256300, 24339776, 22466155, 21562399
     22910007, 22642576, 25096792, 25252388, 26122243, 25031466, 24826961
     24804392, 22912874, 24312736, 24302758, 24414523, 23733399, 22959377
     23514258, 25369310, 21548970, 23642240, 22266611, 23058710, 24744349
     25918872, 24598011, 25797611, 23755469, 25667779, 21131090, 22202129
     22478792, 25814949, 22830589, 22295723, 22993705, 25213169, 23102612
     22458470, 23750747, 21888279, 23267559, 22295940, 22730188, 25674499
     23712604, 25137084, 25350730, 22811754, 26127417, 20822775, 24439762
     23661056, 23607346, 23641740, 23499047, 22352402, 23751229, 25439681
     24345528, 22514172, 25927416, 25463128, 23478103, 23587474, 23763062
     21425179, 23067041, 24359320, 22046726, 21763449, 23479013, 23275654
     25231249, 23133585, 22004485, 23608765, 25087704, 26000622, 24752349
     23108041, 22455149, 25462009, 26253307, 22103949, 24310901, 21452073
     23580290, 25414758, 23040154, 22257964, 26159982, 22888353, 24751551
     21805148, 21481506, 22553129, 23328064, 20656312



--------------------------------------------------------------------------------

OPatch succeeded.
[oracle@dbvgg 26849940]$
```



#### **GoldenGate18c(18.1.0.0.0)のインストール**

#### **メディア・ファイルの解凍**

```sh
#コマンド
cd /home/oracle/software/goldengate/18.1.0.0/V980002-01
ls -l
unzip V980002-01.zip
```

```sh
#実行結果
[oracle@dbvgg V980002-01]$ cd /home/oracle/software/goldengate/18.1.0.0/V980002-01
[oracle@dbvgg V980002-01]$
[oracle@dbvgg V980002-01]$ ll
合計 383516
-rwxr-xr-x 1 oracle oinstall 392717701 10月 19 11:16 2018 V980002-01.zip
[oracle@dbvgg V980002-01]$
[oracle@dbvgg V980002-01]$
[oracle@dbvgg V980002-01]$ unzip V980002-01.zip
Archive:  V980002-01.zip
   creating: fbo_ggs_Linux_x64_shiphome/
  ～中略～
  inflating: fbo_ggs_Linux_x64_shiphome/Disk1/stage/sizes/oracle.oggcore.top18.1.0.0.0ora18c.sizes.properties
  inflating: OGG-18.1.0.0-README.txt
  inflating: OGG_WinUnix_Rel_Notes_18.1.0.0.0.pdf
[oracle@dbvgg V980002-01]$
```



#### **サイレントインストール用のレスポンスファイルの修正**

★部分が修正箇所になります。環境に合わせて修正する必要があります。

```sh
cd ./fbo_ggs_Linux_x64_shiphome/Disk1/response
ls -l
vi oggcore.rsp
```

```sh
#oggcore.rspの修正内容
####################################################################
## Copyright(c) Oracle Corporation 2018. All rights reserved.     ##
##                                                                ##
## Specify values for the variables listed below to customize     ##
## your installation.                                             ##
##                                                                ##
## Each variable is associated with a comment. The comment        ##
## can help to populate the variables with the appropriate        ##
## values.                                                        ##
##                                                                ##
## IMPORTANT NOTE: This file should be secured to have read       ##
## permission only by the oracle user or an administrator who     ##
## own this installation to protect any sensitive input values.   ##
##                                                                ##
####################################################################

#-------------------------------------------------------------------------------
# Do not change the following system generated value.
#-------------------------------------------------------------------------------
oracle.install.responseFileVersion=/oracle/install/rspfmt_ogginstall_response_schema_v12_1_2


################################################################################
##                                                                            ##
## Oracle GoldenGate installation option and details                          ##
##                                                                            ##
################################################################################

#-------------------------------------------------------------------------------
# Specify the installation option.
# Specify ORA18c for installing Oracle GoldenGate for Oracle Database 18c or
#         ORA12c for installing Oracle GoldenGate for Oracle Database 12c or
#         ORA11g for installing Oracle GoldenGate for Oracle Database 11g
#-------------------------------------------------------------------------------
INSTALL_OPTION=ORA18c ★←

#-------------------------------------------------------------------------------
# Specify a location to install Oracle GoldenGate
#-------------------------------------------------------------------------------
SOFTWARE_LOCATION=/gg/gg2 ★←

#-------------------------------------------------------------------------------
# Specify true to start the manager after installation.
#-------------------------------------------------------------------------------
START_MANAGER=false ★←

#-------------------------------------------------------------------------------
# Specify a free port within the valid range for the manager process.
# Required only if START_MANAGER is true.
#-------------------------------------------------------------------------------
MANAGER_PORT=

#-------------------------------------------------------------------------------
# Specify the location of the Oracle Database.
# Required only if START_MANAGER is true.
#-------------------------------------------------------------------------------
DATABASE_LOCATION=


################################################################################
##                                                                            ##
## Specify details to Create inventory for Oracle installs                    ##
## Required only for the first Oracle product install on a system.            ##
##                                                                            ##
################################################################################

#-------------------------------------------------------------------------------
# Specify the location which holds the install inventory files.
# This is an optional parameter if installing on
# Windows based Operating System.
#-------------------------------------------------------------------------------
INVENTORY_LOCATION=

#-------------------------------------------------------------------------------
# Unix group to be set for the inventory directory.
# This parameter is not applicable if installing on
# Windows based Operating System.
#-------------------------------------------------------------------------------
UNIX_GROUP_NAME=


```



#### **GoldenGateインストール**

```sh
cd /home/oracle/software/goldengate/18.1.0.0/V980002-01/fbo_ggs_Linux_x64_shiphome/Disk1
./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/18.1.0.0/V980002-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
```

```sh
#実行結果
[oracle@dbvgg Disk1]$ ./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/18.1.0.0/V980002-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
Oracle Universal Installerを起動中です...

一時領域の確認中: 120MBを超えている必要があります.   実際 25219MB    問題なし
スワップ領域の確認中: 150MBを超えている必要があります.   実際 7855MB    問題なし
Oracle Universal Installerの起動を準備中 /tmp/OraInstall2019-03-29_05-44-14PM. お待ちください...
このインストール・セッションのログは次の場所にあります:
 /u01/app/oraInventory/logs/installActions2019-03-29_05-44-14PM.log
Oracle GoldenGate Coreのインストールが成功しました。
詳細は'/u01/app/oraInventory/logs/silentInstall2019-03-29_05-44-14PM.log'を確認してください。
Successfully Setup Software.

[oracle@dbvgg Disk1]$
```



#### **Trailファイル格納ディレクトリの作成**

「/gg/gg1/c11」はソース側のCaptureプロセスが生成するLocal Trailの格納ディレクトリ、「/gg/gg2/d11」はData Pumpがターゲット側に生成するRemote Trailの格納ディレクトリとなります。

```sh
mkdir -p /gg/gg1/dirdat/c11 #Local Trail用の格納ディレクトリ
mkdir -p /gg/gg2/dirdat/d11 #Remote Trail用の格納ディレクトリ
```



#### **DB環境変更（ソース側）**

#### **表領域の作成**

```sql
. /home/oracle/.oraenv_db112s --環境変数の読み込み
sqlplus / as sysdba
create tablespace ggdata datafile '/u01/app/oracle/oradata/DB112S/datafile/ggdata.dbf' size 5G;
```



#### **伝搬対象ユーザ、及びGoldenGate管理ユーザの作成**

```sql
CREATE USER ggs IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;
CREATE USER ggtest IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;

GRANT dba TO ggs;
GRANT dba TO ggtest;
exec dbms_goldengate_auth.grant_admin_privilege('GGS');
```



#### **初期化パラメータの変更/最小サプリメンタルロギングの設定**

```sql
-- 事前確認
show parameter enable_goldengate_replication
select name,supplemental_log_data_min from v$database;
select log_mode from v$database;

-- 初期化パラメータの変更
alter system set enable_goldengate_replication=true scope=both;
alter system set streams_pool_size=1250M scope=both SID='*'; -- Integrated Capture要件

-- 最小サプリメンタルロギングの設定
alter database add supplemental log data;
alter system switch logfile;

-- 設定変更確認
show parameter enable_goldengate_replication
select name,supplemental_log_data_min from v$database;
select log_mode from v$database;
exit
```

```sql
-- 実行結果
SQL> show parameter enable_goldengate_replication

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
enable_goldengate_replication        boolean     FALSE
SQL>
SQL> select name,supplemental_log_data_min from v$database;

NAME      SUPPLEME
--------- --------
DB112S    NO

SQL> select log_mode from v$database;

LOG_MODE
------------
ARCHIVELOG

SQL>
SQL>
SQL> alter system set enable_goldengate_replication=true scope=both;

システムが変更されました。

SQL> alter system set streams_pool_size=1250M scope=both SID='*';

システムが変更されました。

SQL> alter database add supplemental log data;

データベースが変更されました。

SQL> alter system switch logfile;

システムが変更されました。

SQL> show parameter enable_goldengate_replication

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
enable_goldengate_replication        boolean     TRUE
SQL> select name,supplemental_log_data_min from v$database;

NAME      SUPPLEME
--------- --------
DB112S    YES

SQL> select log_mode from v$database;

LOG_MODE
------------
ARCHIVELOG

SQL>

```



#### **DB環境変更（ターゲット側）**

#### **表領域の作成**

```sql
. /home/oracle/.oraenv_db18s --環境変数の読み込み
sqlplus / as sysdba
create tablespace ggdata datafile '/u01/app/oracle/oradata/DB18S/ggdata.dbf' size 1G;
alter session set container=db18p1;
create tablespace ggdata datafile '/u01/app/oracle/oradata/DB18S/db18p1/ggdata.dbf' size 5G;

```



#### **伝搬対象ユーザ、及びGoldenGate管理ユーザの作成**

```sql
alter session set container=cdb$root;
show con_name
CREATE USER c##ggs IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;
alter session set container=db18p1;
show con_name
CREATE USER ggtest IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;

alter session set container=cdb$root;
GRANT DBA TO c##ggs container=all;
exec dbms_goldengate_auth.grant_admin_privilege('C##GGS');

alter session set container=db18p1;
GRANT DBA TO ggtest;
exec dbms_goldengate_auth.grant_admin_privilege('C##GGS');
```



#### **初期化パラメータの変更/最小サプリメンタルロギングの設定**

```sql
alter session set container=cdb$root;
show con_name

-- 事前確認
show parameter enable_goldengate_replication
select name,supplemental_log_data_min from v$database;
select log_mode from v$database;

-- 初期化パラメータの変更
alter system set enable_goldengate_replication=true scope=both;
alter system set streams_pool_size=1250M scope=both SID='*'; -- Integrated Replicat要件

-- 最小サプリメンタルロギングの設定
alter database add supplemental log data;  -- ターゲット側なので本来であれば不要。logminer要件のため設定
alter system switch logfile;

-- 設定変更確認
show parameter enable_goldengate_replication
select name,supplemental_log_data_min from v$database;
select log_mode from v$database;
```

```sql
-- 実行結果
SQL> alter session set container=cdb$root;

セッションが変更されました。

SQL>
SQL> show con_name

CON_NAME
------------------------------
CDB$ROOT
SQL> show parameter enable_goldengate_replication

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
enable_goldengate_replication        boolean     FALSE
SQL> select name,supplemental_log_data_min from v$database;

NAME      SUPPLEME
--------- --------
DB18S     NO

SQL> select log_mode from v$database;

LOG_MODE
------------
ARCHIVELOG

SQL> alter system set enable_goldengate_replication=true scope=both;

システムが変更されました。

SQL> alter system set streams_pool_size=1250M scope=both SID='*';

システムが変更されました。

SQL> alter database add supplemental log data;

データベースが変更されました。

SQL> alter system switch logfile;

システムが変更されました。

SQL> show parameter enable_goldengate_replication

NAME                                 TYPE        VALUE
------------------------------------ ----------- ------------------------------
enable_goldengate_replication        boolean     TRUE
SQL> select name,supplemental_log_data_min from v$database;

NAME      SUPPLEME
--------- --------
DB18S     YES

SQL> select log_mode from v$database;

LOG_MODE
------------
ARCHIVELOG

SQL>
```



#### **GoldenGate環境設定**

#### **GG_HOME配下のサブディレクトリ作成**

サプリメンタル・ロギングはソース側で実施します。

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1
./ggsci
create subdirs
exit

cd /gg/gg2
./ggsci
create subdirs
exit
```

```sh
# 実行結果
[oracle@dbvgg gg1]$ ./ggsci

Oracle GoldenGate Command Interpreter for Oracle
Version 12.2.0.1.170919 OGGCORE_12.2.0.1.0OGGBP_PLATFORMS_171030.0908_FBO
Linux, x64, 64bit (optimized), Oracle 11g on Oct 30 2017 19:19:45
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2017, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> create subdirs

Creating subdirectories under current directory /gg/gg1

Parameter files                /gg/gg1/dirprm: created
Report files                   /gg/gg1/dirrpt: created
Checkpoint files               /gg/gg1/dirchk: created
Process status files           /gg/gg1/dirpcs: created
SQL script files               /gg/gg1/dirsql: created
Database definitions files     /gg/gg1/dirdef: created
Extract data files             /gg/gg1/dirdat: created
Temporary files                /gg/gg1/dirtmp: created
Credential store files         /gg/gg1/dircrd: created
Masterkey wallet files         /gg/gg1/dirwlt: created
Dump files                     /gg/gg1/dirdmp: created


GGSCI (dbvgg.jp.oracle.com) 2>
GGSCI (dbvgg.jp.oracle.com) 3> exit
[oracle@dbvgg gg1]$ cd /gg/gg2
[oracle@dbvgg gg2]$ ./ggsci

Oracle GoldenGate Command Interpreter for Oracle
Version 18.1.0.0.0 OGGCORE_18.1.0.0.0_PLATFORMS_180928.0432_FBO
Linux, x64, 64bit (optimized), Oracle 18c on Sep 29 2018 07:21:38
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2018, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> create subdirs

Creating subdirectories under current directory /gg/gg2

Parameter file                 /gg/gg2/dirprm: created.
Report file                    /gg/gg2/dirrpt: created.
Checkpoint file                /gg/gg2/dirchk: created.
Process status files           /gg/gg2/dirpcs: created.
SQL script files               /gg/gg2/dirsql: created.
Database definitions files     /gg/gg2/dirdef: created.
Extract data files             /gg/gg2/dirdat: created.
Temporary files                /gg/gg2/dirtmp: created.
Credential store files         /gg/gg2/dircrd: created.
Masterkey wallet files         /gg/gg2/dirwlt: created.
Dump files                     /gg/gg2/dirdmp: created.


GGSCI (dbvgg.jp.oracle.com) 2> exit
[oracle@dbvgg gg2]$
```



#### **スキーマ・レベルのサプリメンタルロギングの実施**

サプリメンタル・ロギングはソース側で実施します。

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1
./ggsci
dblogin userid ggs@db112s, password oracle
add schematrandata ggtest
```

```sh
# 実行結果
[oracle@dbvgg gg1]$ ./ggsci

Oracle GoldenGate Command Interpreter for Oracle
Version 12.2.0.1.170919 OGGCORE_12.2.0.1.0OGGBP_PLATFORMS_171030.0908_FBO
Linux, x64, 64bit (optimized), Oracle 11g on Oct 30 2017 19:19:45
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2017, Oracle and/or its affiliates. All rights reserved.

GGSCI (dbvgg.jp.oracle.com) 1> dblogin userid ggs@db112s, password oracle
Successfully logged into database.

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 2> add schematrandata ggtest

2019-03-29 17:59:55  INFO    OGG-01788  SCHEMATRANDATA has been added on schema ggtest.

2019-03-29 17:59:55  INFO    OGG-01976  SCHEMATRANDATA for scheduling columns has been added on schema ggtest.

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 3>
```



#### **GGパラメータファイルの作成**

GoldenGateのパラメータは各プロセスごとに作成する必要があります。GLOBALS、MGRパラメータはソース、及びターゲット側に存在するので両サイトで作成する必要があります。

#### **GLOBALSパラメータ（ソース側）**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1

./ggsci
EDIT PARAMS GLOBALS

#下記をviエディタで指定する
SYSLOG NONE
GGSCHEMA ggs
NODUPMSGSUPPRESSION

view params GLOBALS
```



#### **MGRパラメータ（ソース側）**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1

./ggsci
EDIT PARAMS MGR

# MGRファイルの設定
PORT 7809

AUTOSTART EXTRACT c11
AUTOSTART EXTRACT d11
AUTORESTART EXTRACT c11, RETRIES 2, WAITMINUTES 1, RESETMINUTES 60
AUTORESTART EXTRACT d11, RETRIES 5, WAITMINUTES 1, RESETMINUTES 60

-- Trailファイルのメンテンス設定
PURGEOLDEXTRACTS ./dirdat/c11/*,  USECHECKPOINTS, MINKEEPDAYS 1

view params GLOBALS

```



#### **Captureパラメータ（ソース側）**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1

./ggsci
EDIT PARAMS C11

# CAPTUREファイルの設定
EXTRACT c11
USERID ggs@db112s,PASSWORD oracle
EXTTRAIL ./dirdat/c11/lt
CACHEMGR CACHESIZE 4GB
DISCARDFILE ./dirrpt/c11.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY
DDL INCLUDE ALL
DDLOPTIONS CAPTUREGLOBALTEMPTABLE,REPORT
TRANLOGOPTIONS INTEGRATEDPARAMS (MAX_SGA_SIZE 1250, PARALLELISM 2)

TABLE ggtest.* ;

view params MGR

```



#### **Data Pumpパラメータ（ソース側）**

今回は筐体内の2DB間のレプリケーション設定なので、RMTHOSTに「localhost」を設定しています。本来ならばターゲットサーバのhostname、もしくはIPアドレスの指定が必要です。

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1

./ggsci
EDIT PARAMS d11

# Data Pumpファイルの設定
EXTRACT d11
PASSTHRU
RMTHOST localhost,  MGRPORT 7810
RMTTRAIL ./dirdat/d11/rt

TABLE ggtest.*;

view params c11

```



#### **GLOBALSパラメータ（ターゲット側）**

```sh
. /home/oracle/.oraenv_db18s --環境変数の読み込み
cd /gg/gg2

./ggsci
EDIT PARAM GLOBALS

GGSCHEMA c##ggs
NODUPMSGSUPPRESSION

view params GLOBALS

```



#### **MGRパラメータ（ソース側）**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg2

./ggsci
EDIT PARAMS MGR

# MGRファイルの設定
PORT 7810

AUTOSTART REPLICAT r11
AUTORESTART REPLICAT r11, RETRIES 2, WAITMINUTES 1, RESETMINUTES 60

-- Trailファイルのメンテンス設定
PURGEOLDEXTRACTS ./dirdat/d11/*,  USECHECKPOINTS, MINKEEPDAYS 1


```



#### **Replicatパラメータ（ターゲット側）**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg2

./ggsci
EDIT PARAMS R11

REPLICAT r11
USERID c##ggs@db18p1, PASSWORD oracle
DBOPTIONS INTEGRATEDPARAMS(PARALLELISM 4,MAX_PARALLELISM 4)

DISCARDFILE ./dirrpt/r11.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY

DDL INCLUDE ALL
DDLOPTIONS CAPTUREGLOBALTEMPTABLE,REPORT
REPORTCOUNT EVERY 10 MINUTES, RATE

BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;

```



#### **GoldenGateプロセス作成**

#### **ソース側のプロセス作成**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1
./ggsci

#DBログイン
dblogin userid ggs@db112s,password oracle

#Captuteプロセスの作成・追加
REGISTER EXTRACT c11 DATABASE
add extract c11, integrated,tranlog, begin now
add exttrail  ./dirdat/c11/lt, extract c11, megabytes 500

#Data Pumpプロセスの作成・追加
add extract d11, exttrailsource ./dirdat/c11/lt
add rmttrail ./dirdat/d11/rt, extract d11

#確認
info all
```

```sh
# 実行結果
GGSCI (dbvgg.jp.oracle.com) 1> dblogin userid ggs@db112s,password oracle
Successfully logged into database.

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 2> REGISTER EXTRACT c11 DATABASE

2019-03-29 18:18:00  INFO    OGG-02003  Extract C11 successfully registered with database at SCN 1089847.

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 3> add extract c11, integrated,tranlog, begin now
EXTRACT (Integrated) added.


GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 4> add exttrail  ./dirdat/c11/lt, extract c11, megabytes 500
EXTTRAIL added.

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 5>

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 5>

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 5> add extract d11, exttrailsource ./dirdat/c11/lt
EXTRACT added.


GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 6>

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 6> add rmttrail ./dirdat/d11/rt, extract d11
RMTTRAIL added.

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 7>

GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 7> info all

Program     Status      Group       Lag at Chkpt  Time Since Chkpt

MANAGER     STOPPED
EXTRACT     STOPPED     C11         00:00:00      00:00:17
EXTRACT     STOPPED     D11         00:00:00      00:00:07


GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 8>
```



#### **ターゲット側のプロセス作成**

ReplicatはPDBに対して適用するため、dblogin時に指定する接続記述子はCDB$ROOTではなく適用するPDBへの指定が必要です。

またIntegrated Catptureの場合はregisterコマンドが必要でしたが、Integrated Replicatの場合は不要です。（内部的に発行されています。）

```sh
. /home/oracle/.oraenv_db18s --環境変数の読み込み
cd /gg/gg2
./ggsci

#DBログイン
dblogin userid c##ggs@db18p1,password oracle

#Replicatプロセスの作成
ADD REPLICAT r11,integrated EXTTRAIL ./dirdat/d11/rt

#状態確認
info all
```

```sh
# 実行結果
GGSCI (dbvgg.jp.oracle.com) 1> dblogin userid c##ggs@db18p1,password oracle

Successfully logged into database DB18P1.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 2>
GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 2> ADD REPLICAT r11,integrated EXTTRAIL ./dirdat/d11/rt
REPLICAT (Integrated) added.


GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 3>
GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 3> info all

Program     Status      Group       Lag at Chkpt  Time Since Chkpt

MANAGER     STOPPED
REPLICAT    STOPPED     R11         00:00:00      00:00:20


GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 4>

```



#### **GoldenGateプロセス起動**

ソース側のData Pumpプロセスはターゲット側のMGRプロセスと通信をします。したがって、先にターゲット側のMGRプロセスを起動する必要があるため、ターゲット側から起動を行います。

#### **ターゲット側のプロセス起動**

```sh
. /home/oracle/.oraenv_db18s --環境変数の読み込み
cd /gg/gg1
./ggsci

#起動コマンド
start mgr

# mgrのパラメータでautostartを設定しているためreplicatプロセスの起動は不要。
#start r11

#状態確認コマンド
info all
```



```sh
# 実行結果
[oracle@dbvgg gg2]$ ./ggsci

Oracle GoldenGate Command Interpreter for Oracle
Version 18.1.0.0.0 OGGCORE_18.1.0.0.0_PLATFORMS_180928.0432_FBO
Linux, x64, 64bit (optimized), Oracle 18c on Sep 29 2018 07:21:38
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2018, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> info all

Program     Status      Group       Lag at Chkpt  Time Since Chkpt

MANAGER     STOPPED
REPLICAT    STOPPED     R11         00:00:00      00:00:49


GGSCI (dbvgg.jp.oracle.com) 2> start mgr
Manager started.


GGSCI (dbvgg.jp.oracle.com) 3> info all

Program     Status      Group       Lag at Chkpt  Time Since Chkpt

MANAGER     RUNNING
REPLICAT    RUNNING     R11         00:00:00      00:00:03


GGSCI (dbvgg.jp.oracle.com) 4>

```



#### **ソース側のプロセス起動**

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1
./ggsci

#起動コマンド
start mgr
# mgrのパラメータでautostartを設定しているためcapture、data pumpプロセスの起動は不要。
# start c11
# start d11

#状態確認コマンド
info all
```



```sh
# 実行結果
[oracle@dbvgg gg1]$ ./ggsci

Oracle GoldenGate Command Interpreter for Oracle
Version 12.2.0.1.170919 OGGCORE_12.2.0.1.0OGGBP_PLATFORMS_171030.0908_FBO
Linux, x64, 64bit (optimized), Oracle 11g on Oct 30 2017 19:19:45
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2017, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> info all

Program     Status      Group       Lag at Chkpt  Time Since Chkpt

MANAGER     STOPPED
EXTRACT     STOPPED     C11         00:00:02      00:00:30
EXTRACT     STOPPED     D11         00:00:00      00:00:29


GGSCI (dbvgg.jp.oracle.com) 2> start mgr
Manager started.


GGSCI (dbvgg.jp.oracle.com) 3> info all

Program     Status      Group       Lag at Chkpt  Time Since Chkpt

MANAGER     RUNNING
EXTRACT     RUNNING     C11         00:00:10      00:00:07
EXTRACT     RUNNING     D11         00:00:00      00:00:04


GGSCI (dbvgg.jp.oracle.com) 4>

```



#### **Appendix**

#### **OGG-02912エラー対応**

**DB11.2とGG12.2(Integrated Capture)**の組み合わせで初回起動時、OGG-02912が発生し Capture プロセスが ABENDする場合があります。(適用されているPSU/BPに依存します。)

Oracle GoldenGate12.2 からTrailファイルのフォーマットが変更されていることによるエラーです。（データベース側のログマイナーに関するファンクションが対応していない場合に発生します。）

```text
ERROR OGG-02912 Patch 17030189 is required on your Oracle mining database for trail format RELEASE 12.2 or later.
```

エラーが発生した場合はエラーメッセージにある通り「Patch 17030189」を適用するか、GG_HOME配下にある「prvtlmpg.plb」を実行することでエラーを回避することが出来ます。

```sh
. /home/oracle/.oraenv_db112s --環境変数の読み込み
cd /gg/gg1
sqlplus / as sysdba
@prvtlmpg.plb
```

```sh
-- 実行結果
[oracle@dbvgg gg1]$ sqlplus / as sysdba

SQL*Plus: Release 11.2.0.4.0 Production on 金 3月 29 18:22:29 2019

Copyright (c) 1982, 2013, Oracle.  All rights reserved.



Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing options
に接続されました。
SQL> @prvtlmpg.plb

Oracle GoldenGate Workaround prvtlmpg

This script provides a temporary workaround for bug 17030189.
It is strongly recommended that you apply the official Oracle
Patch for bug 17030189 from My Oracle Support instead of using
this workaround.

This script must be executed in the mining database of Integrated
Capture. You will be prompted for the username of the mining user.
Use a double quoted identifier if the username is case sensitive
or contains special characters. In a CDB environment, this script
must be executed from the CDB$ROOT container and the mining user
must be a common user.

===========================  WARNING  ==========================
You MUST stop all Integrated Captures that belong to this mining
user before proceeding!
================================================================

Enter Integrated Capture mining user: ggs

Installing workaround...
エラーはありません。
エラーはありません。
エラーはありません。
Installation completed.
SQL>
SQL> Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, OLAP, Data Mining and Real Application Testing optionsとの接続が切断されました。
[oracle@dbvgg gg1]$

```