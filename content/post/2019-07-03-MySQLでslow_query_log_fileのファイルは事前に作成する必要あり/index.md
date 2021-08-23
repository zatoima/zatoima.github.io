---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLでslow_query_log_fileのファイルは事前に作成する必要あり"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-slow_query_log_file-error.html
date: 2019-07-03
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


`slow_query_log_file` で指定するスロークエリログファイルは事前に作成しておく必要があるという話。常識？

### スロークエリログ関連のシステム変数

```sql
[mysqld]
slow_query_log=ON
slow_query_log_file = /var/log/slow.log
long_query_time=0
```

事前に作成しておかないとエラーが出力される。

```sql
mysqld: File '/var/log/slow.log' not found (Errcode: 13 - Permission denied)
2019-07-01T11:16:23.095556Z 0 [ERROR] Could not use /var/log/slow.log for logging (error 13 - Permission denied). Turning logging off for the server process. To turn it on again: fix the cause, then either restart the query logging by using "SET GLOBAL SLOW_QUERY_LOG=ON" or restart the MySQL server.
```

