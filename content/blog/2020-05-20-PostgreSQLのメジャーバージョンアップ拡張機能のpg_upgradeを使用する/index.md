---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのメジャーバージョンアップ拡張機能のpg_upgradeを使用する"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-versionup-pg_upgrade-extention.html
date: 2020-05-20
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

### pg_upgradeの概要

> pg_upgrade https://www.postgresql.jp/document/12/html/pgupgrade.html

pg_upgradeはPostgreSQLのメジャーバージョンアップ時に使用されるツールで、バックアップ・リストアやpg_dump等の論理的な移行をせずに旧バージョンの PostgreSQLのデータを新バージョンのPostgreSQLに移行することが可能。

アウトオブプレース・アップグレードとインプレース・アップグレードの考えであり、pg_upgradeはインプレース・アップグレードとなる。一方の論理的な移行（レプリケーション、pg_dump移行等）はアウトオブプレース・アップグレードとなる。ダウンタイムは必要だが、一般的なバックアップリストア方式よりも時間は短くなる傾向にある。

pg_upgradeには２つのモードがある。

| モード       | 説明                                                         |
| ------------ | ------------------------------------------------------------ |
| コピーモード | 既存のデータベースクラスタのデータを、新規PostgreSQL  のデータベースクラスタにコピー（デフォルト） |
| リンクモード | 既存のデータベースクラスタと新規データベースクラスタをハードリンクで繋ぎ、データを共有する |

※コピーモードの注意点として下記がある

- pg_upgrade直後は一時的にデータ容量が2倍になる。(./delete_old_cluster.shで削除すれば問題無し)
- （未検証だが、おそらく）移行時間がデータ容量と比例する

※リンクモードの注意点として下記がある

- ファイルのコピーがないのでアップグレード自体は非常に高速となる

- 必要なディスクもコピーモードに比べて少ない

- 新しいPostgreSQLクラスタを一度実行すると旧クラスタは使用できなくなる

- 新旧のクラスタが同じファイルシステム上にあることが必要


### 手順

#### 事前準備

***

この環境自体は下記記事で作った一時的な検証環境を使用。

> EC2上のRHEL8(Red Hat Enterprise Linux)にPostgreSQL11と12をyumでインストール | my opinion is my own https://zatoima.github.io/aws-ec2-rhel-postgresql-install.html
>

検証なのでゼロベースからスタートする。

##### PostgreSQLの停止

```sh
. $HOME/.pgsql11_env
pg_ctl stop

. $HOME/.pgsql12_env
pg_ctl stop
```

#####  データファイルの削除

```sh
rm -rf $HOME/11/*
rm -rf $HOME/12/*
```

##### 初期化(rootで実行)

```sh
/usr/pgsql-11/bin/postgresql-11-setup initdb
/usr/pgsql-12/bin/postgresql-12-setup initdb
```

##### テストデータのロード

```sh
. $HOME/.pgsql11_env
pg_ctl start
pgcli
CREATE TABLE aozora_kaisekidata(file VARCHAR(30),num INT,row INT,word TEXT,subtype1 VARCHAR(30),subtype2 VARCHAR(30),subtype3 VARCHAR(30),subtype4 VARCHAR(10),conjtype VARCHAR(15),conjugation VARCHAR(15),basic TEXT,ruby TEXT,pronunce TEXT );
time psql -d postgres -U postgres -c "COPY aozora_kaisekidata(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < $HOME/utf8_all.csv
```

ここでoid2nameでオブジェクトの情報を控えておく。

```sh
[postgres@pgsql ~]$ oid2name -t aozora_kaisekidata
From database "postgres":
  Filenode          Table Name
------------------------------
     16384  aozora_kaisekidata
```

また、この状態での容量は約10GBとなる。

```sh
postgres> SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;                                                                                                       
+-----------+------------------+
| datname   | pg_size_pretty   |
|-----------+------------------|
| postgres  | 9584 MB          |
| template1 | 7585 kB          |
| template0 | 7585 kB          |
+-----------+------------------+
```

