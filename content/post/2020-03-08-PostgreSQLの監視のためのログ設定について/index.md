---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLの監視のためのログ設定について"
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



### はじめに

監視には「レスポンス問題発生の予測」、「問題発生時の原因特定」という大きな目的があります。定期的なデータベース稼働に関するヘルスチェックを行う場合に、必要な情報が取得出来ていなければなりません。今回はログ出力の観点から代表的なPostgreSQLのログ管理の代表的なパラメータをまとめてみます。

### バージョン情報

```sh
pgbench=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### log関連の代表的なパラメータ一覧

| パラメータ名                       | 観点               | デフォルト値      | 内容                                                         |
| ---------------------------------- | ------------------ | ----------------- | ------------------------------------------------------------ |
| log_destination                    | ログ取得・配置     | stderr            | stderr,csvlog,syslogの設定                                   |
| logging_collector                  | ログ取得・配置     | on                | stderr,csvlogの内容をリダイレクトするかどうか                |
| log_directory                      | ログ取得・配置     | log               | どのディレクトリにログ・ファイルを格納するか                 |
| log_filename                       | ログ取得・配置     | postgresql-%a.log | ファイル名の指定                                             |
| client_min_messages                | ログ取得タイミング | notice            | クライアントに送信するレベル設定。DEBUG5、 DEBUG4、DEBUG3、DEBUG2、  DEBUG1、LOG、NOTICE、 WARNING、ERROR、FATAL、およびPANICから選ぶ。 |
| log_min_messages                   | ログ取得タイミング | warning           | サーバログに書き込むためのレベル設定。DEBUG5、  DEBUG4、DEBUG3、DEBUG2、 DEBUG1、LOG、NOTICE、 WARNING、ERROR、FATAL、およびPANICから選ぶ。 |
| log_min_error_statement            | ログ取得タイミング | error             | サーバログにエラーとなったSQLを書き込む際のレベル設定        |
| log_min_duration_statement         | ログ取得タイミング | -1                | 指定した以上に実行に時間が掛かったSQLをサーバログに書き込むための設定。単位はミリ秒。 |
| log_temp_files                     | ログ取得タイミング | -1                | 指定したサイズ以上の一時ファイルが作成された場合ログに記録。単位はKB。 |
| log_statement                      | ログ取得タイミング | -1                | どのSQL文をログに記録するかを制御します。 有効な値は、none（off）、ddl、mod、およびall（全てのメッセージ）。modは、全てのddl文に加え、INSERT、UPDATE、DELETE、TRUNCATE、およびCOPY FROMといった、データ変更文をログに記録。 PREPAREとEXPLAIN ANALYZEコマンドも、そこに含まれるコマンドが適切な種類であればログが取得。 |
| log_checkpoints                    | ログ取得対象       | off               | チェックポイントに関する情報を出力する                       |
| log_connections/log_disconnections | ログ取得対象       | off               | サーバへの接続/切断情報を記載する                            |
| log_lock_waits                     | ログ取得対象       | off               | ロック獲得のために一定時間待たされた場合に出力する。時間はdeadlock_timeoutパラメータで指定。 |
| log_line_prefix                    | ログ取得対象       | %m [%p]           | 各ログの先頭に出力する情報を設定。  %u:ユーザ名、%d:データベース名、%r:ホスト名/IPアドレス、ポート番号、%m:ミリ秒付きタイムスタンプ |
| log_rotation_age                   | ログメンテナンス   | 1d                | 指定した時間でログ・ファイルをハウスキーピングする           |
| log_rotation_size                  | ログメンテナンス   | 0                 | 指定したサイズでログ・ファイルをハウスキーピングする         |
| log_truncate_on_rotation           | ログメンテナンス   | on                | ハウスキーピング時に同じログ・ファイルが存在する場合に追記するか上書きするか設定 |
| log_file_mode                      | その他             | 600               | ログ・ファイルのパーミッションを指定                         |

全パラメータはマニュアルをご参照ください。

> 19.8. エラー報告とログ取得 https://www.postgresql.jp/document/10/html/runtime-config-logging.html

### postgresql.conf

デフォルトの監視設定は最低限です。スロークエリの監視、チェックポイント頻度の監視、接続情報、一時ファイルの生成頻度、生成量の監視は必要かと思います。あとはファイル名、及びファイルに書き込まれる接頭辞は必要に応じて変更してもらえれば良いと思います。"#"にてコメントしているところはデフォルトから変更しているところとなります。

```sh
log_destination=stderr
logging_collector=on
log_directory=log
log_filename='postgresql-%Y%m%d.log' #ファイル名の変更
client_min_messages=notice
log_min_messages=warning
log_min_error_statement=error
log_min_duration_statement=3000 #スロークエリの検知
log_checkpoints=on #チェックポイントの頻度の確認のために有効化
log_connections=on #クライアントからの接続情報をログに書き込む
log_disconnections=on #クライアントからの切断情報をログに書き込む
log_temp_files=1024 #一時ファイル生成時にログに書き込む
log_statement=ddl #DDLの実行をログに書き込む
log_lock_waits=off
log_line_prefix='[%t]%u %d %p[%l] ' #接頭辞のカスタマイズ
log_rotation_age=1d
log_rotation_size=0
log_truncate_on_rotation=on
log_file_mode=0644 #postgresユーザ以外に読取り権限を付与。ログ監視を想定。
```

デフォルトから変更した一つ一つパラメータの効果を見ていきます。

##### ファイル名の変更 ▶ log_filename='postgresql-%Y%m%d.log'

ファイル名に日付が付くようになりました。

```sh
-rw-r----- 1 postgres postgres    534 Mar  3 03:05 postgresql-20200303.log
```

##### スロークエリの検知 ▶ log_min_duration_statement=3000

設定した3000ミリ秒（3秒）以上のクエリを実行した場合、下記のようにSQL文とdurationが出力されます。実行計画を合わせて確認したい場合は、auro_explainの拡張機能と合わせてどうぞ。

```sh
[2020-03-03 03:15:03 UTC]postgres postgres 2457[13] LOG:  duration: 6695.655 ms  statement: select count(*) from t1,t2;
```

> PostgreSQLのauto_explainで特定クエリの実行計画を出力する | my opinion is my own https://zatoima.github.io/postgresql-about-auto_explain.html

##### チェックポイントの頻度の確認のために有効化 ▶ log_checkpoints

チェックポイントに関する情報が出力されます。

```sh
[2020-03-03 03:40:43 UTC]  2558[3] LOG:  checkpoint starting: time
[2020-03-03 03:41:12 UTC]  2558[4] LOG:  checkpoint complete: wrote 289 buffers (1.8%); 0 WAL file(s) added, 0 removed, 0 recycled; write=28.864 s, sync=0.000 s, total=28.869 s; sync files=24, longest=0.000 s, average=0.000 s; distance=3312 kB, estimate=3312 kB
```

##### クライアントからの接続情報 ▶ log_connections

```sh
[2020-03-03 03:13:20 UTC][unknown] [unknown] 2450[1] LOG:  connection received: host=[local]
[2020-03-03 03:13:20 UTC]postgres postgres 2450[2] LOG:  connection authorized: user=postgres database=postgres
```

クライアントからの切断情報 ▶ log_disconnections

```sh
[2020-03-03 03:14:04 UTC]postgres postgres 2450[3] LOG:  disconnection: session time: 0:00:44.331 user=postgres database=postgres host=[local]
```

##### 一時ファイル生成時にログに書き込む ▶ log_temp_files

省略。

##### DDLの実行をログに書き込む ▶ log_statement

```sh
[2020-03-03 03:23:12 UTC]postgres postgres 2567[11] LOG:  statement: create table t3(a numeric);
```

##### 接頭辞のカスタマイズ ▶ log_line_prefix

`[2020-03-03 03:13:20 UTC]postgres postgres 2450[2]`が出るようになった。接続元が仮に多い場合はホスト名も出るように設定しても良いかも。

```sh
[2020-03-03 03:13:20 UTC]postgres postgres 2450[2] LOG:  connection authorized: user=postgres database=postgres
```

##### postgresユーザ以外に読取り権限を付与 ▶ log_file_mode

groupに読取り権限が付くようになりました。

```sh
-rw-r----- 1 postgres postgres    534 Mar  3 03:05 postgresql-20200303.log
```













