---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Summary of PostgreSQL pg_dump and pg_restore"
subtitle: ""
summary: " "
tags: ["PostgreSQL","pg_dump", "pg_restore"]
categories: ["PostgreSQL"]
url: postgresql-about-pg_dump-pg_restore.html
date: 2019-12-03
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



## Introduction

Since I expect to look this up repeatedly, I'm documenting PostgreSQL's pg_dump and pg_restore here.

Backups can be taken in either script file format or archive file format. The restore method differs for each.

1. Logical backup in script file format: restore with psql
2. Logical backup in archive file format: restore with pg_restore

## Basic Commands

### 1. Logical Backup in Script File Format

#### Database-Level Backup

Dump the database named `mydb` to a SQL script file.

```sql
pg_dump mydb > db.sql
```

#### Table-Level Backup

Dump a single table named `mytab`.

```sql
pg_dump -t mytab mydb > db.sql
```

#### Restore

Restore the contents of db.sql into a database named `newdb`.

```
psql -d newdb -f db.sql
```



### 2. Logical Backup in Archive File Format

In this case, data is compressed, so some data reduction occurs depending on the data and data types.

#### Database-Level Backup

Dump the database named `mydb` in archive file format.

```sql
pg_dump -Fc mydb > db.dump
```

#### Table-Level Backup

Dump a single table named `mytab` in archive file format.

```sql
pg_dump -t mytab -Fc mydb > db.dump
```

#### Restore

Restore the contents of db.dump into a database named `newdb`.

```
pg_restore -d newdb db.dump
```

### 3. Command Options

##### pg_dump

| Short Option | Long Option         | Description                                                                                      |
| ------------ | ------------------- | ------------------------------------------------------------------------------------------------ |
| -a           | --data-only         | Dump only the data, not the schema (data definitions)                                            |
| -b           | --blobs             | Include large objects in the dump. This is the default behavior unless --schema, --table, or --schema-only is specified |
| -c           | --clean             | Output commands to clean (drop) database objects prior to outputting commands to create them. Script format only. |
| -C           | --create            | Begin the output with a command to create the database itself, followed by a command to connect to it. Script format only. |
| -f file      | --file=file         | Send output to the specified file                                                                |
| -F format    | --format=format     | p/plain: Output a plain-text SQL script file                                                     |
|              |                     | c/custom: Output a custom-format archive suitable for input into pg_restore                      |
| -s           | --schema-only       | Dump only the schema (data definitions), not the data                                            |
| -j njobs     | --jobs=njobs        | Run the dump in parallel by dumping njobs tables simultaneously                                  |
| -d dbname    | --dbname=dbname     | Specifies the name of the database to connect to                                                 |
| -h host      | --host=host         | Specifies the host name of the machine on which the server is running                            |
| -p port      | --port=port         | The TCP port on which the server listens for connections                                         |
| -U username  | --username=username | Specifies the connection user name                                                               |

##### pg_restore

| Short Option | Long Option         | Description                                                                                      |
| ------------ | ------------------- | ------------------------------------------------------------------------------------------------ |
| -a           | --data-only         | Restore only the data, not the schema (data definitions)                                         |
| -c           | --clean             | Clean (drop) database objects before recreating them                                             |
| -C           | --create            | Create the database before restoring                                                             |
| -d dbname    | --dbname=dbname     | Connect to database dbname and restore directly into this database                               |
| -e           | --exit-on-error     | Exit if an error is encountered while sending SQL commands to the database                       |
| -F format    | --format=format     | pg_restore automatically recognizes the format, so this option is not required                   |
|              |                     | p/plain: Output a plain-text SQL script file                                                     |
|              |                     | c/custom: Output a custom-format archive suitable for input into pg_restore                      |
| -j njobs     | --jobs=njobs        | Use multiple concurrent jobs for data loading, index creation, and constraint creation           |
| -s           | --schema-only       | Restore only the schema (data definitions) from archive entries, not the data (table contents)   |
| -h host      | --host=host         | Specifies the host name of the machine on which the server is running                            |
| -p port      | --port=port         | The TCP port on which the server listens for connections                                         |
| -U username  | --username=username | Specifies the connection user name                                                               |
| -v           | --verbose           | Specifies verbose mode                                                                           |

### 4. Commonly Used Command Examples

When using with AWS RDS and similar services, you are connecting to a remote host, so the `-h` option is required.

Export only table data with pg_dump (custom mode):

```sh
pg_dump -h aurorapostgresdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U <username> -a -t <table_name> -Fc <db_name> > rds01.custom
```

Connect to rds01, drop objects before importing, then import:

```sh
pg_restore -v -h aurorapostgresdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U <username> -c -C -d <db_name> /home/ec2-user/rds01_dump_2.custom
```

Import only the schema definition:

```sh
pg_restore -v -h rdspostgresql1.xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U <username> -s -d <db_name> /home/ec2-user/rds01_dump_2.custom
```

Import only data:

```sh
pg_restore -v -h aurorapostgresdb.xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U <username> -a -d <db_name> /home/ec2-user/rds01_dump_2.custom
```

Run restore in parallel (8 parallel jobs):

```
pg_restore -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -j 8 -d tpcc tpcc.dump
```



## References

> pg_dump [https://www.postgresql.jp/document/10/html/app-pgdump.html](https://www.postgresql.jp/document/10/html/app-pgdump.html)

> pg_restore [https://www.postgresql.jp/document/10/html/app-pgrestore.html](https://www.postgresql.jp/document/10/html/app-pgrestore.html)
