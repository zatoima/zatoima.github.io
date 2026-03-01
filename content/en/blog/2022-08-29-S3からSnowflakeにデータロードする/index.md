---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Loading Data from S3 (External Stage) into Snowflake"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-dataload-from-s3-to-snowflake
date: 2022-08-29
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

Loading data from S3 (external stage) into Snowflake.

### Creating an IAM Policy

Created as `sf_policy`:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion"
            ],
            "Resource": "arn:aws:s3:::snowflake-bucket-work/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::snowflake-bucket-work"
        }
    ]
}
```

### Creating an IAM Role

Created as `sf_role`:

- Select AWS account
- Select another AWS account and temporarily enter your own AWS Account ID
  - Note: The trust relationship will be modified later to grant access to Snowflake
- Click "Require external ID" and enter a dummy ID
  - The trust relationship will be modified later to specify the Snowflake stage's external ID. An external ID is required to allow a third party (Snowflake) to access AWS resources (i.e., S3)
- Attach the `sf_policy` created above

![image-20220824142339311](image-20220824142339311.png)

![image-20220824142551527](image-20220824142551527.png)

### Creating Cloud Storage Integration on Snowflake Side

```sql
CREATE STORAGE INTEGRATION snowflake_and_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<AWS Account>:role/sf_role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://snowflake-bucket-work/')
;
```

Note: Only account administrators (users with ACCOUNTADMIN role) or roles with global CREATE INTEGRATION privilege can execute this command.

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>CREATE STORAGE INTEGRATION snowflake_and_s3_integration
                                   TYPE = EXTERNAL_STAGE
                                   STORAGE_PROVIDER = S3
                                   ENABLED = TRUE
                                   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<AWS Account>:role/sf_role'
                                   STORAGE_ALLOWED_LOCATIONS = ('s3://snowflake-bucket-work/')
                                 ;
+----------------------------------------------------------------+
| status                                                         |
|----------------------------------------------------------------|
| Integration SNOWFLAKE_AND_S3_INTEGRATION successfully created. |
+----------------------------------------------------------------+
1 Row(s) produced. Time Elapsed: 1.015s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>desc integration snowflake_and_s3_integration;
+---------------------------+---------------+------------------------------------------------+------------------+
| property                  | property_type | property_value                                 | property_default |
|---------------------------+---------------+------------------------------------------------+------------------|
| ENABLED                   | Boolean       | true                                           | false            |
| STORAGE_PROVIDER          | String        | S3                                             |                  |
| STORAGE_ALLOWED_LOCATIONS | List          | s3://snowflake-bucket-work/                    | []               |
| STORAGE_BLOCKED_LOCATIONS | List          |                                                | []               |
| STORAGE_AWS_IAM_USER_ARN  | String        | arn:aws:iam::xxxxxxxxx:user/qvl6-s-jpss8756 |                  |
| STORAGE_AWS_ROLE_ARN      | String        | arn:aws:iam::<AWS Account>:role/sf_role         |                  |
| STORAGE_AWS_EXTERNAL_ID   | String        | <Snowflake Account>_SFCRole=3_ZGmPmtzjlkklddeysL+zqym2qW8= |                  |
| COMMENT                   | String        |                                                |                  |
+---------------------------+---------------+------------------------------------------------+------------------+
8 Row(s) produced. Time Elapsed: 0.713s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
```

Note the values of `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID`.