ちなみに、このデータ自体は下記方法で作成している。

> 青空文庫作品の形態素解析データをRDS PostgreSQLにインポートする | my opinion is my own https://zatoima.github.io/postgresql-aozora-bunko-data-import.html
>

##### 事前準備（PostgreSQLの停止）

```sh
. $HOME/.pgsql11_env
pg_ctl stop

. $HOME/.pgsql12_env
pg_ctl stop
```

#### pg_upgradeの実施

***

##### 1.) コピーモードでpg_upgradeを実施

10GB弱のDB容量のアップグレード実行に約3分程度掛かっている。

```sh
[postgres@pgsql ~]$ . $HOME/.pgsql12_env
[postgres@pgsql ~]$ time /usr/pgsql-12/bin/pg_upgrade -r -d /var/lib/pgsql/11/data -D /var/lib/pgsql/12/data -b /usr/pgsql-11/bin -B /usr/pgsql-12/bin
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok
Checking database user is the install user                  ok
Checking database connection settings                       ok
Checking for prepared transactions                          ok
Checking for reg* data types in user tables                 ok
Checking for contrib/isn with bigint-passing mismatch       ok
Checking for tables WITH OIDS                               ok
Checking for invalid "sql_identifier" user columns          ok
Creating dump of global objects                             ok
Creating dump of database schemas
                                                            ok
Checking for presence of required libraries                 ok
Checking database user is the install user                  ok
Checking for prepared transactions                          ok

If pg_upgrade fails after this point, you must re-initdb the
new cluster before continuing.

Performing Upgrade
------------------
Analyzing all rows in the new cluster                       ok
Freezing all rows in the new cluster                        ok
Deleting files from new pg_xact                             ok
Copying old pg_xact to new server                           ok
Setting next transaction ID and epoch for new cluster       ok
Deleting files from new pg_multixact/offsets                ok
Copying old pg_multixact/offsets to new server              ok
Deleting files from new pg_multixact/members                ok
Copying old pg_multixact/members to new server              ok
Setting next multixact ID and offset for new cluster        ok
Resetting WAL archives                                      ok
Setting frozenxid and minmxid counters in new cluster       ok
Restoring global objects in the new cluster                 ok
Restoring database schemas in the new cluster
                                                            ok
Copying user relation files
                                                            ok
Setting next OID for new cluster                            ok
Sync data directory to disk                                 ok
Creating script to analyze new cluster                      ok
Creating script to delete old cluster                       ok

Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade so,
once you start the new server, consider running:
    ./analyze_new_cluster.sh

Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh

real	2m45.122s
user	0m0.174s
sys	0m6.919s
[postgres@pgsql ~]$ 
```

コピーモードなのでinodeも別となっている。（※リンクモードの場合はここが同一となる。（後述））

