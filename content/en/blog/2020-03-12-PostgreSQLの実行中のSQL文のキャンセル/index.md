---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Canceling Running SQL Statements in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-sql-statement-cancell.html
date: 2020-03-12
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



### Running a Long-Running Query

Performing a cross join and counting the results.

```sql
select count(*) from t1,t2,t3,t4,t5;
```

### Checking Running SQL

```sql
postgres=# select pid,query_start,state,query from pg_stat_activity order by query_start asc limit 5;
 pid  |          query_start          | state  |                                           query
------+-------------------------------+--------+---------------------------------------------------------------------------------------
 2567 | 2020-03-03 03:39:22.744191+00 | active | select count(*) from t1,t2,t3,t4,t5;
 2863 | 2020-03-03 03:44:25.423124+00 | active | select pid,query_start,state,query from pg_stat_activity order by query_start asc limit 5;
```

### Canceling Running SQL

The following functions can be used to cancel queries. pg_cancel_backend sends SIGINT, and pg_terminate_backend appears to send a SIGTERM signal to the server.

> 9.26. System Administration Functions https://www.postgresql.jp/document/10/html/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL-TABLE

| Name                            | Return Type | Description                                                  |
| ------------------------------- | ----------- | ------------------------------------------------------------ |
| pg_cancel_backend(*pid* int)    | boolean     | Cancel the current query of the backend. Can also be executed when the calling user is a member of the role of the backend being canceled, or has been granted pg_signal_backend privileges. However, only a superuser can cancel a superuser's backend. |
| pg_terminate_backend(*pid* int) | boolean     | Terminate the backend. Can also be executed when the calling user is a member of the role of the backend being terminated, or has been granted pg_signal_backend privileges. However, only a superuser can terminate a superuser's backend. |

##### pg_cancel_backend Function

Cancels the current query of the backend. When executed, the SQL execution is canceled but the connection remains.

```sh
select pg_cancel_backend(2567);

postgres=# select pg_cancel_backend(2567);
 pg_cancel_backend
-------------------
 t
(1 row)

-- terminal
postgres=# select count(*) from t1,t2,t3,t4,t5;

ERROR:  canceling statement due to user request

-- log
[2020-03-03 03:52:20 UTC]postgres postgres 2567[27] ERROR:  canceling statement due to user request
[2020-03-03 03:52:20 UTC]postgres postgres 2567[28] STATEMENT:  select count(*) from t1,t2,t3,t4,t5;
```

##### pg_terminate_backend Function

pg_terminate_backend disconnects the connection itself, after which a reconnection is made.

```sh
select pg_terminate_backend(2567);

postgres=# select pg_terminate_backend(2567);
 pg_terminate_backend
----------------------
 t
(1 row)

-- terminal
postgres=# select count(*) from t1,t2,t3,t4,t5;
FATAL:  terminating connection due to administrator command
server closed the connection unexpectedly
	This probably means the server terminated abnormally
	before or while processing the request.
The connection to the server was lost. Attempting reset: Succeeded.

-- log
[2020-03-03 03:54:14 UTC]postgres postgres 2567[29] FATAL:  terminating connection due to administrator command
[2020-03-03 03:54:14 UTC]postgres postgres 2567[30] STATEMENT:  select count(*) from t1,t2,t3,t4,t5;
[2020-03-03 03:54:14 UTC]postgres postgres 2567[31] LOG:  disconnection: session time: 0:33:20.877 user=postgres database=postgres host=[local]
[2020-03-03 03:54:14 UTC][unknown] [unknown] 2918[1] LOG:  connection received: host=[local]
[2020-03-03 03:54:14 UTC]postgres postgres 2918[2] LOG:  connection authorized: user=postgres database=postgres
```