### Modifying IAM Role Trust Relationship

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Principal": {
				"AWS": "<STORAGE_AWS_IAM_USER_ARN>"
			},
			"Action": "sts:AssumeRole",
			"Condition": {
				"StringEquals": {
					"sts:ExternalId": "<STORAGE_AWS_EXTERNAL_ID>"
				}
			}
		}
	]
}
```

### Creating an External Stage

```sql
CREATE STAGE s3_ext_stage STORAGE_INTEGRATION = snowflake_and_s3_integration URL = 's3://snowflake-bucket-work/';
```

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>CREATE STAGE s3_ext_stage STORAGE_INTEGRATION = snowflake_and_s3_integration URL = 's3://snowflake-bucket-work/';
+-----------------------------------------------+
| status                                        |
|-----------------------------------------------|
| Stage area S3_EXT_STAGE successfully created. |
+-----------------------------------------------+
zatoima#COMPUTE_WH@TESTDB.PUBLIC>show stages;
+-------------------------------+--------------+---------------+-------------+-----------------------------+-----------------+--------------------+--------------+---------+----------------+----------+-------+----------------------+------------------------------+
| created_on                    | name         | database_name | schema_name | url                         | has_credentials | has_encryption_key | owner        | comment | region         | type     | cloud | notification_channel | storage_integration          |
|-------------------------------+--------------+---------------+-------------+-----------------------------+-----------------+--------------------+--------------+---------+----------------+----------+-------+----------------------+------------------------------|
| 2022-08-23 22:45:45.523 -0700 | S3_EXT_STAGE | TESTDB        | PUBLIC      | s3://snowflake-bucket-work/ | N               | N                  | ACCOUNTADMIN |         | ap-northeast-1 | EXTERNAL | AWS   | NULL                 | SNOWFLAKE_AND_S3_INTEGRATION |
+-------------------------------+--------------+---------------+-------------+-----------------------------+-----------------+--------------------+--------------+---------+----------------+----------+-------+----------------------+------------------------------+
1 Row(s) produced. Time Elapsed: 0.098s
```

### Loading Data

```sql
copy into t1 from @s3_ext_stage pattern='test.csv';
```

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>copy into t1 from @s3_ext_stage pattern='test.csv';
+-------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
| file                                | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
|-------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
| s3://snowflake-bucket-work/test.csv | LOADED |          10 |          10 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
+-------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
1 Row(s) produced. Time Elapsed: 2.675s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>select * from t1;
+---+--------+--------+----+-------------------------------+
| A | B      | C      |  D | E                             |
|---+--------+--------+----+-------------------------------|
| 0 | 111111 | 222222 |  1 | 2022-08-23 22:47:44.214 -0700 |
| 1 | 111111 | 222222 |  2 | 2022-08-23 22:47:44.214 -0700 |
| 2 | 111111 | 222222 |  3 | 2022-08-23 22:47:44.214 -0700 |
| 3 | 111111 | 222222 |  4 | 2022-08-23 22:47:44.214 -0700 |
| 4 | 111111 | 222222 |  5 | 2022-08-23 22:47:44.214 -0700 |
| 5 | 111111 | 222222 |  6 | 2022-08-23 22:47:44.214 -0700 |
| 6 | 111111 | 222222 |  7 | 2022-08-23 22:47:44.214 -0700 |
| 7 | 111111 | 222222 |  8 | 2022-08-23 22:47:44.214 -0700 |
| 8 | 111111 | 222222 |  9 | 2022-08-23 22:47:44.214 -0700 |
| 9 | 111111 | 222222 | 10 | 2022-08-23 22:47:44.214 -0700 |
+---+--------+--------+----+-------------------------------+
10 Row(s) produced. Time Elapsed: 0.198s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>

```

#### Load Options

ON_ERROR options:

| CONTINUE        | If an error is found, continue loading the file. Rows where errors are found will not be loaded. |
| --------------- | ------------------------------------------------------------ |
| SKIP_FILE       | If an error is found, skip the file. |
| SKIP_FILE_n     | If the number of error rows found in the file is n or more, skip the file. |
| SKIP_FILE_n%    | If the percentage of error rows found in the file exceeds the specified percentage, skip the file. |
| ABORT_STATEMENT | If an error is found in the data file, abort the load operation. |

- [COPY INTO <table> — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#copy-options-copyoptions)

### Unloading Data

```sql
copy into @s3_ext_stage/unload/ from t1;
```

By default, data is unloaded in compressed form.

### References

- [Option 1: Configuring a Snowflake Storage Integration to Access Amazon S3 — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration.html)

- [Unloading to Amazon S3 — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-unload-s3.html#unloading-into-amazon-s3)
