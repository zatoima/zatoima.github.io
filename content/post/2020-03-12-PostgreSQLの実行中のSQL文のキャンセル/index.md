---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLの実行中のSQLをキャンセルする"
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



### 長時間掛かるクエリ実行

直積結合して件数カウント。

```sql
select count(*) from t1,t2,t3,t4,t5;
```

### 実行中のSQLの確認

```sql
postgres=# select pid,query_start,state,query from pg_stat_activity order by query_start asc limit 5;
 pid  |          query_start          | state  |                                           query                                            
------+-------------------------------+--------+---------------------------------------------------------------------------------------
 2567 | 2020-03-03 03:39:22.744191+00 | active | select count(*) from t1,t2,t3,t4,t5;
 2863 | 2020-03-03 03:44:25.423124+00 | active | select pid,query_start,state,query from pg_stat_activity order by query_start asc limit 5;
```

### 実行中のSQLのキャンセル

下記の関数でキャンセル可能。pg_cancel_backendはSIGINT。pg_terminate_backendはSIGTERMのシグナルをサーバ側に送る模様。

> 9.26. システム管理関数 https://www.postgresql.jp/document/10/html/functions-admin.html#FUNCTIONS-ADMIN-SIGNAL-TABLE

| 名前                            | 戻り型  | 説明                                                         |
| ------------------------------- | ------- | ------------------------------------------------------------ |
| pg_cancel_backend(*pid* int)    | boolean | バックエンドの現在の問い合わせを取り消す。  関数を呼ぶユーザが取り消す対象のバックエンドのロールのメンバーであるとき、あるいはpg_signal_backendの権限を与えられているときも実行できます。 ただし、スーパーユーザのバックエンドはスーパーユーザのみが取り消せます。 |
| pg_terminate_backend(*pid* int) | boolean | バックエンドを終了する。  関数を呼ぶユーザが終了対象のバックエンドのロールのメンバーであるとき、あるいはpg_signal_backendの権限を与えられているときも実行できます。 ただし、スーパーユーザのバックエンドはスーパーユーザのみが終了できます。 |

##### pg_cancel_backend関数

バックエンドの現在の問い合わせを取り消す。実行した場合、SQL実行はキャンセルするが、接続したまま。

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

##### pg_terminate_backend関数

pg_terminate_backendは接続自体を切断され、その後に再接続がされる。

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





