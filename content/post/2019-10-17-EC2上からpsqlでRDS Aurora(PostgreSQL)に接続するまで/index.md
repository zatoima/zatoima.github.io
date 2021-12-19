---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2上からpsqlでAurora(PostgreSQL)に接続するまで"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "RDS", "Aurora", "PostgreSQL"]
categories: ["AWS", "EC2", "RDS", "Aurora", "PostgreSQL"]
url: aws-ec2-psql-install.html
date: 2019-10-17
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: falsEC
---





EC2にpsqlをインストールし、その後構築済みのAurora(PostgreSQL)の環境に接続するまでをメモ。

### 実行コマンド

```sh
sudo yum search postgresql
sudo yum -y install postgresql.x86_64

psql -h <エンドポイント> -U <ユーザ名> -d <DB名>
```

### OS情報

```sh
[ec2-user@donald-dev-ec2-bastin ~]$ uname -a
Linux donald-dev-ec2-bastin x.xx.xxx-xxx.xxx.amzn2.x86_64 #1 SMP Thu Aug 15 15:29:58 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

### yum searchでPostgreSQL client programsを探す

実行結果から`postgresql.x86_64`が`PostgreSQL client programs`と判明。

```sh
[ec2-user@donald-dev-ec2-bastin ~]$ sudo yum search postgresql
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
================================================================================= N/S matched: postgresql ==================================================================================
freeradius-postgresql.x86_64 : Postgresql support for freeradius
pcp-pmda-postgresql.x86_64 : Performance Co-Pilot (PCP) metrics for PostgreSQL
postgresql.x86_64 : PostgreSQL client programs
postgresql-contrib.x86_64 : Extension modules distributed with PostgreSQL
postgresql-devel.x86_64 : PostgreSQL development header files and libraries
postgresql-docs.x86_64 : Extra documentation for PostgreSQL
postgresql-jdbc.noarch : JDBC driver for PostgreSQL
postgresql-jdbc-javadoc.noarch : API docs for postgresql-jdbc
postgresql-libs.x86_64 : The shared libraries required for any PostgreSQL clients
postgresql-libs.i686 : The shared libraries required for any PostgreSQL clients
postgresql-odbc.x86_64 : PostgreSQL ODBC driver
postgresql-plperl.x86_64 : The Perl procedural language for PostgreSQL
postgresql-plpython.x86_64 : The Python2 procedural language for PostgreSQL
postgresql-pltcl.x86_64 : The Tcl procedural language for PostgreSQL
postgresql-server.x86_64 : The programs needed to create and run a PostgreSQL server
postgresql-static.x86_64 : Statically linked PostgreSQL libraries
postgresql-test.x86_64 : The test suite distributed with PostgreSQL
postgresql-upgrade.x86_64 : Support for upgrading from the previous major release of PostgreSQL
qt-postgresql.x86_64 : PostgreSQL driver for Qt's SQL classes
qt-postgresql.i686 : PostgreSQL driver for Qt's SQL classes
qt3-PostgreSQL.x86_64 : PostgreSQL drivers for Qt 3's SQL classes
qt3-PostgreSQL.i686 : PostgreSQL drivers for Qt 3's SQL classes
qt5-qtbase-postgresql.x86_64 : PostgreSQL driver for Qt5's SQL classes
qt5-qtbase-postgresql.i686 : PostgreSQL driver for Qt5's SQL classes
PyGreSQL.x86_64 : A Python client library for PostgreSQL
apr-util-pgsql.x86_64 : APR utility library PostgreSQL DBD driver
libdbi-dbd-pgsql.x86_64 : PostgreSQL plugin for libdbi
perl-DBD-Pg.x86_64 : A PostgreSQL interface for perl
php-pgsql.x86_64 : A PostgreSQL database module for PHP
python-psycopg2.x86_64 : A PostgreSQL database adapter for Python
python-psycopg2-debug.x86_64 : A PostgreSQL database adapter for Python 2 (debug build)
python-psycopg2-doc.x86_64 : Documentation for psycopg python PostgreSQL database adapter
redland-pgsql.x86_64 : PostgreSQL storage support for Redland
rhdb-utils.x86_64 : Miscellaneous utilities for PostgreSQL - Red Hat Edition
tcl-pgtcl.x86_64 : A Tcl client library for PostgreSQL

  Name and summary matches only, use "search all" for everything.
