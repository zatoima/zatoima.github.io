---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Using pg_upgrade for PostgreSQL Major Version Upgrades"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-versionup-pg_upgrade-extention.html
date: 2020-05-20
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

### Overview of pg_upgrade

> pg_upgrade https://www.postgresql.jp/document/12/html/pgupgrade.html

pg_upgrade is a tool used for PostgreSQL major version upgrades. It allows you to migrate data from an old PostgreSQL version to a new one without a logical migration via backup/restore or pg_dump.

The concepts are out-of-place upgrade and in-place upgrade. pg_upgrade is an in-place upgrade. Logical migration (replication, pg_dump migration, etc.) is an out-of-place upgrade. While downtime is required, it tends to take less time than typical backup-restore methods.

pg_upgrade has two modes:

| Mode       | Description                                                         |
| ---------- | ------------------------------------------------------------------- |
| Copy mode  | Copies data from the existing database cluster to the new PostgreSQL cluster (default) |
| Link mode  | Hard-links the existing database cluster to the new one, sharing data |

Notes on copy mode:
- Immediately after pg_upgrade, data volume temporarily doubles. (Resolved by running ./delete_old_cluster.sh)
- Migration time likely scales proportionally with data size (unverified)

Notes on link mode:
- No file copying means the upgrade itself is very fast
- Less disk space required compared to copy mode
- Once the new PostgreSQL cluster is started, the old cluster cannot be used
- Old and new clusters must be on the same filesystem

### Steps

#### Prerequisites

---

This environment was created in the following article:

> Installing PostgreSQL 11 and 12 with yum on RHEL8 (Red Hat Enterprise Linux) on EC2 | my opinion is my own https://zatoima.github.io/aws-ec2-rhel-postgresql-install.html

Since this is a test, starting from zero.

##### Stop PostgreSQL

```sh
. $HOME/.pgsql11_env
pg_ctl stop

. $HOME/.pgsql12_env
pg_ctl stop
```

##### Delete Data Files

```sh
rm -rf $HOME/11/*
rm -rf $HOME/12/*
```

##### Initialize (Run as root)

```sh
/usr/pgsql-11/bin/postgresql-11-setup initdb
/usr/pgsql-12/bin/postgresql-12-setup initdb
```

##### Load Test Data

```sh
. $HOME/.pgsql11_env
pg_ctl start
pgcli
CREATE TABLE aozora_kaisekidata(file VARCHAR(30),num INT,row INT,word TEXT,subtype1 VARCHAR(30),subtype2 VARCHAR(30),subtype3 VARCHAR(30),subtype4 VARCHAR(10),conjtype VARCHAR(15),conjugation VARCHAR(15),basic TEXT,ruby TEXT,pronunce TEXT );
time psql -d postgres -U postgres -c "COPY aozora_kaisekidata(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < $HOME/utf8_all.csv
```

Note the object information with oid2name:

```sh
[postgres@pgsql ~]$ oid2name -t aozora_kaisekidata
From database "postgres":
  Filenode          Table Name
------------------------------
     16384  aozora_kaisekidata
```

At this point the data size is approximately 10GB:

```sh
postgres> SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;
+-----------+------------------+
| datname   | pg_size_pretty   |
|-----------+------------------|
| postgres  | 9584 MB          |
| template1 | 7585 kB          |
| template0 | 7585 kB          |
+-----------+------------------+
```

This data was created using the following method:

> Importing Morphological Analysis Data of Aozora Bunko Works into RDS PostgreSQL | my opinion is my own https://zatoima.github.io/postgresql-aozora-bunko-data-import.html

##### Pre-check (Stop PostgreSQL)

```sh
. $HOME/.pgsql11_env
pg_ctl stop

. $HOME/.pgsql12_env
pg_ctl stop
```

#### Run pg_upgrade

---

##### 1.) Run pg_upgrade in Copy Mode

Upgrading approximately 10GB of DB takes about 3 minutes.

