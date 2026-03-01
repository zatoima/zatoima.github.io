---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle 19cで拡張VARCHAR2型を導入"
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

# コマンド

DBをupgradeモードとする。

```
shutdown immediate
startup upgrade
select status from v$instance;
```

初期化パラメータの変更

```
ALTER SYSTEM SET max_string_size=extended SCOPE=SPFILE;
```

utl32k.sqlの実行

```
@?/rdbms/admin/utl32k.sql
```

マルチテナント環境なので、PDB$SEEDにも実行

```
alter session set container=PDB$SEED;
@?/rdbms/admin/utl32k.sql
```

DB停止、起動

```
shutdown immediate
startup
show parameters max_string_size
```

# ログ

```

SQL> shutdown immediate
データベースがクローズされました。
データベースがディスマウントされました。
ORACLEインスタンスがシャットダウンされました。
SQL> startup upgrade
ORACLEインスタンスが起動しました。

Total System Global Area 2415918568 bytes
Fixed Size		    9137640 bytes
Variable Size		  754974720 bytes
Database Buffers	 1644167168 bytes
Redo Buffers		    7639040 bytes
データベースがマウントされました。
データベースがオープンされました。

SQL> select status from v$instance;

STATUS
------------------------------------
OPEN MIGRATE

SQL> show con_name

CON_NAME
------------------------------
CDB$ROOT


SQL> ALTER SYSTEM SET max_string_size=extended SCOPE=SPFILE;

システムが変更されました。


SQL> @?/rdbms/admin/utl32k.sql

セッションが変更されました。


セッションが変更されました。

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

レコードが選択されませんでした。

DOC>#######################################################################
DOC>#######################################################################
DOC>   The following statement will cause an "ORA-01722: invalid number"
DOC>   error if the database does not have compatible >= 12.0.0
DOC>
DOC>   Set compatible >= 12.0.0 and retry.
DOC>#######################################################################
DOC>#######################################################################
DOC>#

PL/SQLプロシージャが正常に完了しました。


セッションが変更されました。


0行が更新されました。


コミットが完了しました。


システムが変更されました。


PL/SQLプロシージャが正常に完了しました。


コミットが完了しました。


システムが変更されました。


セッションが変更されました。


セッションが変更されました。


表が作成されました。


表が作成されました。


表が作成されました。


表が切り捨てられました。


0行が作成されました。


PL/SQLプロシージャが正常に完了しました。


STARTTIME
--------------------------------------------------------------------------------
02/10/2021 14:52:52.619389000


PL/SQLプロシージャが正常に完了しました。

エラーはありません。

PL/SQLプロシージャが正常に完了しました。


セッションが変更されました。


セッションが変更されました。


0行が作成されました。


レコードが選択されませんでした。


レコードが選択されませんでした。

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

PL/SQLプロシージャが正常に完了しました。


PL/SQLプロシージャが正常に完了しました。


コミットが完了しました。


パッケージが変更されました。


パッケージが変更されました。


セッションが変更されました。
SQL> alter session set container=PDB$SEED;

セッションが変更されました。

SQL> 
SQL> @?/rdbms/admin/utl32k.sql

セッションが変更されました。

～中略～

SQL> shutdown immediate

データベースがクローズされました。
データベースがディスマウントされました。
ORACLEインスタンスがシャットダウンされました。
SQL> SQL> 
SQL> 
SQL> 
SQL> startup
ORACLEインスタンスが起動しました。

Total System Global Area 2415918568 bytes
Fixed Size		    9137640 bytes
Variable Size		  754974720 bytes
Database Buffers	 1644167168 bytes
Redo Buffers		    7639040 bytes
データベースがマウントされました。
データベースがオープンされました。
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

