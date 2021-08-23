---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2上のRHEL8(Red Hat Enterprise Linux)にPostgreSQL11と12をyumでインストール"
subtitle: ""
summary: " "
tags: ["AWS","EC2","PostgreSQL","RHEL"]
categories: ["AWS","EC2","PostgreSQL","RHEL"]
url: aws-ec2-rhel-postgresql-install.html
date: 2020-05-18
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

EC2上のRHEL 8 (Red Hat Enterprise Linux)にPostgreSQL 11と12をyumでインストールしてみる。２つのバージョンを入れるのは後続の記事で整理予定のpg_upgradeの拡張機能を使用した検証をやってみたいから。Amazon Linux2にPostgreSQLをyumでインストールする方法はこちらをどうぞ。

> EC2(Amazon Linux2)にPostgreSQLをインストールする | my opinion is my own https://zatoima.github.io/postgresql-ec2-insatll.html

Red hatのバージョンはこちら

```
[ec2-user@pgsql ~]$ cat /etc/redhat-release 
Red Hat Enterprise Linux release 8.2 (Ootpa)
```

### リポジトリの追加

```
sudo yum -y localinstall https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
```

> 参考：PostgreSQL RPM Repository (with Yum) https://yum.postgresql.org/repopackages.php

### EPELリポジトリの追加

> PostgreSQL RPM Repository (with Yum) https://yum.postgresql.org/repopackages.php
>
> Please note that PostgreSQL YUM repository depends on EPEL repository for some packages. RHEL/CentOS/, etc. users should install EPEL repo RPM along with PGDG repo RPMs to satisfy dependencies.

