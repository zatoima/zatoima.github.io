---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Configure Auditing for Specific Users Only Using pgaudit Extension in Aurora PostgreSQL"
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



#### Enable Parameter Group

Modify the parameter group associated with the DB instance, use the shared preload library that includes pgaudit, set the pgaudit.role parameter to rds_pgaudit. At the parameter group level, set the pgaudit.log parameter to none so that database, role, or table can be specified at the database, role, or table level.

#### Create a dedicated database role called rds_pgaudit

```
postgres=> CREATE ROLE rds_pgaudit;
CREATE ROLE
```

#### Enable pgaudit extension

```
CREATE EXTENSION pgaudit;
```

#### Verify settings

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

#### Create a sample DB for auditing

```
postgres=> create database auditdb WITH OWNER postgres;
CREATE DATABASE
```

#### Switch database connection

```
postgres=> \c auditdb
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
You are now connected to database "auditdb" as user "postgres".
```

#### Create users

```sql
auditdb=> CREATE ROLE audit_user1 WITH CREATEDB CREATEROLE LOGIN PASSWORD 'xxxxxx';
CREATE ROLE
auditdb=> CREATE ROLE audit_user2 WITH CREATEDB CREATEROLE LOGIN PASSWORD 'xxxxxx';
CREATE ROLE
```

#### Change user audit settings

Configure audit_user1 to audit all operations.

```
auditdb=> ALTER ROLE audit_user1 set pgaudit.log='All';
ALTER ROLE
auditdb=> ALTER ROLE audit_user2 set pgaudit.log='NONE';
ALTER ROLE
```

#### Verify user audit settings

```
auditdb=> select rolname,rolconfig from pg_roles where rolname in ('postgres','audit_user1','audit_user2');
   rolname   |     rolconfig
-------------+--------------------
 audit_user1 | {pgaudit.log=All}
 audit_user2 | {pgaudit.log=NONE}
 postgres    |
(3 rows)
```

#### Execute DDL/DML with audit_user1 (auditing enabled)

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
auditdb-> SELECT num                         a -- generated value
auditdb->       ,'1'                         b -- constant
auditdb->       ,to_char(num,'FM00000')      c -- generated value (for ID-like strings)
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

#### Verify log output

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

#### Execute DDL/DML with audit_user2 (auditing not configured)

```
auditdb=> \c - audit_user2;
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
You are now connected to database "auditdb" as user "audit_user2".
auditdb=>
auditdb=>
auditdb=>
auditdb=> CREATE TABLE t2 AS
auditdb-> SELECT num                         a -- generated value
auditdb->       ,'1'                         b -- constant
auditdb->       ,to_char(num,'FM00000')      c -- generated value (for ID-like strings)
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

#### Verify log output

No log output for audit_user2 operations.

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

#### References

> Audit an Amazon RDS DB Instance Running PostgreSQL Using the pgaudit Extension https://aws.amazon.com/jp/premiumsupport/knowledge-center/rds-postgresql-pgaudit/
>
> pgAudit Open Source PostgreSQL Audit Logging https://github.com/pgaudit/pgaudit
