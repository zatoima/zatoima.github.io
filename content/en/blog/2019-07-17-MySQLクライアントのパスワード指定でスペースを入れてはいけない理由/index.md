---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Why You Should Not Include a Space When Specifying a Password for the MySQL Client"
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



### Do Not Put a Space When Specifying the Password
When logging into MySQL, you typically use the command `mysql -u root -p<password>`. There have been many cases where adding a space after `-p` results in an error (or prompts for a password). I re-checked the manual to understand why a space is not allowed.

> MySQL :: MySQL 5.6 Reference Manual :: 4.2.4 Using Options on the Command Line https://dev.mysql.com/doc/refman/5.6/ja/command-line-options.html
>
> The password option can also be specified in its short form as `-p*pass_val*` or `-p`. However, in the short form, if you specify the password value, it must follow the option letter *with no intervening space*. The reason for this is that if a space follows the option letter, the program has no way to tell whether the following argument is the password value or some other type of argument.

This is documented clearly. Because of the ambiguity when a space is added, it is strictly not allowed, as the program cannot determine whether the specified password is actually a password or another type of option argument.

#### Specifying the Password Without a Space (Correct Method)

Logs in successfully.

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

#### Specifying the Password With a Space (Incorrect Method)

As shown by the `Enter password:` output in the console, the `mysql` password that was supposedly specified is not recognized. After logging in, checking with the status command shows a connection to the "mysql" database.

The `mysql` that was thought to be the password is being interpreted as the database name to log into.

*As a note: please don't use "mysql" as a password in the first place. Also, as shown in the warning, don't enter the password directly on the command line when logging in. The password can be revealed by the history command and is a security risk.*

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
Current database:       mysql   ★← Connected to "mysql" database
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
