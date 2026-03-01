---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "IAM認証を使用したAurora(PostgreSQL)への接続"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-iam-connect.html
date: 2020-06-28
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

### IAMデータベース認証の有効化

マネージメントコンソール、もしくは下記コマンドで有効化する

```sh
aws rds modify-db-cluster --db-cluster-identifier aurorapgsqlv1 --apply-immediately --enable-iam-database-authentication
```

### IAMデータベース認証が有効になっているか確認

```sh
aws rds describe-db-clusters --db-cluster-identifier aurorapgsqlv1 --query 'DBClusters[].[IAMDatabaseAuthenticationEnabled]' --output table
```

### IAMデータベース認証用のPostgreSQLユーザを作成

`rds_iam`は固定。

```sql
CREATE USER iam_user WITH LOGIN;
grant rds_iam to iam_user;
```

### IAMポリシーを作成

AWS CLIから作成するので`iam_rds_connect.json`を作成

```sh
cat << EOF > iam_rds_connect.json  
{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Effect": "Allow",
         "Action": [
             "rds-db:connect"
         ],
         "Resource": [
             "arn:aws:rds-db:ap-northeast-1:xxxxxxxxxxx:dbuser:cluster-ALPQLYUXTQZEQ7M7F5UBRC7WTU/iam_user"
         ]
      }
   ]
}
EOF
```

`Resource`箇所でリージョン、アカウントID、クラスタID、PostgreSQLのユーザ名を指定。

クラスタIDは下記CLIで確認が可能。

```sh
aws rds describe-db-clusters --db-cluster-identifier aurorapgsqlv1 --query "DBClusters[0].[DbClusterResourceId]"
```

#### IAMポリシーを作成

```sh
aws iam create-policy --policy-name iam_rds_connect --policy-document file://iam_rds_connect.json 
```

```sh
[ec2-user@bastin ~]$ aws iam create-policy --policy-name iam_rds_connect --policy-document file://iam_rds_connect.json 
{
    "Policy": {
        "PolicyName": "iam_rds_connect", 
        "PermissionsBoundaryUsageCount": 0, 
        "CreateDate": "2020-06-21T10:50:56Z", 
        "AttachmentCount": 0, 
        "IsAttachable": true, 
        "PolicyId": "ANPAR23YLZYEHAKGAXPDT", 
        "DefaultVersionId": "v1", 
        "Path": "/", 
        "Arn": "arn:aws:iam::xxxxxxxxxxx:policy/iam_rds_connect", 
        "UpdateDate": "2020-06-21T10:50:56Z"
    }
}
[ec2-user@bastin ~]$ 
```

IAMユーザが`AdministratorAccess`のように強い権限を所持していたらここまででOKで、権限を絞っているのであれば`IAM ユーザーまたはロールへの IAM ポリシーのアタッチ`が必要となる。

> IAM データベースアクセス用の IAM ポリシーの作成と使用 - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.IAMPolicy.html

### IAMデータベースを使用したAurora PostgreSQLへの接続

認証情報は `aws rds generate-db-auth-token`で取得可能。PostgreSQLへの接続時には環境変数のPGPASSWORDに変数として入れる。認証トークンは数百の文字で構成されて長いので、コピペしてログインよりもこちらの方法の方がスマート。

```sh
export PGPASSWORD=`aws --region ap-northeast-1 rds generate-db-auth-token --hostname aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com --port 5432 --username iam_user`
psql -h aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U iam_user -d postgres
```

##### 成功パターン

```sh
[ec2-user@bastin ~]$ export PGPASSWORD=`aws --region ap-northeast-1 rds generate-db-auth-token --hostname aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com --port 5432 --username iam_user`
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U iam_user -d postgres
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=> select version();
                                   version                                   
-----------------------------------------------------------------------------
 PostgreSQL 11.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.9.3, 64-bit
(1 row)

postgres=> select aurora_version();
 aurora_version 
----------------
 3.2.1
(1 row)
```

##### 失敗パターン

```sh
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U iam_user -d postgres
psql: FATAL:  password authentication failed for user "iam_user"
FATAL:  password authentication failed for user "iam_user"
```

### 最後に

RDS(Aurora含む)への接続時の認証は他にもSystems Manager パラメータストアやSecrets Manager等、色々あってどれを使うべきか迷う、、。IAM認証に関してその他の注意事項等はマニュアルを参照。`データベースクラスターの 1 秒あたりの最大接続数は、クラスタータイプとワークロードに応じて制限される場合があります。`と記載あるのが個人的には気になるところ。

https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html

https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.html
> IAM データベース認証の MySQL の制限事項
> IAM データベース認証の PostgreSQL の制限事項