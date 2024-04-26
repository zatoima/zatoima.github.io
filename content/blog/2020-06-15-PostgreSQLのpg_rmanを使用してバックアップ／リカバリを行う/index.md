---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_rmanを使用してバックアップ／リカバリを行う"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg_rman-backup-recovery.html
date: 2020-06-15
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

### pg_rmanの概要

pg_rmanの手順メモ。rmanと名前についている通り、Oracle の Recovery Managerを意識した機能です。標準機能では使用できない増分バックアップが出来ることでバックアップの短縮に繋がるはず。

- 全体バックアップに加え、増分バックアップが可能
- バックアップの圧縮が可能
- バックアップの世代管理やバックアップ一覧を表示できる
- バックアップの対象はデータベースクラスタの他にアーカイブログ、サーバログが含めることができる
- タイムライン指定、リカバリしたい日付時刻指定が可能
- データベースクラスタ外のテーブルスペースを含めたバックアップが可能

### pg_rmanのインストール

下記のgithubのリポジトリから最新のバージョンをインストールします。

> Releases · ossc-db/pg_rman https://github.com/ossc-db/pg_rman/releases

```sh
sudo wget https://github.com/ossc-db/pg_rman/releases/download/V1.3.9/pg_rman-1.3.9-1.pg10.rhel7.x86_64.rpm
sudo rpm -ivh pg_rman-1.3.9-1.pg10.rhel7.x86_64.rpm
```

```sh
[postgres@postdb ~]$ pg_rman --help
pg_rman manage backup/recovery of PostgreSQL database.

Usage:
  pg_rman OPTION init
  pg_rman OPTION backup
  pg_rman OPTION restore
  pg_rman OPTION show [DATE]
  pg_rman OPTION show detail [DATE]
  pg_rman OPTION validate [DATE]
  pg_rman OPTION delete DATE
  pg_rman OPTION purge

Common Options:
  -D, --pgdata=PATH         location of the database storage area
  -A, --arclog-path=PATH    location of archive WAL storage area
  -S, --srvlog-path=PATH    location of server log storage area
  -B, --backup-path=PATH    location of the backup storage area
  -c, --check               show what would have been done
  -v, --verbose             show what detail messages
  -P, --progress            show progress of processed files

Backup options:
  -b, --backup-mode=MODE    full, incremental, or archive
  -s, --with-serverlog      also backup server log files
  -Z, --compress-data       compress data backup with zlib
  -C, --smooth-checkpoint   do smooth checkpoint before backup
  -F, --full-backup-on-error   switch to full backup mode
                               if pg_rman cannot find validate full backup
                               on current timeline
      NOTE: this option is only used in --backup-mode=incremental or archive.
  --keep-data-generations=NUM keep NUM generations of full data backup
  --keep-data-days=NUM        keep enough data backup to recover to N days ago
  --keep-arclog-files=NUM   keep NUM of archived WAL
  --keep-arclog-days=DAY    keep archived WAL modified in DAY days
  --keep-srvlog-files=NUM   keep NUM of serverlogs
  --keep-srvlog-days=DAY    keep serverlog modified in DAY days
  --standby-host=HOSTNAME   standby host when taking backup from standby
  --standby-port=PORT       standby port when taking backup from standby

Restore options:
  --recovery-target-time    time stamp up to which recovery will proceed
  --recovery-target-xid     transaction ID up to which recovery will proceed
  --recovery-target-inclusive whether we stop just after the recovery target
  --recovery-target-timeline  recovering into a particular timeline
  --hard-copy                 copying archivelog not symbolic link

Catalog options:
  -a, --show-all            show deleted backup too

Delete options:
  -f, --force               forcibly delete backup older than given DATE

Connection options:
  -d, --dbname=DBNAME       database to connect
  -h, --host=HOSTNAME       database server host or socket directory
  -p, --port=PORT           database server port
  -U, --username=USERNAME   user name to connect as
  -w, --no-password         never prompt for password
  -W, --password            force password prompt

Generic options:
  -q, --quiet               don't show any INFO or DEBUG messages
  --debug                   show DEBUG messages
  --help                    show this help, then exit
  --version                 output version information, then exit

Read the website for details. <http://github.com/ossc-db/pg_rman>
Report bugs to <http://github.com/ossc-db/pg_rman/issues>.
[postgres@postdb ~]$ 
```

