---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2(Amazon Linux2)にPostgreSQLをインストールする"
subtitle: ""
summary: " "
tags: ["PostgreSQL","EC2","AWS"]
categories: ["PostgreSQL","EC2","AWS"]
url: postgresql-ec2-insatll.html
date: 2019-12-28
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



Amazon LinuxにRed hat用のリポジトリからyumでインストールしようとするとエラーになるので無理やりAmazon Linux2でYumでインストールしようという内容。

ちなみに、PostgreSQLのコミュニティでは下記がYumで利用可能なプラットフォームとされていますのでご注意ください。

> PostgreSQL RPM Repository (with Yum) https://yum.postgresql.org/
>
> ## Available Platforms
>
> - Red Hat Enterprise Linux/CentOS/Oracle Enterprise Linux 8
> - Red Hat Enterprise Linux/CentOS/Oracle Enterprise Linux/Scientific Linux 7
> - Red Hat Enterprise Linux/CentOS/Oracle Enterprise Linux/Scientific Linux 6
> - SuSE Enterprise Linux 12 SP5
> - Fedora 32
> - Fedora 31
> - Fedora 30

デフォルトで参照しているAmazon Linuxのリポジトリは古いので、リポジトリをlocalにinsatllする。ただ、Amazon Linuxにredhat用のリポジトリをyumでインストールしようとするとエラーになる。

> Error: Package: pgdg-redhat-repo-42.0-5.noarch (/pgdg-redhat-repo-latest.noarch)
>            Requires: /etc/redhat-release

```sh
[ec2-user@postdb ~]$ sudo yum -y localinstall https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
pgdg-redhat-repo-latest.noarch.rpm                                                                                                                                   | 5.8 kB  00:00:00     
Examining /var/tmp/yum-root-Ie6yep/pgdg-redhat-repo-latest.noarch.rpm: pgdg-redhat-repo-42.0-5.noarch
Marking /var/tmp/yum-root-Ie6yep/pgdg-redhat-repo-latest.noarch.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package pgdg-redhat-repo.noarch 0:42.0-5 will be installed
--> Processing Dependency: /etc/redhat-release for package: pgdg-redhat-repo-42.0-5.noarch
--> Processing Dependency: /etc/redhat-release for package: pgdg-redhat-repo-42.0-5.noarch
--> Finished Dependency Resolution
Error: Package: pgdg-redhat-repo-42.0-5.noarch (/pgdg-redhat-repo-latest.noarch)
           Requires: /etc/redhat-release
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
[ec2-user@postdb ~]$ 

```

Amazon Linux用のリポジトリがないので、rpmをダウンロードしてpgdg-redhat-all.repoを書き換える。

```sh
[ec2-user@postdb ~]$ wget https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
--2019-12-15 04:39:47--  https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
Resolving download.postgresql.org (download.postgresql.org)... 217.196.149.55, 72.32.157.246, 87.238.57.227, ...
Connecting to download.postgresql.org (download.postgresql.org)|217.196.149.55|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5932 (5.8K) [application/x-redhat-package-manager]
Saving to: ‘pgdg-redhat-repo-latest.noarch.rpm’

100%[==================================================================================================================================================>] 5,932       --.-K/s   in 0s      

2019-12-15 04:39:49 (189 MB/s) - ‘pgdg-redhat-repo-latest.noarch.rpm’ saved [5932/5932]

[ec2-user@postdb ~]$ 
[ec2-user@postdb ~]$ sudo rpm -Uvh --nodeps pgdg-redhat-repo-latest.noarch.rpm
warning: pgdg-redhat-repo-latest.noarch.rpm: Header V4 DSA/SHA1 Signature, key ID 442df0f8: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:pgdg-redhat-repo-42.0-5          ################################# [100%]
[ec2-user@postdb ~]$ 
[ec2-user@postdb ~]$ sudo sed --in-place -e "s/\$releasever/7/g" /etc/yum.repos.d/pgdg-redhat-all.repo
[ec2-user@postdb ~]$ 
[ec2-user@postdb ~]$ 

```

