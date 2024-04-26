---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのLogical Decodingについて"
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

#### はじめに

Logical DecodingでWALに記録されたデータベースに対するアクティビティの履歴情報を抽出、参照することが出来る。Oracle DatabaseでいうところのLogMinerに近い機能と理解。機能としてはlogminerの方が細かい内容を確認出来る。PostgreSQLではDDLの内容まではLogical Decodingの対象とできないようだ。PostgreSQL9.4から実装されたLogical Decoding機能なのでこれからに期待。

なお、論理レプリケーションで使われるCDCも本機能を基に実装されている。

マニュアルはこちら。

> https://www.postgresql.jp/document/10/html/logicaldecoding.htm
>
> 第48章 ロジカルデコーディング

#### 設定方法

##### postgresql.confを変更

wal_levelを「logical」にmax_replication_slotsを「1」以上に変更する。PostgreSQL10の場合は、max_replication_slotsはデフォルト10となっているので特に変更の必要はない。wal_levelをデフォルトからlogicalに変更すると当然WALの生成量が増える。wal_levelを変更するので再起動が必要。

```text
#postgresql.conf
wal_level = logical
max_replication_slots = 10
```

##### プラグインのインストール

Logical Decodingのプラグインによって出力形式が異なる。decodeのpluginの一覧は下記のURLに記載がある。

> https://wiki.postgresql.org/wiki/Logical_Decoding_Plugins
>
> Logical Decoding Plugins

ここでは、contribの中に最初から含まれている`test_decoding`と追加のインストールは必要だが、SQL Formatベースの`decoder_raw`をインストールしたい。

##### test_decodingプラグインのインストール

ソースのルートにcontribディレクトリがあるのでそこからmake installでインストールする。

```sh
$ cd contrib/test_decoding
$ make
# make insatll
```

もしくはyumでインストールする。rpmなｄのパッケージでインストールしている場合はこっち。

```sh
sudo yum install postgresql10-contrib
```

##### decoder_rawプラグインのインストール

githubからcloneしてmake installでインストールする。

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
gcc -Wall -Wmissing-prototypes -Wpointer-arith -Wdeclaration-after-statement -Wendif-labels -Wmissing-format-attribute -Wformat-security -fno-strict-aliasing -fwrapv -fexcess-precision=standard -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC -I. -I./ -I/usr/pgsql-10/include/server -I/usr/pgsql-10/include/internal  -D_GNU_SOURCE -I/usr/include/libxml2  -I/usr/include  -c -o decoder_raw.o decoder_raw.c
gcc -Wall -Wmissing-prototypes -Wpointer-arith -Wdeclaration-after-statement -Wendif-labels -Wmissing-format-attribute -Wformat-security -fno-strict-aliasing -fwrapv -fexcess-precision=standard -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC -L/usr/pgsql-10/lib -Wl,--as-needed  -L/usr/lib64 -Wl,--as-needed -Wl,-rpath,'/usr/pgsql-10/lib',--enable-new-dtags  -shared -o decoder_raw.so decoder_raw.o
/bin/mkdir -p '/usr/pgsql-10/lib'
/bin/install -c -m 755  decoder_raw.so '/usr/pgsql-10/lib/'
[root@postdb decoder_raw]# 
[root@postdb decoder_raw]# echo $?
0
[root@postdb decoder_raw]# 
```

makeインストール後には/usr/pgsql-10/lib配下に関連するライブラリが配置されている。

```sh
-bash-4.2$ pwd
/usr/pgsql-10/lib
-bash-4.2$ ls -l decoder_raw*
-rwxr-xr-x 1 root root 75304 Dec 28 11:16 decoder_raw.so
-bash-4.2$ 
```

#### ロジカルデコーディング関連の関数

関連する関数は多くはない。この3つで十分なはず。

- ##### pg_create_logical_replication_slot

  ```sql
  pg_create_logical_replication_slot(slot_name name, plugin name [, temporary boolean])	
  ```

  - 論理(デコード)レプリケーションスロットを作成する。

    第1引数：slot_name を指定

    第2引数：plugin name を指定

    第3引数：trueに設定するとそのスロットは現行セッションに限定される（オプション）

- ##### pg_drop_replication_slot

  ```sql
  pg_drop_replication_slot(slot_name name)	
  ```

  - 論理(デコード)レプリケーションスロットを削除する。

    第1引数：slot_name を指定

- ##### pg_logical_slot_get_changes

  ```sql
  pg_logical_slot_get_changes(slot_name name, upto_lsn pg_lsn, upto_nchanges int, VARIADIC options text[])	
  ```

- 変更履歴を確認する

  第1引数：slot_name を指定

  第2引数：確認するLSN を指定

  第3引数：何行分出力するか

  第4引数：出力プラグインのオプションをkeyとvalueで指定

#### 1.) ロジカルデコーディングを行ってみる（<u>test_decodingプラグイン</u>を使用）

##### レプリケーションスロットの作成

ロジカルデコーディングを行いたいデータベースでpg_create_logical_replication_slotを実行してレプリケーション・スロットを作成する。

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

##### 変更履歴を確認

当然現時点では特に操作を行っていないので何も出力されない。

```sql
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
(0 rows)
```

##### テーブルに対してDDLを行ってみる

DDLでは特に内容は出力されない。BEGINとCOMMITは出力される。

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

##### テーブルに対してDMLを行ってみる

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

##### レプリケーションスロットを削除

```sql
SELECT * FROM pg_drop_replication_slot('decodeslot1');
```

#### 2.) ロジカルデコーディングを行ってみる（<u>decoder_rawプラグイン</u>を使用）

ロジカルデコーディングを行いたいデータベースでpg_create_logical_replication_slotを実行してレプリケーション・スロットを作成する。

##### レプリケーションスロットの作成

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

##### 変更履歴を確認

当然現時点では特に操作を行っていないので何も出力されない。

```sql
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
 lsn | xid | data 
-----+-----+------
(0 rows)
```

##### テーブルに対してDDLを行ってみる

DDLでは特に内容は出力されない。test_decodingと異なりBEGINとCOMMITも出力されない。

```sql
postgres=# CREATE TABLE data(id serial primary key, data text);
CREATE TABLE
postgres=# SELECT * FROM pg_logical_slot_get_changes('decodeslot1', NULL, NULL);
 lsn | xid | data 
-----+-----+------
(0 rows)
```

##### テーブルに対してDMLを行ってみる

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

##### レプリケーションスロットを削除

```sql
SELECT * FROM pg_drop_replication_slot('decodeslot1');
```



