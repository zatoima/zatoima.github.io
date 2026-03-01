---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ORA-31633 and ORA-01647 Failures During Full Transportable Tablespace"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-full-tts-oraerror.html
date: 2019-04-12
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

The Full Transportable Export/Import feature allows you to move an entire database to a different database instance.

Since it can migrate all data from the entire database, you do not need to separately create indexes and various objects (procedures, packages, etc.) in the target database.

Also, similar to Transportable Tablespace (TTS), data files can be physically copied, so there is no need to create intermediate files. This method is faster compared to Data Pump. (Metadata still needs to be exported separately.)

Please also refer to the following white paper:

> https://www.oracle.com/technetwork/jp/database/enterprise-edition/full-transportable-wp-12c-1973971-ja.pdf
>
> \> Oracle Database 12c: Full Transportable Export/Import

#### **Procedure Overview**

> 1) On the source database, put each user-defined tablespace in read-only mode and export the database.
>
> - Verify that the following parameters are set to the specified values:
>   TRANSPORTABLE=ALWAYS
>   FULL=Y
> - If the source database is Oracle Database 11g Release 2 (11.2.0.3) or later, you need to set the VERSION parameter to 12 or higher.
> - If the source database contains encrypted tablespaces or tablespaces containing tables with encrypted columns, you must specify ENCRYPTION_PWD_PROMPT=YES or the ENCRYPTION_PASSWORD parameter.
> - The export dump file contains both the metadata for objects stored in user-defined tablespaces, and the metadata and data for user-defined objects stored in administrative tablespaces (such as SYSTEM and SYSAUX).



#### **Error Details**

Following the procedure overview above, when putting user tablespaces in read-only mode and running expdp with `TRANSPORTABLE=ALWAYS` and `FULL=Y`, `ORA-31633` and `ORA-01647` errors occurred.

```sh
[oracle@dbvop]$ expdp DPUSR/oracle full=y transportable=always directory=dp_dir dumpfile=full_tts.dmp encryption_password=oracle logfile=full_tts_export.log

Export: Release 12.1.0.2.0 - Production on Wed Mar 13 15:04:08 2019

Copyright (c) 1982, 2014, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 12c Enterprise Edition Release 12.1.0.2.0 - 64bit Production
With the Partitioning, Real Application Clusters, Oracle Label Security, OLAP,
Advanced Analytics, Oracle Database Vault and Real Application Testing options
ORA-31626: job does not exist
ORA-31633: unable to create master table "DPUSR.SYS_EXPORT_FULL_07"
ORA-06512: at "SYS.DBMS_SYS_ERROR", line 95
ORA-06512: at "SYS.KUPV$FT", line 1048
ORA-01647: tablespace 'USERS' is read-only, cannot allocate space in it
```

#### **Cause**

The cause is that the following manual restriction was triggered.

> https://docs.oracle.com/cd/E57425_01/121/SUTIL/GUID-206EC89B-5E43-4CCF-8B78-2C7F91FC5D7D.htm
>
> TRANSPORT_TABLESPACES
>
> The default tablespace of the user running the export cannot be set to any of the tablespaces being transported.

The white paper and manual procedures run as the "system" user, and the default tablespace for the system user is "SYSAUX".

In this case, we were running with a Data Pump-specific user `DPUSR`. This user had a "user tablespace" set as the default tablespace, which caused the error.

#### **Workaround**

Either of the following two options:

1. Run as SYS or SYSTEM user
2. Temporarily change the default tablespace of the Data Pump user DPUSR to "SYSAUX"
