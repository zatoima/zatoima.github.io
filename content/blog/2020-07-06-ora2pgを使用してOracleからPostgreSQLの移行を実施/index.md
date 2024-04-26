---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ora2pgを使用してOracleからPostgreSQLのスキーマ移行を実施"
subtitle: ""
summary: " "
tags: ["Oracle","PostgreSQL","DB Migration"]
categories: ["Oracle","PostgreSQL","DB Migration"]
url: oracle-postgresql-ora2pg-migration.html
date: 2020-07-06
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

ora2pgのセットアップ、変換作業の実施。インストール手順は[ora2pgのサイト](http://ora2pg.darold.net/documentation.html)を参照。

- #### Instant Client Packageのインストール

Instant Clientのrpmダウンロードは[Oracle社のサイト](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)から。

```
sudo rpm -ivh oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient19.6-devel-19.6.0.0.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient19.6-jdbc-19.6.0.0.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient19.6-sqlplus-19.6.0.0.0-1.x86_64.rpm
```

- #### 環境変数の設定

```
vi .bash_profile

↓下記を追記
export LD_LIBRARY_PATH=/usr/lib/oracle/19.6/client64/lib
export ORACLE_HOME=/usr/lib/oracle/19.6/client64/lib
```

```
source .bash_profile
```

- #### DBD::Oracleのインストール

```
sudo su -
export LD_LIBRARY_PATH=/usr/lib/oracle/19.6/client64/lib
export ORACLE_HOME=/usr/lib/oracle/19.6/client64/lib

yum -y install perl-CPAN
yum -y install libyaml-devel
yum -y install gcc

perl -MCPAN -e shell #全てEnter
perl -MCPAN -e 'install DBI'
perl -MCPAN -e 'install DBD::Oracle'
```

- #### ora2pgのインストール

```
sudo su - ec2-user
sudo yum -y install git
git clone https://github.com/darold/ora2pg.git
cd ./ora2pg
perl Makefile.PL
make && make install
```

ora2pgのインストール自体は以上で終了。

- #### ora2pgの初期セッティング

```
mkdir ora2pg
ora2pg --project_base ~/ora2pg --init_project migration_test
```

- #### ora2pg.confの設定

./config配下にora2pg.confが作成されているのでこのファイルを修正する。細かい挙動を制御するパラメータもあるが割愛。

```
vi ./config/ora2pg.conf
```

```
# Set Oracle database connection (datasource, user, password)
ORACLE_DSN	dbi:Oracle:host=xxxxxxxxxxxxx;sid=ora19db;port=1521
ORACLE_USER	ikotest
ORACLE_PWD	oracle

# Oracle schema/owner to use
SCHEMA	ikotest
```

- #### スキーマ定義の全体export実施

```
./export_schema.sh
```

実行後は「reports」、「schema」配下を重点的に確認

```
├── config
│   └── ora2pg.conf
├── CONSTRAINTS_output.sql
├── data
├── export_schema.sh
├── import_all.sh
├── INDEXES_output.sql
├── reports
│   ├── columns.txt
│   ├── report.html
│   └── tables.txt
├── schema
│   ├── dblinks
│   ├── directories
│   ├── functions
│   ├── grants
│   ├── mviews
│   ├── packages
│   ├── partitions
│   ├── procedures
│   ├── sequences
│   ├── synonyms
│   │   └── synonym.sql
│   ├── tables
│   │   ├── CONSTRAINTS_table.sql
│   │   ├── INDEXES_table.sql
│   │   └── table.sql
│   ├── tablespaces
│   ├── triggers
│   ├── types
│   └── views
└── sources
    ├── functions
    ├── mviews
    ├── packages
    ├── partitions
    ├── procedures
    ├── triggers
    ├── types
    └── views
```

- ##### SQL変換

```
ora2pg -c config/ora2pg.conf -i input.sql -o output.sql -t QUERY
```







