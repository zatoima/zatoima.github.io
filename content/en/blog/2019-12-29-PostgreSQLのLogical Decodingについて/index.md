---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "About PostgreSQL Logical Decoding"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-logical-decoding.html
date: 2019-12-29
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

#### Introduction

Logical Decoding allows you to extract and view historical information about database activity recorded in the WAL. I understand it as a feature similar to Oracle Database's LogMiner. Functionally, LogMiner can retrieve more detailed content. It appears that PostgreSQL's Logical Decoding cannot capture DDL content. Since Logical Decoding was implemented in PostgreSQL 9.4, there's hope for future improvements.

Note that the CDC used in logical replication is also implemented based on this feature.

The manual is here:

> https://www.postgresql.jp/document/10/html/logicaldecoding.htm
>
> Chapter 48. Logical Decoding

#### Configuration

##### Modify postgresql.conf

Set wal_level to "logical" and set max_replication_slots to "1" or more. In PostgreSQL 10, max_replication_slots defaults to 10, so no change is needed there. Changing wal_level from the default to logical will naturally increase WAL generation. A restart is required when changing wal_level.

```text
#postgresql.conf
wal_level = logical
max_replication_slots = 10
```

##### Plugin Installation

The output format differs by Logical Decoding plugin. A list of decode plugins is available at:

> https://wiki.postgresql.org/wiki/Logical_Decoding_Plugins
>
> Logical Decoding Plugins

Here I want to install `test_decoding`, which is included in contrib from the start, and `decoder_raw`, which requires additional installation but provides SQL format-based output.

##### Installing the test_decoding Plugin

Build and install from the contrib directory in the source root:

```sh
$ cd contrib/test_decoding
$ make
# make install
```

Or install via yum. Use this if you installed via rpm package:

```sh
sudo yum install postgresql10-contrib
```

##### Installing the decoder_raw Plugin

Clone from GitHub and install via make:

> https://github.com/michaelpq/pg_plugins/tree/master/decoder_raw

```sh
[root@postdb tmp]# pwd
/tmp
    [root@postdb tmp]# git clone https://github.com/michaelpq/pg_plugins.git
Cloning into 'pg_plugins'...
remote: Enumerating objects: 105, done.
remote: Counting objects: 100% (105/105), done.
remote: Compressing objects: 100% (50/50), done.
remote: Total 1760 (delta 54), reused 90 (delta 47), pack-reused 1655
Receiving objects: 100% (1760/1760), 345.58 KiB | 716.00 KiB/s, done.
Resolving deltas: 100% (1125/1125), done.
[root@postdb tmp]# cd /tmp/pg_plugins/decoder_raw
[root@postdb decoder_raw]#
[root@postdb decoder_raw]# export PATH=$PATH:/usr/pgsql-10/bin
[root@postdb decoder_raw]# make install
gcc -Wall -Wmissing-prototypes ...
...
/bin/mkdir -p '/usr/pgsql-10/lib'
/bin/install -c -m 755  decoder_raw.so '/usr/pgsql-10/lib/'
[root@postdb decoder_raw]#
[root@postdb decoder_raw]# echo $?
0
[root@postdb decoder_raw]#
```

After make install, the related library is placed under /usr/pgsql-10/lib:

```sh
-bash-4.2$ pwd
/usr/pgsql-10/lib
-bash-4.2$ ls -l decoder_raw*
-rwxr-xr-x 1 root root 75304 Dec 28 11:16 decoder_raw.so
-bash-4.2$
```

#### Logical Decoding Related Functions

There aren't many related functions. These three should be sufficient.

- ##### pg_create_logical_replication_slot

  ```sql
  pg_create_logical_replication_slot(slot_name name, plugin name [, temporary boolean])
  ```

  - Creates a logical (decode) replication slot.

    First argument: specify slot_name

    Second argument: specify plugin name

    Third argument: if set to true, the slot is limited to the current session (optional)

- ##### pg_drop_replication_slot

  ```sql
  pg_drop_replication_slot(slot_name name)
  ```

  - Drops a logical (decode) replication slot.

    First argument: specify slot_name

- ##### pg_logical_slot_get_changes

  ```sql
  pg_logical_slot_get_changes(slot_name name, upto_lsn pg_lsn, upto_nchanges int, VARIADIC options text[])
  ```

- View change history

  First argument: specify slot_name

  Second argument: specify the LSN to check up to

  Third argument: number of rows to output

  Fourth argument: specify output plugin options as key-value pairs

#### 1.) Trying Logical Decoding (using the **test_decoding** plugin)

##### Create Replication Slot

Execute pg_create_logical_replication_slot in the database where you want to perform Logical Decoding to create a replication slot.

