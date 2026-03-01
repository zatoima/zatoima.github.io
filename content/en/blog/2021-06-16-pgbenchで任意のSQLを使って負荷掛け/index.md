---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Load Testing with Custom SQL Using pgbench"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pgbench-performance-sql-test
date: 2021-06-16
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



### SQL to Execute

```
cat << EOF > query.sql
<Write SQL here>
EOF
```

### Parallel Execution Using pgbench

In this case, running the SQL 100 times with 5 clients and 5 threads.

```
pgbench -r -c 5 -j 5 -n -t 100 -f query.sql -U awsuser -h aurora-postgresql.xxxxxx.ap-northeast-1.redshift.amazonaws.com -d postgres -p 5439
```

### Option Descriptions

> pgbench https://www.postgresql.jp/document/12/html/pgbench.html

```
-j threads --jobs=threads
Number of worker threads in pgbench

-r --report-latencies
Reports per-statement average latency (execution time as seen by the client) for each command after benchmark completion

-c clients --client=clients
Number of simulated clients, i.e., number of concurrent database sessions

-f filename --file=filename
Specifies the SQL file to execute

-t transactions --transactions=transactions
Number of transactions each client runs. Default is 10.
```
