---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLのFLUSH PRIVILEGESが必要なケース"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-flush-privileges.html
date: 2019-07-01
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



### はじめに

MySQLで権限周りのオペレーションをする時に脳死状態で `FLUSH PRIVILEGES`を実行しているケースがあります。

### 権限管理の概要

権限周りの情報は`user`、`db`、`tables_priv`、`columns_priv`、および `procs_priv` あたりのテーブルに保持していて、高速化のためにメモリ上のキャッシュに保持している模様。

> https://dev.mysql.com/doc/refman/5.6/ja/privileges-provided.html
>
> 6.2.1 MySQL で提供される権限
>
> アカウント権限に関する情報は、`mysql` データベース内の `user`、`db`、`tables_priv`、`columns_priv`、および `procs_priv` テーブルに格納されます ([セクション6.2.2「権限システム付与テーブル」](https://dev.mysql.com/doc/refman/5.6/ja/grant-tables.html)を参照してください)。MySQL サーバーはこれらのテーブルの内容を起動時にメモリーに読み取り、[セクション6.2.6「権限変更が有効化される時期」](https://dev.mysql.com/doc/refman/5.6/ja/privilege-changes.html)に示す条件でこれらを再ロードします。

`GRANT`、`REVOKE`、`SET PASSWORD`、`RENAME USER` で操作を行った場合は特に `FLUSH PRIVILEGES`は不要と明示的にこちらに書いています。

> https://dev.mysql.com/doc/refman/5.6/ja/privilege-changes.html
>
> ### 6.2.6 権限変更が有効化される時期
>
> ユーザーが `GRANT`、`REVOKE`、`SET PASSWORD`、`RENAME USER` などのアカウント管理ステートメントを使用して、付与テーブルを間接的に変更した場合、サーバーはそれらの変更を認識し、再びすぐに付与テーブルをメモリーにロードします。
>
> `INSERT`、`UPDATE`、`DELETE` などのステートメントを使用して、付与テーブルを直接変更する場合、サーバーを再起動するか、テーブルをリロードするようサーバーに指示するまで、変更内容は権限チェックに影響しません。付与テーブルを直接変更したが、それらをリロードし忘れた場合、サーバーを再起動するまで変更は*影響しません*。このため、変更したのに違いが現れないことを不思議に思うことがあるかもしれません。

### FLUSH PRIVILEGESが不要なケース

#### ユーザ作成

```sql
CREATE USER 'mytest'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

#### ユーザー一覧を表示する

```sql
SELECT host, user FROM mysql.user;
```

#### 権限付与

```sql
grant all on *.* to 'mytest'@'localhost' IDENTIFIED BY 'Oracle2019%';
```

#### 権限確認

```sql
show grants for mytest@localhost;
```

#### 権限剥奪

```sql
revoke all on *.* from 'mytest'@'localhost';
```

### FLUSH PRIVILEGESが必要なケース

#### ユーザ削除

一方、`INSERT`、`UPDATE`、`DELETE` などのステートメントを使用して、付与テーブルを直接変更する場合、サーバーを再起動するか、テーブルをリロードするようサーバーに指示するまで、変更内容は権限チェックに影響しません。と記載があるので、deleteでmysql.userを直接メンテナンスする場合の挙動とDROP USERした場合の挙動を実機で確認してみる。

##### 1.)drop userを使用した場合

```sql
DROP USER mytest@'localhost';
```

drop userの場合はアカウント管理ステートメントになるのでuser関連のメモリ上の情報も同期的にflushされる。（FLUSH PRIVILEGESは不要）

```sql
【コマンド結果】
mysql> DROP USER mytest@'localhost';
Query OK, 0 rows affected (0.00 sec)
mysql> show grants for mytest@localhost;
ERROR 1141 (42000): There is no such grant defined for user 'mytest' on host 'localhost'
```

##### 2.)mysql.userからdelete文で削除

```sql
delete from mysql.user where user like 'mytest' and host like 'localhost';
```

drop userと異なりこちらのユーザ削除方法の場合は、メモリに権限関連の情報が残ってしまうので `FLUSH PRIVILEGES` が必要になってくる。

```sql
mysql> delete from mysql.user where user like 'mytest' and host like 'localhost';
Query OK, 1 row affected (0.00 sec)

mysql> show grants for mytest@localhost; #mytestユーザの情報が残っている。
+--------------------------------------------+
| Grants for mytest@localhost                |
+--------------------------------------------+
| GRANT USAGE ON *.* TO 'mytest'@'localhost' |
+--------------------------------------------+
1 row in set (0.00 sec)

mysql> FLUSH PRIVILEGES; #flush privilegesコマンドで反映
Query OK, 0 rows affected (0.01 sec)

mysql> show grants for mytest@localhost;
ERROR 1141 (42000): There is no such grant defined for user 'mytest' on host 'localhost'
mysql>
```

### まとめ

今回はユーザ削除を例に実施してみたが、直接user表をメンテするようなオペレーションする場合は`FLUSH PRIVILEGES`必要になってくるはず。

