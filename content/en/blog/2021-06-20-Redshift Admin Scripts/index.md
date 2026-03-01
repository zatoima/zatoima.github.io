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

### List

| No. | Script                        | Description                                                   |
| --- | ----------------------------- | ------------------------------------------------------------- |
| 1   | commit_stats.sql              | Displays information about cluster resource consumption due to COMMIT statements |
| 2   | copy_performance.sql          | Displays the longest running copies in the past 7 days        |
| 3   | current_session_info.sql      | Query that displays information about sessions with currently running queries |
| 4   | filter_used.sql               | Returns filters applied to tables during scans. Useful for choosing sort keys. |
| 5   | generate_calendar.sql         | Creates a calendar dimension table useful for star schema joins |
| 6   | missing_table_stats.sql       | Displays EXPLAIN plans that have flagged "no statistics" on underlying tables for queries |
| 7   | perf_alert.sql                | Returns top occurrences of alerts, joins with table scans, and SQL text |
| 8   | table_alerts.sql              | Returns the number of alerts related to table access           |
| 9   | predicate_columns.sql         | Returns information about predicate columns on tables          |
| 10  | queuing_queries.sql           | Displays queries waiting in WLM query slots                    |
| 11  | queue_resources_hourly.sql    | Returns hourly resource usage for WLM query queues             |
| 12  | running_queues.sql            | Returns running and queued queries and consumed resources       |
| 13  | table_info.sql                | Returns table storage information (size, skew, etc.)           |
| 14  | table_inspector.sql           | Table analysis based on "Analyze Table Design" content. Complements table_info.sql |
| 15  | top_queries.sql               | Returns the top 50 statements that consumed the most time in the past 7 days |
| 16  | top_queries_and_cursors.sql   | Returns the top 50 statements that consumed the most time in the past 7 days - including cursor text |
| 17  | unscanned_table_summary.sql   | Summarizes storage consumed by unscanned tables                |
| 18  | wlm_apex.sql                  | Returns the overall high watermark for WLM query queues and when the queue last occurred |
| 19  | wlm_apex_hourly.sql           | Returns hourly high watermarks for WLM query queues            |
| 20  | wlm_qmr_rule_candidates.sql   | Calculates candidates for new WLM query monitoring rules       |
| 21  | user_to_be_dropped_objs.sql   | Searches for objects owned by users that cannot be dropped     |
| 22  | user_to_be_dropped_privs.sql  | Searches for privileges granted to users that cannot be dropped |

> https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AdminScripts

### Execute

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
