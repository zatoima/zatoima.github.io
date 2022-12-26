---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "log_fdw拡張機能を使用してAurora PostgreSQLのログを分析する"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-log_fdw-analyze-postgreslog.html
date: 2020-12-08
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

PostgreSQLのログをSQLベースで分析出来たら良いなって思ったのが始まり。調べて見ると便利な拡張機能があったのでメモ。

#### 拡張機能の有効化

```sql
CREATE EXTENSION log_fdw;
```

#### 外部データラッパーとしてログサーバーを作成

```sql
CREATE SERVER log_server FOREIGN DATA WRAPPER log_fdw;
```

#### ログファイルのリストを取得

```sql
SELECT * from list_postgres_log_files() order by 1;
SELECT * FROM list_postgres_log_files() WHERE file_name LIKE 'postgresql.log.%.csv' ORDER BY 1 DESC;
```

#### ログをインプットにテーブルを作成

```sql
SELECT create_foreign_table_for_log_file('postgresql_log_20201206', 'log_server', 'postgresql.log.2020-12-06.csv');  
```

#### 作成される外部テーブルと各カラムに入るサンプルデータ

| カラム例               | サンプル例                                         |
| ---------------------- | -------------------------------------------------- |
| log_time               | 2020-12-06 09:02:55.872+00                         |
| user_name              | postgres                                           |
| database_name          | postgres                                           |
| process_id             | 32418                                              |
| connection_from        | 10-0-1-123                                         |
| session_id             | 5fcc9e3f.7ea2                                      |
| session_line_num       | 2                                                  |
| command_tag            | authentication                                     |
| session_start_time     | 2020-12-06 09:02:55+00                             |
| virtual_transaction_id | 8/65                                               |
| transaction_id         | 0                                                  |
| error_severity         | FATAL                                              |
| sql_state_code         | 28P01                                              |
| message                | password authentication failed for user "postgres" |
| detail                 | Password does not match for user "postgres".       |
| hint                   |                                                    |
| internal_query         |                                                    |
| internal_query_pos     |                                                    |
| context                |                                                    |
| query                  |                                                    |
| query_pos              |                                                    |
| location               |                                                    |
| application_name       |                                                    |

#### ログの中身を確認

```sql
select * from postgresql_log_20201206;
```

#### 特定サーバからログイン失敗した回数を確認

```sql
select count(*) from postgresql_log_20201206 where connection_from like '10.0.1.123%' and message like '%password authentication failed %';
```

#### 不要になった外部テーブルを削除

```sql
DROP FOREIGN TABLE postgresql_log_20201206;
```

#### 参考

> https://aws.amazon.com/jp/blogs/news/working-with-rds-and-aurora-postgresql-logs-part-2/
>
> log_fdw を使用して外部テーブル経由でログデータを表示する