リポジトリ導入後のPostgreSQLパッケージの確認

```sh
[ec2-user@postdb ~]$ yum info postgresql10-server
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                                             | 2.4 kB  00:00:00     
pgdg10                                                                 | 3.6 kB  00:00:00     
pgdg11                                                                 | 3.6 kB  00:00:00     
pgdg12                                                                 | 3.6 kB  00:00:00     
pgdg94                                                                 | 3.6 kB  00:00:00     
pgdg95                                                                 | 3.6 kB  00:00:00     
pgdg96                                                                 | 3.6 kB  00:00:00     
(1/12): pgdg12/x86_64/group_gz                                         |  245 B  00:00:00     
(2/12): pgdg11/x86_64/group_gz                                         |  245 B  00:00:00     
(3/12): pgdg10/x86_64/group_gz                                         |  245 B  00:00:00     
(4/12): pgdg94/x86_64/group_gz                                         |  247 B  00:00:00     
(5/12): pgdg95/x86_64/group_gz                                         |  249 B  00:00:00     
(6/12): pgdg12/x86_64/primary_db                                       | 139 kB  00:00:00     
(7/12): pgdg96/x86_64/group_gz                                         |  249 B  00:00:00     
(8/12): pgdg94/x86_64/primary_db                                       | 389 kB  00:00:00     
(9/12): pgdg96/x86_64/primary_db                                       | 413 kB  00:00:00     
(10/12): pgdg95/x86_64/primary_db                                      | 401 kB  00:00:00     
(11/12): pgdg10/x86_64/primary_db                                      | 406 kB  00:00:02     
(12/12): pgdg11/x86_64/primary_db                                      | 362 kB  00:00:02     
105 packages excluded due to repository priority protections
Available Packages
Name        : postgresql10-server
Arch        : x86_64
Version     : 10.11
Release     : 2PGDG.rhel7
Size        : 4.5 M
Repo        : pgdg10/x86_64
Summary     : The programs needed to create and run a PostgreSQL server
URL         : https://www.postgresql.org/
License     : PostgreSQL
Description : PostgreSQL is an advanced Object-Relational database management system (DBMS).
            : The postgresql10-server package contains the programs needed to create
            : and run a PostgreSQL server, which will in turn allow you to create
            : and maintain PostgreSQL databases.

[ec2-user@postdb ~]$ 
```

PostgreSQL11 と PostgreSQL12もインストール可能な状態。

```sh
[ec2-user@postdb ~]$ yum info postgresql11-server
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
105 packages excluded due to repository priority protections
Available Packages
Name        : postgresql11-server
Arch        : x86_64
Version     : 11.6
Release     : 2PGDG.rhel7
Size        : 4.7 M
Repo        : pgdg11/x86_64
Summary     : The programs needed to create and run a PostgreSQL server
URL         : https://www.postgresql.org/
License     : PostgreSQL
Description : PostgreSQL is an advanced Object-Relational database management system (DBMS).
            : The postgresql11-server package contains the programs needed to create
            : and run a PostgreSQL server, which will in turn allow you to create
            : and maintain PostgreSQL databases.

[ec2-user@postdb ~]$ yum info postgresql12-server
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
105 packages excluded due to repository priority protections
Available Packages
Name        : postgresql12-server
Arch        : x86_64
Version     : 12.1
Release     : 2PGDG.rhel7
Size        : 13 M
Repo        : pgdg12/x86_64
Summary     : The programs needed to create and run a PostgreSQL server
URL         : https://www.postgresql.org/
License     : PostgreSQL
Description : PostgreSQL is an advanced Object-Relational database management system (DBMS).
            : The postgresql12-server package contains the programs needed to create
            : and run a PostgreSQL server, which will in turn allow you to create
            : and maintain PostgreSQL databases.

[ec2-user@postdb ~]$ 

```

PostgreSQL10をインストールする。

