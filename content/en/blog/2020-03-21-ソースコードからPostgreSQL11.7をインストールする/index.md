---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing PostgreSQL 11.7 from Source Code"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-11.7-install-source-code.html
date: 2020-03-21
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



This assumes PostgreSQL 11.7. PostgreSQL is easy to install whether using yum or building from source.

### Pre-checks

#### GNU make Version

Confirm it is version 3.80 or higher.

```sh
make --version
```

#### Install gcc

```sh
sudo yum -y install gcc
```

#### readline-devel Package

```sh
sudo yum -y install readline-devel
```

#### zlib-devel Package

```sh
sudo yum -y install zlib-devel
```

#### Create OS User

```sh
groupadd -g 1101 postgres
useradd -u 1101 -g postgres -G postgres -d /home/postgres postgres
passwd postgres
```

### PostgreSQL Installation (performed as postgres user)

#### Download Source & Extract

```sh
wget https://ftp.postgresql.org/pub/source/v11.7/postgresql-11.7.tar.gz
tar xvfz postgresql-11.7.tar.gz
```

If you need to modify the source code, do so at this point.

```sh
cd ./postgresql-11.7/contrib/pg_trgm
vi ./trgm.h

#Comment out KEEPONLYALNUM
```

#### Build & Install

```sh
cd $HOME/postgresql-11.7
./configure --prefix=$HOME/pgsql/11
make
make install
```

### PostgreSQL Initialization

#### Create $PGDATA

```sh
mkdir -p /home/postgres/pgsql/11/data
```

#### Initialize DB

```sh
sudo su - postgres
whoami
export PGDATA=/home/postgres/pgsql/11/data
/home/postgres/pgsql/11/bin/initdb --pgdata=$PGDATA
/home/postgres/pgsql/11/bin/pg_ctl start --pgdata=$PGDATA
/home/postgres/pgsql/11/bin/pg_ctl status --pgdata=$PGDATA
```

#### Connect and Verify Version

```sh
[postgres@post11db bin]$ ./psql
psql (11.7)
Type "help" for help.

postgres=#
postgres=# select version();
                                                version
--------------------------------------------------------------------------------------------------------
 PostgreSQL 11.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-6), 64-bit
(1 row)
```

#### Reference

> Chapter 16. Installation from Source Code https://www.postgresql.jp/document/11/html/installation.html