上記の記載の通り、EPELリポジトリのいくつかのパッケージに依存しているため、EPELリポジトリを追加する必要がある模様。（特にインストールせずともインストール自体は出来た。）

 [EPEL](https://fedoraproject.org/wiki/EPEL/ja)（Extra Packages for Enterprise Linux）とは、Red Hat Enterprise Linux（RHEL）向けの「追加パッケージ」を提供するリポジトリ。

```sh
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
```

インストール実施後、epelリポジトリが使用可能になる。

```
[ec2-user@pgsql ~]$ yum repolist
repo id                                                                     repo name                                                                                                 status
epel/x86_64                                                                 Extra Packages for Enterprise Linux 7 - x86_64                                                            13,273
```

### インストール可能なバージョンの確認

postgresql11と12の最新版の11.8と12.3が使用可能。RHEL7用のリポジトリに入っているPostgreSQLのパッケージ名と微妙に違うような、、、

```
[ec2-user@pgsql ~]$ sudo yum info postgresql11-server
Last metadata expiration check: 1:06:25 ago on Sat 16 May 2020 07:30:17 PM JST.
Installed Packages
Name         : postgresql11-server
Version      : 11.8
Release      : 1PGDG.rhel8
Architecture : x86_64
Size         : 19 M
Source       : postgresql11-11.8-1PGDG.rhel8.src.rpm
Repository   : @System
From repo    : pgdg11
Summary      : The programs needed to create and run a PostgreSQL server
URL          : https://www.postgresql.org/
License      : PostgreSQL
Description  : PostgreSQL is an advanced Object-Relational database management system (DBMS).
             : The postgresql11-server package contains the programs needed to create
             : and run a PostgreSQL server, which will in turn allow you to create
             : and maintain PostgreSQL databases.
[ec2-user@pgsql ~]$ sudo yum info postgresql12-server
Last metadata expiration check: 1:06:37 ago on Sat 16 May 2020 07:30:17 PM JST.
Installed Packages
Name         : postgresql12-server
Version      : 12.3
Release      : 1PGDG.rhel8
Architecture : x86_64
Size         : 20 M
Source       : postgresql12-12.3-1PGDG.rhel8.src.rpm
Repository   : @System
From repo    : pgdg12
Summary      : The programs needed to create and run a PostgreSQL server
URL          : https://www.postgresql.org/
License      : PostgreSQL
Description  : PostgreSQL is an advanced Object-Relational database management system (DBMS).
             : The postgresql12-server package contains the programs needed to create
             : and run a PostgreSQL server, which will in turn allow you to create
             : and maintain PostgreSQL databases.
```

### PostgreSQL11のインストール

PostgreSQL11をインストールしてみる。

```sh
sudo yum -y install postgresql11-server
```

バージョンを確認。

```
[ec2-user@pgsql ~]$ /usr/pgsql-11/bin/postgres --version
postgres (PostgreSQL) 11.8
```

OS側にpostgresユーザが作成される。

```
[ec2-user@pgsql ~]$ cat /etc/passwd
～中略～
ec2-user:x:1000:1000:Cloud User:/home/ec2-user:/bin/bash
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash
```

postgresql11-contribとpostgresql11-develも合わせてインストールする。

```sh
[ec2-user@pgsql ~]$ sudo yum -y install postgresql11-contrib.x86_64 postgresql11-devel.x86_64
```

### PostgreSQL12のインストール

PostgreSQL12をインストールする。（※手順はPostgreSQL11とほぼ一緒）

```sh
sudo yum -y install postgresql12-server
```

バージョンを確認してみる。

```
[ec2-user@pgsql ~]$ /usr/pgsql-12/bin/postgres --version
postgres (PostgreSQL) 12.3
```

postgresql11-contribとpostgresql11-develも合わせてインストールする。

```sh
[ec2-user@pgsql ~]$ sudo yum -y install postgresql12-contrib.x86_64 postgresql12-devel.x86_64
```

### DB初期化、PostgreSQLの起動停止、接続確認等

DBの初期化を行う。rootで実施。

```sh
[root@pgsql ~]# /usr/pgsql-11/bin/postgresql-11-setup initdb
Initializing database ... OK
[root@pgsql ~]# /usr/pgsql-12/bin/postgresql-12-setup initdb
Initializing database ... OK
```

自動起動設定を行う

```sh
[root@pgsql ~]# systemctl enable postgresql-11
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-11.service to /usr/lib/systemd/system/postgresql-12.service.
[root@pgsql ~]# systemctl enable postgresql-12
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-12.service to /usr/lib/systemd/system/postgresql-12.service.
```

PostgreSQL11と12で起動ポートが重複するため、PostgreSQL12用のpostgresql.confを修正して一方の起動ポートを変更する

```
sed -i "s/#port = 5432/port = 5433/g" "/var/lib/pgsql/12/data/postgresql.conf"
```

問題なくPostgreSQLの起動、停止、再起動が出来るか確認する

```sh
sudo systemctl start postgresql-11.service
sudo systemctl stop postgresql-11.service
sudo systemctl restart postgresql-11.service

sudo systemctl start postgresql-12.service
sudo systemctl stop postgresql-12.service
sudo systemctl restart postgresql-12.service
```

環境変数を用意

```
vi .pgsql11_env

--------------
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/usr/pgsql-11/bin
[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/11/data
export PGDATA

export PGPORT=5432

# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile
--------------
```

```
vi .pgsql12_env

--------------
export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/usr/pgsql-12/bin
[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/12/data
export PGDATA

export PGPORT=5433

# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile
--------------
```

接続確認

```
[postgres@pgsql ~]$ . .pgsql11_env 
[postgres@pgsql ~]$ 
[postgres@pgsql ~]$ psql
psql (12.3, server 11.8)
Type "help" for help.

postgres=# select version();
                                                version                                     
            
--------------------------------------------------------------------------------------------
------------
 PostgreSQL 11.8 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 8.3.1 20191121 (Red Hat 8.3.1
-5), 64-bit
(1 row)
[postgres@pgsql ~]$ . .pgsql12_env 
[postgres@pgsql ~]$ psql
psql (12.3)
Type "help" for help.

postgres=# select version();
                                                version                                     
            
--------------------------------------------------------------------------------------------
------------
 PostgreSQL 12.3 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 8.3.1 20191121 (Red Hat 8.3.1
-5), 64-bit
(1 row)

```

次はこの環境を使ってpg_upgradeの動作確認検証を行う予定。