```sh
[postgres@pgsql ~]$ find . | grep 16384 | xargs ls -li
239076379 -rw-------. 1 postgres postgres 1073741824 May 16 22:54 ./11/data/base/13141/16384
239076383 -rw-------. 1 postgres postgres 1073741824 May 16 22:54 ./11/data/base/13141/16384.1
239076384 -rw-------. 1 postgres postgres 1073741824 May 16 22:55 ./11/data/base/13141/16384.2
239076385 -rw-------. 1 postgres postgres 1073741824 May 16 22:49 ./11/data/base/13141/16384.3
239076386 -rw-------. 1 postgres postgres 1073741824 May 16 22:50 ./11/data/base/13141/16384.4
239076387 -rw-------. 1 postgres postgres 1073741824 May 16 22:50 ./11/data/base/13141/16384.5
239076388 -rw-------. 1 postgres postgres 1073741824 May 16 22:51 ./11/data/base/13141/16384.6
239076389 -rw-------. 1 postgres postgres 1073741824 May 16 22:51 ./11/data/base/13141/16384.7
239076390 -rw-------. 1 postgres postgres 1073741824 May 16 22:52 ./11/data/base/13141/16384.8
239076391 -rw-------. 1 postgres postgres  375709696 May 16 22:53 ./11/data/base/13141/16384.9
239076382 -rw-------. 1 postgres postgres    2490368 May 16 22:53 ./11/data/base/13141/16384_fsm
 96472658 -rw-------. 1 postgres postgres 1073741824 May 16 22:55 ./12/data/base/16401/16384
 96472661 -rw-------. 1 postgres postgres 1073741824 May 16 22:55 ./12/data/base/16401/16384.1
 96472662 -rw-------. 1 postgres postgres 1073741824 May 16 22:56 ./12/data/base/16401/16384.2
 96472663 -rw-------. 1 postgres postgres 1073741824 May 16 22:56 ./12/data/base/16401/16384.3
 96472664 -rw-------. 1 postgres postgres 1073741824 May 16 22:56 ./12/data/base/16401/16384.4
 96472665 -rw-------. 1 postgres postgres 1073741824 May 16 22:56 ./12/data/base/16401/16384.5
 96472666 -rw-------. 1 postgres postgres 1073741824 May 16 22:57 ./12/data/base/16401/16384.6
 96472667 -rw-------. 1 postgres postgres 1073741824 May 16 22:57 ./12/data/base/16401/16384.7
 96472668 -rw-------. 1 postgres postgres 1073741824 May 16 22:57 ./12/data/base/16401/16384.8
 96472669 -rw-------. 1 postgres postgres  375709696 May 16 22:57 ./12/data/base/16401/16384.9
 96472670 -rw-------. 1 postgres postgres    2490368 May 16 22:57 ./12/data/base/16401/16384_fsm
```

##### 2.) リンクモードでpg_upgradeを実施

実行自体は10秒も掛からず終わった。

```sh
[postgres@pgsql ~]$ time /usr/pgsql-12/bin/pg_upgrade -r -k -d /var/lib/pgsql/11/data -D /var/lib/pgsql/12/data -b /usr/pgsql-11/bin -B /usr/pgsql-12/bin
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok
Checking database user is the install user                  ok
Checking database connection settings                       ok
Checking for prepared transactions                          ok
Checking for reg* data types in user tables                 ok
Checking for contrib/isn with bigint-passing mismatch       ok
Checking for tables WITH OIDS                               ok
Checking for invalid "sql_identifier" user columns          ok
Creating dump of global objects                             ok
Creating dump of database schemas
                                                            ok
Checking for presence of required libraries                 ok
Checking database user is the install user                  ok
Checking for prepared transactions                          ok

If pg_upgrade fails after this point, you must re-initdb the
new cluster before continuing.

Performing Upgrade
------------------
Analyzing all rows in the new cluster                       ok
Freezing all rows in the new cluster                        ok
Deleting files from new pg_xact                             ok
Copying old pg_xact to new server                           ok
Setting next transaction ID and epoch for new cluster       ok
Deleting files from new pg_multixact/offsets                ok
Copying old pg_multixact/offsets to new server              ok
Deleting files from new pg_multixact/members                ok
Copying old pg_multixact/members to new server              ok
Setting next multixact ID and offset for new cluster        ok
Resetting WAL archives                                      ok
Setting frozenxid and minmxid counters in new cluster       ok
Restoring global objects in the new cluster                 ok
Restoring database schemas in the new cluster
                                                            ok
Adding ".old" suffix to old global/pg_control               ok

If you want to start the old cluster, you will need to remove
the ".old" suffix from /var/lib/pgsql/11/data/global/pg_control.old.
Because "link" mode was used, the old cluster cannot be safely
started once the new cluster has been started.

Linking user relation files
                                                            ok
Setting next OID for new cluster                            ok
Sync data directory to disk                                 ok
Creating script to analyze new cluster                      ok
Creating script to delete old cluster                       ok

Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade so,
once you start the new server, consider running:
    ./analyze_new_cluster.sh

Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh

real	0m7.014s
user	0m0.103s
sys	0m0.210s
```

