---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Backup/Recovery with PostgreSQL's pg_basebackup"
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



This article covers basic PostgreSQL backup/recovery using pg_basebackup.

### Backup

#### Create Backup Directory

```sh
mkdir $HOME/pg_basebackup_dir
```

#### Set Environment Variable

```sh
export BACKUP_DIR=/var/lib/pgsql/pg_basebackup_dir
```

#### Backup with pg_basebackup

```sh
pg_basebackup -D $BACKUP_DIR -F t -z
ls -l $BACKUP_DIR
```

In this case, we specify tar format for output and enable gzip compression at the default compression level for tar file output.

> pg_basebackup https://www.postgresql.jp/document/10/html/app-pgbasebackup.html

### Data Loss

#### Stop DB

```sh
pg_ctl stop
```

#### Delete Data

Physically simulate data loss.

```sh
rm -r /var/lib/pgsql/10/data/*
```

### Recovery

Now for the recovery.

#### Extract Backup Data

```sh
cd /var/lib/pgsql/10/data
tar xvfz $BACKUP_DIR/base.tar.gz
```

#### Delete pg_wal

```sh
rm -rf /var/lib/pgsql/10/data/pg_wal/*
```

#### Extract Backed-up WAL Files

```sh
cd /var/lib/pgsql/10/data/pg_wal
tar xvfz $BACKUP_DIR/pg_wal.tar.gz
```

#### Create recovery.conf File

```sh
cd /var/lib/pgsql/10/data/
vi /var/lib/pgsql/10/data/recovery.conf

restore_command = 'cp /var/lib/pgsql/10/data/pg_wal/%f %p'
```

By default, recovery proceeds to the most recent recoverable point. If you want to specify a time explicitly for PITR or similar, refer to the following manual and set `recovery_target_name` or `recovery_target_lsn`.

> 27.2. Recovery Target Settings https://www.postgresql.jp/document/10/html/recovery-target-settings.html

#### Start DB

Start using the normal command. At this point, recovery.conf is referenced to perform recovery.

```sh
pg_ctl start
```

#### Log Output During Recovery

```sh
[2020-03-04 13:34:00 UTC]  18052[1] LOG:  database system was interrupted; last known up at 2020-03-04 13:31:23 UTC
[2020-03-04 13:34:00 UTC]  18052[2] LOG:  starting archive recovery
[2020-03-04 13:34:00 UTC]  18052[3] LOG:  restored log file "00000002.history" from archive
[2020-03-04 13:34:00 UTC]  18052[4] LOG:  restored log file "000000020000000000000050" from archive
[2020-03-04 13:34:00 UTC]  18052[5] LOG:  redo starts at 0/50000028
[2020-03-04 13:34:00 UTC]  18052[6] LOG:  consistent recovery state reached at 0/500000F8
[2020-03-04 13:34:00 UTC]  18050[6] LOG:  database system is ready to accept read only connections
cp: cannot stat '/var/lib/pgsql/10/data/pg_wal/000000020000000000000051': No such file or directory
[2020-03-04 13:34:00 UTC]  18052[7] LOG:  redo done at 0/500000F8
[2020-03-04 13:34:00 UTC]  18052[8] LOG:  restored log file "000000020000000000000050" from archive
cp: cannot stat '/var/lib/pgsql/10/data/pg_wal/00000003.history': No such file or directory
[2020-03-04 13:34:00 UTC]  18052[9] LOG:  selected new timeline ID: 3
[2020-03-04 13:34:01 UTC]  18052[10] LOG:  archive recovery complete
[2020-03-04 13:34:01 UTC]  18052[11] LOG:  restored log file "00000002.history" from archive
[2020-03-04 13:34:01 UTC]  18055[1] LOG:  checkpoint starting: end-of-recovery immediate wait
[2020-03-04 13:34:01 UTC]  18055[2] LOG:  checkpoint complete: wrote 0 buffers (0.0%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.000 s, sync=0.000 s, total=0.004 s; sync files=0, longest=0.000 s, average=0.000 s; distance=16384 kB, estimate=16384 kB
[2020-03-04 13:34:01 UTC]  18050[7] LOG:  database system is ready to accept connections
cp: cannot create regular file '/var/lib/pgsql/10/data/pg_wal/archive/00000003.history': No such file or directory
[2020-03-04 13:34:01 UTC]  18064[1] LOG:  archive command failed with exit code 1
[2020-03-04 13:34:01 UTC]  18064[2] DETAIL:  The failed archive command was: cp pg_wal/00000003.history /var/lib/pgsql/10/data/pg_wal/archive/00000003.history
cp: cannot create regular file '/var/lib/pgsql/10/data/pg_wal/archive/00000003.history': No such file or directory
[2020-03-04 13:34:02 UTC]  18064[3] LOG:  archive command failed with exit code 1
[2020-03-04 13:34:02 UTC]  18064[4] DETAIL:  The failed archive command was: cp pg_wal/00000003.history /var/lib/pgsql/10/data/pg_wal/archive/00000003.history
cp: cannot create regular file '/var/lib/pgsql/10/data/pg_wal/archive/00000003.history': No such file or directory
[2020-03-04 13:34:03 UTC]  18064[5] LOG:  archive command failed with exit code 1
[2020-03-04 13:34:03 UTC]  18064[6] DETAIL:  The failed archive command was: cp pg_wal/00000003.history /var/lib/pgsql/10/data/pg_wal/archive/00000003.history
[2020-03-04 13:34:03 UTC]  18064[7] WARNING:  archiving write-ahead log file "00000003.history" failed too many times, will try again later
```
