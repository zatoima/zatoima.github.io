---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLの拡張機能のpgauditで特定ユーザのみの監査を設定する"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL","pgaudit"]
categories: ["AWS","Aurora","PostgreSQL","pgaudit"]
url: aws-aurora-postgresql-pgaudit-user.html
date: 2020-11-20
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



#### パラメータグループの有効化

DB インスタンスに関連付けられているパラメータグループを変更し、pgaudit が含まれている共有事前ロードライブラリを使用して、パラメータ pgaudit.role を設定して、pgaudit.role はロール rds_pgaudit に設定する必要がある。この時、pgaudit.log パラメータの値にデータベース、ロール、またはテーブルを設定するために、パラメータグループレベルでは pgaudit.log パラメータを none に設定。

#### rds_pgaudit という専用のデータベースロールを作成

```
postgres=> CREATE ROLE rds_pgaudit;
CREATE ROLE
```

#### pgaudit 拡張機能を有効化

```
CREATE EXTENSION pgaudit;
```

#### 設定値確認

```
postgres=> show shared_preload_libraries;
      shared_preload_libraries       
-------------------------------------
 rdsutils,pg_stat_statements,pgaudit
(1 row)

postgres=> show pgaudit.role;
 pgaudit.role 
--------------
 rds_pgaudit
(1 row)

postgres=> show pgaudit.log;
 pgaudit.log 
-------------
 none
(1 row)
```

#### 監査対象のサンプルDBの作成

```
postgres=> create database auditdb WITH OWNER postgres;
CREATE DATABASE
```

#### DB接続先の切替

```
postgres=> \c auditdb
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
You are now connected to database "auditdb" as user "postgres".
```

#### ユーザ作成

```sql
auditdb=> CREATE ROLE audit_user1 WITH CREATEDB CREATEROLE LOGIN PASSWORD 'xxxxxx';
CREATE ROLE
auditdb=> CREATE ROLE audit_user2 WITH CREATEDB CREATEROLE LOGIN PASSWORD 'xxxxxx';
CREATE ROLE
```

#### ユーザの監査設定の変更

audit_user1ユーザのみすべての操作の監査を行う設定に。

```
auditdb=> ALTER ROLE audit_user1 set pgaudit.log='All';
ALTER ROLE
auditdb=> ALTER ROLE audit_user2 set pgaudit.log='NONE';
ALTER ROLE
```

#### ユーザの監査設定の確認

```
auditdb=> select rolname,rolconfig from pg_roles where rolname in ('postgres','audit_user1','audit_user2');
   rolname   |     rolconfig      
-------------+--------------------
 audit_user1 | {pgaudit.log=All}
 audit_user2 | {pgaudit.log=NONE}
 postgres    | 
(3 rows)
```

#### 監査設定済のaudit_user1でDDL/DMLを実行

```
auditdb=> \c - audit_user1;
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
You are now connected to database "auditdb" as user "audit_user1".
auditdb=> 
auditdb=> 
auditdb=> 
auditdb=> 
auditdb=> CREATE TABLE t1 AS
auditdb-> SELECT num                         a -- 生成値
auditdb->       ,'1'                         b -- 定数
auditdb->       ,to_char(num,'FM00000')      c -- 生成値を利用（IDなどの文字列）
auditdb->       ,current_timestamp      d 
auditdb-> FROM   generate_series(1,10000000) num
auditdb-> ;
SELECT 10000000
auditdb=> 
auditdb=> select count(*) from t1;
  count   
----------
 10000000
(1 row)

auditdb=> 

```

#### ログ出力を確認

```
2020-11-13 08:06:24 UTC:10.0.1.123(50322):audit_user1@auditdb:[24298]:LOG:  AUDIT: SESSION,1,2,DDL,CREATE TABLE AS,,,"CREATE TABLE t1 AS
	SELECT num                         a 
	      ,'1'                         b 
	      ,to_char(num,'FM00000')      c 
	      ,current_timestamp      d 
	FROM   generate_series(1,10000000) num
	;",<none>
2020-11-13 08:07:36 UTC:10.0.1.123(50322):audit_user1@auditdb:[24298]:LOG:  AUDIT: SESSION,2,1,READ,SELECT,TABLE,public.t1,select count(*) from t1;,<none>
2020-11-13 08:07:36 UTC::@:[32064]:LOG:  AUDIT: SESSION,1,1,READ,SELECT,TABLE,public.t1,select count(*) from t1;,<none>
```

#### 監査設定を行っていないaudit_user2でDDL/DMLを実行

```
auditdb=> \c - audit_user2;
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
You are now connected to database "auditdb" as user "audit_user2".
auditdb=> 
auditdb=> 
auditdb=> 
auditdb=> CREATE TABLE t2 AS
auditdb-> SELECT num                         a -- 生成値
auditdb->       ,'1'                         b -- 定数
auditdb->       ,to_char(num,'FM00000')      c -- 生成値を利用（IDなどの文字列）
auditdb->       ,current_timestamp      d 
auditdb-> FROM   generate_series(1,100000) num
auditdb-> ;
SELECT 100000
auditdb=> select count(*) from t2;
 count  
--------
 100000
(1 row)

auditdb=> 
```

#### ログ出力を確認

特にaudit_user2の操作のログは出力されていない。

```
2020-11-13 08:06:24 UTC:10.0.1.123(50322):audit_user1@auditdb:[24298]:LOG:  AUDIT: SESSION,1,2,DDL,CREATE TABLE AS,,,"CREATE TABLE t1 AS
	SELECT num                         a 
	      ,'1'                         b 
	      ,to_char(num,'FM00000')      c 
	      ,current_timestamp      d 
	FROM   generate_series(1,10000000) num
	;",<none>
2020-11-13 08:07:36 UTC:10.0.1.123(50322):audit_user1@auditdb:[24298]:LOG:  AUDIT: SESSION,2,1,READ,SELECT,TABLE,public.t1,select count(*) from t1;,<none>
2020-11-13 08:07:36 UTC::@:[32064]:LOG:  AUDIT: SESSION,1,1,READ,SELECT,TABLE,public.t1,select count(*) from t1;,<none>
```

#### 参考

> pgaudit 拡張機能を使用して、 PostgreSQL を実行する Amazon RDS DB インスタンスを監査する https://aws.amazon.com/jp/premiumsupport/knowledge-center/rds-postgresql-pgaudit/
>
> pgAudit Open Source PostgreSQL Audit Logging https://github.com/pgaudit/pgaudit