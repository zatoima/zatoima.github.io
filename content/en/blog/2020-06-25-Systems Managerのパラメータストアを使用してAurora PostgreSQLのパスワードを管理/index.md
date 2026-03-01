---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Managing Aurora PostgreSQL Passwords Using AWS Systems Manager Parameter Store"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-parameter-store-connect.html
date: 2020-06-25
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

### Prerequisites

#### Introduction

Create a user `testuser` with password `p@sstest` on the Aurora PostgreSQL side.

```
CREATE ROLE testuser WITH LOGIN PASSWORD 'p@sstest';
```

When logging in with psql, set the credentials as environment variables and connect as follows. However, keeping the password somewhere is not a secure approach.

```
[ec2-user@bastin ~]$ export PGUSER=testuser
[ec2-user@bastin ~]$ export PGPASSWORD=xxxxx
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.
postgres=> \conninfo
You are connected to database "postgres" as user "testuser" on host "aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com" at port "5432".
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
```

#### Store Parameters in Systems Manager

Store two parameters. The userid is stored as a `plain text (String)` and the password as a `SecureString`.

```
aws ssm put-parameter --name 'pgsql.connect.userid' --type 'String' --value 'testuser'
aws ssm put-parameter --name 'pgsql.connect.password' --type 'SecureString' --value 'p@sstest'
```

Retrieve a parameter. Getting `pgsql.connect.userid`:

```
[ec2-user@bastin ~]$ aws ssm get-parameters --name 'pgsql.connect.userid'
{
    "InvalidParameters": [],
    "Parameters": [
        {
            "Name": "pgsql.connect.userid",
            "DataType": "text",
            "LastModifiedDate": 1592740003.175,
            "Value": "testuser",
            "Version": 1,
            "Type": "String",
            "ARN": "arn:aws:ssm:ap-northeast-1:xxxxxx:parameter/pgsql.connect.userid"
        }
    ]
}
```

Next, get `pgsql.connect.password`. For parameters stored as `SecureString`, the `--with-decryption` flag must be added to the command. Without this option, the value is output in encrypted form. (KMS is used internally, and decryption is only possible with KMS permissions.)

```
[ec2-user@bastin ~]$ aws ssm get-parameters --name 'pgsql.connect.password'
{
    "InvalidParameters": [],
    "Parameters": [
        {
            "Name": "pgsql.connect.password",
            "DataType": "text",
            "LastModifiedDate": 1592740007.647,
            "Value": "AQICAHimGbBDsXKAeEMDoI4Kw/rpZAgukrSwYmqXyAKBupBtkwFYzzG2rJ2dnIePkkrTPZdsAAAAZjBkBgkqhkiG9w0BBwagVzBVAgEAMFAGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMoiJHw/NeYmZj35gYAgEQgCNgQlRcIz7EgkLxyHV4weHFwONVhdTI9m3OilaP2ikVHLbqQg==",
            "Version": 1,
            "Type": "SecureString",
            "ARN": "arn:aws:ssm:ap-northeast-1:xxxxxx:parameter/pgsql.connect.password"
        }
    ]
}
[ec2-user@bastin ~]$
[ec2-user@bastin ~]$ aws ssm get-parameters --name 'pgsql.connect.password' --with-decryption
{
    "InvalidParameters": [],
    "Parameters": [
        {
            "Name": "pgsql.connect.password",
            "DataType": "text",
            "LastModifiedDate": 1592740007.647,
            "Value": "p@sstest",
            "Version": 1,
            "Type": "SecureString",
            "ARN": "arn:aws:ssm:ap-northeast-1:xxxxxx:parameter/pgsql.connect.password"
        }
    ]
}
```

#### Connecting to Aurora (PostgreSQL)

Using the `aws ssm get-parameters` command eliminates the security risk of hardcoding passwords.

```sh
[ec2-user@bastin ~]$ export PGUSER=$(aws ssm get-parameters --name 'pgsql.connect.userid' | jq -r '.Parameters[].Value')
[ec2-user@bastin ~]$ export PGPASSWORD=$(aws ssm get-parameters --name 'pgsql.connect.password' --with-decryption | jq -r '.Parameters[].Value')
[ec2-user@bastin ~]$
[ec2-user@bastin ~]$ echo $PGUSER
testuser
[ec2-user@bastin ~]$ echo $PGPASSWORD
p@sstest
[ec2-user@bastin ~]$
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=> \conninfo
You are connected to database "postgres" as user "testuser" on host "aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com" at port "5432".
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
postgres=>
```

Next, I'll try `AWS Secrets Manager`, which can be used similarly.

#### Additional References

EC2 Systems Manager "Parameter Store" That Can Store Arbitrary Parameters Turned Out to Be Convenient - kakakakakku blog https://kakakakakku.hatenablog.com/entry/2017/06/10/181603

AWS Parameter Store vs. Secrets Manager — Which Should You Use? Comparison - Qiita https://qiita.com/tomoya_oka/items/a3dd44879eea0d1e3ef5