[ec2-user@donald-dev-ec2-bastin ~]$ 
```

### PostgreSQL client programsをインストール

```sh
[ec2-user@donald-dev-ec2-bastin ~]$ sudo yum -y install postgresql.x86_64
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                                                                                                                                           | 2.4 kB  00:00:00     
Resolving Dependencies
--> Running transaction check
---> Package postgresql.x86_64 0:9.2.24-1.amzn2.0.1 will be installed
--> Processing Dependency: postgresql-libs(x86-64) = 9.2.24-1.amzn2.0.1 for package: postgresql-9.2.24-1.amzn2.0.1.x86_64
--> Processing Dependency: libpq.so.5()(64bit) for package: postgresql-9.2.24-1.amzn2.0.1.x86_64
--> Running transaction check
---> Package postgresql-libs.x86_64 0:9.2.24-1.amzn2.0.1 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================================================================
 Package                                         Arch                                   Version                                            Repository                                  Size
============================================================================================================================================================================================
Installing:
 postgresql                                      x86_64                                 9.2.24-1.amzn2.0.1                                 amzn2-core                                 3.0 M
Installing for dependencies:
 postgresql-libs                                 x86_64                                 9.2.24-1.amzn2.0.1                                 amzn2-core                                 235 k

Transaction Summary
============================================================================================================================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 3.3 M
Installed size: 17 M
Downloading packages:
(1/2): postgresql-libs-9.2.24-1.amzn2.0.1.x86_64.rpm                                                                                                                 | 235 kB  00:00:00     
(2/2): postgresql-9.2.24-1.amzn2.0.1.x86_64.rpm                                                                                                                      | 3.0 MB  00:00:00     
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                        15 MB/s | 3.3 MB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : postgresql-libs-9.2.24-1.amzn2.0.1.x86_64                                                                                                                                1/2 
  Installing : postgresql-9.2.24-1.amzn2.0.1.x86_64                                                                                                                                     2/2 
  Verifying  : postgresql-9.2.24-1.amzn2.0.1.x86_64                                                                                                                                     1/2 
  Verifying  : postgresql-libs-9.2.24-1.amzn2.0.1.x86_64                                                                                                                                2/2 

Installed:
  postgresql.x86_64 0:9.2.24-1.amzn2.0.1                                                                                                                                                    

Dependency Installed:
  postgresql-libs.x86_64 0:9.2.24-1.amzn2.0.1                                                                                                                                               

Complete!
[ec2-user@donald-dev-ec2-bastin ~]$ 

```

### Aurora(PostgreSQL)へ接続

接続時にはセキュリティグループ等でEC2上の踏み台サーバからPostgreSQLへの接続を許可が必要。

```sh
[ec2-user@donald-dev-ec2-bastin ~]$ psql -h <エンドポイント> -U <ユーザ名> -d <DB名>
Password for user master: 
psql (9.2.24, server 10.7)
WARNING: psql version 9.2, server version 10.0.
         Some psql features might not work.
SSL connection (cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256)
Type "help" for help.

aurorapostdb=> 
```

### その他

EC2構築直後の状態で `yum -y install postgresql.x86_64`を行った場合、デフォルトのリポジトリを参照するのでpsqlのバージョンが古い。そういった場合は、手動でリポジトリを追加して任意のpsqlのバージョンをダウンロードすれば良い。

参考：

> EC2(Amazon Linux2)にPostgreSQLをインストールする | my opinion is my own https://zatoima.github.io/postgresql-ec2-insatll.html



