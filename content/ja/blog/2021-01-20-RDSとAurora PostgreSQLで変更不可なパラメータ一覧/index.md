---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDSとAurora PostgreSQLで変更不可なパラメータ一覧"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-postgresql-parameter-modifiable.html
date: 2021-01-20
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

# はじめに

AWSのAuroraとRDS PostgreSQLで変更不可なパラメータに結構差異があってハマりそうだったので、差異をメモしておく。下記のコマンドで抽出して、"変更可能"が"FALSE"を一覧化している。

# コマンド

RDS PostgreSQL

```
aws rds describe-db-cluster-parameters --db-cluster-parameter-group-name default.aurora-postgresql11 | jq -r '["名前","値","許可された値","変更可能","送信元","適用タイプ","データ型","説明","ApplyMethod","MinimumEngineVersion"], (.Parameters[] | [.ParameterName,.ParameterValue,.AllowedValues,.IsModifiable,.Source,.ApplyType,.DataType,.Description,.ApplyMethod,.MinimumEngineVersion]) | @csv'
```

Aurora PostgreSQL DBクラスターパラメータグループ

```
aws rds describe-db-cluster-parameters --db-cluster-parameter-group-name default.aurora-postgresql11 | jq -r '["名前","値","許可された値","変更可能","送信元","適用タイプ","データ型","説明","ApplyMethod","MinimumEngineVersion"], (.Parameters[] | [.ParameterName,.ParameterValue,.AllowedValues,.IsModifiable,.Source,.ApplyType,.DataType,.Description,.ApplyMethod,.MinimumEngineVersion]) | @csv'
```

Aurpra PostgreSQL DBパラメータグループ

```
aws rds describe-db-parameters --db-parameter-group-name default.aurora-postgresql11 | jq -r '["名前","値","許可された値","変更可能","送信元","適用タイプ","データ型","説明","ApplyMethod","MinimumEngineVersion"], (.Parameters[] | [.ParameterName,.ParameterValue,.AllowedValues,.IsModifiable,.Source,.ApplyType,.DataType,.Description,.ApplyMethod,.MinimumEngineVersion]) | @csv'
```

# 変更が出来ないパラメータ一覧

PostgreSQL11を対象。"変更可能"が"FALSE"を一覧化。

※実際にパラメータが変更可能となっていても、実際の挙動がどうなるのかは注意が必要なはず。例えば、Auroraはチェックポイントの動きがRDS PostgreSQLと違うので、`full_page_writes`を変更して動作が変わるとは思えない…。

| RDS                            | Aurora(DBクラスターパラメータグループ) | Aurora(DB パラメータグループ)  |
| ------------------------------ | -------------------------------------- | ------------------------------ |
| archive_command                | archive_command                        | checkpoint_timeout             |
| archive_timeout                | archive_timeout                        | config_file                    |
| config_file                    | checkpoint_timeout                     | db_user_namespace              |
| data_directory                 | config_file                            | effective_io_concurrency       |
| db_user_namespace              | data_directory                         | exit_on_error                  |
| exit_on_error                  | db_user_namespace                      | hba_file                       |
| fsync                          | effective_io_concurrency               | hot_standby_feedback           |
| full_page_writes               | exit_on_error                          | ident_file                     |
| hba_file                       | hba_file                               | listen_addresses               |
| ident_file                     | hot_standby_feedback                   | lo_compat_privileges           |
| listen_addresses               | huge_pages                             | log_directory                  |
| lo_compat_privileges           | ident_file                             | log_file_mode                  |
| log_directory                  | listen_addresses                       | log_line_prefix                |
| log_file_mode                  | lo_compat_privileges                   | log_timezone                   |
| logging_collector              | log_directory                          | log_truncate_on_rotation       |
| log_line_prefix                | log_file_mode                          | logging_collector              |
| log_timezone                   | logging_collector                      | rds.superuser_variables        |
| log_truncate_on_rotation       | log_line_prefix                        | restart_after_crash            |
| port                           | log_timezone                           | ssl_ca_file                    |
| rds.extensions                 | log_truncate_on_rotation               | ssl_cert_file                  |
| rds.max_tcp_buffers            | min_wal_size                           | ssl_ciphers                    |
| rds.superuser_variables        | port                                   | ssl_key_file                   |
| restart_after_crash            | rds.extensions                         | stats_temp_directory           |
| server_encoding                | rds.superuser_variables                | superuser_reserved_connections |
| ssl_ca_file                    | restart_after_crash                    | syslog_facility                |
| ssl_cert_file                  | server_encoding                        | unix_socket_directories        |
| ssl_ciphers                    | ssl_ca_file                            | unix_socket_group              |
| ssl_key_file                   | ssl_cert_file                          | unix_socket_permissions        |
| stats_temp_directory           | ssl_ciphers                            | wal_receiver_status_interval   |
| superuser_reserved_connections | ssl_key_file                           |                                |
| syslog_facility                | stats_temp_directory                   |                                |
| unix_socket_directories        | superuser_reserved_connections         |                                |
| unix_socket_group              | syslog_facility                        |                                |
| unix_socket_permissions        | unix_socket_directories                |                                |
| wal_sync_method                | unix_socket_group                      |                                |
|                                | unix_socket_permissions                |                                |
|                                | wal_receiver_status_interval           |                                |