```sh
[ec2-user@postdb ~]$ sudo yum -y install postgresql10-server
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                                       | 2.4 kB  00:00:00     
pgdg10                                                           | 3.6 kB  00:00:00     
pgdg11                                                           | 3.6 kB  00:00:00     
pgdg12                                                           | 3.6 kB  00:00:00     
pgdg94                                                           | 3.6 kB  00:00:00     
pgdg95                                                           | 3.6 kB  00:00:00     
pgdg96                                                           | 3.6 kB  00:00:00     
(1/12): pgdg11/x86_64/group_gz                                   |  245 B  00:00:01     
(2/12): pgdg12/x86_64/group_gz                                   |  245 B  00:00:01     
(3/12): pgdg10/x86_64/group_gz                                   |  245 B  00:00:01     
(4/12): pgdg10/x86_64/primary_db                                 | 406 kB  00:00:01     
(5/12): pgdg11/x86_64/primary_db                                 | 362 kB  00:00:01     
(6/12): pgdg95/x86_64/group_gz                                   |  249 B  00:00:00     
(7/12): pgdg94/x86_64/group_gz                                   |  247 B  00:00:00     
(8/12): pgdg96/x86_64/group_gz                                   |  249 B  00:00:00     
(9/12): pgdg95/x86_64/primary_db                                 | 401 kB  00:00:00     
(10/12): pgdg12/x86_64/primary_db                                | 139 kB  00:00:01     
(11/12): pgdg94/x86_64/primary_db                                | 389 kB  00:00:01     
(12/12): pgdg96/x86_64/primary_db                                                                                                                                    | 413 kB  00:00:01     
105 packages excluded due to repository priority protections
Resolving Dependencies
--> Running transaction check
---> Package postgresql10-server.x86_64 0:10.11-2PGDG.rhel7 will be installed
--> Processing Dependency: postgresql10-libs(x86-64) = 10.11-2PGDG.rhel7 for package: postgresql10-server-10.11-2PGDG.rhel7.x86_64
--> Processing Dependency: postgresql10(x86-64) = 10.11-2PGDG.rhel7 for package: postgresql10-server-10.11-2PGDG.rhel7.x86_64
--> Processing Dependency: libpq.so.5()(64bit) for package: postgresql10-server-10.11-2PGDG.rhel7.x86_64
--> Running transaction check
---> Package postgresql10.x86_64 0:10.11-2PGDG.rhel7 will be installed
---> Package postgresql10-libs.x86_64 0:10.11-2PGDG.rhel7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================================================
 Package                                             Arch                                   Version                                            Repository                              Size
================================================================================================================
Installing:
 postgresql10-server                                 x86_64                                 10.11-2PGDG.rhel7                                  pgdg10                                 4.5 M
Installing for dependencies:
 postgresql10                                        x86_64                                 10.11-2PGDG.rhel7                                  pgdg10                                 1.6 M
 postgresql10-libs                                   x86_64                                 10.11-2PGDG.rhel7                                  pgdg10                                 356 k

Transaction Summary
================================================================================================================
Install  1 Package (+2 Dependent packages)

Total download size: 6.5 M
Installed size: 28 M
Downloading packages:
warning: /var/cache/yum/x86_64/2/pgdg10/packages/postgresql10-10.11-2PGDG.rhel7.x86_64.rpm: Header V4 DSA/SHA1 Signature, key ID 442df0f8: NOKEY          ] 979 kB/s | 960 kB  00:00:05 ETA 
Public key for postgresql10-10.11-2PGDG.rhel7.x86_64.rpm is not installed
(1/3): postgresql10-10.11-2PGDG.rhel7.x86_64.rpm                                                       | 1.6 MB  00:00:01     
(2/3): postgresql10-libs-10.11-2PGDG.rhel7.x86_64.rpm                                                  | 356 kB  00:00:02     
(3/3): postgresql10-server-10.11-2PGDG.rhel7.x86_64.rpm                                                | 4.5 MB  00:00:00     
-----------------------------------------------------------
Total                                                                                                                                                       2.7 MB/s | 6.5 MB  00:00:02     
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG
Importing GPG key 0x442DF0F8:
 Userid     : "PostgreSQL RPM Building Project <pgsqlrpms-hackers@pgfoundry.org>"
 Fingerprint: 68c9 e2b9 1a37 d136 fe74 d176 1f16 d2e1 442d f0f8
 Package    : pgdg-redhat-repo-42.0-5.noarch (installed)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
** Found 1 pre-existing rpmdb problem(s), 'yum check' output follows:
pgdg-redhat-repo-42.0-5.noarch has missing requires of /etc/redhat-release
  Installing : postgresql10-libs-10.11-2PGDG.rhel7.x86_64                                                        1/3 
  Installing : postgresql10-10.11-2PGDG.rhel7.x86_64                                                             2/3 
  Installing : postgresql10-server-10.11-2PGDG.rhel7.x86_64                                                      3/3 
  Verifying  : postgresql10-libs-10.11-2PGDG.rhel7.x86_64                                                        1/3 
  Verifying  : postgresql10-server-10.11-2PGDG.rhel7.x86_64                                                      2/3 
  Verifying  : postgresql10-10.11-2PGDG.rhel7.x86_64                                                             3/3 

Installed:
  postgresql10-server.x86_64 0:10.11-2PGDG.rhel7                                                                                                                                            

Dependency Installed:
  postgresql10.x86_64 0:10.11-2PGDG.rhel7                                                    postgresql10-libs.x86_64 0:10.11-2PGDG.rhel7                                                   

Complete!
[ec2-user@postdb ~]$ /usr/pgsql-10/bin/postgres --version
postgres (PostgreSQL) 10.11
[ec2-user@postdb ~]$ 

```

