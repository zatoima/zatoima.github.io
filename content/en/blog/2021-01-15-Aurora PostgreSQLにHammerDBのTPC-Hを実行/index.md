---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Running HammerDB TPC-H Against Aurora PostgreSQL"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-hammerdb-benchmark-tpc-h.html
date: 2021-01-15
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

Running TPC-H against Aurora PostgreSQL.

For TPC-C, see the following:

> Running HammerDB TPC-C Against Aurora PostgreSQL | my opinion is my own https://zatoima.github.io/aws-aurora-postgresql-hammerdb-benchmark.html

### Introduction

This uses the CLI, so I referred to the HammerDB documentation below.

> Chapter 8. Command Line Interface (CLI) https://hammerdb.com/docs/ch08.html

### Prerequisites

Assumes PostgreSQL-related libraries are already installed. If not, install them with the following:

```sh
sudo yum -y install postgresql
sudo yum -y install postgresql-contrib
```

### Download HammerDB Installer

```sh
wget https://github.com/TPC-Council/HammerDB/releases/download/v3.3/HammerDB-3.3-Linux.tar.gz
tar xvzf HammerDB-3.3-Linux.tar.gz
cd HammerDB-3.3
```

> HammerDB https://hammerdb.com/download.html

### Library Check

Verify that the PostgreSQL library check shows Success.

```
Checking database library for PostgreSQL
Success ... loaded library Pgtcl for PostgreSQL
```

```sh
[ec2-user@bastin HammerDB-3.3]$ ls -l
total 100
drwxr-xr-x  2 ec2-user ec2-user    19 Oct 18  2019 agent
drwxr-xr-x  2 ec2-user ec2-user    37 Oct 21  2019 bin
-rwxr-xr-x  1 ec2-user ec2-user 29218 Oct 16  2019 ChangeLog
drwxr-xr-x  2 ec2-user ec2-user   178 Oct 16  2019 config
-rwxr-xr-x  1 ec2-user ec2-user  7274 Oct 16  2019 hammerdb
-rwxr-xr-x  1 ec2-user ec2-user  3167 Oct 16  2019 hammerdbcli
-rwxr-xr-x  1 ec2-user ec2-user  2508 Oct 16  2019 hammerdbws
drwxr-xr-x  2 ec2-user ec2-user    39 Jul 19  2019 images
drwxr-xr-x  2 ec2-user ec2-user  4096 Oct 21  2019 include
drwxr-xr-x 21 ec2-user ec2-user  4096 Oct 21  2019 lib
-rwxr-xr-x  1 ec2-user ec2-user 34666 Jul 19  2019 license
drwxr-xr-x  2 ec2-user ec2-user  4096 Oct 16  2019 modules
-rwxr-xr-x  1 ec2-user ec2-user   116 Oct 16  2019 readme
drwxr-xr-x 10 ec2-user ec2-user   126 Jul 19  2019 src
[ec2-user@bastin HammerDB-3.3]$ ./hammerdbcli
HammerDB CLI v3.3
Copyright (C) 2003-2019 Steve Shaw
Type "help" for a list of commands
The xml is well-formed, applying configuration
hammerdb>librarycheck
Checking database library for Oracle
Error: failed to load Oratcl - can't read "env(ORACLE_HOME)": no such variable
Ensure that Oracle client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for MSSQLServer
Error: failed to load tdbc::odbc - couldn't load file "libiodbc.so": libiodbc.so: cannot open shared object file: No such file or directory
Ensure that MSSQLServer client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for Db2
Error: failed to load db2tcl - couldn't load file "/home/ec2-user/HammerDB-3.3/lib/db2tcl2.0.0/libdb2tcl.so.0.0.1": libdb2.so.1: cannot open shared object file: No such file or directory
Ensure that Db2 client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for MySQL
Error: failed to load mysqltcl - couldn't load file "/home/ec2-user/HammerDB-3.3/lib/mysqltcl-3.052/libmysqltcl3.052.so": libmysqlclient.so.21: cannot open shared object file: No such file or directory
Ensure that MySQL client libraries are installed and the location in the LD_LIBRARY_PATH environment variable
Checking database library for PostgreSQL
Success ... loaded library Pgtcl for PostgreSQL
Checking database library for Redis
Success ... loaded library redis for Redis
```

