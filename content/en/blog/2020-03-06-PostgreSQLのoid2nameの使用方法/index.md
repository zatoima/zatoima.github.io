---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Use PostgreSQL's oid2name"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-how-to-use-oid2name
date: 2020-03-06
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



An object identifier (oid) is an ID that PostgreSQL uses internally to uniquely identify various objects stored in the database (tables, indexes, functions, operators, data type definitions, and more).

> 8.18. Object Identifier Types https://www.postgresql.jp/document/10/html/datatype-oid.html

This is a memo on how to use oid2name, which is used to view oids from the OS side.

### Display Help

***

```sh
-bash-4.2$ oid2name -h
oid2name helps examining the file structure used by PostgreSQL.

Usage:
  oid2name [OPTION]...

Options:
  -d DBNAME      database to connect to
  -f FILENODE    show info for table with given file node
  -H HOSTNAME    database server host or socket directory
  -i             show indexes and sequences too
  -o OID         show info for table with given OID
  -p PORT        database server port number
  -q             quiet (don't show headers)
  -s             show all tablespaces
  -S             show system objects too
  -t TABLE       show info for named table
  -U NAME        connect as specified database user
  -V, --version  output version information, then exit
  -x             extended (show additional columns)
  -?, --help     show this help, then exit

The default action is to show all database OIDs.

Report bugs to <pgsql-bugs@postgresql.org>.
```

### Run Without Arguments

***

```sh
-bash-4.2$ oid2name
All databases:
    Oid  Database Name  Tablespace
----------------------------------
  16456        pgbench  pg_default
  16392         pgtest  pg_default
  13865       postgres  pg_default
  13864      template0  pg_default
      1      template1  pg_default
```

### Run Per Tablespace

***

```sh
-bash-4.2$ oid2name -s
All tablespaces:
   Oid  Tablespace Name
-----------------------
  1663       pg_default
  1664        pg_global
```

### Run for a Specific Database

***

```sh
-bash-4.2$ oid2name -d pgbench
From database "pgbench":
  Filenode        Table Name
----------------------------
     16469  pgbench_accounts
     16466  pgbench_branches
     16479   pgbench_history
     16460   pgbench_tellers
```

### Also Display Indexes

***

```sh
-bash-4.2$ oid2name -d pgbench -i
From database "pgbench":
  Filenode             Table Name
---------------------------------
     16469       pgbench_accounts
     16474  pgbench_accounts_pkey
     16466       pgbench_branches
     16470  pgbench_branches_pkey
     16479        pgbench_history
     16460        pgbench_tellers
     16472   pgbench_tellers_pkey
```

### Specify a Specific Table in a Specific Database

***

```sh
-bash-4.2$ oid2name -d pgbench -t pgbench_accounts
From database "pgbench":
  Filenode        Table Name
----------------------------
     16469  pgbench_accounts
```