OS側にpostgresユーザが作成される。

```
[ec2-user@postdb ~]$ cat /etc/passwd
～中略～
ec2-user:x:1000:1000:EC2 Default User:/home/ec2-user:/bin/bash
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash
[ec2-user@postdb ~]$ 
```

postgresql10-contribとpostgresql10-develも合わせてインストールする。

```sh
[root@postdb ~]# yum install postgresql10-devel
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
105 packages excluded due to repository priority protections
Resolving Dependencies
--> Running transaction check
---> Package postgresql10-devel.x86_64 0:10.11-2PGDG.rhel7 will be installed
--> Processing Dependency: libicu-devel for package: postgresql10-devel-10.11-2PGDG.rhel7.x86_64
--> Running transaction check
---> Package libicu-devel.x86_64 0:50.1.2-17.amzn2 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================
 Package                   Arch          Version                    Repository         Size
============================================================================================
Installing:
 postgresql10-devel        x86_64        10.11-2PGDG.rhel7          pgdg10            2.0 M
Installing for dependencies:
 libicu-devel              x86_64        50.1.2-17.amzn2            amzn2-core        702 k

Transaction Summary
============================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 2.7 M
Installed size: 13 M
Is this ok [y/d/N]: n
Exiting on user command
Your transaction was saved, rerun it with:
 yum load-transaction /tmp/yum_save_tx.2019-12-28.11-00.54JiTC.yumtx
[root@postdb ~]# 
[root@postdb ~]# yum install postgresql10-contrib
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
105 packages excluded due to repository priority protections
Resolving Dependencies
--> Running transaction check
---> Package postgresql10-contrib.x86_64 0:10.11-2PGDG.rhel7 will be installed
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.22)(64bit) for package: postgresql10-contrib-10.11-2PGDG.rhel7.x86_64
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.18)(64bit) for package: postgresql10-contrib-10.11-2PGDG.rhel7.x86_64
--> Processing Dependency: libxslt.so.1(LIBXML2_1.0.11)(64bit) for package: postgresql10-contrib-10.11-2PGDG.rhel7.x86_64
--> Processing Dependency: libxslt.so.1()(64bit) for package: postgresql10-contrib-10.11-2PGDG.rhel7.x86_64
--> Running transaction check
---> Package libxslt.x86_64 0:1.1.28-5.amzn2.0.2 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================
 Package                    Arch         Version                     Repository        Size
============================================================================================
Installing:
 postgresql10-contrib       x86_64       10.11-2PGDG.rhel7           pgdg10           587 k
Installing for dependencies:
 libxslt                    x86_64       1.1.28-5.amzn2.0.2          amzn2-core       243 k

Transaction Summary
============================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 830 k
Installed size: 2.5 M
Is this ok [y/d/N]: y
Downloading packages:
(1/2): libxslt-1.1.28-5.amzn2.0.2.x86_64.rpm                         | 243 kB  00:00:00     
(2/2): postgresql10-contrib-10.11-2PGDG.rhel7.x86_64.rpm             | 587 kB  00:00:02     
--------------------------------------------------------------------------------------------
Total                                                       281 kB/s | 830 kB  00:00:02     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : libxslt-1.1.28-5.amzn2.0.2.x86_64                                        1/2 
  Installing : postgresql10-contrib-10.11-2PGDG.rhel7.x86_64                            2/2 
  Verifying  : libxslt-1.1.28-5.amzn2.0.2.x86_64                                        1/2 
  Verifying  : postgresql10-contrib-10.11-2PGDG.rhel7.x86_64                            2/2 

Installed:
  postgresql10-contrib.x86_64 0:10.11-2PGDG.rhel7                                           

Dependency Installed:
  libxslt.x86_64 0:1.1.28-5.amzn2.0.2                                                       

Complete!
[root@postdb ~]# 
```

