---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLの自動Vacuumの実行タイミングと関連するパラメータ"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-auto-vacuum-parameter-timing.html
date: 2020-03-16
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



### Auto Vacuumの概要

デフォルトでonになっているAuto Vacuum。Vacuumと同時にAnalyzeも実施してくれます。マニュアル的にはAuto Vacuumが推奨です。

> 24.1. 定常的なバキューム作業 https://www.postgresql.jp/document/10/html/routine-vacuuming.html

### Auto  Vacuumの実行タイミング

バキュームの実行タイミングは 

`UPDATE+DELETE回数 = 閾値 < autovacuum_vacuum_threshold（デフォルト 50）+ autovacuum_vacuum_scale_factor(デフォルト0.2)  × pg_class.reltuples`

一方、Analyzeの実行タイミングは

`UPDATE+DELETE+INSERT回数 = 閾値 < autovacuum_analyze_threshold（デフォルト 50）+ autovacuum_analyze_scale_factor(デフォルト0.1)  × pg_class.reltuples`となる。

※pg_class.reltuplesはテーブル内の行数。 VACUUM、ANALYZE、CREATE INDEXなどの一部のDDLコマンドで更新される。

### Auto  Vacuumのパラメータについて

| パラメータ                      | 分類    | デフォルト | パラメータ説明                                               |
| ------------------------------- | ------- | ---------- | ------------------------------------------------------------ |
| autovacuum                      | VACUUM  | on         | 自動バキュームを行うかどうか                                 |
| log_autovaccum_min_duration     | VACUUM  | -1         | 指定した時間（ミリ秒）以上に処理を行った場合にログを出力する。デフォルトでは無効 |
| autovacuum_max_workers          | VACUUM  | 3          | 自動バキュームの同時実行ワーカーの最大数                     |
| autovaccum_naptime              | VACUUM  | 1min       | 自動バキュームの必要性を確認する期間                         |
| autovacuum_vacuum_threshold     | VACUUM  | 50         | VACUUMを起動するために必要な、更新もしくは削除されたタプルの最小数 |
| autovacuum_vacuum_scale_factor  | VACUUM  | 0.2        | VACUUMを起動するか否かを決定するときに、autovacuum_vacuum_thresholdに足し算するテーブル容量の割合を指定 |
| autovacuum_analyze_threshold    | ANALYZE | 50         | ANALYZEを起動するために必要な、更新もしくは削除されたタプルの最小数 |
| autovacuum_analyze_scale_factor | ANALYZE | 0.1        | ANALYZEを起動するか否かを決定するときに、autovacuum_vacuum_thresholdに足し算するテーブル容量の割合を指定 |

### 実行履歴の確認方法

```sql
\x
SELECT
    schemaname,
    relname,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze,
    vacuum_count,
    autovacuum_count,
    autoanalyze_count
FROM
    pg_stat_user_tables;
```

### 実行結果

```sql
-[ RECORD 1 ]-----+------------------------------
schemaname        | public
relname           | pgbench_tellers
last_vacuum       | 2020-02-29 07:29:38.682063+00
last_autovacuum   | 2020-02-29 05:40:58.708216+00
last_analyze      | 2020-02-29 07:29:38.682594+00
last_autoanalyze  | 2020-02-29 05:40:58.708747+00
vacuum_count      | 8
autovacuum_count  | 28
autoanalyze_count | 27
-[ RECORD 2 ]-----+------------------------------
schemaname        | public
relname           | pgbench_history
last_vacuum       | 2020-02-29 07:29:38.73807+00
last_autovacuum   | 
last_analyze      | 2020-02-29 07:29:38.747484+00
last_autoanalyze  | 2020-02-29 05:40:58.744441+00
vacuum_count      | 3
autovacuum_count  | 0
autoanalyze_count | 20
-[ RECORD 3 ]-----+------------------------------
schemaname        | public
relname           | pgbench_branches
last_vacuum       | 2020-02-29 07:29:38.683765+00
last_autovacuum   | 2020-02-29 05:40:58.721649+00
last_analyze      | 2020-02-29 07:29:38.683963+00
last_autoanalyze  | 2020-02-29 05:40:58.72242+00
vacuum_count      | 8
autovacuum_count  | 28
autoanalyze_count | 27
-[ RECORD 4 ]-----+------------------------------
schemaname        | public
relname           | pgbench_accounts
last_vacuum       | 2020-02-29 07:29:38.69804+00
last_autovacuum   | 
last_analyze      | 2020-02-29 07:29:38.734999+00
last_autoanalyze  | 2020-02-27 13:24:59.247779+00
vacuum_count      | 3
autovacuum_count  | 0
autoanalyze_count | 25
```

参考

> 19.10. 自動Vacuum作業 https://www.postgresql.jp/document/10/html/runtime-config-autovacuum.html