---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQL検証用テーブル作成（データベース作成～テストデータの準備まで）"
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


データベース作成、ユーザ作成、権限付与、テーブル作成、テストデータの準備までを実施。

### database作成

```sql
CREATE DATABASE mydb;
show databases;

use mydb;
```

### ユーザ作成

```sql
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

### ユーザー一覧を表示する

```sql
SELECT host, user FROM mysql.user;
```

### 権限付与

```sql
grant all on *.* to 'myuser'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

### 作成したユーザで接続

```sql
mysql -u myuser -p
```

### テーブル作成

```sql
CREATE TABLE t1 (
  a INT PRIMARY KEY AUTO_INCREMENT,
  b VARCHAR(10),
  c VARCHAR(30),
  d INT UNSIGNED,
  e DATETIME
);
```

### テストデータの挿入

```sql
INSERT INTO t1 () VALUES ();
INSERT INTO t1 (a) SELECT 0 FROM t1;
INSERT INTO t1 (a) SELECT 0 FROM t1;
INSERT INTO t1 (a) SELECT 0 FROM t1;
INSERT INTO t1 (a) SELECT 0 FROM t1;

UPDATE t1 SET
  b = CONCAT('商品', a),
  c = SUBSTRING(MD5(RAND()), 1, 30),
  d = CEIL(RAND() * 10000),
  e = ADDTIME(CONCAT_WS(' ','2014-01-01' + INTERVAL RAND() * 180 DAY, '00:00:00'), SEC_TO_TIME(FLOOR(0 + (RAND() * 86401))));

```

### 参考

> SQLで大量のテストデータ作成 - Qiita https://qiita.com/cobot00/items/8d59e0734314a88d74c7
