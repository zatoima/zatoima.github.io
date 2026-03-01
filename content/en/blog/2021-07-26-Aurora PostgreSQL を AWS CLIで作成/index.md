---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Creating Aurora PostgreSQL with AWS CLI"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-aurora-aws-cli-create-cluster-instance
date: 2021-07-26
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



The flow appears to be `create-db-cluster` → `create-db-instance`. Since it cannot be done in a single command, multiple executions are required.

### Creating a Cluster

```sh
aws rds create-db-cluster \
    --db-cluster-identifier        aurorapgsqlv1-cluster1 \
    --engine                       aurora-postgresql \
    --engine-version               11.9 \
    --master-username              postgres \
    --master-user-password         postgres \
    --db-subnet-group-name         devvpc-db-sub-pvt \
    --vpc-security-group-ids       sg-01f24d968d81d144a \
    --availability-zones           "ap-northeast-1a" "ap-northeast-1c" "ap-northeast-1d" \
    --port                         5432 \
    --database-name                postgres
```

> create-db-cluster — AWS CLI 1.20.3 Command Reference https://docs.aws.amazon.com/cli/latest/reference/rds/create-db-cluster.html

### Creating an Instance

```sh
aws rds create-db-instance \
    --db-instance-identifier       aurorapgsqlv1-instance1 \
    --db-instance-class            db.r5.large \
    --engine                       aurora-postgresql \
    --engine-version               11.9 \
    --availability-zone            "ap-northeast-1c"  \
    --db-cluster-identifier        aurorapgsqlv1-cluster1 \
    --db-parameter-group-name      aurora-pgsql11
```

To create a read replica, run the same command again:

```sh
aws rds create-db-instance \
    --db-instance-identifier       aurorapgsqlv1-instance2 \
    --db-instance-class            db.r5.large \
    --engine                       aurora-postgresql \
    --engine-version               11.9 \
    --availability-zone            "ap-northeast-1d" \
    --db-cluster-identifier        aurorapgsqlv1-cluster1 \
    --db-parameter-group-name      aurora-pgsql11
```

> create-db-instance — AWS CLI 1.20.3 Command Reference https://docs.aws.amazon.com/cli/latest/reference/rds/create-db-instance.html

### Result

As shown below, it was confirmed from the management console as well.

![image-20210721234314409](image-20210721234314409.png)
