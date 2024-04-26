---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "docker-composeでPostgreSQL構築"
subtitle: ""
summary: " "
tags: ["Docker","PostgreSQL"]
categories: ["Docker","PostgreSQL"]
url: postgres-docker-compose-install
date: 2021-12-07
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

### イメージ検索

公式の`postgres`を使用する

```sh
[ec2-user@bastin postgres-docker]$ docker search postgres
NAME                                    DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
postgres                                The PostgreSQL object-relational database sy…   10247     [OK]       
sameersbn/postgresql                                                                    161                  [OK]
postgrest/postgrest                     REST API for any Postgres database              51                   
centos/postgresql-96-centos7            PostgreSQL is an advanced Object-Relational …   45                   
wrouesnel/postgres_exporter             Postgres metrics exporter for Prometheus.       30                   
arm32v7/postgres                        The PostgreSQL object-relational database sy…   29                   
prodrigestivill/postgres-backup-local   Backup PostgresSQL to local filesystem with …   21                   [OK]
centos/postgresql-10-centos7            PostgreSQL is an advanced Object-Relational …   19                   
schickling/postgres-backup-s3           Backup PostgresSQL to S3 (supports periodic …   19                   [OK]
debezium/postgres                       PostgreSQL for use with Debezium change data…   18                   [OK]
arm64v8/postgres                        The PostgreSQL object-relational database sy…   17                   
centos/postgresql-94-centos7            PostgreSQL is an advanced Object-Relational …   16                   
postdock/postgres                       PostgreSQL server image, can work in master …   14                   [OK]
clkao/postgres-plv8                     Docker image for running PLV8 1.4 on Postgre…   13                   [OK]
camptocamp/postgres                     Docker image for PostgreSQL including some e…   8                    [OK]
centos/postgresql-95-centos7            PostgreSQL is an advanced Object-Relational …   6                    
jgiannuzzi/postgres-bdr                 Docker image for PostgreSQL with BDR support    5                    [OK]
dcm4che/postgres-dcm4chee               PostgreSQL for dcm4che-arc 5.x                  5                    [OK]
centos/postgresql-12-centos7            PostgreSQL is an advanced Object-Relational …   4                    
blacklabelops/postgres                  Postgres Image for Atlassian Applications       4                    [OK]
tmaier/postgresql-client                Run the PostgreSQL Client (psql) within a do…   2                    [OK]
ansibleplaybookbundle/postgresql-apb    An APB which deploys RHSCL PostgreSQL           2                    [OK]
fredboat/postgres                       PostgreSQL 10.0 used in FredBoat's docker-co…   1                    
openshift/postgresql-92-centos7         DEPRECATED: A Centos7 based PostgreSQL v9.2 …   1                    
manageiq/postgresql                     Container with PostgreSQL and built on CentO…   0                    [OK]
```

### タグ検索

特定のバージョンを指定する場合はタグを調べておく

```sh
curl -s https://registry.hub.docker.com/v1/repositories/postgres/tags | jq -r '.[].name'
```

### docker-compose.ymlの準備

```sh
version: '3'

services:
  postgres:
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      PGPASSWORD: postgres
      POSTGRES_DB: postgres
      TZ: "Asia/Tokyo"
    ports:
      - 5432:5432
    volumes:
      - postgres:/var/lib/postgresql/data

volumes:
  postgres:
```

### コンテナ作成

```sh
[ec2-user@bastin postgres-docker]$ docker-compose up -d
Creating network "postgres-docker_default" with the default driver
Creating volume "postgres-docker_postgres" with default driver
Creating volume "postgres-docker_pgadmin" with default driver
Pulling postgres (postgres:latest)...
latest: Pulling from library/postgres
e5ae68f74026: Already exists
7b8fcc7e1ad0: Pull complete
7527d03e2f77: Pull complete
80e55689f4d0: Pull complete
8a79eb6d69c9: Pull complete
397705f2d093: Pull complete
de36ec4eb0a5: Pull complete
08d878a022c1: Pull complete
7677029670ff: Pull complete
1d24b3d9557e: Pull complete
e085b018338c: Pull complete
063b09ff12e9: Pull complete
a39fee215a44: Pull complete
Digest: sha256:f76241d07218561e3d1a334eae6a5bf63c70b49f35ffecb7f020448e30e37390
Status: Downloaded newer image for postgres:latest
Creating postgres-docker_postgres_1 ... done

```

### プロセス確認、接続

```sh
[ec2-user@bastin postgres-docker]$ ps -ef | grep postgres
ec2-user  1193 29347  0 13:30 pts/1    00:00:00 grep --color=auto postgres
libstor+ 31469 31428  0 13:28 ?        00:00:00 postgres
libstor+ 31777 31469  0 13:28 ?        00:00:00 postgres: checkpointer 
libstor+ 31778 31469  0 13:28 ?        00:00:00 postgres: background writer 
libstor+ 31779 31469  0 13:28 ?        00:00:00 postgres: walwriter 
libstor+ 31780 31469  0 13:28 ?        00:00:00 postgres: autovacuum launcher 
libstor+ 31781 31469  0 13:28 ?        00:00:00 postgres: stats collector 
libstor+ 31782 31469  0 13:28 ?        00:00:00 postgres: logical replication launcher 
[ec2-user@bastin postgres-docker]$ 
[ec2-user@bastin postgres-docker]$ 
[ec2-user@bastin postgres-docker]$ psql -h localhost -p 5432 -d postgres -U postgres
psql (11.12, server 14.1 (Debian 14.1-1.pgdg110+1))
WARNING: psql major version 11, server major version 14.
         Some psql features might not work.
Type "help" for help.

postgres=# select version();
                                                           version                                                           
-----------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 14.1 (Debian 14.1-1.pgdg110+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 10.2.1-6) 10.2.1 20210110, 64-bit
(1 row)

postgres=# 

```

