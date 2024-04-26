---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Systems Managerのパラメータストアを使用してAurora PostgreSQLのパスワードを管理"
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

### 事前準備

#### はじめに

Aurora PostgreSQL側にユーザ名`testuser`、パスワード`p@sstest`で作成。

```
CREATE ROLE testuser WITH LOGIN PASSWORD 'p@sstest';
```

psqlでログインする場合には環境変数に設定して下記のように接続。パスワードをどこかに持つ必要があってセキュアな状態とは言えない。。。

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

#### Systems Managerにパラメータを格納

2つのパラメータを格納してみる。useridは`平文(String)`でpasswordは`SecureString`で格納。

```
aws ssm put-parameter --name 'pgsql.connect.userid' --type 'String' --value 'testuser'
aws ssm put-parameter --name 'pgsql.connect.password' --type 'SecureString' --value 'p@sstest'
```

パラメータを取得してみる。`pgsql.connect.userid`を取得する。

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

次に`pgsql.connect.password`を取得。`SecureString`で格納したパラメータについては`--with-decryption`を付与してコマンドを実行する必要がある。このオプションがないと暗号化された状態でvalueが出力される。（内部的にはKMSが使用されており、KMSの使用権限を持っていなければ復号化が出来ない。）

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

#### Aurora(PostgreSQL)へ接続

`aws ssm get-parameters`コマンドを使用することでパスワードを直書きするというセキュリティ的なリスクが無くなる。

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

次は同じような使い方が出来る`AWS Secrets Manager`を触ってみる。

#### その他参考情報

任意のパラメータを格納できる EC2 Systems Manager「パラメータストア」を試したら便利だった - kakakakakku blog https://kakakakakku.hatenablog.com/entry/2017/06/10/181603

AWSのParameter StoreとSecrets Manager、結局どちらを使えばいいのか？比較 - Qiita https://qiita.com/tomoya_oka/items/a3dd44879eea0d1e3ef5

