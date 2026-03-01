---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing PostgreSQL 11 and 12 with yum on RHEL8 (Red Hat Enterprise Linux) on EC2"
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



### Introduction

Let's install PostgreSQL 11 and 12 via yum on RHEL 8 (Red Hat Enterprise Linux) on EC2. I'm installing both versions because I plan to test the pg_upgrade extension for major version upgrades in a follow-up article. For instructions on installing PostgreSQL via yum on Amazon Linux 2, see here:

> Installing PostgreSQL on EC2 (Amazon Linux 2) | my opinion is my own https://zatoima.github.io/postgresql-ec2-insatll.html

The Red Hat version is:

```
[ec2-user@pgsql ~]$ cat /etc/redhat-release
Red Hat Enterprise Linux release 8.2 (Ootpa)
```

### Add Repository

```
sudo yum -y localinstall https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
```

> Reference: PostgreSQL RPM Repository (with Yum) https://yum.postgresql.org/repopackages.php

### Add EPEL Repository

> PostgreSQL RPM Repository (with Yum) https://yum.postgresql.org/repopackages.php
>
> Please note that PostgreSQL YUM repository depends on EPEL repository for some packages. RHEL/CentOS/, etc. users should install EPEL repo RPM along with PGDG repo RPMs to satisfy dependencies.

As stated above, since some packages depend on the EPEL repository, it appears that EPEL must be added. (Installation itself was possible without it.)

[EPEL](https://fedoraproject.org/wiki/EPEL/ja) (Extra Packages for Enterprise Linux) is a repository that provides additional packages for Red Hat Enterprise Linux (RHEL).

```sh
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
```

After installation, the epel repository becomes available.

```
[ec2-user@pgsql ~]$ yum repolist
repo id                                                                     repo name                                                                                                 status
epel/x86_64                                                                 Extra Packages for Enterprise Linux 7 - x86_64                                                            13,273
```

### Check Available Versions

The latest versions postgresql11 11.8 and postgresql12 12.3 are available. The package names seem slightly different from those in the RHEL7 repository...

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

### Install PostgreSQL 11

```sh
sudo yum -y install postgresql11-server
```

Verify the version:

```
[ec2-user@pgsql ~]$ /usr/pgsql-11/bin/postgres --version
postgres (PostgreSQL) 11.8
```

The postgres OS user is created:

```
[ec2-user@pgsql ~]$ cat /etc/passwd
～(omitted)～
ec2-user:x:1000:1000:Cloud User:/home/ec2-user:/bin/bash
postgres:x:26:26:PostgreSQL Server:/var/lib/pgsql:/bin/bash
```

Also install postgresql11-contrib and postgresql11-devel:

```sh
[ec2-user@pgsql ~]$ sudo yum -y install postgresql11-contrib.x86_64 postgresql11-devel.x86_64
```

### Install PostgreSQL 12

Install PostgreSQL 12. (The steps are almost identical to PostgreSQL 11.)

```sh
sudo yum -y install postgresql12-server
```

Verify the version:

```
[ec2-user@pgsql ~]$ /usr/pgsql-12/bin/postgres --version
postgres (PostgreSQL) 12.3
```

Also install postgresql12-contrib and postgresql12-devel:

```sh
[ec2-user@pgsql ~]$ sudo yum -y install postgresql12-contrib.x86_64 postgresql12-devel.x86_64
```

### DB Initialization, Start/Stop, and Connection Verification

Initialize the DB. Run as root.

```sh
[root@pgsql ~]# /usr/pgsql-11/bin/postgresql-11-setup initdb
Initializing database ... OK
[root@pgsql ~]# /usr/pgsql-12/bin/postgresql-12-setup initdb
Initializing database ... OK
```

Configure autostart:

```sh
[root@pgsql ~]# systemctl enable postgresql-11
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-11.service to /usr/lib/systemd/system/postgresql-12.service.
[root@pgsql ~]# systemctl enable postgresql-12
Created symlink from /etc/systemd/system/multi-user.target.wants/postgresql-12.service to /usr/lib/systemd/system/postgresql-12.service.
```

Since PostgreSQL 11 and 12 share the same startup port, change the port in postgresql.conf for PostgreSQL 12:

```
sed -i "s/#port = 5432/port = 5433/g" "/var/lib/pgsql/12/data/postgresql.conf"
```

Verify that start, stop, and restart work for both:

```sh
sudo systemctl start postgresql-11.service
sudo systemctl stop postgresql-11.service
sudo systemctl restart postgresql-11.service

sudo systemctl start postgresql-12.service
sudo systemctl stop postgresql-12.service
sudo systemctl restart postgresql-12.service
```

Set up environment variables:

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

Connection verification:

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

Next, I plan to use this environment to test pg_upgrade behavior.
