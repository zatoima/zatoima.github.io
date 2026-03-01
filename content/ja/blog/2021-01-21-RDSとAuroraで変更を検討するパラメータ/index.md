---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDSとAuroraで変更を検討するパラメータ(PostgreSQL)"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-postgresql-parameter-change.html
date: 2021-01-21
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

AuroraやRDSはマネージド・サービスなので、パラメータチューニングが不要だが、要件や性能問題次第ではチューニングの必要があるのでそれをまとめたい。

# 変更を検討するパラメータ一覧

気付いたら都度追加していく。現在のパラメータ(setting列)は、Aurora、RDS共に`r5.large`のインスタンスタイプから抽出

変更を検討するパラメータと書きつつ、AuroraとRDSで変更可能なパラメータも異なり、変更できないものもあるので注意。checkpoint_timeout等はチェックポイントチューニングでいじるところではあるが、RDSは変更出来て、Auroraでは変更出来ない模様。

> RDSとAurora PostgreSQLで変更不可なパラメータ一覧 | my opinion is my own https://zatoima.github.io/aws-aurora-rds-postgresql-parameter-modifiable.html

| name                             | setting(Aurora)              | setting(RDS)               | boot_val                       | unit | context       |
| -------------------------------- | ---------------------------- | -------------------------- | ------------------------------ | ---- | ------------- |
| archive_timeout                  | 300 ※変更不可                | 300 ※変更不可              | 0                              | s    | sighup        |
| autovacuum_max_workers           | 3                            | 3                          | 3                              |      | postmaster    |
| checkpoint_completion_target     | 0.5                          | 0.9                        | 0.5                            |      | sighup        |
| checkpoint_timeout               | 60                           | 300 ※変更不可              | 300                            | s    | sighup        |
| deadlock_timeout                 | 1000                         | 1000                       | 1000                           | ms   | superuser     |
| effective_io_concurrency         | 256                          | 1 ※変更不可                | 256                            |      | user          |
| lc_messages                      |                              |                            |                                |      | superuser     |
| log_filename                     | postgresql.log.%Y-%m-%d-%H%M | postgresql.log.%Y-%m-%d-%H | postgresql-%Y-%m-%d_%H%M%S.log |      | sighup        |
| log_hostname                     | off                          | on                         | off                            |      | sighup        |
| log_min_duration_statement       | -1                           | -1                         | -1                             | ms   | rds_superuser |
| log_rotation_age                 | 60                           | 60                         | 1440                           | min  | sighup        |
| log_rotation_size                | 100000                       | 10240                      | 10240                          | kB   | sighup        |
| log_timezone                     | UTC ※変更不可                | UTC ※変更不可              | GMT                            |      | sighup        |
| max_connections                  | 1710                         | 1710                       | 100                            |      | postmaster    |
| max_parallel_maintenance_workers | 2                            | 2                          | 2                              |      | user          |
| max_parallel_workers             | 8                            | 8                          | 8                              |      | user          |
| max_parallel_workers_per_gather  | 2                            | 2                          | 2                              |      | user          |
| max_worker_processes             | 8                            | 8                          | 8                              |      | postmaster    |
| random_page_cost                 | 4                            | 4                          | 4                              |      | user          |
| shared_buffers                   | 1304235                      | 497507                     | 1024                           | 8kB  | postmaster    |
| superuser_reserved_connections   | 3                            | 3                          | 3                              |      | postmaster    |
| wal_buffers                      | 2048                         | 8192                       | -1                             | 8kB  | postmaster    |

# 抽出用SQL

```sql
SELECT
    name,
    setting,
    boot_val,
    unit,
    context
FROM
    pg_settings
WHERE
    name IN ('max_connections','superuser_reserved_connections','lc_messages','archive_timeout','log_filename','log_rotation_age','log_rotation_size','log_min_duration_statement','log_hostname','log_timezone','shared_buffers','effective_io_concurrency','max_worker_processes','max_parallel_maintenance_workers','max_parallel_workers_per_gather','max_parallel_workers','wal_buffers','checkpoint_timeout','checkpoint_completion_target','random_page_cost','autovacuum_max_workers','deadlock_timeout')
ORDER BY 1;
```

# パラメータ個別メモ

#### deadlock_timeout

デッドロックの検査は負荷が高いので、デフォルトの1000ms(1秒)より上げても良い。

#### checkpoint_completion_target

#### checkpoint_timeout

AuroraとRDSでデフォルトの設定値が異なる。パフォーマンス問題が発生した場合に変更する方向。

※Auroraはチェックポイント自体の概念が無く、log_bufferに入ってきたメモリは都度ストレージ側に流れていくはずなので、変更の意味があるかは不明。

> PostgreSQLのcheckpoint_completion_targetについてメモ | my opinion is my own https://zatoima.github.io/postgresql-about-checkpoint_completion_target.html

#### log_filename

#### log_hostname

#### log_min_duration_statement

#### log_rotation_age

#### log_rotation_size

#### log_timezone

ログ要件に応じて変更

#### max_connections

OSS版のPostgreSQLの`100`と比較するとパラメータは調整されているが、コネクション数自体は要件次第。インスタンスタイプをスケールアップするとmax_connectionsも一緒に上がっていく。

