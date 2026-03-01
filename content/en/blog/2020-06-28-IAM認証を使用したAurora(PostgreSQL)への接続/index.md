---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Connecting to Aurora (PostgreSQL) Using IAM Authentication"
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

### Enable IAM Database Authentication

Enable using the Management Console or the following command:

```sh
aws rds modify-db-cluster --db-cluster-identifier aurorapgsqlv1 --apply-immediately --enable-iam-database-authentication
```

### Verify IAM Database Authentication Is Enabled

```sh
aws rds describe-db-clusters --db-cluster-identifier aurorapgsqlv1 --query 'DBClusters[].[IAMDatabaseAuthenticationEnabled]' --output table
```

### Create a PostgreSQL User for IAM Database Authentication

`rds_iam` is fixed.

```sql
CREATE USER iam_user WITH LOGIN;
grant rds_iam to iam_user;
```

### Create an IAM Policy

Create `iam_rds_connect.json` to create from AWS CLI:

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

Specify the region, account ID, cluster ID, and PostgreSQL username in the `Resource` section.

The cluster ID can be retrieved with the following CLI command:

```sh
aws rds describe-db-clusters --db-cluster-identifier aurorapgsqlv1 --query "DBClusters[0].[DbClusterResourceId]"
```

#### Create the IAM Policy

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

If the IAM user has strong permissions like `AdministratorAccess`, this is sufficient. If permissions are restricted, you also need to `Attach the IAM policy to an IAM user or role`.

> Creating and Using an IAM Policy for IAM Database Access - Amazon Aurora https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.IAMPolicy.html

### Connecting to Aurora PostgreSQL Using IAM Database Authentication

Authentication credentials can be obtained with `aws rds generate-db-auth-token`. When connecting to PostgreSQL, set the token in the `PGPASSWORD` environment variable. Since the authentication token is long (hundreds of characters), this method is more practical than copy-pasting.

```sh
export PGPASSWORD=`aws --region ap-northeast-1 rds generate-db-auth-token --hostname aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com --port 5432 --username iam_user`
psql -h aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U iam_user -d postgres
```

##### Success Pattern

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

##### Failure Pattern

```sh
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U iam_user -d postgres
psql: FATAL:  password authentication failed for user "iam_user"
FATAL:  password authentication failed for user "iam_user"
```

### Closing Notes

There are various other authentication options for connecting to RDS (including Aurora), such as Systems Manager Parameter Store and Secrets Manager — it can be hard to decide which to use. Refer to the manual for other notes on IAM authentication. One thing that personally catches my attention is: "The maximum number of connections per second to your database cluster can be limited depending on the cluster type and your workload."

https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html

https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.html
> IAM database authentication limitations for MySQL
> IAM database authentication limitations for PostgreSQL
