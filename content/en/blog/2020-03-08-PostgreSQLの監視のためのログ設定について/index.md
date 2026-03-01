---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQL Log Configuration for Monitoring"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-monitoring-log.html
date: 2020-03-08
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



### Introduction

Monitoring has two primary purposes: "predicting response issues before they occur" and "identifying the cause when an issue occurs." When performing regular health checks on database operations, it is essential to be able to retrieve the necessary information. Here I will summarize the key PostgreSQL log management parameters from the perspective of log output.

### Version Information

```sh
pgbench=# select version();
                                                 version
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### List of Key Log-Related Parameters

| Parameter Name                     | Category           | Default Value     | Description                                                  |
| ---------------------------------- | ------------------ | ----------------- | ------------------------------------------------------------ |
| log_destination                    | Log collection/placement | stderr       | Settings for stderr, csvlog, syslog                         |
| logging_collector                  | Log collection/placement | on           | Whether to redirect stderr/csvlog content                   |
| log_directory                      | Log collection/placement | log          | Which directory to store log files in                       |
| log_filename                       | Log collection/placement | postgresql-%a.log | Specifies the file name                                  |
| client_min_messages                | Log collection timing | notice          | Level setting for messages sent to the client. Choose from DEBUG5, DEBUG4, DEBUG3, DEBUG2, DEBUG1, LOG, NOTICE, WARNING, ERROR, FATAL, and PANIC. |
| log_min_messages                   | Log collection timing | warning         | Level setting for writing to the server log. Choose from DEBUG5, DEBUG4, DEBUG3, DEBUG2, DEBUG1, LOG, NOTICE, WARNING, ERROR, FATAL, and PANIC. |
| log_min_error_statement            | Log collection timing | error           | Level setting for writing SQL that resulted in an error to the server log |
| log_min_duration_statement         | Log collection timing | -1              | Setting for writing SQL that took longer than the specified time to the server log. Unit is milliseconds. |
| log_temp_files                     | Log collection timing | -1              | Logs when a temporary file larger than the specified size is created. Unit is KB. |
| log_statement                      | Log collection timing | -1              | Controls which SQL statements are logged. Valid values are none (off), ddl, mod, and all (all messages). mod logs all ddl statements plus data modification statements like INSERT, UPDATE, DELETE, TRUNCATE, and COPY FROM. PREPARE and EXPLAIN ANALYZE commands are also logged if the commands they contain are of the appropriate type. |
| log_checkpoints                    | Log target         | off               | Outputs information about checkpoints                       |
| log_connections/log_disconnections | Log target         | off               | Records connection/disconnection information to the server  |
| log_lock_waits                     | Log target         | off               | Outputs when waiting a certain time to acquire a lock. Time is specified by the deadlock_timeout parameter. |
| log_line_prefix                    | Log target         | %m [%p]           | Sets the information output at the beginning of each log line. %u: username, %d: database name, %r: hostname/IP address, port number, %m: timestamp with milliseconds |
| log_rotation_age                   | Log maintenance    | 1d                | Housekeeps log files at the specified time interval         |
| log_rotation_size                  | Log maintenance    | 0                 | Housekeeps log files at the specified size                  |
| log_truncate_on_rotation           | Log maintenance    | on                | Sets whether to append or overwrite when the same log file exists during housekeeping |
| log_file_mode                      | Other              | 600               | Specifies the permissions for log files                     |

Please refer to the manual for all parameters.

> 19.8. Error Reporting and Logging https://www.postgresql.jp/document/10/html/runtime-config-logging.html

### postgresql.conf

The default monitoring settings are minimal. I think you need to monitor slow queries, checkpoint frequency, connection information, temporary file creation frequency, and creation volume. The file name and the prefix written to the file can be changed as needed. Lines with "#" comments indicate settings changed from the default.

```sh
log_destination=stderr
logging_collector=on
log_directory=log
log_filename='postgresql-%Y%m%d.log' #Change file name
client_min_messages=notice
log_min_messages=warning
log_min_error_statement=error
log_min_duration_statement=3000 #Detect slow queries
log_checkpoints=on #Enable to check checkpoint frequency
log_connections=on #Write client connection information to log
log_disconnections=on #Write client disconnection information to log
log_temp_files=1024 #Write to log when a temporary file is created
log_statement=ddl #Write DDL execution to log
log_lock_waits=off
log_line_prefix='[%t]%u %d %p[%l] ' #Customize prefix
log_rotation_age=1d
log_rotation_size=0
log_truncate_on_rotation=on
log_file_mode=0644 #Grant read permissions to users other than postgres. Assumes log monitoring.
```

Let's look at the effect of each parameter changed from the default.

##### Change File Name - log_filename='postgresql-%Y%m%d.log'

The file name now includes the date.

```sh
-rw-r----- 1 postgres postgres    534 Mar  3 03:05 postgresql-20200303.log
```

##### Detect Slow Queries - log_min_duration_statement=3000

When a query takes longer than the set 3000 milliseconds (3 seconds), the SQL statement and duration are output as shown below. If you want to also check the execution plan, use it together with the auto_explain extension.

```sh
[2020-03-03 03:15:03 UTC]postgres postgres 2457[13] LOG:  duration: 6695.655 ms  statement: select count(*) from t1,t2;
```

> Outputting Execution Plans for Specific Queries with PostgreSQL's auto_explain | my opinion is my own https://zatoima.github.io/postgresql-about-auto_explain.html

##### Enable to Check Checkpoint Frequency - log_checkpoints

Information about checkpoints is output.

```sh
[2020-03-03 03:40:43 UTC]  2558[3] LOG:  checkpoint starting: time
[2020-03-03 03:41:12 UTC]  2558[4] LOG:  checkpoint complete: wrote 289 buffers (1.8%); 0 WAL file(s) added, 0 removed, 0 recycled; write=28.864 s, sync=0.000 s, total=28.869 s; sync files=24, longest=0.000 s, average=0.000 s; distance=3312 kB, estimate=3312 kB
```

##### Client Connection Information - log_connections

```sh
[2020-03-03 03:13:20 UTC][unknown] [unknown] 2450[1] LOG:  connection received: host=[local]
[2020-03-03 03:13:20 UTC]postgres postgres 2450[2] LOG:  connection authorized: user=postgres database=postgres
```

Client Disconnection Information - log_disconnections

```sh
[2020-03-03 03:14:04 UTC]postgres postgres 2450[3] LOG:  disconnection: session time: 0:00:44.331 user=postgres database=postgres host=[local]
```

##### Write to Log When a Temporary File is Created - log_temp_files

Omitted.

##### Write DDL Execution to Log - log_statement

```sh
[2020-03-03 03:23:12 UTC]postgres postgres 2567[11] LOG:  statement: create table t3(a numeric);
```

##### Customize Prefix - log_line_prefix

`[2020-03-03 03:13:20 UTC]postgres postgres 2450[2]` is now output. If there are many connection sources, it might be good to also include the hostname.

```sh
[2020-03-03 03:13:20 UTC]postgres postgres 2450[2] LOG:  connection authorized: user=postgres database=postgres
```

##### Grant Read Permissions to Users Other Than postgres - log_file_mode

The group now has read permissions.

```sh
-rw-r----- 1 postgres postgres    534 Mar  3 03:05 postgresql-20200303.log
```
