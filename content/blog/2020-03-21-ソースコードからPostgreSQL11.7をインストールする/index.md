---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ソースコードからPostgreSQL11.7をインストールする"
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



PostgreSQL11.7を前提としています。PostgreSQLはyumでもソースからビルドするパターンでも簡単。

### 事前確認

#### GNU makeのバージョン

3.80以上であることを確認

```sh
make --version
```

#### gccのインストール

```sh
sudo yum -y install gcc
```

#### readline-develパッケージ

```sh
sudo yum -y install readline-devel
```

#### zlib-develパッケージ

```sh
sudo yum -y install zlib-devel
```

#### OSユーザ作成

```sh
groupadd -g 1101 postgres
useradd -u 1101 -g postgres -G postgres -d /home/postgres postgres
passwd postgres
```

### PostgreSQLインストール(postgresユーザで実施)

#### ソースダウンロード&解凍

```sh
wget https://ftp.postgresql.org/pub/source/v11.7/postgresql-11.7.tar.gz
tar xvfz postgresql-11.7.tar.gz
```

<u>ソースコードに手を入れる場合は</u>このタイミングで修正

```sh
cd ./postgresql-11.7/contrib/pg_trgm
vi ./trgm.h

#KEEPONLYALNUM を コメントアウトする
```

#### ビルド&インストール

```sh
cd $HOME/postgresql-11.7
./configure --prefix=$HOME/pgsql/11
make
make install
```

### PostgreSQL初期化

#### $PGDATA を作成

```sh
mkdir -p /home/postgres/pgsql/11/data
```

#### DBの初期化

```sh
sudo su - postgres
whoami
export PGDATA=/home/postgres/pgsql/11/data
/home/postgres/pgsql/11/bin/initdb --pgdata=$PGDATA
/home/postgres/pgsql/11/bin/pg_ctl start --pgdata=$PGDATA
/home/postgres/pgsql/11/bin/pg_ctl status --pgdata=$PGDATA
```

#### 接続、バージョン確認

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

#### 参考

> 第16章 ソースコードからインストール https://www.postgresql.jp/document/11/html/installation.html