### HammerDB Parameter Configuration

##### Set Target DB to PostgreSQL

```sh
hammerdb> dbset db pg
```

##### Set Benchmark to TPC-H

```sh
hammerdb> dbset bm TPC-H
```

##### Set Target Hostname

```sh
hammerdb> diset connection pg_host aurorav1.cluster-cm678nkt5thr.ap-northeast-1.rds.amazonaws.com
```

##### Set Superuser Username and Password

```sh
hammerdb> diset tpch pg_tpch_superuser postgres
hammerdb> diset tpch pg_tpch_superuserpass postgres
```

##### Set Scale Factor

Adjust the data volume.

```sh
hammerdb> diset tpch pg_scale_fact 1
```

##### Set Number of Users for Schema Build

```sh
hammerdb> diset tpch pg_num_tpch_threads 4
```

##### Verify Settings

```sh
hammerdb>print dict
Dictionary Settings for PostgreSQL
connection {
 pg_host = aurorav1.cluster-cm678nkt5thr.ap-northeast-1.rds.amazonaws.com
 pg_port = 5432
}
tpch       {
 pg_scale_fact         = 1
 pg_tpch_superuser     = postgres
 pg_tpch_superuserpass = postgres
 pg_tpch_defaultdbase  = postgres
 pg_tpch_user          = tpch
 pg_tpch_pass          = tpch
 pg_tpch_dbase         = tpch
 pg_tpch_gpcompat      = false
 pg_tpch_gpcompress    = false
 pg_num_tpch_threads   = 4
 pg_total_querysets    = 1
 pg_raise_query_error  = false
 pg_verbose            = false
 pg_refresh_on         = false
 pg_degree_of_parallel = 2
 pg_update_sets        = 1
 pg_trickle_refresh    = 1000
 pg_refresh_verbose    = false
 pg_cloud_query        = false
 pg_rs_compat          = false
}

```

### Schema Creation

##### Create Schema and Load Test Data

This takes some time as data loading runs.

```sh
hammerdb>buildschema
Script cleared
Building 1 Warehouses(s) with 1 Virtual User
Ready to create a 1 Warehouse PostgreSQL TPC-C schema
in host xxxxxx.CLUSTER-xxxxxxxx.AP-NORTHEAST-1.RDS.AMAZONAWS.COM:5432 under user TPCC in database TPCC?
Enter yes or no: replied yes
Vuser 1 created - WAIT IDLE
RUNNING - TPC-C creation
Vuser 1:RUNNING
Vuser 1:CREATING TPCC SCHEMA
Vuser 1:CREATING DATABASE tpcc under OWNER tpcc

～omitted～
Vuser 1:GATHERING SCHEMA STATISTICS
Vuser 1:TPCC SCHEMA COMPLETE
Vuser 1:FINISHED SUCCESS
ALL VIRTUAL USERS COMPLETE
                          TPC-C Driver Script
hammerdb>
```

After setting the scale factor to 10x and logging in to the tpcc database on the PostgreSQL side after completion, you can confirm that 9 tables have been created.

```sh
postgres@aurorapgsqlv1:tpcc> \dt+
+----------+------------+--------+---------+---------+---------------+
| Schema   | Name       | Type   | Owner   | Size    | Description   |
|----------+------------+--------+---------+---------+---------------|
| public   | customer   | table  | tpcc    | 371 MB  | <null>        |
| public   | district   | table  | tpcc    | 168 kB  | <null>        |
| public   | history    | table  | tpcc    | 56 MB   | <null>        |
| public   | item       | table  | tpcc    | 21 MB   | <null>        |
| public   | new_order  | table  | tpcc    | 7864 kB | <null>        |
| public   | order_line | table  | tpcc    | 656 MB  | <null>        |
| public   | orders     | table  | tpcc    | 43 MB   | <null>        |
| public   | stock      | table  | tpcc    | 710 MB  | <null>        |
| public   | warehouse  | table  | tpcc    | 40 kB   | <null>        |
+----------+------------+--------+---------+---------+---------------+
SELECT 9
Time: 0.021s
```

