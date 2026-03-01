---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "S3(外部ステージ)からSnowflakeにデータロードする"
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

S3(外部ステージ)からSnowflakeにデータロードしてみる。

### IAMポリシーの作成

`sf_policy`として作成

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

### IAMロールの作成

`sf_role`として作成

- AWSアカウントを選択
- 別のAWSアカウントを選択して自分の AWS アカウントID を一時的に入力
  - なお、後で信頼関係を変更し、Snowflakeへのアクセスを許可する
- "外部IDを要求する"をクリックしてダミーのIDを入力しておく
  - 後で信頼関係を変更し、Snowflakeステージの外部 ID を指定します。AWS リソース（つまり、S3）へのアクセスをサードパーティ（つまり、Snowflake）に対して許可するには、外部 ID が必要
- 上記で作成した`sf_policy`をアタッチする

![image-20220824142339311](image-20220824142339311.png)

![image-20220824142551527](image-20220824142551527.png)

### Snowflake側でクラウドストレージ統合を作成

```sql
CREATE STORAGE INTEGRATION snowflake_and_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<AWSアカウント>:role/sf_role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://snowflake-bucket-work/')
;
```

※本コマンドを実行できるのはアカウント管理者（ ACCOUNTADMIN ロールを持つユーザー）またはグローバル CREATE INTEGRATION 権限を持つロールのみ

```sql
zatoima#COMPUTE_WH@TESTDB.PUBLIC>CREATE STORAGE INTEGRATION snowflake_and_s3_integration
                                   TYPE = EXTERNAL_STAGE
                                   STORAGE_PROVIDER = S3
                                   ENABLED = TRUE
                                   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<AWSアカウント>:role/sf_role'
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
| STORAGE_AWS_ROLE_ARN      | String        | arn:aws:iam::<AWSアカウント>:role/sf_role         |                  |
| STORAGE_AWS_EXTERNAL_ID   | String        | <Snowflakeアカウント>_SFCRole=3_ZGmPmtzjlkklddeysL+zqym2qW8= |                  |
| COMMENT                   | String        |                                                |                  |
+---------------------------+---------------+------------------------------------------------+------------------+
8 Row(s) produced. Time Elapsed: 0.713s
zatoima#COMPUTE_WH@TESTDB.PUBLIC>
```

`STORAGE_AWS_IAM_USER_ARN`と`STORAGE_AWS_EXTERNAL_ID`の値を控えておく

### IAMロールの信頼関係の修正



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

### 外部ステージの作成

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

### データロード

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

#### ロード時のオプション

ON_ERRORオプション

| CONTINUE        | エラーが見つかった場合は、ファイルのロードを続行します。エラーが見つかった行はロードされません。 |
| --------------- | ------------------------------------------------------------ |
| SKIP_FILE       | エラーが見つかった場合はファイルをスキップします。           |
| SKIP_FILE_数値  | ファイル内で見つかったエラー行の数が指定された数以上の場合は、ファイルをスキップします。 |
| SKIP_FILE_数値% | ファイル内で見つかったエラー行の割合が指定された割合を超えた場合は、ファイルをスキップします。 |
| ABORT_STATEMENT | データファイルでエラーが見つかった場合は、ロード操作を中止します。 |

- [COPY INTO <テーブル> — Snowflake Documentation](https://docs.snowflake.com/ja/sql-reference/sql/copy-into-table.html#copy-options-copyoptions)

### データアンロード

```sql
copy into @s3_ext_stage/unload/ from t1;
```

デフォルトでは圧縮された状態でアンロードされる。

### 参照

- [オプション1：Amazon S3にアクセスするためのSnowflakeストレージ統合の構成 — Snowflake Documentation](https://docs.snowflake.com/ja/user-guide/data-load-s3-config-storage-integration.html)

- [Amazon S3へのアンロード — Snowflake Documentation](https://docs.snowflake.com/ja/user-guide/data-unload-s3.html#unloading-into-amazon-s3)
