---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshift Admin Scripts"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-admin-script-memo
date: 2021-06-20
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

### 一覧

| No.  | スクリプト                   | 概要                                                         |
| ---- | ---------------------------- | ------------------------------------------------------------ |
| 1    | commit_stats.sql             | COMMIT文によるクラスタリソースの消費に関する情報を表示       |
| 2    | copy_performance.sql         | 過去7日間で最も長く実行されたコピーを表示                    |
| 3    | current_session_info.sql     | 現在実行中のクエリを持つセッションについての情報を表示するクエリ |
| 4    | filter_used.sql              | スキャン時にテーブルに適用されるフィルタを返す。ソートキーの選択に役立ちます。 |
| 5    | generate_calendar.sql        | スタースキーマ結合に便利なカレンダー・ディメンジョン・テーブルの作成 |
| 6    | missing_table_stats.sql      | クエリには、基礎となるテーブルで「統計情報がない」というフラグを立てた EXPLAIN プランが表示 |
| 7    | perf_alert.sql               | アラート、テーブルスキャンとの結合、SQLテキストの上位出現率を返す |
| 8    | table_alerts.sql             | テーブルアクセスに関連するアラートの発生件数を返す           |
| 9    | predicate_columns.sql        | テーブル上のプレディケート・カラムに関する情報を返す         |
| 10   | queuing_queries.sql          | WLM クエリスロットで待機しているクエリの表示                 |
| 11   | queue_resources_hourly.sql   | WLM クエリキューの時間ごとのリソース使用量を返す             |
| 12   | running_queues.sql           | 実行中およびキューイング中のクエリと消費されたリソースを返す |
| 13   | table_info.sql               | テーブルのストレージ情報（サイズ、スキューなど）を返す       |
| 14   | table_inspector.sql          | テーブル設計の分析」の内容に基づくテーブルの分析。table_info.sqlを補完 |
| 15   | top_queries.sql              | 過去7日間で最も時間を消費したステートメントのトップ50を返す  |
| 16   | top_queries_and_cursors.sql  | 過去7日間で最も時間を消費したステートメントのトップ50を返す - カーソルテキストを含む |
| 17   | unscanned_table_summary.sql  | スキャンされていないテーブルで消費されたストレージをまとめます。 |
| 18   | wlm_apex.sql                 | WLM クエリキューの全体的なハイウォーターマークとキューが最後に発生した時間を返す |
| 19   | wlm_apex_hourly.sql          | WLM クエリキューの時間ごとのハイウォーターマークを返す       |
| 20   | wlm_qmr_rule_candidates.sql  | 新しい WLM クエリ監視ルールの候補を算出                      |
| 21   | user_to_be_dropped_objs.sql  | ドロップできないユーザが所有するオブジェクトの検索           |
| 22   | user_to_be_dropped_privs.sql | ドロップできないユーザに付与されている権限の検索             |

> https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AdminScripts

### 実行

```
\i commit_stats.sql;
\i copy_performance.sql;
\i current_session_info.sql;
\i filter_used.sql;
\i generate_calendar.sql;
\i insert_into_table_dk_mismatch.sql;
\i lock_wait.sql;
\i missing_table_stats.sql;
\i perf_alert.sql;
\i predicate_columns.sql;
\i queue_resources_hourly.sql;
\i queuing_queries.sql;
\i running_queues.sql;
\i table_alerts.sql;
\i table_info.sql;
\i table_inspector.sql;
\i top_queries_and_cursors.sql;
\i top_queries.sql;
\i unscanned_table_summary.sql;
\i user_to_be_dropped_objs.sql;
\i user_to_be_dropped_privs.sql;
\i wlm_apex_hourly.sql;
\i wlm_apex.sql;
\i wlm_qmr_rule_candidates.sql;
```

