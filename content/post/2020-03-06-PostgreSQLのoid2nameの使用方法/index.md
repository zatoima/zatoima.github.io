---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのoid2nameの使用方法"
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



オブジェクト識別子(oid)とは、PostgreSQLがDB内部に格納している様々なオブジェクト(テーブルやインデックス、関数、演算子、データ型定義などなど)を一意に識別するためのID。

> 8.18. オブジェクト識別子データ型 https://www.postgresql.jp/document/10/html/datatype-oid.html

oidをOS側から見たい時に使用するoid2nameの使い方メモ。

### ヘルプ表示

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

### 引数無しで実行

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

### テーブルスペース単位で実行

***

```sh
-bash-4.2$ oid2name -s
All tablespaces:
   Oid  Tablespace Name
-----------------------
  1663       pg_default
  1664        pg_global
```

### 特定データベースを指定して実行

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

### インデックスも追加で表示

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

### 特定データベースの特定テーブルを指定

***

```sh
-bash-4.2$ oid2name -d pgbench -t pgbench_accounts
From database "pgbench":
  Filenode        Table Name
----------------------------
     16469  pgbench_accounts
```




