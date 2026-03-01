---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "シグナル(TERM／INT／HUP)によるPostgresプロセスへの影響"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-signal-process-term-int-hup.html
date: 2020-03-11
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

表題の通り、シグナル(TERM／INT／HUP)によるpostgresプロセスへの影響を確認してみます。

### PostgreSQLのシャットダウンモードについて

まず前提となるシャットダウン時のモード。

| shutdown mode                | 説明                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| スマートシャットダウンモード | 新しい接続を禁止しますが、既に存在するセッションは通常通り動作。既存セッションが通常に終了するまではシャットダウンしない。 |
| 高速シャットダウンモード     | サーバは新しい接続を禁止し全ての存在するサーバプロセスにSIGTERMを送り、この結果サーバプロセスは現在のトランザクションをアボートし、即座に終了する |
| 即時シャットダウン           | 全ての子プロセスに SIGQUITを送り、即座に終了。次回起動時にWALを使用してリカバリをする必要がある。 |

次にシグナルを送った場合(killした場合)の挙動を確認してみる。

#### SIGINTの場合

```sh
[postgres@postdb ~]$ ps -ef | grep "/usr/pgsql-10/bin/postgres" | grep -v grep
postgres  5632     1  0 03:00 pts/3    00:00:00 /usr/pgsql-10/bin/postgres
[postgres@postdb ~]$ kill -SIGINT 5632
```

#### log出力

高速シャットダウンモードとなる

```sh
[2020-03-10 12:02:28 JST]  5632[7] LOG:  received fast shutdown request
[2020-03-10 12:02:28 JST]  5632[8] LOG:  aborting any active transactions
[2020-03-10 12:02:28 JST]  5632[9] LOG:  worker process: logical replication launcher (PID 5641) exited with exit code 1
[2020-03-10 12:02:28 JST]  5635[1] LOG:  shutting down
[2020-03-10 12:02:28 JST]  5635[2] LOG:  checkpoint starting: shutdown immediate
[2020-03-10 12:02:28 JST]  5635[3] LOG:  checkpoint complete: wrote 1 buffers (0.0%); 0 WAL file(s) added, 10 removed, 0 recycled; write=0.015 s, sync=0.000 s, total=0.046 s; sync files=1, longest=0.000 s, average=0.000 s; distance=16384 kB, estimate=16384 kB
[2020-03-10 12:02:28 JST]  5632[10] LOG:  database system is shut down
```

#### SIGTERMの場合

```sh
[postgres@postdb ~]$ ps -ef | grep "/usr/pgsql-10/bin/postgres" | grep -v grep
postgres  5678     1  9 03:06 pts/3    00:00:00 /usr/pgsql-10/bin/postgres
[postgres@postdb ~]$ kill -SIGTERM 5678
```

#### log出力

スマートシャットダウンモード

```
[2020-03-10 12:06:56 JST]  5678[7] LOG:  received smart shutdown request
[2020-03-10 12:06:56 JST]  5678[8] LOG:  worker process: logical replication launcher (PID 5687) exited with exit code 1
[2020-03-10 12:06:56 JST]  5681[1] LOG:  shutting down
[2020-03-10 12:06:56 JST]  5681[2] LOG:  checkpoint starting: shutdown immediate
[2020-03-10 12:06:56 JST]  5681[3] LOG:  checkpoint complete: wrote 0 buffers (0.0%); 0 WAL file(s) added, 1 removed, 0 recycled; write=0.015 s, sync=0.000 s, total=0.024 s; sync files=0, longest=0.000 s, average=0.000 s; distance=16384 kB, estimate=16384 kB
[2020-03-10 12:06:56 JST]  5678[9] LOG:  database system is shut down
```

#### SIGHUPの場合

```sh
[postgres@postdb ~]$ ps -ef | grep "/usr/pgsql-10/bin/postgres" | grep -v grep
postgres  5695     1  3 03:08 pts/3    00:00:00 /usr/pgsql-10/bin/postgres
[postgres@postdb ~]$ kill -SIGHUP 5695
```

#### log出力

SIGHUPの場合はパラメータファイルの再読み込み

```sh
[2020-03-10 12:08:33 JST]  5695[7] LOG:  received SIGHUP, reloading configuration files
```

#### SIGQUITの場合

```
[postgres@postdb ~]$ ps -ef | grep "/usr/pgsql-10/bin/postgres" | grep -v grep
postgres  5695     1  0 03:08 pts/3    00:00:00 /usr/pgsql-10/bin/postgres
[postgres@postdb ~]$ kill -SIGQUIT 5695
```

#### log出力

即時シャットダウンとなる

```
[2020-03-10 12:09:40 JST]  5695[8] LOG:  received immediate shutdown request
[2020-03-10 12:09:40 JST]  5701[1] WARNING:  terminating connection because of crash of another server process
[2020-03-10 12:09:40 JST]  5701[2] DETAIL:  The postmaster has commanded this server process to roll back the current transaction and exit, because another server process exited abnormally and possibly corrupted shared memory.
[2020-03-10 12:09:40 JST]  5701[3] HINT:  In a moment you should be able to reconnect to the database and repeat your command.
[2020-03-10 12:09:40 JST]  5695[9] LOG:  archiver process (PID 5702) exited with exit code 1
[2020-03-10 12:09:40 JST]  5695[10] LOG:  database system is shut down
```

即時シャットダウンとなるので、次回起動時には`redo starts`の適用が始まる。

```
[2020-03-10 12:10:06 JST]  5725[1] LOG:  database system was interrupted; last known up at 2020-03-10 12:08:20 JST
[2020-03-10 12:10:06 JST]  5725[2] LOG:  database system was not properly shut down; automatic recovery in progress
[2020-03-10 12:10:06 JST]  5725[3] LOG:  redo starts at 3/71000098
[2020-03-10 12:10:06 JST]  5725[4] LOG:  invalid record length at 3/710000D0: wanted 24, got 0
[2020-03-10 12:10:06 JST]  5725[5] LOG:  redo done at 3/71000098
[2020-03-10 12:10:06 JST]  5725[6] LOG:  checkpoint starting: end-of-recovery immediate
[2020-03-10 12:10:06 JST]  5725[7] LOG:  checkpoint complete: wrote 0 buffers (0.0%); 0 WAL file(s) added, 1 removed, 0 recycled; write=0.013 s, sync=0.000 s, total=0.019 s; sync files=0, longest=0.000 s, average=0.000 s; distance=0 kB, estimate=0 kB
[2020-03-10 12:10:06 JST]  5723[6] LOG:  database system is ready to accept connections
```