### postgresql.confの設定

```
archive_mode = on
archive_command = 'cp %p /var/lib/pgsql/10/data/pg_wal/archive/%f'
wal_level = archive
log_directory = 'pg_log'
```

### 環境変数編集

BACKUP_PATHを下記の通りとします。

```
$ export BACKUP_PATH=/var/lib/pgsql/pg_rman_backup
```

### バックアップカタログの初期化

```
[postgres@postdb ~]$ pg_rman init
INFO: ARCLOG_PATH is set to '/var/lib/pgsql/10/data/pg_wal/archive'
INFO: SRVLOG_PATH is set to '/var/lib/pgsql/10/data/log'
[postgres@postdb ~]$ 
```

### フルバックアップの取得

```sh
[postgres@postdb ~]$ pg_rman init
INFO: ARCLOG_PATH is set to '/var/lib/pgsql/10/data/pg_wal/archive'
INFO: SRVLOG_PATH is set to '/var/lib/pgsql/10/data/log'
[postgres@postdb ~]$ 
[postgres@postdb ~]$ 
[postgres@postdb ~]$ pg_rman backup --backup-mode=full
INFO: copying database files
INFO: copying archived WAL files
INFO: backup complete
INFO: Please execute 'pg_rman validate' to verify the files are correctly copied.
[postgres@postdb ~]$ 
```

### バックアップの検証

validateを実施しないとリストア出来ない。バックアップ後すぐに実施するのが良さそう。

```
[postgres@postdb ~]$ pg_rman validate
INFO: validate: "2020-03-04 12:55:57" backup and archive log files by CRC
INFO: backup "2020-03-04 12:55:57" is valid
[postgres@postdb ~]$ 
```

### バックアップ後のディレクトリ状態

```
cd /var/lib/pgsql/pg_rman_backup
ls -l
```

### 増分バックアップの実施

```
[postgres@postdb ~]$ pg_rman backup --backup-mode=incremental --with-serverlog
INFO: copying database files
INFO: copying archived WAL files
INFO: copying server log files
INFO: backup complete
INFO: Please execute 'pg_rman validate' to verify the files are correctly copied.
[postgres@postdb ~]$ pg_rman validate
INFO: validate: "2020-03-04 12:58:38" backup, archive log files and server log files by CRC
INFO: backup "2020-03-04 12:58:38" is valid
[postgres@postdb ~]$ 
```

### バックアップ後のディレクトリ状態

```
cd /var/lib/pgsql/pg_rman_backup
ls -l
```

### バックアップの表示

```
[postgres@postdb ~]$ pg_rman show
=====================================================================
 StartTime           EndTime              Mode    Size   TLI  Status 
=====================================================================
2020-03-04 12:58:38  2020-03-04 12:58:41  INCR    42MB     1  OK
2020-03-04 12:55:57  2020-03-04 12:56:15  FULL  1078MB     1  OK
[postgres@postdb ~]$ 
```

### リストア前のDBの停止

```
[postgres@postdb ~]$ pg_ctl stop
waiting for server to shut down.... done
server stopped
[postgres@postdb ~]$ 
```

### DBの破壊

雑にDBを破損させました。

```
[postgres@postdb base]$ pwd
/var/lib/pgsql/10/data/base
[postgres@postdb base]$ ls -l
total 0
[postgres@postdb base]$ 
[postgres@postdb base]$ psql
psql: FATAL:  database "postgres" does not exist
DETAIL:  The database subdirectory "base/13865" is missing.
[postgres@postdb base]$ 
```

### 前回バックアップ時点の最新までリストア

