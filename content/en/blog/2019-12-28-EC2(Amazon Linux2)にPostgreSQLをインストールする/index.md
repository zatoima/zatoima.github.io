---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing PostgreSQL on EC2 (Amazon Linux 2)"
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



This covers how to forcefully install PostgreSQL via Yum on Amazon Linux 2, given that using the Red Hat repository on Amazon Linux fails with an error.

Note that the PostgreSQL community lists the following as Yum-supported platforms:

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

The default Amazon Linux repository is outdated, so we install the repository locally. However, installing the Red Hat repository for Amazon Linux via yum fails with an error:

> Error: Package: pgdg-redhat-repo-42.0-5.noarch (/pgdg-redhat-repo-latest.noarch)
>            Requires: /etc/redhat-release

```sh
[ec2-user@postdb ~]$ sudo yum -y localinstall https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
...
Error: Package: pgdg-redhat-repo-42.0-5.noarch (/pgdg-redhat-repo-latest.noarch)
           Requires: /etc/redhat-release
 You could try using --skip-broken to work around the problem
 You could try running: rpm -Va --nofiles --nodigest
[ec2-user@postdb ~]$

```

Since there's no Amazon Linux-specific repository, download the rpm and rewrite pgdg-redhat-all.repo:

```sh
[ec2-user@postdb ~]$ wget https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
...
2019-12-15 04:39:49 (189 MB/s) - 'pgdg-redhat-repo-latest.noarch.rpm' saved [5932/5932]

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

Check available PostgreSQL packages after installing the repository:

```sh
[ec2-user@postdb ~]$ yum info postgresql10-server
...
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

PostgreSQL 11 and PostgreSQL 12 are also available:

```sh
[ec2-user@postdb ~]$ yum info postgresql11-server
...
Available Packages
Name        : postgresql11-server
...
Version     : 11.6
...

[ec2-user@postdb ~]$ yum info postgresql12-server
...
Available Packages
Name        : postgresql12-server
...
Version     : 12.1
...

[ec2-user@postdb ~]$

```

Install PostgreSQL 10:

```sh
[ec2-user@postdb ~]$ sudo yum -y install postgresql10-server
...
Installed:
  postgresql10-server.x86_64 0:10.11-2PGDG.rhel7

Dependency Installed:
  postgresql10.x86_64 0:10.11-2PGDG.rhel7                   postgresql10-libs.x86_64 0:10.11-2PGDG.rhel7

Complete!
[ec2-user@postdb ~]$ /usr/pgsql-10/bin/postgres --version
postgres (PostgreSQL) 10.11
[ec2-user@postdb ~]$

```

The postgres OS user is created:

```
[ec2-user@postdb ~]$ cat /etc/passwd
...
ec2-user:x:1000:1000:EC2 Default User:/home/ec2-user:/bin/bash
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash
[ec2-user@postdb ~]$
```

Also install postgresql10-contrib and postgresql10-devel:

```sh
[root@postdb ~]# yum install postgresql10-contrib
...
Installed:
  postgresql10-contrib.x86_64 0:10.11-2PGDG.rhel7

Dependency Installed:
  libxslt.x86_64 0:1.1.28-5.amzn2.0.2

Complete!
[root@postdb ~]#
```

Initialize the database (run as root):

```sh
[root@postdb ~]# /usr/pgsql-10/bin/postgresql-10-setup initdb
Initializing database ... OK
```

Configure auto-start:

```sh
[root@postdb ~]# systemctl enable postgresql-10
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-10.service to /usr/lib/systemd/system/postgresql-10.service.
```

Starting, stopping, and restarting PostgreSQL:

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
```

Connect and verify:

```
[ec2-user@postdb pgsql-10]$ su - postgres
Password:
Last login: Sun Dec 15 04:59:38 UTC 2019 on pts/1
-bash-4.2$
-bash-4.2$ psql --version
psql (PostgreSQL) 10.11
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
