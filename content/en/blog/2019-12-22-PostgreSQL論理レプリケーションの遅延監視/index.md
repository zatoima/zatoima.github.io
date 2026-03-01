---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Monitoring Lag in PostgreSQL Logical Replication"
subtitle: ""
summary: " "
tags: ["AWS", "Aurora", "RDS", "PostgreSQL"]
categories: ["AWS", "Aurora", "RDS", "PostgreSQL"]
url: postgresql-logical-replication-monitoring.html
date: 2019-12-22
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

***

Organizing lag monitoring for logical replication. The environment uses AWS Aurora and RDS PostgreSQL-compatible, version 10.7.

<br/>

#### Check WAL Read Position

***

```sql
repdb=> select pg_current_wal_lsn();
-[ RECORD 1 ]------+----------
pg_current_wal_lsn | 0/4F94888
```

<br/>

#### Check Replication Lag

***

Check the pg_stat_replication view on the Publisher side.

```sql
\x
select * from pg_stat_replication;

repdb=> select * from pg_stat_replication;
-[ RECORD 1 ]----+------------------------------
pid              | 19407
usesysid         | 16393
usename          | postgres
application_name | auroratopostgresql
client_addr      | xxx.xxx.xxx.xx
client_hostname  |
client_port      | 46478
backend_start    | 2019-12-14 09:24:19.187306+00
backend_xmin     |
state            | streaming
sent_lsn         | 0/4F67640
write_lsn        | 0/4F67640
flush_lsn        | 0/4F67640
replay_lsn       | 0/4F67640
write_lag        | 00:00:01.582706
flush_lag        | 00:00:01.985095
replay_lag       | 00:00:01.582706
sync_priority    | 0
sync_state       | async

repdb=>
```

WAL log positions are important. The position can be identified from sent_lsn, write_lsn, flush_lsn, replay_lsn, etc.

| Column     | Type   | Description                                                                              |
| ---------- | ------ | ---------------------------------------------------------------------------------------- |
| sent_lsn   | pg_lsn | Last write-ahead log location sent on this connection.                                   |
| write_lsn  | pg_lsn | Last write-ahead log location written to disk by this standby server.                   |
| flush_lsn  | pg_lsn | Last write-ahead log location flushed to disk by this standby server.                   |
| replay_lsn | pg_lsn | Last write-ahead log location replayed into the database on this standby server.         |

> 28.2. Statistics Collector https://www.postgresql.jp/document/10/html/monitoring-stats.html#PG-STAT-REPLICATION-VIEW

The relationship between sent_lsn, write_lsn, flush_lsn, and replay_lsn is expected to be as follows (**requires verification**). Using these LSN positions, you can identify whether the problem lies on the Publisher side, the network, or in the Subscriber's apply process.

<img src="image-20191222184441556.png" alt="image-20191222184441556" style="zoom:50%;" />

The state column also shows the WAL sender state:

> Current state of the WAL sender. Possible values are:
>
> - startup: This WAL sender is starting up.
> - catchup: This WAL sender's connected standby is trying to catch up with the primary.
> - streaming: This WAL sender is streaming changes after its connected standby server has caught up with the primary.
> - backup: This WAL sender is sending a backup.
> - stopping: This WAL sender is stopping.

That said, from a lag monitoring perspective, the update frequency of pg_stat_replication is "when the write or flush lsn position changes" or "the number of seconds specified by wal_receiver_status_interval," so it's better to use the method described below for judgment. Since wal_receiver_status_interval defaults to 10 seconds, it's possible that the WAL application has finished but pg_stat_replication hasn't been updated yet. You can only see the result after the 10-second wal_receiver_status_interval has elapsed and you query pg_stat_replication. In environments where wal_receiver_status_interval has been adjusted or where replication is constantly running, this view should be useful.

Since PostgreSQL LSN values are hexadecimal, comparing positions can sometimes be unclear. In that case, use the `pg_wal_lsn_diff` function. Note that the output is in bytes.

> https://www.postgresql.jp/document/10/html/functions-admin.html
>
> pg_wal_lsn_diff calculates the difference in bytes between two write-ahead log locations. It can be used together with pg_stat_replication or the functions shown in Table 9.79 to confirm replication lag.

```sql
SELECT
    pg_wal_lsn_diff(sent_lsn,write_lsn) write_diff,
    pg_wal_lsn_diff(sent_lsn,flush_lsn) flush_diff,
    pg_wal_lsn_diff(sent_lsn,replay_lsn) replay_diff
FROM
    pg_stat_replication;
```

1.) When there is a difference:

```sql
repdb=> select pg_wal_lsn_diff(sent_lsn,write_lsn) write_diff, pg_wal_lsn_diff(sent_lsn, flush_lsn) flush_diff, pg_wal_lsn_diff(sent_lsn,replay_lsn) replay_diff from pg_stat_replication;
-[ RECORD 1 ]---------
write_diff  | 26749408
flush_diff  | 26749408
replay_diff | 26749408
```

2.) When there is no difference:

```sql
repdb=> select pg_wal_lsn_diff(sent_lsn,write_lsn) write_diff, pg_wal_lsn_diff(sent_lsn, flush_lsn) flush_diff, pg_wal_lsn_diff(sent_lsn,replay_lsn) replay_diff from pg_stat_replication;
-[ RECORD 1 ]--
write_diff  | 0
flush_diff  | 0
replay_diff | 0
```

<br/>

On the Subscriber side, you can check using the following method. Since it shows time, it's more intuitive.

```sql
repdb=> select * from pg_stat_subscription;
-[ RECORD 1 ]---------+------------------------------
subid                 | 16425
subname               | auroratopostgresql
pid                   | 15008
relid                 |
received_lsn          | 0/4F87048
last_msg_send_time    | 2019-12-14 09:40:29.125815+00
last_msg_receipt_time | 2019-12-14 09:40:29.135405+00
latest_end_lsn        | 0/4F87048
latest_end_time       | 2019-12-14 09:40:29.125815+00
```