```
[postgres@postdb ~]$ pg_rman restore
INFO: the recovery target timeline ID is not given
INFO: use timeline ID of current database cluster as recovery target: 1
INFO: calculating timeline branches to be used to recovery target point
INFO: searching latest full backup which can be used as restore start point
INFO: found the full backup can be used as base in recovery: "2020-03-04 12:55:57"
INFO: copying online WAL files and server log files
INFO: clearing restore destination
INFO: validate: "2020-03-04 12:55:57" backup and archive log files by SIZE
INFO: backup "2020-03-04 12:55:57" is valid
INFO: restoring database files from the full mode backup "2020-03-04 12:55:57"
INFO: searching incremental backup to be restored
INFO: validate: "2020-03-04 12:58:38" backup, archive log files and server log files by SIZE
INFO: backup "2020-03-04 12:58:38" is valid
INFO: restoring database files from the incremental mode backup "2020-03-04 12:58:38"
INFO: searching backup which contained archived WAL files to be restored
INFO: backup "2020-03-04 12:58:38" is valid
INFO: restoring WAL files from backup "2020-03-04 12:58:38"
INFO: restoring online WAL files and server log files
INFO: generating recovery.conf
INFO: restore complete
HINT: Recovery will start automatically when the PostgreSQL server is started.
[postgres@postdb ~]$ 
[postgres@postdb ~]$ pg_ctl status
pg_ctl: no server running
```

pg_ctl start時のログ・ファイルを確認したところリカバリ処理が走っている。`2020-03-04 12:58:40.102645+00`時点まで戻ったことが確認出来る。

```
[postgres@postdb log]$ cat postgresql-20200304.log 
[2020-03-04 13:05:24 UTC]  17807[1] LOG:  database system was interrupted; last known up at 2020-03-04 12:58:38 UTC
[2020-03-04 13:05:24 UTC]  17807[2] LOG:  starting archive recovery
[2020-03-04 13:05:24 UTC]  17807[3] LOG:  restored log file "000000010000000000000047" from archive
[2020-03-04 13:05:24 UTC]  17807[4] LOG:  redo starts at 0/47000028
[2020-03-04 13:05:24 UTC]  17807[5] LOG:  consistent recovery state reached at 0/470000F8
[2020-03-04 13:05:24 UTC]  17805[6] LOG:  database system is ready to accept read only connections
[2020-03-04 13:05:24 UTC]  17807[6] LOG:  restored log file "000000010000000000000048" from archive
[2020-03-04 13:05:25 UTC]  17807[7] LOG:  restored log file "000000010000000000000049" from archive
[2020-03-04 13:05:25 UTC]  17807[8] LOG:  restored log file "00000001000000000000004A" from archive
cp: cannot stat ‘/var/lib/pgsql/10/data/pg_wal/archive/00000001000000000000004B’: No such file or directory
[2020-03-04 13:05:25 UTC]  17807[9] LOG:  invalid record length at 0/4B000098: wanted 24, got 0
[2020-03-04 13:05:25 UTC]  17807[10] LOG:  redo done at 0/4B000028
[2020-03-04 13:05:25 UTC]  17807[11] LOG:  last completed transaction was at log time 2020-03-04 12:58:40.102645+00

```

物理ファイルもリストアされている。

```
[postgres@postdb base]$ pwd
/var/lib/pgsql/10/data/base
[postgres@postdb base]$ ls -l
total 60
drwx------ 2 postgres postgres 8192 Mar  4 13:03 1
drwx------ 2 postgres postgres 8192 Mar  4 13:03 13864
drwx------ 2 postgres postgres 8192 Mar  4 13:03 13865
drwx------ 2 postgres postgres 8192 Mar  4 13:03 16392
drwx------ 2 postgres postgres 8192 Mar  4 13:03 16456
[postgres@postdb base]$ find . | more
.
./1
./1/18121
./1/18121_fsm
./1/18121_vm
./1/18124
./1/18124_fsm
./1/18124_vm
./1/18126
./1/18127
./1/18128
./1/18128_fsm
./1/18128_vm
./1/18131
```

### PITR

特定時点まで戻す場合は下記を実行する、

```
pg_rman restore --recovery-target-time '2020-03-04 22:00:00'
```

### pg_rmanのコマンド・オプション

##### Usage

> pg_rman https://ossc-db.github.io/pg_rman/index-ja.html
>

### 参考

> pg_rman (PostgreSQL のバックアップ/リストア管理ツール) https://www.sraoss.co.jp/tech-blog/pgsql/pg_rman/



