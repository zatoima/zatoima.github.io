---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Analyzing Aurora PostgreSQL Logs Using the log_fdw Extension"
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

I started thinking it would be nice to analyze PostgreSQL logs using SQL. After looking into it, I found a convenient extension.

#### Enable the Extension

```sql
CREATE EXTENSION log_fdw;
```

#### Create a Log Server as a Foreign Data Wrapper

```sql
CREATE SERVER log_server FOREIGN DATA WRAPPER log_fdw;
```

#### Get a List of Log Files

```sql
SELECT * from list_postgres_log_files() order by 1;
SELECT * FROM list_postgres_log_files() WHERE file_name LIKE 'postgresql.log.%.csv' ORDER BY 1 DESC;
```

#### Create a Table Using a Log File as Input

```sql
SELECT create_foreign_table_for_log_file('postgresql_log_20201206', 'log_server', 'postgresql.log.2020-12-06.csv');
```

#### Created Foreign Table and Sample Data for Each Column

| Column Example         | Sample Data                                        |
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

#### View Log Contents

```sql
select * from postgresql_log_20201206;
```

#### Check Number of Login Failures from a Specific Server

```sql
select count(*) from postgresql_log_20201206 where connection_from like '10.0.1.123%' and message like '%password authentication failed %';
```

#### Drop the Foreign Table When No Longer Needed

```sql
DROP FOREIGN TABLE postgresql_log_20201206;
```

#### References

> https://aws.amazon.com/blogs/news/working-with-rds-and-aurora-postgresql-logs-part-2/
>
> View log data through a foreign table using log_fdw
