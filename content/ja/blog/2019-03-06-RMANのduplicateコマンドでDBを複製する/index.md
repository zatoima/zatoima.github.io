---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RMANのduplicateコマンドでDBを複製する"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-rman-ruplicate.html
date: 2019-03-06
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



#### **はじめに**

データベースの複製パターンには下記4つのパターンがあります。

システム的な要件によって選べる選択肢が変わってくると思います。

今回の例では4.の「ターゲットまたはリカバリ・カタログへの接続なしで実行するバックアップベースの複製」で実施しています。

------

1. アクティブな複製

   オープン状態またはマウント状態のデータベースから直接複製します。

2. ターゲット接続なしで実行するバックアップベースの複製

   RMANは、既存のRMANバックアップおよびコピーから複製ファイルを作成します。

   この形式では、補助インスタンスおよびリカバリ・カタログへの接続が必要

3. ターゲット接続を指定したバックアップベースの複製

   既存のRMANバックアップおよびコピーから複製ファイルを作成します。

4. ターゲットまたはリカバリ・カタログへの接続なしで実行するバックアップベースの複製

   BACKUP LOCATIONで指定した場所に配置されたRMANバックアップおよびコピーから複製ファイルを作成

------

RMANバックアップからリストア・リカバリする場合もデータベースの複製となりますが、今回の例では含んでいません。

**環境構成**

同一筐体内に複製する手順となります。

| No   | データベース名 | DBバージョン | 備考   |
| ---- | -------------- | ------------ | ------ |
| 1    | db121s         | 12.1.0.2     | 複製元 |
| 2    | db121t         | 12.1.0.2     | 複製先 |

**複製元で**RMANバックアップの取得

```sql
rman target /
run {
  BACKUP INCREMENTAL LEVEL 0 DATABASE FORMAT '/home/oracle/rman/db121s/full_%d_%T_%U' SPFILE PLUS ARCHIVELOG FORMAT '/home/oracle/rman/db121s/ARCH_%d_%T_%U';
  BACKUP AS COPY CURRENT CONTROLFILE FORMAT '/home/oracle/rman/db121s/CNT_%d_%T_%U.ctl';
}
```

#### **複製先のクリーンアップ**

```sql
rm -rf /u01/app/oracle/oradata/DB121T/*
```

#### **複製先パラメータファイル作成**

複製元のデータベースに接続し、spfileから編集用のpfileを作成する。

```sql
. /home/oracle/.oraenv_db121s
sqlplus / as sysdba
create pfile='/tmp/initdb121t.ora' from spfile;
exit
```

#### **複製先パラメータファイル編集**

複製元に依存する値を複製先に記載を変更する。（例：db_nameは「db121s」から「db121t」へ）

```sql
vi /tmp/initdb121t.ora

以下のパラメータの値を変更する
・*.cluster_database     : false																・*.control_files        : /u01/app/oracle/oradata/db121t
・*.db_name              : db121t
・*.db_unique_name       : db121t
・*.dispatchers          : (PROTOCOL=TCP) (SERVICE=db121tXDB)								

以下のパラメータの値を追加する
*.DB_FILE_NAME_CONVERT='/u01/app/oracle/oradata/DB121S/datafile/','/u01/app/oracle/oradata/DB121T/datafile/'
*.LOG_FILE_NAME_CONVERT='/u01/app/oracle/oradata/DB121S/onlinelog/','/u01/app/oracle/oradata/DB121T/onlinelog'
```

#### **補助インスタンス起動**

```sql
. /home/oracle/.oraenv_db121t
sqlplus / as sysdba
startup nomount pfile='/tmp/initdb121t.ora'
```

#### **spfile**の作成

```sql
create spfile = '/u01/app/oracle/product/12.1.0.2/dbhome_2/dbs/spfiledb121t.ora' from pfile='/tmp/initdb121t.ora';
exit
```

#### **複製コマンドの実施**

```sql
rman auxiliary /
run {			
duplicate database to db121t backup location '/home/oracle/rman/db121s';			
}
```

RMANのduplicateコマンドの詳細についてはマニュアルをご確認ください。

> Oracle® Databaseバックアップおよびリカバリ・リファレンス 12cリリース1 (12.1) 
>
> https://docs.oracle.com/cd/E57425_01/121/RCMRF/rcmsynta020.htm
>
> DUPLICATE