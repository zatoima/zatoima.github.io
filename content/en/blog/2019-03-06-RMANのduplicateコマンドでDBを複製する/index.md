---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Duplicating a Database with the RMAN Duplicate Command"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-rman-ruplicate.html
date: 2019-03-06
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



#### **Introduction**

There are four patterns for database duplication.

The available options depend on the system requirements.

In this example, we use pattern 4: "Backup-based duplication without connecting to target or recovery catalog".

------

1. Active duplication

   Duplicates directly from an open or mounted database.

2. Backup-based duplication without target connection

   RMAN creates duplicate files from existing RMAN backups and copies.

   This form requires a connection to the auxiliary instance and the recovery catalog.

3. Backup-based duplication with target connection

   Creates duplicate files from existing RMAN backups and copies.

4. Backup-based duplication without connecting to target or recovery catalog

   Creates duplicate files from RMAN backups and copies placed at the location specified by BACKUP LOCATION.

------

Note that restore and recovery from an RMAN backup is also a form of database duplication, but it is not covered in this example.

**Environment Configuration**

This procedure duplicates within the same host.

| No   | Database Name | DB Version | Notes       |
| ---- | ------------- | ----------- | ----------- |
| 1    | db121s        | 12.1.0.2    | Source      |
| 2    | db121t        | 12.1.0.2    | Destination |

Take an RMAN backup **on the source**:

```sql
rman target /
run {
  BACKUP INCREMENTAL LEVEL 0 DATABASE FORMAT '/home/oracle/rman/db121s/full_%d_%T_%U' SPFILE PLUS ARCHIVELOG FORMAT '/home/oracle/rman/db121s/ARCH_%d_%T_%U';
  BACKUP AS COPY CURRENT CONTROLFILE FORMAT '/home/oracle/rman/db121s/CNT_%d_%T_%U.ctl';
}
```

#### **Clean Up Destination**

```sql
rm -rf /u01/app/oracle/oradata/DB121T/*
```

#### **Create Destination Parameter File**

Connect to the source database and create an editable pfile from the spfile.

```sql
. /home/oracle/.oraenv_db121s
sqlplus / as sysdba
create pfile='/tmp/initdb121t.ora' from spfile;
exit
```

#### **Edit Destination Parameter File**

Change values that depend on the source to destination-specific values. (e.g., change db_name from "db121s" to "db121t")

```sql
vi /tmp/initdb121t.ora

Change the following parameter values:
- *.cluster_database     : false
- *.control_files        : /u01/app/oracle/oradata/db121t
- *.db_name              : db121t
- *.db_unique_name       : db121t
- *.dispatchers          : (PROTOCOL=TCP) (SERVICE=db121tXDB)

Add the following parameters:
*.DB_FILE_NAME_CONVERT='/u01/app/oracle/oradata/DB121S/datafile/','/u01/app/oracle/oradata/DB121T/datafile/'
*.LOG_FILE_NAME_CONVERT='/u01/app/oracle/oradata/DB121S/onlinelog/','/u01/app/oracle/oradata/DB121T/onlinelog'
```

#### **Start Auxiliary Instance**

```sql
. /home/oracle/.oraenv_db121t
sqlplus / as sysdba
startup nomount pfile='/tmp/initdb121t.ora'
```

#### **Create spfile**

```sql
create spfile = '/u01/app/oracle/product/12.1.0.2/dbhome_2/dbs/spfiledb121t.ora' from pfile='/tmp/initdb121t.ora';
exit
```

#### **Execute Duplicate Command**

```sql
rman auxiliary /
run {
duplicate database to db121t backup location '/home/oracle/rman/db121s';
}
```

For details on the RMAN duplicate command, please refer to the manual:

> Oracle® Database Backup and Recovery Reference 12c Release 1 (12.1)
>
> https://docs.oracle.com/cd/E57425_01/121/RCMRF/rcmsynta020.htm
>
> DUPLICATE
