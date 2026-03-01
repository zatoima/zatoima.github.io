---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Creating MySQL Test Tables (From Database Creation to Test Data Preparation)"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-testtable-create.html
date: 2019-06-27
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


Steps from database creation, user creation, privilege granting, table creation, through test data preparation.

### Creating a database

```sql
CREATE DATABASE mydb;
show databases;

use mydb;
```

### Creating a user

```sql
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

### Displaying the user list

```sql
SELECT host, user FROM mysql.user;
```

### Granting privileges

```sql
grant all on *.* to 'myuser'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

### Connecting with the created user

```sql
mysql -u myuser -p
```

### Creating a table

```sql
CREATE TABLE t1 (
  a INT PRIMARY KEY AUTO_INCREMENT,
  b VARCHAR(10),
  c VARCHAR(30),
  d INT UNSIGNED,
  e DATETIME
);
```

### Inserting test data

```sql
INSERT INTO t1 () VALUES ();
INSERT INTO t1 (a) SELECT 0 FROM t1;
INSERT INTO t1 (a) SELECT 0 FROM t1;
INSERT INTO t1 (a) SELECT 0 FROM t1;
INSERT INTO t1 (a) SELECT 0 FROM t1;

UPDATE t1 SET
  b = CONCAT('Item', a),
  c = SUBSTRING(MD5(RAND()), 1, 30),
  d = CEIL(RAND() * 10000),
  e = ADDTIME(CONCAT_WS(' ','2014-01-01' + INTERVAL RAND() * 180 DAY, '00:00:00'), SEC_TO_TIME(FLOOR(0 + (RAND() * 86401))));

```

### Reference

> Creating large amounts of test data with SQL - Qiita https://qiita.com/cobot00/items/8d59e0734314a88d74c7
