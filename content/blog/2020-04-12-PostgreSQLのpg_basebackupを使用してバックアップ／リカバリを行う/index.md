---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_basebackupを使用してバックアップ／リカバリを行う"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pg_basebackup-backup-recovery.html
date: 2020-04-12
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


pg_basebackupを使ったPostgreSQLの基本的なバックアップ/リカバリを実施する。

### バックアップ

#### バックアップディレクトリの作成

```sh
mkdir $HOME/pg_basebackup_dir
```

#### 環境変数の設定

```sh
export BACKUP_DIR=/var/lib/pgsql/pg_basebackup_dir
```

#### pg_basebackupでのバックアップ

```sh
pg_basebackup -D $BACKUP_DIR -F t -z
ls -l $BACKUP_DIR
```

今回は フォーマットでtarファイルを指定してしており、かつtarファイル出力のデフォルトの圧縮レベルによるgzip圧縮を有効にしている。

> pg_basebackup https://www.postgresql.jp/document/10/html/app-pgbasebackup.html

### データ損失

#### DB停止

```sh
pg_ctl stop
```

#### データ削除

物理的にデータを損失させる。

```sh
rm -r /var/lib/pgsql/10/data/*
```

### リカバリ

ここからがリカバリ。

#### バックアップデータの展開

```sh
cd /var/lib/pgsql/10/data
tar xvfz $BACKUP_DIR/base.tar.gz
```

#### pg_walの削除

```sh
rm -rf /var/lib/pgsql/10/data/pg_wal/*
```

#### バックアップしたwalファイルの解凍

```sh
cd /var/lib/pgsql/10/data/pg_wal
tar xvfz $BACKUP_DIR/pg_wal.tar.gz
```

#### バックアップしたwalファイルの解凍

```sh
cd /var/lib/pgsql/10/data/pg_wal
tar xvfz $BACKUP_DIR/pg_wal.tar.gz
```

#### recovery.confファイルの作成

```sh
cd /var/lib/pgsql/10/data/
vi /var/lib/pgsql/10/data/recovery.conf

restore_command = 'cp /var/lib/pgsql/10/data/pg_wal/%f %p'
```

デフォルトではリカバリ可能な最新時点までリカバリされるが、PITRなど時間を明示的に指定したい場合は下記マニュアルを参考にしつつ`recovery_target_name`や`recovery_target_lsn`を設定する。

> 27.2. リカバリ対象の設定 https://www.postgresql.jp/document/10/html/recovery-target-settings.html

#### DB起動

通常のコマンドと同様にスタートする。この時recovery.confを参照してリカバリを行う。

```sh
pg_ctl start
```

#### リカバリ時のログ出力

```sh
[2020-03-04 13:34:00 UTC]  18052[1] LOG:  database system was interrupted; last known up at 2020-03-04 13:31:23 UTC
[2020-03-04 13:34:00 UTC]  18052[2] LOG:  starting archive recovery
[2020-03-04 13:34:00 UTC]  18052[3] LOG:  restored log file "00000002.history" from archive
[2020-03-04 13:34:00 UTC]  18052[4] LOG:  restored log file "000000020000000000000050" from archive
[2020-03-04 13:34:00 UTC]  18052[5] LOG:  redo starts at 0/50000028
[2020-03-04 13:34:00 UTC]  18052[6] LOG:  consistent recovery state reached at 0/500000F8
[2020-03-04 13:34:00 UTC]  18050[6] LOG:  database system is ready to accept read only connections
cp: cannot stat ‘/var/lib/pgsql/10/data/pg_wal/000000020000000000000051’: No such file or directory
[2020-03-04 13:34:00 UTC]  18052[7] LOG:  redo done at 0/500000F8
[2020-03-04 13:34:00 UTC]  18052[8] LOG:  restored log file "000000020000000000000050" from archive
cp: cannot stat ‘/var/lib/pgsql/10/data/pg_wal/00000003.history’: No such file or directory
[2020-03-04 13:34:00 UTC]  18052[9] LOG:  selected new timeline ID: 3
[2020-03-04 13:34:01 UTC]  18052[10] LOG:  archive recovery complete
[2020-03-04 13:34:01 UTC]  18052[11] LOG:  restored log file "00000002.history" from archive
[2020-03-04 13:34:01 UTC]  18055[1] LOG:  checkpoint starting: end-of-recovery immediate wait
[2020-03-04 13:34:01 UTC]  18055[2] LOG:  checkpoint complete: wrote 0 buffers (0.0%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.000 s, sync=0.000 s, total=0.004 s; sync files=0, longest=0.000 s, average=0.000 s; distance=16384 kB, estimate=16384 kB
[2020-03-04 13:34:01 UTC]  18050[7] LOG:  database system is ready to accept connections
cp: cannot create regular file ‘/var/lib/pgsql/10/data/pg_wal/archive/00000003.history’: No such file or directory
[2020-03-04 13:34:01 UTC]  18064[1] LOG:  archive command failed with exit code 1
[2020-03-04 13:34:01 UTC]  18064[2] DETAIL:  The failed archive command was: cp pg_wal/00000003.history /var/lib/pgsql/10/data/pg_wal/archive/00000003.history
cp: cannot create regular file ‘/var/lib/pgsql/10/data/pg_wal/archive/00000003.history’: No such file or directory
[2020-03-04 13:34:02 UTC]  18064[3] LOG:  archive command failed with exit code 1
[2020-03-04 13:34:02 UTC]  18064[4] DETAIL:  The failed archive command was: cp pg_wal/00000003.history /var/lib/pgsql/10/data/pg_wal/archive/00000003.history
cp: cannot create regular file ‘/var/lib/pgsql/10/data/pg_wal/archive/00000003.history’: No such file or directory
[2020-03-04 13:34:03 UTC]  18064[5] LOG:  archive command failed with exit code 1
[2020-03-04 13:34:03 UTC]  18064[6] DETAIL:  The failed archive command was: cp pg_wal/00000003.history /var/lib/pgsql/10/data/pg_wal/archive/00000003.history
[2020-03-04 13:34:03 UTC]  18064[7] WARNING:  archiving write-ahead log file "00000003.history" failed too many times, will try again later
```