##### Kill the Load Client Process

```sh
hammerdb>vudestroy
Destroying Virtual Users
Virtual Users Destroyed
vudestroy success
```

##### Load Script

```sh
hammerdb>loadscript
TPC-C Driver Script
Script loaded, Type "print script" to view
```

#### Configure and Create Test Client (Virtual Users)

```sh
hammerdb>vuset vu 4
hammerdb>vuset logtotemp 1
hammerdb>vuset showoutput 1
hammerdb>vuset unique 1
hammerdb>vuset timestamps 1
hammerdb>print vuconf
Virtual Users = 4
User Delay(ms) = 500
Repeat Delay(ms) = 500
Iterations = 1
Show Output = 1
Log Output = 1
Unique Log Name = 1
No Log Buffer = 0
Log Timestamps = 1

hammerdb>
hammerdb> vucreate
Vuser 1 created MONITOR - WAIT IDLE
Vuser 2 created - WAIT IDLE
Vuser 3 created - WAIT IDLE
Vuser 4 created - WAIT IDLE
Vuser 5 created - WAIT IDLE
Logging activated
to /tmp/hammerdb_5FADF0FE5B3F03E293835333.log
5 Virtual Users Created with Monitor VU

hammerdb>vustatus
1 = WAIT IDLE
2 = WAIT IDLE
3 = WAIT IDLE
4 = WAIT IDLE
5 = WAIT IDLE
```

### Pre-Execution Preparation

Running HammerDB in this state can take a very long time due to the following reason, so some additional steps are needed.

