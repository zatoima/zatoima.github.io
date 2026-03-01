---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Querying S3 External Tables in Snowflake"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-s3-external-table-query
date: 2022-10-12
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

### Overview

- You can query Parquet, CSV, and other files placed on S3
  - Understood as a feature similar to Redshift Spectrum

### Notes

- File values are stored in a column called "VALUE" in JSON object format
- Querying data stored outside the database may be slower than querying native database tables (as stated in the manual)

  > Querying data stored outside the database may be slower than querying native database tables.
  >
  > https://docs.snowflake.com/en/user-guide/tables-external-intro.html

  - To improve performance, combine with materialized views
    - [Materialized Views for External Tables — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-external-intro.html#label-materialized-views-over-external-tables)
- For performance, partitions should be used aggressively

### Creating a File Format

```sql
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    COMPRESSION = 'AUTO'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 0
    FIELD_OPTIONALLY_ENCLOSED_BY = NONE
    DATE_FORMAT = 'AUTO'
    TIMESTAMP_FORMAT = 'AUTO'
    NULL_IF = ('');
```

### Creating an External Stage

Using the external stage created below. Refer to this for IAM settings as well.

[Loading Data from S3 (External Stage) into Snowflake | my opinion is my own](https://zatoima.github.io/snowflake-dataload-from-s3-to-snowflake/)

```
zatoima#COMPUTE_WH@TESTDB.PUBLIC>show stages;
+-------------------------------+--------------+---------------+-------------+-----------------------------+-----------------+--------------------+--------------+---------+----------------+----------+-------+----------------------+------------------------------+
| created_on                    | name         | database_name | schema_name | url                         | has_credentials | has_encryption_key | owner        | comment | region         | type     | cloud | notification_channel | storage_integration          |
|-------------------------------+--------------+---------------+-------------+-----------------------------+-----------------+--------------------+--------------+---------+----------------+----------+-------+----------------------+------------------------------|
| 2022-08-23 22:45:45.523 -0700 | S3_EXT_STAGE | TESTDB        | PUBLIC      | s3://snowflake-bucket-work/ | N               | N                  | ACCOUNTADMIN |         | ap-northeast-1 | EXTERNAL | AWS   | NULL                 | SNOWFLAKE_AND_S3_INTEGRATION |
+-------------------------------+--------------+---------------+-------------+-----------------------------+-----------------+--------------------+--------------+---------+----------------+----------+-------+----------------------+------------------------------+
1 Row(s) produced. Time Elapsed: 0.077s
```

### Building an External Table

```sql
CREATE EXTERNAL TABLE t1
  WITH location = @S3_EXT_STAGE
  auto_refresh = true
  file_format = csv_format;
```

Even when auto_refresh is set to TRUE, when files on the S3 side change, you need to perform a refresh. For AWS S3, the following settings must be configured in advance.

- [Auto-Refresh for External Tables on Amazon S3 — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-external-s3.html)

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>ALTER EXTERNAL TABLE t1 refresh;

+--------+-------------------+-----------------------------------------+
| file   | status            | description                             |
|--------+-------------------+-----------------------------------------|
| t1.csv | REGISTERED_UPDATE | File registered (updated) successfully. |
+--------+-------------------+-----------------------------------------+
1 Row(s) produced. Time Elapsed: 0.480s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
zatoima#COMPUTE_WH@TESTDB.PUBLIC>select * from t1;
+-----------------------------------------+
| VALUE                                   |
|-----------------------------------------|
| {                                       |
|   "c1": "0",                            |
|   "c2": "111111",                       |
|   "c3": "222222",                       |
|   "c4": " 1",                           |
|   "c5": "2022-08-23 22:47:44.214 -0700" |
| }                                       |
| {                                       |
|   "c1": "1",                            |
|   "c2": "111111",                       |
|   "c3": "222222",                       |
|   "c4": " 2",                           |
|   "c5": "2022-08-23 22:47:44.214 -0700" |
| }                                       |
+-----------------------------------------+
2 Row(s) produced. Time Elapsed: 1.077s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
```

The update status can be checked with `SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('table_name');`.

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>select SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('T1');
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('T1')                                                                                                                                                                                                                                        |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| {"executionState":"RUNNING","pendingFileCount":0,"notificationChannelName":"arn:aws:sqs:ap-northeast-1:xxxxx:sf-snowpipe-xxxx-88QZUsuy_HLwocQAHjHNUA","numOutstandingMessagesOnChannel":0,"lastPulledFromChannelTimestamp":"2022-08-25T07:24:54.217Z"} |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

```

- [SYSTEM$EXTERNAL\_TABLE\_PIPE\_STATUS](https://docs.snowflake.com/en/sql-reference/functions/system_external_table_pipe_status.html)

Execution log

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>CREATE EXTERNAL TABLE t1
                                   WITH location = @S3_EXT_STAGE
                                   auto_refresh = true
                                   file_format = csv_format;
+--------------------------------+
| status                         |
|--------------------------------|
| Table T1 successfully created. |
+--------------------------------+
1 Row(s) produced. Time Elapsed: 4.079s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
zatoima#COMPUTE_WH@TESTDB.PUBLIC>show tables;
+-------------------------------+----------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+----------------------+-----------------+-------------+
| created_on                    | name     | database_name | schema_name | kind  | comment | cluster_by | rows | bytes | owner        | retention_time | automatic_clustering | change_tracking | is_external |
|-------------------------------+----------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+----------------------+-----------------+-------------|
| 2022-08-14 05:17:22.196 -0700 | LINEITEM | TESTDB        | PUBLIC      | TABLE |         |            |    0 |     0 | ACCOUNTADMIN | 1              | OFF                  | OFF             | N           |
| 2022-08-25 00:05:01.262 -0700 | T1       | TESTDB        | PUBLIC      | TABLE |         |            | NULL |     0 | ACCOUNTADMIN | 1              | OFF                  | OFF             | Y           |
+-------------------------------+----------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+----------------------+-----------------+-------------+
2 Row(s) produced. Time Elapsed: 0.146s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
zatoima#COMPUTE_WH@TESTDB.PUBLIC>select * from t1;
+-----------------------------------------+
| VALUE                                   |
|-----------------------------------------|
| {                                       |
|   "c1": "0",                            |
|   "c2": "111111",                       |
|   "c3": "222222",                       |
|   "c4": "1",                            |
|   "c5": "2022-08-23 22:47:44.214 -0700" |
| }                                       |
| {                                       |
|   "c1": "1",                            |
|   "c2": "111111",                       |
|   "c3": "222222",                       |
|   "c4": "2",                            |
|   "c5": "2022-08-23 22:47:44.214 -0700" |
| }                                       |
~~omitted~~
zatoima#COMPUTE_WH@TESTDB.PUBLIC>SELECT value :c1, value :c2, value :c3, value :c4, value :c5 FROM t1 LIMIT 10 ;
+-----------+-----------+-----------+-----------+---------------------------------+
| VALUE :C1 | VALUE :C2 | VALUE :C3 | VALUE :C4 | VALUE :C5                       |
|-----------+-----------+-----------+-----------+---------------------------------|
| "0"       | "111111"  | "222222"  | "1"       | "2022-08-23 22:47:44.214 -0700" |
| "1"       | "111111"  | "222222"  | "2"       | "2022-08-23 22:47:44.214 -0700" |
| "2"       | "111111"  | "222222"  | "3"       | "2022-08-23 22:47:44.214 -0700" |
| "3"       | "111111"  | "222222"  | "4"       | "2022-08-23 22:47:44.214 -0700" |
| "4"       | "111111"  | "222222"  | "5"       | "2022-08-23 22:47:44.214 -0700" |
| "5"       | "111111"  | "222222"  | "6"       | "2022-08-23 22:47:44.214 -0700" |
| "6"       | "111111"  | "222222"  | "7"       | "2022-08-23 22:47:44.214 -0700" |
| "7"       | "111111"  | "222222"  | "8"       | "2022-08-23 22:47:44.214 -0700" |
| "8"       | "111111"  | "222222"  | "9"       | "2022-08-23 22:47:44.214 -0700" |
| "9"       | "111111"  | "222222"  | "10"      | "2022-08-23 22:47:44.214 -0700" |
+-----------+-----------+-----------+-----------+---------------------------------+
10 Row(s) produced. Time Elapsed: 0.653s
```

### Reference

- [Introduction to External Tables — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-external-intro.html)
