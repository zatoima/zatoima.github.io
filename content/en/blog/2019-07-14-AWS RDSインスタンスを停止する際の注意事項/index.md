---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Precautions When Stopping an AWS RDS Instance"
subtitle: ""
summary: " "
tags: ["AWS", "RDS"]
categories: ["AWS", "RDS"]
url: aws-rds-stop-cautions.html
date: 2019-07-14
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



### Introduction

After reading the following RDS manual, I noticed several pitfalls worth noting.

> Temporarily stopping an Amazon RDS DB instance - Amazon Relational Database Service https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/USER_StopInstance.html

### Maximum Days for Stopping

A stop is only possible for a maximum of 1 week. Be aware that **stopping does not mean you won't be charged indefinitely**.

> You can stop a DB instance for up to 7 days. If you don't start your DB instance manually in 7 days, Amazon RDS automatically starts your DB instance so that it doesn't fall behind any required maintenance updates.

### DB Engines That Can Be Stopped

Most DB engines can be stopped.

> MariaDB
>
> Microsoft SQL Server
>
> MySQL
>
> Oracle
>
> PostgreSQL

However, as noted: `You can't stop a Multi-AZ Amazon RDS for SQL Server DB instance`, so be careful when operating Multi-AZ SQL Server.

### Restrictions

> You can't stop a DB instance that has a read replica, or that is a read replica.
>
> You can't stop a Multi-AZ Amazon RDS for SQL Server DB instance.
>
> You can't modify a stopped DB instance.
>
> You can't delete an option group that is associated with a stopped DB instance.
>
> You can't delete a DB parameter group that is associated with a stopped DB instance.

##### You can't modify a stopped DB instance.

This means that if you want to upgrade the instance type while stopped, you cannot do so while it is stopped.

##### You can't stop a DB instance that has a read replica, or that is a read replica.

While this might be acceptable in development environments, in production environments many system configurations use read replicas, so there are likely many systems that cannot use the stop operation due to this restriction.

### Summary

Buffer caches, shared pools (Oracle), InnoDB buffer pools (MySQL), etc. are naturally cleared from the cache when the DB is restarted. (Using MySQL InnoDB buffer pool preloading may help.)

Since buffer caches and shared pools are critically important for SQL performance, you should only use the RDS stop operation when there is a clear reason to prioritize cost over performance and operational management (such as a development environment). At minimum, a different way of thinking is required compared to DB on EC2 operations.

### Reference

> Why you shouldn't use stop operation for RDS in production – Server Works Engineer Blog http://blog.serverworks.co.jp/tech/2019/06/26/stopdbinstance/