> HammerDBをCLIで使うなど（８）：PostgreSQLにTPC-Hを実行してみる - なからなLife https://atsuizo.hatenadiary.jp/entry/2019/09/04/090000
>
> The indexes created are different from those for MySQL!
>
> For example, the largest table in TPC-H, "LINEITEM", has a foreign key constraint referencing the PARTSUPP table as follows:
>
> ```
> CONSTRAINT lineitem_partsupp_fk FOREIGN KEY (l_partkey, l_suppkey)
>         REFERENCES public.partsupp (ps_partkey, ps_suppkey)
> ```
>
>
> In PostgreSQL:
>
> > Foreign keys must reference columns that are a primary key or form a unique constraint. This means that the referenced columns always have an index (the basis of the primary key or unique constraint). Therefore, checking whether a matching row exists in the reference is efficient. Since deleting rows from the referenced table or updating referenced rows requires a scan of the referencing table for rows matching the old value, it is usually a good idea to index the referencing columns as well. This is not always required, and there are many options for how to index, so **declaring a foreign key constraint does not automatically create an index on the referencing columns.**
> > [5.3. Constraints](https://www.postgresql.jp/document/10/html/ddl-constraints.html#DDL-CONSTRAINTS-FK)
>
> Therefore, while the PARTSUPP table's (ps_partkey, ps_suppkey) columns have a primary key constraint (and thus an index), the LINEITEM table's l_partkey, l_suppkey columns have no index.
>
> In SQL-20, LINEITEM's l_partkey, l_suppkey have a FK referencing PARTSUPP's ps_partkey, ps_suppkey, and these are used for joining. But since l_partkey, l_suppkey themselves have no index, a full scan (SeqScan) occurs.
>
> As a result, the execution cost of a subquery that joins on these foreign key columns and processes the result with an aggregate function becomes extremely large.

Therefore, before execution, log in to the tpch database as the tpch user and create the following indexes:

```
CREATE INDEX ON customer (C_NATIONKEY);
CREATE INDEX ON lineitem (L_ORDERKEY);
CREATE INDEX ON lineitem (L_SUPPKEY);
CREATE INDEX ON lineitem (L_PARTKEY,L_SUPPKEY);
CREATE INDEX ON nation (N_REGIONKEY);
CREATE INDEX ON orders (O_CUSTKEY);
CREATE INDEX ON partsupp (PS_PARTKEY);
CREATE INDEX ON partsupp (PS_SUPPKEY);
CREATE INDEX ON supplier (S_NATIONKEY);
CREATE INDEX ON lineitem (L_SHIPDATE);
CREATE INDEX ON lineitem (L_COMMITDATE);
CREATE INDEX ON lineitem (L_RECEIPTDATE);
CREATE INDEX ON orders (O_ORDERDATE);
```

### Running HammerDB

```sh
hammerdb> vurun
```

##### Execution Results

```sh
hammerdb>vurun
RUNNING - PostgreSQL TPC-H
Vuser 1:RUNNING
Vuser 1:Executing Query 21 (1 of 22)
Vuser 2:RUNNING
Vuser 2:Executing Query 6 (1 of 22)
Vuser 3:RUNNING
Vuser 3:Executing Query 8 (1 of 22)
Vuser 4:RUNNING
Vuser 4:Executing Query 5 (1 of 22)
Vuser 2:query 6 completed in 3.016 seconds
Vuser 2:Executing Query 17 (2 of 22)
Vuser 4:query 5 completed in 2.78 seconds
Vuser 4:Executing Query 21 (2 of 22)
Vuser 1:query 21 completed in 5.485 seconds
Vuser 1:Executing Query 3 (2 of 22)
Vuser 1:query 3 completed in 2.953 seconds
Vuser 1:Executing Query 18 (3 of 22)
Vuser 4:query 21 completed in 5.661 seconds
Vuser 4:Executing Query 14 (3 of 22)
Vuser 3:query 8 completed in 9.447 seconds
Vuser 3:Executing Query 5 (2 of 22)
Vuser 4:query 14 completed in 1.777 seconds
Vuser 4:Executing Query 19 (4 of 22)
Vuser 4:query 19 completed in 0.348 seconds
Vuser 4:Executing Query 15 (5 of 22)
Vuser 3:query 5 completed in 2.148 seconds
Vuser 3:Executing Query 4 (3 of 22)
Vuser 2:query 17 completed in 9.567 seconds
Vuser 2:Executing Query 14 (3 of 22)
Vuser 3:query 4 completed in 0.81 seconds
Vuser 3:Executing Query 6 (4 of 22)
Vuser 2:query 14 completed in 1.566 seconds
Vuser 2:Executing Query 16 (4 of 22)
Vuser 3:query 6 completed in 2.785 seconds
Vuser 3:Executing Query 17 (5 of 22)
Vuser 2:query 16 completed in 7.821 seconds
Vuser 2:Executing Query 19 (5 of 22)
Vuser 2:query 19 completed in 0.243 seconds
Vuser 2:Executing Query 10 (6 of 22)
Vuser 3:query 17 completed in 8.858 seconds
Vuser 3:Executing Query 7 (6 of 22)
Vuser 3:query 7 completed in 3.284 seconds
Vuser 3:Executing Query 1 (7 of 22)
Vuser 4:query 15 completed in 17.023 seconds
Vuser 4:Executing Query 17 (6 of 22)
Vuser 2:query 10 completed in 6.98 seconds
Vuser 2:Executing Query 9 (7 of 22)
Vuser 1:query 18 completed in 26.544 seconds
Vuser 1:Executing Query 5 (4 of 22)
Vuser 1:query 5 completed in 2.252 seconds
Vuser 1:Executing Query 11 (5 of 22)
Vuser 1:query 11 completed in 0.781 seconds
Vuser 1:Executing Query 7 (6 of 22)
Vuser 2:query 9 completed in 9.707 seconds
Vuser 2:Executing Query 2 (8 of 22)
Vuser 1:query 7 completed in 2.585 seconds
Vuser 1:Executing Query 6 (7 of 22)
Vuser 4:query 17 completed in 13.075 seconds
Vuser 4:Executing Query 12 (7 of 22)
Vuser 1:query 6 completed in 2.757 seconds
Vuser 1:Executing Query 20 (8 of 22)
Vuser 1:query 20 completed in 0.943 seconds
Vuser 1:Executing Query 17 (9 of 22)
Vuser 2:query 2 completed in 5.946 seconds
Vuser 2:Executing Query 15 (9 of 22)
Vuser 4:query 12 completed in 3.236 seconds
Vuser 4:Executing Query 6 (8 of 22)
Vuser 4:query 6 completed in 2.542 seconds
Vuser 4:Executing Query 4 (9 of 22)
Vuser 3:query 1 completed in 20.678 seconds
Vuser 3:Executing Query 18 (8 of 22)
Vuser 4:query 4 completed in 0.767 seconds
Vuser 4:Executing Query 9 (10 of 22)
Vuser 1:query 17 completed in 13.149 seconds
Vuser 1:Executing Query 12 (10 of 22)
Vuser 1:query 12 completed in 3.912 seconds
Vuser 1:Executing Query 16 (11 of 22)
Vuser 4:query 9 completed in 13.335 seconds
Vuser 4:Executing Query 8 (11 of 22)
Vuser 4:query 8 completed in 1.575 seconds
Vuser 4:Executing Query 16 (12 of 22)
Vuser 2:query 15 completed in 18.843 seconds
Vuser 2:Executing Query 8 (10 of 22)
Vuser 2:query 8 completed in 0.921 seconds
Vuser 2:Executing Query 5 (11 of 22)
Vuser 2:query 5 completed in 1.495 seconds
Vuser 2:Executing Query 22 (12 of 22)
Vuser 2:query 22 completed in 0.785 seconds
Vuser 2:Executing Query 12 (13 of 22)
Vuser 1:query 16 completed in 9.12 seconds
Vuser 1:Executing Query 15 (12 of 22)
Vuser 2:query 12 completed in 3.083 seconds
Vuser 2:Executing Query 7 (14 of 22)
Vuser 4:query 16 completed in 8.094 seconds
Vuser 4:Executing Query 11 (13 of 22)
Vuser 4:query 11 completed in 0.576 seconds
Vuser 4:Executing Query 2 (14 of 22)
Vuser 2:query 7 completed in 2.229 seconds
Vuser 2:Executing Query 13 (15 of 22)
Vuser 3:query 18 completed in 26.223 seconds
Vuser 3:Executing Query 22 (9 of 22)
Vuser 3:query 22 completed in 0.718 seconds
Vuser 3:Executing Query 14 (10 of 22)
Vuser 4:query 2 completed in 4.166 seconds
Vuser 4:Executing Query 10 (15 of 22)
Vuser 3:query 14 completed in 1.276 seconds
Vuser 3:Executing Query 9 (11 of 22)
Vuser 2:query 13 completed in 6.832 seconds
Vuser 2:Executing Query 18 (16 of 22)
Vuser 4:query 10 completed in 7.385 seconds
Vuser 4:Executing Query 18 (16 of 22)
Vuser 3:query 9 completed in 11.277 seconds
Vuser 3:Executing Query 10 (12 of 22)
Vuser 1:query 15 completed in 18.736 seconds
Vuser 1:Executing Query 13 (13 of 22)
Vuser 3:query 10 completed in 7.917 seconds
Vuser 3:Executing Query 15 (13 of 22)
Vuser 1:query 13 completed in 13.717 seconds
Vuser 1:Executing Query 10 (14 of 22)
Vuser 1:query 10 completed in 7.634 seconds
Vuser 1:Executing Query 2 (15 of 22)
Vuser 2:query 18 completed in 33.341 seconds
Vuser 2:Executing Query 1 (17 of 22)
Vuser 1:query 2 completed in 4.614 seconds
Vuser 1:Executing Query 8 (16 of 22)
Vuser 1:query 8 completed in 1.044 seconds
Vuser 1:Executing Query 14 (17 of 22)
Vuser 4:query 18 completed in 33.215 seconds
Vuser 4:Executing Query 1 (17 of 22)
Vuser 1:query 14 completed in 1.698 seconds
Vuser 1:Executing Query 19 (18 of 22)
Vuser 1:query 19 completed in 0.303 seconds
Vuser 1:Executing Query 9 (19 of 22)
Vuser 3:query 15 completed in 26.017 seconds
Vuser 3:Executing Query 11 (14 of 22)
Vuser 3:query 11 completed in 1.312 seconds
Vuser 3:Executing Query 20 (15 of 22)
Vuser 3:query 20 completed in 1.176 seconds
Vuser 3:Executing Query 2 (16 of 22)
Vuser 1:query 9 completed in 11.02 seconds
Vuser 1:Executing Query 22 (20 of 22)
Vuser 1:query 22 completed in 1.261 seconds
Vuser 1:Executing Query 1 (21 of 22)
Vuser 3:query 2 completed in 6.488 seconds
Vuser 3:Executing Query 21 (17 of 22)
Vuser 3:query 21 completed in 9.238 seconds
Vuser 3:Executing Query 19 (18 of 22)
Vuser 3:query 19 completed in 0.417 seconds
Vuser 3:Executing Query 13 (19 of 22)
Vuser 2:query 1 completed in 28.195 seconds
Vuser 2:Executing Query 4 (18 of 22)
Vuser 2:query 4 completed in 1.517 seconds
Vuser 2:Executing Query 20 (19 of 22)
Vuser 2:query 20 completed in 1.775 seconds
Vuser 2:Executing Query 3 (20 of 22)
Vuser 4:query 1 completed in 27.942 seconds
Vuser 4:Executing Query 13 (18 of 22)
Vuser 2:query 3 completed in 5.823 seconds
Vuser 2:Executing Query 11 (21 of 22)
Vuser 2:query 11 completed in 0.55 seconds
Vuser 2:Executing Query 21 (22 of 22)
Vuser 3:query 13 completed in 10.16 seconds
Vuser 3:Executing Query 16 (20 of 22)
Vuser 4:query 13 completed in 9.648 seconds
Vuser 4:Executing Query 7 (19 of 22)
Vuser 4:query 7 completed in 2.796 seconds
Vuser 4:Executing Query 22 (20 of 22)
Vuser 2:query 21 completed in 7.339 seconds
Vuser 2:Completed 1 query set(s) in 157 seconds
Vuser 2:FINISHED SUCCESS
Vuser 1:query 1 completed in 27.607 seconds
Vuser 1:Executing Query 4 (22 of 22)
Vuser 4:query 22 completed in 0.616 seconds
Vuser 4:Executing Query 3 (21 of 22)
Vuser 1:query 4 completed in 0.512 seconds
Vuser 1:Completed 1 query set(s) in 159 seconds
Vuser 1:FINISHED SUCCESS
Vuser 3:query 16 completed in 8.796 seconds
Vuser 3:Executing Query 12 (21 of 22)
Vuser 4:query 3 completed in 1.766 seconds
Vuser 4:Executing Query 20 (22 of 22)
Vuser 4:query 20 completed in 0.292 seconds
Vuser 4:Completed 1 query set(s) in 158 seconds
Vuser 4:FINISHED SUCCESS
Vuser 3:query 12 completed in 1.208 seconds
Vuser 3:Executing Query 3 (22 of 22)
Vuser 3:query 3 completed in 0.941 seconds
Vuser 3:Completed 1 query set(s) in 161 seconds
Vuser 3:FINISHED SUCCESS
ALL VIRTUAL USERS COMPLETE
                          TPC-H Driver Script
hammerdb>

```

### Cleanup

```sh
hammerdb>vucomplete
true
hammerdb>vudestroy
Destroying Virtual Users
Virtual Users Destroyed
vudestroy success

hammerdb>clearscript
Script cleared
```

### References

> HammerDBをCLIで使うなど（８）：PostgreSQLにTPC-Hを実行してみる - なからなLife https://atsuizo.hatenadiary.jp/entry/2019/09/04/090000
>
> Chapter 8. Command Line Interface (CLI) https://hammerdb.com/docs/ch08.html