#### autovacuum_max_workers

#### max_parallel_maintenance_workers

#### max_parallel_workers

#### max_parallel_workers_per_gather

#### max_worker_processes

VacuumやAnalyzeのチューニング時に微調整

#### shared_buffers

Auroraの場合は、DB パラメータグループでのデフォルト値は全メモリの75%に設定される。これは、Aurora PostgreSQLがダブルバッファリングを使用しておらず、OS側のファイルシステムキャッシュが必要ないため。他のメモリ系パラメータに振った方が良ければ微調整。

> Shared_Buffers DB パラメータのデフォルト値と Amazon RDS PostgreSQL および Aurora PostgreSQL の間に差がある理由を理解する https://aws.amazon.com/jp/premiumsupport/knowledge-center/rds-aurora-postgresql-shared-buffers/

#### wal_buffers

未だディスクに書き込まれていないWALデータに対して使用される共有メモリ容量。commit時にこのバッファからディスクに書き込まれる。書き込みが多く、CPUが多い場合は数MBに拡張することで効果は得られるが、Aurora、RDS共に基本的にはデフォルト値で問題無さそう。

#### random_page_cost

非シーケンシャル的に取り出されるディスクページのコストに対するプランナの推測を設定。この値を小さくすることで相対的にインデックススキャンを行うことになる。一般的にランダムリードに関してはHDDよりSDDの方が早いので、SSDの場合は`1.0`等に設定することもある。場合によってはデフォルトの4.0より下げても良いかも。

# インスタンスタイプのスケールアップで変わるパラメータは？

上記のパラメータを対象に何が変わるのか調べてみた。`max_connections`や`shared_buffers`は変更される。一方でCPU、メモリが増えているにも関わらず、パラレル度の指定やwal_buffers等には変更がない。

| name                             | setting(Aurora)<br />※r5.large | setting(Aurora)<br />※r5.2xlarge | setting(RDS)<br />※r5.large | setting(RDS)<br />※r5.2xlarge |
| -------------------------------- | ------------------------------ | -------------------------------- | --------------------------- | ----------------------------- |
| archive_timeout                  | 300                            | 300                              | 300                         | 300                           |
| autovacuum_max_workers           | 3                              | 3                                | 3                           | 3                             |
| checkpoint_completion_target     | 0.5                            | 0.5                              | 0.9                         | 0.9                           |
| checkpoint_timeout               | 60                             | 60                               | 300                         | 300                           |
| deadlock_timeout                 | 1000                           | 1000                             | 1000                        | 1000                          |
| effective_io_concurrency         | 256                            | 256                              | 1                           | 1                             |
| lc_messages                      |                                |                                  |                             |                               |
| log_filename                     | postgresql.log.%Y-%m-%d-%H%M   | postgresql.log.%Y-%m-%d-%H%M     | postgresql.log.%Y-%m-%d-%H  | postgresql.log.%Y-%m-%d-%H    |
| log_hostname                     | off                            | off                              | on                          | on                            |
| log_min_duration_statement       | -1                             | -1                               | -1                          | -1                            |
| log_rotation_age                 | 60                             | 60                               | 60                          | 60                            |
| log_rotation_size                | 100000                         | 100000                           | 10240                       | 10240                         |
| log_timezone                     | UTC                            | UTC                              | UTC                         | UTC                           |
| max_connections                  | 1710                           | 5000                             | 1710                        | 5000                          |
| max_parallel_maintenance_workers | 2                              | 2                                | 2                           | 2                             |
| max_parallel_workers             | 8                              | 8                                | 8                           | 8                             |
| max_parallel_workers_per_gather  | 2                              | 2                                | 2                           | 2                             |
| max_worker_processes             | 8                              | 8                                | 8                           | 8                             |
| random_page_cost                 | 4                              | 4                                | 4                           | 4                             |
| shared_buffers                   | 1304235                        | 5474754                          | 497507                      | 2029633                       |
| superuser_reserved_connections   | 3                              | 3                                | 3                           | 3                             |
| wal_buffers                      | 2048                           | 2048                             | 8192                        | 8192                          |

# 参考

> PostgresqlCO.NF：人間のためのPostgreSQLの設定 https://postgresqlco.nf/doc/ja/param/

> PostgreSQL11 設定パラメーター解体新書 / PostgreSQL 11 parameter - Speaker Deck https://speakerdeck.com/ester41/postgresql-11-parameter?slide=2
>
> PostgreSQL安定運用のための障害予防と検知 https://www.ospn.jp/osc2014.enterprise/pdf/OSC2014_Enterprise_hp.pdf
>
> PostgreSQL のパフォーマンスチューニング - Qiita https://qiita.com/cuzic/items/f9b846e6171a54079d77
>
> Oracle データベースを Amazon RDS PostgreSQL または Amazon Aurora PostgreSQL に移行する上でのベスト プラクティス: PostgreSQL 環境のターゲット データベースに関する考慮事項 | Amazon Web Services ブログ https://aws.amazon.com/jp/blogs/news/best-practices-for-migrating-an-oracle-database-to-amazon-rds-postgresql-or-amazon-aurora-postgresql-target-database-considerations-for-the-postgresql-environment/



