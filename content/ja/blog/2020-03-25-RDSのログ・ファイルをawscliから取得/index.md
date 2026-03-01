---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS/Auroraのログファイルをawscliから取得・確認する"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-log-file-get.html
date: 2020-03-25
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



マネージメントコンソールから確認するのが面倒な時にCLIから実行するのを想定しています。

### 事前準備

jqコマンドを使って整形するので事前にインストールする

```sh
sudo yum -y install jq
```

### ログ・ファイルの取得方法

```sh
aws rds describe-db-instances | jq '.DBInstances[].DBInstanceIdentifier'
aws rds describe-db-log-files --db-instance-identifier aurorapostgresqlv1-instance-1
aws rds download-db-log-file-portion --db-instance-identifier aurorapostgresqlv1-instance-1 --log-file-name "error/postgres.log" --output text
```

### 実行例

##### 取得対象のインスタンス名を取得

```sh
[ec2-user@bastin ~]$ aws rds describe-db-instances | jq '.DBInstances[].DBInstanceIdentifier'
"aurorapostgresqlv1-instance-1"
[ec2-user@bastin ~]$ 
```

##### 出力されているログ・ファイルの取得

最新のファイルかどうかは`LastWritten`から確認可能。

```sh
[ec2-user@bastin ~]$ aws rds describe-db-log-files --db-instance-identifier aurorapostgresqlv1-instance-1
{
    "DescribeDBLogFiles": [
        {
            "LastWritten": 1582951862000, 
            "LogFileName": "error/postgres.log", 
            "Size": 1380
        }, 
        {
            "LastWritten": 1582951868000, 
            "LogFileName": "error/postgresql.log.2020-02-29-0451", 
            "Size": 891
        }, 
        {
            "LastWritten": 1582952400000, 
            "LogFileName": "error/postgresql.log.2020-02-29-0500", 
            "Size": 0
        }, 
        {
            "LastWritten": 1582956000000, 
            "LogFileName": "error/postgresql.log.2020-02-29-0600", 
            "Size": 0
        }
    ]
}
```

##### ログ・ファイルを出力

```sh
[ec2-user@bastin ~]$ aws rds download-db-log-file-portion --db-instance-identifier aurorapostgresqlv1-instance-1 --log-file-name "error/postgres.log" --output text
2020-02-29 04:51:01.093 GMT [5665] LOG:  skipping missing configuration file "/rdsdbdata/db/postgresql.auto.conf"
2020-02-29 04:51:01 UTC::@:[5665]:WARNING:  unrecognized configuration parameter "rds.custom_dns_resolution"
2020-02-29 04:51:01 UTC::@:[5665]:WARNING:  unrecognized configuration parameter "rds.enable_plan_management"
2020-02-29 04:51:01 UTC::@:[5665]:LOG:  database system is shut down
Postgres Shared Memory Value: 11132993536 bytes
2020-02-29 04:51:02.647 GMT [5783] LOG:  skipping missing configuration file "/rdsdbdata/db/postgresql.auto.conf"
2020-02-29 04:51:02 UTC::@:[5783]:WARNING:  unrecognized configuration parameter "rds.custom_dns_resolution"
2020-02-29 04:51:02 UTC::@:[5783]:WARNING:  unrecognized configuration parameter "rds.enable_plan_management"
2020-02-29 04:51:02 UTC::@:[5783]:LOG:  listening on IPv4 address "0.0.0.0", port 5432
2020-02-29 04:51:02 UTC::@:[5783]:LOG:  listening on IPv6 address "::", port 5432
2020-02-29 04:51:02 UTC::@:[5783]:LOG:  listening on Unix socket "/tmp/.s.PGSQL.5432"
2020-02-29 04:51:02 UTC::@:[5783]:LOG:  could not write pg_stat_statement file "pg_stat_tmp/pgss_query_texts.stat": No such file or directory
2020-02-29 04:51:02 UTC::@:[5783]:LOG:  redirecting log output to logging collector process
2020-02-29 04:51:02 UTC::@:[5783]:HINT:  Future log output will appear in directory "/rdsdbdata/log/error".
```

