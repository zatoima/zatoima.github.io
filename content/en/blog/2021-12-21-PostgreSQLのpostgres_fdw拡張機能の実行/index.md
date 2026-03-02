---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Running the postgres_fdw Extension in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-extension-fdw-install
date: 2021-12-21
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

## Running postgres_fdw

### Enabling the Extension

```sql
CREATE EXTENSION postgres_fdw;
```

### Defining a Foreign Server

Create a foreign server for the `test1` database.

```sql
CREATE SERVER fdw_app FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'test1');
```

### Defining a User Mapping for the Foreign Server

```sql
CREATE USER MAPPING FOR public SERVER fdw_app OPTIONS (user 'postgres', password 'postgres');
```

### Creating a Foreign Table

Create the `t2` table as a foreign table using the `fdw_app` foreign server.

```sql
CREATE FOREIGN TABLE t2 (a integer, b text,c text, d timestamp with time zone) SERVER fdw_app;
```

For foreign tables, the type appears as `foreign table`.

```sql
postgres=> \d
                List of relations
 Schema |    Name     |     Type      |  Owner
--------+-------------+---------------+----------
 public | t1          | table         | postgres
 public | t2          | foreign table | postgres
 public | v_dblink_t1 | view          | postgres
```

You can also create foreign tables using [IMPORT FOREIGN SCHEMA](https://www.postgresql.jp/document/13/html/sql-importforeignschema.html).

### Querying

```sql
postgres=> select count(*) from t2;
   count
-----------
 100000000
(1 row)
```

## Characteristics of postgres_fdw

- Pushdown functionality
  - WHERE clauses (filtering) and ORDER BY clauses (sorting) in SQL statements are executed on the remote side
    - A clear advantage over dblink
- Supports updates
  - Does not support INSERT statements with ON CONFLICT DO UPDATE clause

## Considerations for postgres_fdw

- Transaction control
  - Care must be taken regarding the timing of COMMIT on the remote side and the transaction isolation level (see reference links for details)
- Performance
  - Tends to become slower depending on the amount of data transferred
  - The remote execution option has a default fetch_size of 100, so tuning may be necessary depending on the use case

### References

> F.33. postgres_fdw https://www.postgresql.jp/document/13/html/postgres-fdw.html
>
> PostgreSQL 9.6 の postgres_fdw について検証してみた | SIOS Tech. Lab https://tech-lab.sios.jp/archives/8641#i
>
> 外部データとの連携 ～FDWで様々なデータソースとつなぐ～｜PostgreSQLインサイド : 富士通 https://www.fujitsu.com/jp/products/software/resources/feature-stories/postgres/article-index/fdw-overview/
