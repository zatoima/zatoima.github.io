---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Debug対応のPostgreSQL10をソースコードからビルドしてgdbを使用する"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-gdb-postgresql-install.html
date: 2020-04-03
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



PostgreSQL10.7を前提としています。

### 事前確認

#### GNU makeのバージョン

3.80以上であることを確認

```sh
make --version
```

#### gccのインストール

```sh
sudo yum -y install gcc
```

#### readline-develパッケージ

```sh
sudo yum -y install readline-devel
```

#### zlib-develパッケージ

```sh
sudo yum -y install zlib-devel
```

#### OSユーザ作成

```sh
groupadd -g 1101 postgres
useradd -u 1101 -g postgres -G postgres -d /var/lib/pgsql postgres
passwd postgres
```

#### 権限変更

```sh
chown -R postgres:postgres /var/lib/pgsql
chmod -R 755 /var/lib/pgsql
```

環境変数に下記を追加

```sh
export PGDATA=/var/lib/pgsql/10/data
```

### PostgreSQLインストール

#### ソースダウンロード&解凍

```sh
su - postgres
wget https://ftp.postgresql.org/pub/source/v10.7/postgresql-10.7.tar.gz
tar xvfz postgresql-10.7.tar.gz
```

#### ビルド

```sh
cd $HOME/postgresql-10.7
./configure  --enable-debug --prefix=/var/lib/pgsql/10
make
```

`All of PostgreSQL successfully made. Ready to install.`が出力される。

#### インストール

```sh
make install
```

`PostgreSQL installation complete.`が出力される。

### PostgreSQL初期化

#### DBの初期化

```sh
mkdir -p /var/lib/pgsql/10/data
export PGDATA=/var/lib/pgsql/10/data
whoami
$HOME/10/bin/initdb --pgdata=$PGDATA
$HOME/10/bin/pg_ctl start
$HOME/10/bin/pg_ctl status
```

#### 接続、バージョン確認

環境変数やPATHの設定を行い、接続を行う。

```sh
[postgres@postpub ~]$ psql
psql (10.7)
Type "help" for help.

postgres=# select version();
                                                version                                     
            
--------------------------------------------------------------------------------------------
------------
 PostgreSQL 10.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1
-6), 64-bit
(1 row)
```

#### gdb

本題のgdbを使ってみる。まずは接続中のPIDを確認する。

```sh
postgres=# select pg_backend_pid();
 pg_backend_pid 
----------------
          12072
(1 row)
```

当然、psコマンドからも確認が出来る。

```sh
[ec2-user@postpub ~]$ ps -ef | grep 12072 | grep -v grep
postgres 12072 11888  0 03:42 ?        00:00:00 postgres: postgres postgres [local] idle
```

#### gdbのインストール

```sh
sudo yum -y install gdb
```

```sh
[ec2-user@postpub ~]$ gdb -version
GNU gdb (GDB) Red Hat Enterprise Linux 8.0.1-30.amzn2.0.3
Copyright (C) 2017 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word".
```

プロセス番号をattachする。

```sh
gdb /var/lib/pgsql/10/bin/postgres 12072
```

```sh
[postgres@postpub bin]$ gdb /var/lib/pgsql/10/bin/postgres 12072
GNU gdb (GDB) Red Hat Enterprise Linux 8.0.1-30.amzn2.0.3
Copyright (C) 2017 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /var/lib/pgsql/10/bin/postgres...done.
Attaching to program: /var/lib/pgsql/10/bin/postgres, process 12072
Reading symbols from /lib64/libpthread.so.0...(no debugging symbols found)...done.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
Reading symbols from /lib64/librt.so.1...(no debugging symbols found)...done.
Reading symbols from /lib64/libdl.so.2...(no debugging symbols found)...done.
Reading symbols from /lib64/libm.so.6...(no debugging symbols found)...done.
Reading symbols from /lib64/libc.so.6...(no debugging symbols found)...done.
Reading symbols from /lib64/ld-linux-x86-64.so.2...(no debugging symbols found)...done.
Reading symbols from /lib64/libnss_files.so.2...(no debugging symbols found)...done.
0x00007f0812262f90 in epoll_pwait () from /lib64/libc.so.6
Missing separate debuginfos, use: debuginfo-install glibc-2.26-34.amzn2.x86_64
(gdb) 
```

psql側で下記SQLを実行してみる。gdbで解析中は実行がstopする。（この言い方は正しくないかもしれない。）

```sh
postgres=# select 1;
```

#### bt (back trace) : バックトレース（関数呼出の履歴）を表示

```sh
(gdb) bt
#0  0x00007f0812262f90 in epoll_pwait () from /lib64/libc.so.6
#1  0x00000000006c34ba in WaitEventSetWaitBlock (nevents=1, 
    occurred_events=0x7ffd9a72e630, cur_timeout=-1, set=0x2483798)
    at latch.c:1048
#2  WaitEventSetWait (set=0x2483798, timeout=timeout@entry=-1, 
    occurred_events=occurred_events@entry=0x7ffd9a72e630, 
    nevents=nevents@entry=1, wait_event_info=wait_event_info@entry=100663296)
    at latch.c:1000
#3  0x0000000000603388 in secure_read (port=0x24aa550, 
    ptr=0xc55e80 <PqRecvBuffer>, len=8192) at be-secure.c:169
#4  0x000000000060b888 in pq_recvbuf () at pqcomm.c:963
#5  0x000000000060c54b in pq_getbyte () at pqcomm.c:1006
#6  0x00000000006e16dd in SocketBackend (inBuf=0x7ffd9a72e770) at postgres.c:328
#7  ReadCommand (inBuf=0x7ffd9a72e770) at postgres.c:501
#8  PostgresMain (argc=<optimized out>, argv=argv@entry=0x24aff30, 
    dbname=<optimized out>, username=<optimized out>) at postgres.c:4059
#9  0x0000000000479d43 in BackendRun (port=0x24aa550) at postmaster.c:4405
#10 BackendStartup (port=0x24aa550) at postmaster.c:4077
#11 ServerLoop () at postmaster.c:1755
#12 0x000000000068045c in PostmasterMain (argc=argc@entry=1, 
    argv=argv@entry=0x2482be0) at postmaster.c:1363
#13 0x000000000047b309 in main (argc=1, argv=0x2482be0) at main.c:228

```

#### l (list) : ソースコードの確認

```sh
(gdb) list
47	const char *progname;
48	
49	
50	static void startup_hacks(const char *progname);
51	static void init_locale(const char *categoryname, int category, const char *locale);
52	static void help(const char *progname);
53	static void check_root(const char *progname);
54	
55	
56	/*
(gdb) 
```

#### b (break 関数名) :  プログラムを止めたい場所を指定

```sh
(gdb) l
64	 *		'nil' if the constant qualification is not satisfied.
65	 * ----------------------------------------------------------------
66	 */
67	static TupleTableSlot *
68	ExecResult(PlanState *pstate)
69	{
70		ResultState *node = castNode(ResultState, pstate);
71		TupleTableSlot *outerTupleSlot;
72		PlanState  *outerPlan;
73		ExprContext *econtext;
(gdb) 
```

もう少し勉強してみます。

#### 参考

> 第16章 ソースコードからインストール https://www.postgresql.jp/document/11/html/installation.html
>
> PostgreSQL の構造とソースツリー（３） | Let's Postgres https://lets.postgresql.jp/node/167
>
> 目的別ガイド：内部解析編 | Let's Postgres https://lets.postgresql.jp/node/10



