---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLクライアントのパスワード指定でスペースを入れてはいけない理由"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-password-space.html
date: 2019-07-17
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



### パスワード指定でスペースを入れたらダメ
MySQLにログインする場合、`mysql -u root -p<パスワード>` というコマンドでログインすると思います。`-p`の後ろにスペースを入れてしまい、エラー(もしくはパスワードを求められる)になるというケースが幾度となくありました。スペースを入れてはいけない理由を改めてマニュアルから確認しました。

> MySQL :: MySQL 5.6 リファレンスマニュアル :: 4.2.4 コマンド行でのオプションの使用 https://dev.mysql.com/doc/refman/5.6/ja/command-line-options.html
>
> パスワードオプションは、短い形式で `-p*pass_val*` または `-p` としても指定できます。しかし短い形式の場合、パスワード値を指定する場合は、*間にスペースを入れずに*オプション文字に続けなければいけません。この理由は、オプション文字にスペースが続く場合、続く引数がパスワード値なのかほかの種類の引数なのかをプログラムが判断する方法がないためです。

ここに記載がありますね。スペースを空けてしまうと指定されたパスワードが本当にパスワードなのか他の種類のオプション引数なのかを判別出来ないので厳格にスペースを許可していないとのことでした。

#### スペースを空けずにパスワードを指定（正しい指定方法）

正常にログインが出来ます。

```sql
[root@awsstg-db002 mysql]# mysql -u root -pmysql
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 18
Server version: 5.7.26-log MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>

```

#### スペースを空けてパスワードを指定（誤った指定方法）

`Enter password:`とコンソールに出力されている通り、指定したはずの`mysql`というパスワードが認識されていません。ログイン後にstatusコマンドでどこのデータベースにログインしているか確認してみると「mysql」データベースに接続されています。

パスワードを打ったと思った`mysql`がログインするデータベース名と認識されています。

※そもそもですがパスワードにmysqlとか使うのはやめましょう。あとワーニングにも出力されていますが、ログイン時にパスワードを直書きするのもやめましょう。historyコマンドなどでパスワードがわかってしまいセキュリティ的によくありません。

> mysql: [Warning] Using a password on the command line interface can be insecure.

```sql
[root@awsstg-db002 mysql]# mysql -u root -p mysql
Enter password:
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 5.7.26-log MySQL Community Server (GPL)

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> status
--------------
mysql  Ver 14.14 Distrib 5.7.26, for Linux (x86_64) using  EditLine wrapper

Connection id:          15
Current database:       mysql   ★←
Current user:           root@localhost
SSL:                    Not in use
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         5.7.26-log MySQL Community Server (GPL)
Protocol version:       10
Connection:             Localhost via UNIX socket
Server characterset:    utf8mb4
Db     characterset:    latin1
Client characterset:    utf8mb4
Conn.  characterset:    utf8mb4
UNIX socket:            /var/lib/mysql/mysql.sock
Uptime:                 1 day 5 hours 50 min 25 sec

Threads: 4  Questions: 304  Slow queries: 0  Opens: 242  Flush tables: 1  Open tables: 231  Queries per second avg: 0.002
--------------

mysql>

```