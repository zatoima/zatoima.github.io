---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Enabling Extended VARCHAR2 Type in Oracle 19c"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-19c-extended-varchar2.html
date: 2021-02-12
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

# Commands

Put the DB in upgrade mode.

```
shutdown immediate
startup upgrade
select status from v$instance;
```

Change initialization parameters:

```
ALTER SYSTEM SET max_string_size=extended SCOPE=SPFILE;
```

Execute utl32k.sql:

```
@?/rdbms/admin/utl32k.sql
```

Since this is a multitenant environment, also execute for PDB$SEED:

```
alter session set container=PDB$SEED;
@?/rdbms/admin/utl32k.sql
```

Stop and start the DB:

```
shutdown immediate
startup
show parameters max_string_size
```

# Log

```

SQL> shutdown immediate
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup upgrade
ORACLE instance started.

Total System Global Area 2415918568 bytes
Fixed Size		    9137640 bytes
Variable Size		  754974720 bytes
Database Buffers	 1644167168 bytes
Redo Buffers		    7639040 bytes
Database mounted.
Database opened.

SQL> select status from v$instance;

STATUS
------------------------------------
OPEN MIGRATE

SQL> show con_name

CON_NAME
------------------------------
CDB$ROOT


SQL> ALTER SYSTEM SET max_string_size=extended SCOPE=SPFILE;

System altered.


SQL> @?/rdbms/admin/utl32k.sql

Session altered.


Session altered.

DOC>#######################################################################
DOC>#######################################################################
DOC>   The following statement will cause an "ORA-01722: invalid number"
DOC>   error if the database has not been opened for UPGRADE.
DOC>
DOC>   Perform a "SHUTDOWN ABORT"  and
DOC>   restart using UPGRADE.
DOC>#######################################################################
DOC>#######################################################################
DOC>#

no rows selected

DOC>#######################################################################
DOC>#######################################################################
DOC>   The following statement will cause an "ORA-01722: invalid number"
DOC>   error if the database does not have compatible >= 12.0.0
DOC>
DOC>   Set compatible >= 12.0.0 and retry.
DOC>#######################################################################
DOC>#######################################################################
DOC>#

PL/SQL procedure successfully completed.


Session altered.


0 rows updated.


Commit complete.


System altered.


PL/SQL procedure successfully completed.


Commit complete.


System altered.


Session altered.


Session altered.


Table created.


Table created.


Table created.


Table truncated.


0 rows created.


PL/SQL procedure successfully completed.


STARTTIME
--------------------------------------------------------------------------------
02/10/2021 14:52:52.619389000


PL/SQL procedure successfully completed.

No errors.

PL/SQL procedure successfully completed.


Session altered.


Session altered.


0 rows created.


no rows selected


no rows selected

DOC>#######################################################################
DOC>#######################################################################
DOC>   The following statement will cause an "ORA-01722: invalid number"
DOC>   error if we encountered an error while modifying a column to
DOC>   account for data type length change as a result of enabling or
DOC>   disabling 32k types.
DOC>
DOC>   Contact Oracle support for assistance.
DOC>#######################################################################
DOC>#######################################################################
DOC>#

PL/SQL procedure successfully completed.


PL/SQL procedure successfully completed.


Commit complete.


Package altered.


Package altered.


Session altered.
SQL> alter session set container=PDB$SEED;

Session altered.

SQL>
SQL> @?/rdbms/admin/utl32k.sql

Session altered.

～omitted～

SQL> shutdown immediate

Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> SQL>
SQL>
SQL>
SQL> startup
ORACLE instance started.

Total System Global Area 2415918568 bytes
Fixed Size		    9137640 bytes
Variable Size		  754974720 bytes
Database Buffers	 1644167168 bytes
Redo Buffers		    7639040 bytes
Database mounted.
Database opened.
SQL>
SQL> show parameters max_string_size

NAME				     TYPE
------------------------------------ ---------------------------------
VALUE
------------------------------
max_string_size 		     string
EXTENDED
SQL>

```
