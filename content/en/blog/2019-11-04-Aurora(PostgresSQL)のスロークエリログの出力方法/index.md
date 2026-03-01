---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Output Slow Query Logs for Aurora (PostgreSQL)"
subtitle: ""
summary: " "
tags: ["Aurora","RDS","PostgreSQL"]
categories: ["Aurora","RDS","PostgreSQL"]
url: aws-aurora-postgres-querylog.html
date: 2019-11-04
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



### 1. Check Version

***


```sh
aurorapostdb=> select version();
                                   version
-----------------------------------------------------------------------------
 PostgreSQL 10.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.9.3, 64-bit
(1 row)
```

### 2. Modify Parameter Group

***


> 19.8. Error Reporting and Logging https://www.postgresql.jp/document/10/html/runtime-config-logging.html

```sh
log_statement=all # Controls which SQL statements are logged
log_min_duration_statement=0 # Setting to 0 outputs execution time for all statements
log_destination=csvlog # When csvlog is included in log_destination, log entries are output in "comma-separated values" (CSV) format for easier program loading
log_duration=1
log_error_verbosity=verbose # Controls the amount of detail written to the server log for each logged message
```

### 3. Restart Aurora (to apply parameters)

***

### 4. Verify Parameters

***


```sh
show log_statement;
show log_min_duration_statement;
show log_destination;
show log_duration;
show log_error_verbosity;
```

### 5. Run Test Query

***

Execute a Cartesian product SQL

```sql
select count(*) from pg_tables a, pg_stats b, pg_index c, pg_locks d;
```

### 6. Check from Management Console

***


Check `error/postgresql.log.yyyy-mm-dd-hhmi.csv`

<img src="image-20191218134516337.png" alt="image-20191218134516337" style="zoom:50%;" />