```sql
postgres=# SELECT * FROM pg_create_logical_replication_slot('decodeslot1', 'test_decoding');

slot_name  |    lsn
-------------+-----------
 decodeslot1 | 0/2EFFFA0
(1 row)
postgres=# \x
Expanded display is on.
postgres=#
postgres=# SELECT slot_name, plugin, slot_type, database, active, restart_lsn, confirmed_flush_lsn FROM pg_replication_slots;
-[ RECORD 1 ]-------+--------------
slot_name           | decodeslot1
plugin              | test_decoding
slot_type           | logical
database            | postgres
active              | f
restart_lsn         | 0/2EFFF68
confirmed_flush_lsn | 0/2EFFFA0
```

##### Check Change History

Since no operations have been performed yet, nothing is output:

```sql
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
(0 rows)
```

##### Perform DDL on a Table

DDL does not produce detailed content output. However, BEGIN and COMMIT are output:

```sql
postgres=# CREATE TABLE data(id serial primary key, data text);
CREATE TABLE
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
    lsn    | xid  |    data
-----------+------+-------------
 0/2F20128 | 1051 | BEGIN 1051
 0/2F28278 | 1051 | COMMIT 1051
(4 rows)
```

##### Perform DML on a Table

```sql
postgres=# BEGIN;
BEGIN
postgres=# INSERT INTO data(data) VALUES('1');
INSERT 0 1
postgres=# INSERT INTO data(data) VALUES('2');
INSERT 0 1
postgres=# COMMIT;
COMMIT
postgres=#
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
    lsn    | xid  |                          data
-----------+------+---------------------------------------------------------
 0/2F282F0 | 1052 | BEGIN 1052
 0/2F28358 | 1052 | table public.data: INSERT: id[integer]:1 data[text]:'1'
 0/2F28460 | 1052 | table public.data: INSERT: id[integer]:2 data[text]:'2'
 0/2F28510 | 1052 | COMMIT 1052
(4 rows)

postgres=#
postgres=#
postgres=# INSERT INTO data(data) VALUES('3');
INSERT 0 1
postgres=#
postgres=# SELECT * FROM pg_logical_slot_peek_changes('decodeslot1', NULL, NULL);
    lsn    | xid  |                          data
-----------+------+---------------------------------------------------------
 0/2F28588 | 1053 | BEGIN 1053
 0/2F28588 | 1053 | table public.data: INSERT: id[integer]:3 data[text]:'3'
 0/2F28638 | 1053 | COMMIT 1053
(3 rows)
```

##### Drop the Replication Slot

```sql
SELECT * FROM pg_drop_replication_slot('decodeslot1');
```

#### 2.) Trying Logical Decoding (using the **decoder_raw** plugin)

Execute pg_create_logical_replication_slot in the database where you want to perform Logical Decoding to create a replication slot.

##### Create Replication Slot

```sql
postgres=# SELECT * FROM pg_create_logical_replication_slot('decodeslot1', 'decoder_raw');
  slot_name  |    lsn
-------------+-----------
 decodeslot1 | 0/2F286A8
(1 row)

postgres=# \x
Expanded display is on.
postgres=# SELECT slot_name, plugin, slot_type, database, active, restart_lsn, confirmed_flush_lsn FROM pg_replication_slots;
-[ RECORD 1 ]-------+------------
slot_name           | decodeslot1
plugin              | decoder_raw
slot_type           | logical
database            | postgres
active              | f
restart_lsn         | 0/2F28670
confirmed_flush_lsn | 0/2F286A8
```

##### Check Change History

Since no operations have been performed yet, nothing is output:

```sql
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
 lsn | xid | data
-----+-----+------
(0 rows)
```

##### Perform DDL on a Table

DDL does not produce content output. Unlike test_decoding, BEGIN and COMMIT are also not output:

```sql
postgres=# CREATE TABLE data(id serial primary key, data text);
CREATE TABLE
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
 lsn | xid | data
-----+-----+------
(0 rows)
```

##### Perform DML on a Table

```sql
postgres=# BEGIN;
BEGIN
postgres=# INSERT INTO data(data) VALUES('1');
INSERT 0 1
postgres=# INSERT INTO data(data) VALUES('2');
INSERT 0 1
postgres=# COMMIT;
COMMIT
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
    lsn    | xid  |                        data
-----------+------+-----------------------------------------------------
 0/2F554B0 | 1058 | INSERT INTO public.data (id, data) VALUES (1, '1');
 0/2F55580 | 1058 | INSERT INTO public.data (id, data) VALUES (2, '2');
(2 rows)

postgres=# INSERT INTO data(data) VALUES('3');
INSERT 0 1
postgres=# SELECT * FROM pg_logical_slot_peek_changes('decodeslot1', NULL, NULL);
    lsn    | xid  |                        data
-----------+------+-----------------------------------------------------
 0/2F55630 | 1059 | INSERT INTO public.data (id, data) VALUES (3, '3');
(1 row)
```

##### Drop the Replication Slot

```sql
SELECT * FROM pg_drop_replication_slot('decodeslot1');
```