DBの初期化を行う。rootで実施。

```sh
[root@postdb ~]# /usr/pgsql-10/bin/postgresql-10-setup initdb
Initializing database ... OK
```

自動起動設定を行う

```sh
[root@postdb ~]# systemctl enable postgresql-10
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-10.service to /usr/lib/systemd/system/postgresql-10.service.
```

PostgreSQLの起動、停止、再起動方法

```sh
sudo systemctl start postgresql-10.service
sudo systemctl stop postgresql-10.service
sudo systemctl restart postgresql-10.service

[ec2-user@postdb pgsql-10]$ sudo systemctl start postgresql-10.service
[ec2-user@postdb pgsql-10]$ echo $?
0
[ec2-user@postdb pgsql-10]$ ps -ef | grep postgres | grep -v grep
postgres  4184     1  0 04:58 ?        00:00:00 /usr/pgsql-10/bin/postmaster -D /var/lib/pgsql/10/data/
postgres  4187  4184  0 04:58 ?        00:00:00 postgres: logger process   
postgres  4189  4184  0 04:58 ?        00:00:00 postgres: checkpointer process   
postgres  4190  4184  0 04:58 ?        00:00:00 postgres: writer process   
postgres  4191  4184  0 04:58 ?        00:00:00 postgres: wal writer process   
postgres  4192  4184  0 04:58 ?        00:00:00 postgres: autovacuum launcher process   
postgres  4193  4184  0 04:58 ?        00:00:00 postgres: stats collector process   
postgres  4194  4184  0 04:58 ?        00:00:00 postgres: bgworker: logical replication launcher   
[ec2-user@postdb pgsql-10]$ 
[ec2-user@postdb pgsql-10]$ 
[ec2-user@postdb pgsql-10]$ sudo systemctl stop postgresql-10.service
[ec2-user@postdb pgsql-10]$ 
[ec2-user@postdb pgsql-10]$ 
[ec2-user@postdb pgsql-10]$ ps -ef | grep postgres | grep -v grep
[ec2-user@postdb pgsql-10]$ 
[ec2-user@postdb pgsql-10]$ 

```

接続してみる。

```
[ec2-user@postdb pgsql-10]$ su - postgres
Password: 
Last login: Sun Dec 15 04:59:38 UTC 2019 on pts/1
-bash-4.2$ 
-bash-4.2$ psql --version
psql (PostgreSQL) 10.11
-bash-4.2$ 
-bash-4.2$ 
-bash-4.2$ psql
psql (10.11)
Type "help" for help.

postgres=# 
postgres=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