リンクモードなので、例えば`./11/data/base/13141/16384.1`のファイルのinodeは`272636857`で同一情報となっている。

```sh
[postgres@pgsql ~]$ find . | grep 16384 | xargs ls -li
272636853 -rw-------. 2 postgres postgres 1073741824 May 16 22:42 ./11/data/base/13141/16384
272636857 -rw-------. 2 postgres postgres 1073741824 May 16 22:33 ./11/data/base/13141/16384.1
272636858 -rw-------. 2 postgres postgres 1073741824 May 16 22:33 ./11/data/base/13141/16384.2
272636859 -rw-------. 2 postgres postgres 1073741824 May 16 22:34 ./11/data/base/13141/16384.3
272636860 -rw-------. 2 postgres postgres 1073741824 May 16 22:34 ./11/data/base/13141/16384.4
272636861 -rw-------. 2 postgres postgres 1073741824 May 16 22:35 ./11/data/base/13141/16384.5
272636862 -rw-------. 2 postgres postgres 1073741824 May 16 22:35 ./11/data/base/13141/16384.6
272636863 -rw-------. 2 postgres postgres 1073741824 May 16 22:36 ./11/data/base/13141/16384.7
275458304 -rw-------. 2 postgres postgres 1073741824 May 16 22:36 ./11/data/base/13141/16384.8
275458305 -rw-------. 2 postgres postgres  375709696 May 16 22:38 ./11/data/base/13141/16384.9
272636856 -rw-------. 2 postgres postgres    2490368 May 16 22:38 ./11/data/base/13141/16384_fsm
272636853 -rw-------. 2 postgres postgres 1073741824 May 16 22:42 ./12/data/base/16401/16384
272636857 -rw-------. 2 postgres postgres 1073741824 May 16 22:33 ./12/data/base/16401/16384.1
272636858 -rw-------. 2 postgres postgres 1073741824 May 16 22:33 ./12/data/base/16401/16384.2
272636859 -rw-------. 2 postgres postgres 1073741824 May 16 22:34 ./12/data/base/16401/16384.3
272636860 -rw-------. 2 postgres postgres 1073741824 May 16 22:34 ./12/data/base/16401/16384.4
272636861 -rw-------. 2 postgres postgres 1073741824 May 16 22:35 ./12/data/base/16401/16384.5
272636862 -rw-------. 2 postgres postgres 1073741824 May 16 22:35 ./12/data/base/16401/16384.6
272636863 -rw-------. 2 postgres postgres 1073741824 May 16 22:36 ./12/data/base/16401/16384.7
275458304 -rw-------. 2 postgres postgres 1073741824 May 16 22:36 ./12/data/base/16401/16384.8
275458305 -rw-------. 2 postgres postgres  375709696 May 16 22:38 ./12/data/base/16401/16384.9
272636856 -rw-------. 2 postgres postgres    2490368 May 16 22:38 ./12/data/base/16401/16384_fsm
```

### コピーモードとリンクモードの動作の違い

コピーモードでは出力ログに「Copying user relation files」セクションがある。

```sh
Copying user relation files                                 ok
```

一方、リンクモードの場合は、下記出力がある。

```sh
Adding ".old" suffix to old global/pg_control               ok

If you want to start the old cluster, you will need to remove
the ".old" suffix from /var/lib/pgsql/11/data/global/pg_control.old.
Because "link" mode was used, the old cluster cannot be safely
started once the new cluster has been started.

Linking user relation files
```

### 最後に

各種制限がクリアになればpg_upgradeでのメジャーバージョンアップも良いのかな、、、、と。他メジャーバージョン方法も出来れば試してみたい。