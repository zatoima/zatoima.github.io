---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Using PostgreSQL's dblink Extension: Execution and Caveats"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-extension-dblink-install-and-causion
date: 2021-12-19
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

This is about dblink, not postgres_fdw. The environment used is Aurora PostgreSQL.

> dblink https://www.postgresql.jp/document/13/html/contrib-dblink-function.html

## Running dblink

### Installing dblink

```sql
postgres=> \dx
                 List of installed extensions
  Name   | Version |   Schema   |         Description
---------+---------+------------+------------------------------
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(1 row)

postgres=> create extension dblink;
CREATE EXTENSION
postgres=> \dx
                                 List of installed extensions
  Name   | Version |   Schema   |                         Description
---------+---------+------------+--------------------------------------------------------------
 dblink  | 1.2     | public     | connect to other PostgreSQL databases from within a database
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(2 rows)

postgres=>
```

### Preparation: Creating a Database and Table

We will use dblink to retrieve data from table t1 in the test1 database from another database. Here we create the database and table for that purpose.

```sql
create database test1;
\c test1;
create table t1(a numeric primary key, b varchar(30));
insert into t1 values(1,'this data is at test1 database');
```

### Method 1: Connecting by Creating a Named Connection

#### Creating a Connection

```sql
postgres=> select dblink_connect('dblink-test1','dbname=test1 user=postgres password=postgres');
 dblink_connect
----------------
 OK
(1 row)
```

#### Querying

When querying, you need to specify the data types of the remote table's columns.

```sql
postgres=> select * from dblink('dblink-test1','select a,b from t1') as t1(a numeric, b varchar(30)) ;
 a |               b
---+--------------------------------
 1 | this data is at test1 database
(1 row)
```

Without the data types, you'll get the following error:

```sql
postgres=> select * from dblink('dblink-test1','select a,b from t1');
ERROR:  a column definition list is required for functions returning "record"
LINE 1: select * from dblink('dblink-test1','select a,b from t1');
```

#### Disconnecting

```sql
postgres=> select dblink_disconnect('dblink-test1');
 dblink_disconnect
-------------------
 OK
(1 row)
```

After disconnecting, queries will naturally result in an error:

```sql
postgres=> select * from dblink('dblink-test1','select a,b from t1') as t1(a numeric, b varchar(30)) ;
ERROR:  password is required
DETAIL:  Non-superusers must provide a password in the connection string.
postgres=>
```

### Method 2: Connecting Without Creating a Named Connection

```sql
postgres=> select * from dblink('dbname=test1 user=postgres password=postgres','select a,b from t1') as t1(a numeric, b varchar(30)) ;
 a |               b
---+--------------------------------
 1 | this data is at test1 database
(1 row)
```

## Caveats

- Unique dblink SQL syntax

  - As described above, you need to specify the data types for each column of the remote table. The documentation suggests using views as a convenient workaround.

  > https://www.postgresql.jp/document/13/html/contrib-dblink-function.html
  >
  > A convenient way to use `dblink` with predetermined queries is to create a view. This allows the column type information to be buried in the view, instead of having to spell it out in every query. For example:
  >
  > ```sql
  > CREATE VIEW myremote_pg_proc AS
  > SELECT *
  >  FROM dblink('dbname=postgres options=-csearch_path=',
  >              'select proname, prosrc from pg_proc')
  >  AS t1(proname name, prosrc text);
  >
  > SELECT * FROM myremote_pg_proc WHERE proname LIKE 'bytea%';
  > ```

- When joining remote tables with local tables, all data from the remote table is transferred locally before the join processing or WHERE clause filtering is applied. Depending on the table, this means transferring a large volume of data, resulting in an inefficient execution plan. Even if indexes exist on the remote table, all rows are fetched regardless. This may be manageable for communication within the same server, but when communicating over a network, bandwidth becomes a concern. Even within the same server, it can become a bottleneck depending on the volume of data transferred. Simply fetching all rows is inherently costly.

  In the example below, t1 is a local table and t2 is a remote table. Although we specify t2.a=10 and there is an index on that column, ideally only one row should be fetched, but the execution plan does not work that way. The execution time is also extremely long.

  ```sql
  postgres=> explain analyze select t1.d from dblink('dbname=test1 user=postgres password=postgres','select a from t2') as t2(a integer), t1 where t1.a=t2.a and t2.a=10;
                                                        QUERY PLAN
  -----------------------------------------------------------------------------------------------------------------------
   Nested Loop  (cost=0.00..13.68 rows=5 width=8) (actual time=50611.640..58457.467 rows=1 loops=1)
     ->  Seq Scan on t1  (cost=0.00..1.12 rows=1 width=12) (actual time=1.910..1.914 rows=1 loops=1)
           Filter: (a = 10)
           Rows Removed by Filter: 9
     ->  Function Scan on dblink t2  (cost=0.00..12.50 rows=5 width=4) (actual time=50609.726..58455.547 rows=1 loops=1)
           Filter: (a = 10)
           Rows Removed by Filter: 99999999
   Planning time: 41.712 ms
   Execution time: 58712.667 ms
  (9 rows)
  ```

- Queries via dblink are treated as separate transactions, so to ensure consistency with the current transaction, you need to consider using [two-phase commit](http://www.postgresql.jp/document/current/html/sql-prepare-transaction.html).

## Conclusion

For database link functionality, it's better to use postgres_fdw, which is considered the successor.

> https://www.postgresql.jp/document/13/html/postgres-fdw.html
>
> The functionality of this module substantially overlaps with that of the older [dblink](https://www.postgresql.jp/document/13/html/dblink.html) module. However, `postgres_fdw` provides more transparent and standards-compliant syntax for accessing remote tables, and can give better performance in many cases.

### References

> dblink https://www.postgresql.jp/document/13/html/contrib-dblink-function.html
>
> dblink | Let's POSTGRES https://lets.postgresql.jp/documents/technical/contrib/dblink
>
> PostgreSQL9.3 New Features Verification Vol.2 | Ashisuto https://www.ashisuto.co.jp/corporate/column/technical-column/detail/1198469_2274.html