```sh
[postgres@pgsql ~]$ . $HOME/.pgsql12_env
[postgres@pgsql ~]$ time /usr/pgsql-12/bin/pg_upgrade -r -d /var/lib/pgsql/11/data -D /var/lib/pgsql/12/data -b /usr/pgsql-11/bin -B /usr/pgsql-12/bin
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok
Checking database user is the install user                  ok
Checking database connection settings                       ok
Checking for prepared transactions                          ok
Checking for reg* data types in user tables                 ok
Checking for contrib/isn with bigint-passing mismatch       ok
Checking for tables WITH OIDS                               ok
Checking for invalid "sql_identifier" user columns          ok
Creating dump of global objects                             ok
Creating dump of database schemas
                                                            ok
Checking for presence of required libraries                 ok
Checking database user is the install user                  ok
Checking for prepared transactions                          ok

If pg_upgrade fails after this point, you must re-initdb the
new cluster before continuing.

Performing Upgrade
------------------
Analyzing all rows in the new cluster                       ok
Freezing all rows in the new cluster                        ok
Deleting files from new pg_xact                             ok
Copying old pg_xact to new server                           ok
Setting next transaction ID and epoch for new cluster       ok
Deleting files from new pg_multixact/offsets                ok
Copying old pg_multixact/offsets to new server              ok
Deleting files from new pg_multixact/members                ok
Copying old pg_multixact/members to new server              ok
Setting next multixact ID and offset for new cluster        ok
Resetting WAL archives                                      ok
Setting frozenxid and minmxid counters in new cluster       ok
Restoring global objects in the new cluster                 ok
Restoring database schemas in the new cluster
                                                            ok
Copying user relation files
                                                            ok
Setting next OID for new cluster                            ok
Sync data directory to disk                                 ok
Creating script to analyze new cluster                      ok
Creating script to delete old cluster                       ok

Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade so,
once you start the new server, consider running:
    ./analyze_new_cluster.sh

Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh

real	2m45.122s
user	0m0.174s
sys	0m6.919s
[postgres@pgsql ~]$
```

Since this is copy mode, the inodes are different. (In link mode, they would be the same — described below.)

```sh
[postgres@pgsql ~]$ find . | grep 16384 | xargs ls -li
239076379 -rw-------. 1 postgres postgres 1073741824 May 16 22:54 ./11/data/base/13141/16384
239076383 -rw-------. 1 postgres postgres 1073741824 May 16 22:54 ./11/data/base/13141/16384.1
...
 96472658 -rw-------. 1 postgres postgres 1073741824 May 16 22:55 ./12/data/base/16401/16384
 96472661 -rw-------. 1 postgres postgres 1073741824 May 16 22:55 ./12/data/base/16401/16384.1
...
```

##### 2.) Run pg_upgrade in Link Mode

The execution itself finished in under 10 seconds.

```sh
[postgres@pgsql ~]$ time /usr/pgsql-12/bin/pg_upgrade -r -k -d /var/lib/pgsql/11/data -D /var/lib/pgsql/12/data -b /usr/pgsql-11/bin -B /usr/pgsql-12/bin
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok
...

Linking user relation files
                                                            ok
Setting next OID for new cluster                            ok
Sync data directory to disk                                 ok
Creating script to analyze new cluster                      ok
Creating script to delete old cluster                       ok

Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade so,
once you start the new server, consider running:
    ./analyze_new_cluster.sh

Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh

real	0m7.014s
user	0m0.103s
sys	0m0.210s
```

In link mode, for example `./11/data/base/13141/16384.1` has inode `272636857`, which is the same as the corresponding file in the new cluster.

```sh
[postgres@pgsql ~]$ find . | grep 16384 | xargs ls -li
272636853 -rw-------. 2 postgres postgres 1073741824 May 16 22:42 ./11/data/base/13141/16384
272636857 -rw-------. 2 postgres postgres 1073741824 May 16 22:33 ./11/data/base/13141/16384.1
...
272636853 -rw-------. 2 postgres postgres 1073741824 May 16 22:42 ./12/data/base/16401/16384
272636857 -rw-------. 2 postgres postgres 1073741824 May 16 22:33 ./12/data/base/16401/16384.1
...
```

### Behavior Difference Between Copy and Link Modes

In copy mode, the output log contains a "Copying user relation files" section:

```sh
Copying user relation files                                 ok
```

In link mode, the following output appears instead:

```sh
Adding ".old" suffix to old global/pg_control               ok

If you want to start the old cluster, you will need to remove
the ".old" suffix from /var/lib/pgsql/11/data/global/pg_control.old.
Because "link" mode was used, the old cluster cannot be safely
started once the new cluster has been started.

Linking user relation files
```

### Conclusion

Once various constraints are cleared, pg_upgrade for major version upgrades seems like a viable option. I'd like to try other major version upgrade methods as well.
