---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Auto Vacuum Execution Timing and Related Parameters in PostgreSQL"
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



### Overview of Auto Vacuum

Auto Vacuum is on by default. It also performs Analyze simultaneously with Vacuum. The manual recommends Auto Vacuum.

> 24.1. Routine Vacuuming https://www.postgresql.jp/document/10/html/routine-vacuuming.html

### Auto Vacuum Execution Timing

The vacuum execution timing is:

`Number of UPDATE+DELETE = threshold < autovacuum_vacuum_threshold (default 50) + autovacuum_vacuum_scale_factor (default 0.2) × pg_class.reltuples`

The analyze execution timing is:

`Number of UPDATE+DELETE+INSERT = threshold < autovacuum_analyze_threshold (default 50) + autovacuum_analyze_scale_factor (default 0.1) × pg_class.reltuples`

*pg_class.reltuples is the number of rows in the table. Updated by some DDL commands like VACUUM, ANALYZE, CREATE INDEX.*

### Auto Vacuum Parameters

| Parameter                       | Category | Default | Description                                                  |
| ------------------------------- | -------- | ------- | ------------------------------------------------------------ |
| autovacuum                      | VACUUM   | on      | Whether to perform automatic vacuuming                      |
| log_autovaccum_min_duration     | VACUUM   | -1      | Outputs a log when processing takes longer than the specified time (milliseconds). Disabled by default. |
| autovacuum_max_workers          | VACUUM   | 3       | Maximum number of concurrent autovacuum worker processes    |
| autovaccum_naptime              | VACUUM   | 1min    | The period to check whether autovacuum is needed            |
| autovacuum_vacuum_threshold     | VACUUM   | 50      | Minimum number of updated or deleted tuples needed to trigger VACUUM |
| autovacuum_vacuum_scale_factor  | VACUUM   | 0.2     | Specifies the fraction of table size to add to autovacuum_vacuum_threshold when deciding whether to trigger VACUUM |
| autovacuum_analyze_threshold    | ANALYZE  | 50      | Minimum number of updated or deleted tuples needed to trigger ANALYZE |
| autovacuum_analyze_scale_factor | ANALYZE  | 0.1     | Specifies the fraction of table size to add to autovacuum_vacuum_threshold when deciding whether to trigger ANALYZE |

### How to Check Execution History

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

### Execution Results

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

Reference

> 19.10. Automatic Vacuuming https://www.postgresql.jp/document/10/html/runtime-config-autovacuum.html
