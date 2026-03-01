---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Performing Schema Migration from Oracle to PostgreSQL Using ora2pg"
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

Setting up ora2pg and performing the conversion. For installation steps, refer to the [ora2pg documentation](http://ora2pg.darold.net/documentation.html).

- #### Install Instant Client Package

Download the Instant Client RPM from [Oracle's website](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html).

```
sudo rpm -ivh oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient19.6-devel-19.6.0.0.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient19.6-jdbc-19.6.0.0.0-1.x86_64.rpm
sudo rpm -ivh oracle-instantclient19.6-sqlplus-19.6.0.0.0-1.x86_64.rpm
```

- #### Configure Environment Variables

```
vi .bash_profile

↓Add the following
export LD_LIBRARY_PATH=/usr/lib/oracle/19.6/client64/lib
export ORACLE_HOME=/usr/lib/oracle/19.6/client64/lib
```

```
source .bash_profile
```

- #### Install DBD::Oracle

```
sudo su -
export LD_LIBRARY_PATH=/usr/lib/oracle/19.6/client64/lib
export ORACLE_HOME=/usr/lib/oracle/19.6/client64/lib

yum -y install perl-CPAN
yum -y install libyaml-devel
yum -y install gcc

perl -MCPAN -e shell #Press Enter for all prompts
perl -MCPAN -e 'install DBI'
perl -MCPAN -e 'install DBD::Oracle'
```

- #### Install ora2pg

```
sudo su - ec2-user
sudo yum -y install git
git clone https://github.com/darold/ora2pg.git
cd ./ora2pg
perl Makefile.PL
make && make install
```

That completes the ora2pg installation.

- #### Initial ora2pg Setup

```
mkdir ora2pg
ora2pg --project_base ~/ora2pg --init_project migration_test
```

- #### Configure ora2pg.conf

An `ora2pg.conf` file is created under `./config`. Edit this file. Detailed behavioral parameters are omitted here.

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

- #### Export the Full Schema Definition

```
./export_schema.sh
```

After execution, focus on checking the `reports` and `schema` directories:

```
├── config
│   └── ora2pg.conf
├── CONSTRAINTS_output.sql
├── data
├── export_schema.sh
├── import_all.sh
├── INDEXES_output.sql
├── reports
│   ├── columns.txt
│   ├── report.html
│   └── tables.txt
├── schema
│   ├── dblinks
│   ├── directories
│   ├── functions
│   ├── grants
│   ├── mviews
│   ├── packages
│   ├── partitions
│   ├── procedures
│   ├── sequences
│   ├── synonyms
│   │   └── synonym.sql
│   ├── tables
│   │   ├── CONSTRAINTS_table.sql
│   │   ├── INDEXES_table.sql
│   │   └── table.sql
│   ├── tablespaces
│   ├── triggers
│   ├── types
│   └── views
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

- ##### SQL Conversion

```
ora2pg -c config/ora2pg.conf -i input.sql -o output.sql -t QUERY
```
