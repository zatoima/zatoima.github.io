---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Restoring Individual Tables from a Full Database Logical Backup in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-database-logical-backup-restore-table
date: 2021-10-27
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fa
---









## Commands

### Back Up the Entire Database with pg_dump

```sh
pg_dump -Fc -v -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres pgbench > pgbench.dump
```

### Restore Only a Specific Table with pg_restore

```sh
psql -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "create database pgbench_restore"
pg_restore -v -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d pgbench_restore -t pgbench_accounts pgbench.dump
```

## Execution Log

### Backup

```sh
[ec2-user@bastin ~]$ pg_dump -Fc -v -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres pgbench > pgbench.dump
pg_dump: last built-in OID is 16383
pg_dump: reading extensions
pg_dump: identifying extension members
pg_dump: reading schemas
pg_dump: reading user-defined tables
pg_dump: reading user-defined functions
pg_dump: reading user-defined types
pg_dump: reading procedural languages
pg_dump: reading user-defined aggregate functions
pg_dump: reading user-defined operators
pg_dump: reading user-defined access methods
pg_dump: reading user-defined operator classes
pg_dump: reading user-defined operator families
pg_dump: reading user-defined text search parsers
pg_dump: reading user-defined text search templates
pg_dump: reading user-defined text search dictionaries
pg_dump: reading user-defined text search configurations
pg_dump: reading user-defined foreign-data wrappers
pg_dump: reading user-defined foreign servers
pg_dump: reading default privileges
pg_dump: reading user-defined collations
pg_dump: reading user-defined conversions
pg_dump: reading type casts
pg_dump: reading transforms
pg_dump: reading table inheritance information
pg_dump: reading event triggers
pg_dump: finding extension tables
pg_dump: finding inheritance relationships
pg_dump: reading column info for interesting tables
pg_dump: finding the columns and types of table "public.pgbench_history"
pg_dump: finding the columns and types of table "public.pgbench_tellers"
pg_dump: finding the columns and types of table "public.pgbench_accounts"
pg_dump: finding the columns and types of table "public.pgbench_branches"
pg_dump: flagging inherited columns in subtables
pg_dump: reading indexes
pg_dump: reading indexes for table "public.pgbench_tellers"
pg_dump: reading indexes for table "public.pgbench_accounts"
pg_dump: reading indexes for table "public.pgbench_branches"
pg_dump: flagging indexes in partitioned tables
pg_dump: reading extended statistics
pg_dump: reading constraints
pg_dump: reading triggers
pg_dump: reading rewrite rules
pg_dump: reading policies
pg_dump: reading row security enabled for table "public.pgbench_history"
pg_dump: reading policies for table "public.pgbench_history"
pg_dump: reading row security enabled for table "public.pgbench_tellers"
pg_dump: reading policies for table "public.pgbench_tellers"
pg_dump: reading row security enabled for table "public.pgbench_accounts"
pg_dump: reading policies for table "public.pgbench_accounts"
pg_dump: reading row security enabled for table "public.pgbench_branches"
pg_dump: reading policies for table "public.pgbench_branches"
pg_dump: reading publications
pg_dump: reading publication membership
pg_dump: reading subscriptions
pg_dump: reading large objects
pg_dump: reading dependency data
pg_dump: saving encoding = UTF8
pg_dump: saving standard_conforming_strings = on
pg_dump: saving search_path =
pg_dump: saving database definition
pg_dump: dumping contents of table "public.pgbench_accounts"
pg_dump: dumping contents of table "public.pgbench_branches"
pg_dump: dumping contents of table "public.pgbench_history"
pg_dump: dumping contents of table "public.pgbench_tellers"
[ec2-user@bastin ~]$

```

### Create a Database for Restore

```
[ec2-user@bastin ~]$ psql -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "create database pgbench_restore"
CREATE DATABASE
```

### Restore an Individual Table to the Restore Database

Restore only the pgbench_accounts table:

```
[ec2-user@bastin ~]$ pg_restore -v -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d pgbench_restore -t pgbench_accounts pgbench.dump
pg_restore: connecting to database for restore
pg_restore: creating TABLE "public.pgbench_accounts"
pg_restore: processing data for table "public.pgbench_accounts"
[ec2-user@bastin ~]$ psql -h auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com -d pgbench_restore -U postgres
psql (11.12, server 10.14)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES128-GCM-SHA256, bits: 128, compression: off)
Type "help" for help.

pgbench_restore=> \conninfo
You are connected to database "pgbench_restore" as user "postgres" on host "auroratest1.cluster-xxxxxxx.ap-northeast-1.rds.amazonaws.com" at port "5432".
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES128-GCM-SHA256, bits: 128, compression: off)
pgbench_restore=> \d
              List of relations
 Schema |       Name       | Type  |  Owner
--------+------------------+-------+----------
 public | pgbench_accounts | table | postgres
(1 row)

pgbench_restore=>
```
