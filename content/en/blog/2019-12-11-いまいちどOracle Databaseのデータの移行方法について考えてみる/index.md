---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Reconsidering Oracle Database Data Migration Methods"
subtitle: "JPOUG Advent Calendar 2019, Day 11"
summary: " "
tags: ["Oracle", "Migration"]
categories: ["Oracle"]
url: oracle-jpoug-migration-database.html
date: 2019-12-11
lastmod: 2019-12-11
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


This article is the Day 11 entry in the [JPOUG Advent Calendar 2019](https://adventar.org/calendars/4154). Day 10 was Naotaka Shinogi's [Thinking About Running Databases on Nutanix](https://ameblo.jp/shinogi-gogo/entry-12555315409.html). It reminded me of when I went for a casual interview at Nutanix after getting interested in Nutanix Era.

#### **1. About Migration**

Let's assume an Oracle-to-Oracle upgrade and cloud migration project. Just hearing the words "system migration" makes anyone's heart race, even if they're not directly involved. Database upgrades in particular tend to attract special attention — they're a major event. The data stored in a database is the backbone of business operations, and problems with the database affect the entire system, which is why the stakes are so high. How to do it with "minimal risk," in the "shortest time," and "without incident" is where a DBA gets to show their skills. While the level of impact on users and other systems varies, I think it's actually harder to afford several days of downtime for a database upgrade. Most requirements call for zero downtime, or at most a few hours to one day. There may also be requirements to run old and new systems in parallel after the migration and replicate updates from the new system back to the old. Choosing to continue using Oracle Database in a world where cloud services like AWS RDS and OSS like PostgreSQL and MySQL are available means this is typically an important system with many users.

The traditional method of using Data Pump (or imp/exp for older systems) for data migration has been widely used. The first project I worked on was like this. That project allocated a lot of time for migration. After migrating the data, we verified data integrity by checking record counts and reviewing actual data. Since we were also implementing business requirement changes alongside the infrastructure upgrade, developing migration tools was quite challenging. I felt that database migration should follow the principle of "simple is best." However, when you analyze an existing database, you often find that it uses dblinks to integrate with other systems and requires careful ordering of migration steps, or that each system on a server must be migrated separately — many constraints arise beyond just the database itself.

I've gone on long enough with the introduction, but when it comes to reducing downtime during migration and improving reliability, the design pattern that first comes to mind is differential synchronization. For example:

- Several weeks before migration day: Take a snapshot and transfer the data to the destination
- From several weeks before to migration day itself: Continuously apply differential synchronization
- On migration day: After confirming synchronization has caught up, perform the switchover

The prime examples of this use case are Oracle GoldenGate and AWS Database Migration Service — the most well-known products and services for differential synchronization. This approach shifts the migration-day risk to before the migration date.

#### **2. Oracle Database Data Migration Methods**

As you may know, Oracle Database provides many data migration options:

- export/import (for migration from older versions only)
- Data Pump
- Transportable Tablespace
- Cross-Platform Transportable Tablespace
- Transportable Tablespace using Incremental Backup
- Incremental Cross-Platform Transportable Tablespace
- Full Transportable export/import
- Oracle GoldenGate
- Duplicate from backup
- Data Guard standby promotion to primary
- Oracle Zero Downtime Migration (limited to migration to Oracle Cloud)

Reference:

> Introduction to Oracle Database Upgrade and Migration Best Practices [https://www.oracle.com/technetwork/jp/content/upgrade-patch-seminar-2654134-ja.pdf](https://www.oracle.com/technetwork/jp/content/upgrade-patch-seminar-2654134-ja.pdf)

For this article, I'll cover "Transportable Tablespace using Incremental Backup" and "Oracle Zero Downtime Migration." I chose the incremental transportable tablespace method because despite being a solution capable of significantly reducing downtime, it is underused, and there are few practical "let's try it" articles available online. I chose "Oracle Zero Downtime Migration" because it's a recently released method for migrating data to Oracle Cloud and I was curious about its "Zero Downtime" architecture. I actually tried Oracle Zero Downtime Migration hands-on but ran into errors and got stuck, so I'll summarize what I researched on paper.

#### **3. Transportable Tablespace Using Incremental Backup**

The advantages and effectiveness of Transportable Tablespace using incremental backup are also described in an article by Watanabe-san of COSOL in the [JPOUG Advent Calendar 2016](https://jpoug.doorkeeper.jp/events/53797). Please refer to that as well.

> Illustrating a database migration method to minimize downtime using RMAN differential incremental backup and Full Transportable Export/Import (COSOL Database Engineer's Blog) [http://cosol.jp/techdb/2016/12/illustrate-full-transportable-export-import-with-rman-incremental-backup.html](http://cosol.jp/techdb/2016/12/illustrate-full-transportable-export-import-with-rman-incremental-backup.html)

Incidentally, MOS contains the following how-to knowledge document focused on Cross Platform Transportable Tablespace with Incremental Backup, but as far as I can confirm, the manual itself does not provide step-by-step instructions.

> V4 Reduce Transportable Tablespace Downtime using Cross Platform Incremental Backup (Document ID 2471245.1)

Also, since document 2471245.1 uses Perl scripts for data migration, it's unclear internally what processes and commands are being used. So, I'll manually perform the Transportable Tablespace with Incremental Backup. Since I'm referencing Doc 2471245.1, it should be approximately correct, but if you actually use this method for a migration, you should use the Perl script from the document above. It has many features, including automatic SCN management.

#### **Procedure Flow for Transportable Tablespace Using Incremental Backup**

1. Preparation Phase (source data remains online)

   - Full tablespace backup (Level 0)
   - Transfer the backup set to the target DB side

2. Restore from Level 0 Full Backup

   - Roll forward the backup set taken from the source DB on the target DB

3. Take incremental backup on source and apply to target

   - Transfer the incremental backup set to the target DB side. Apply to the destination data files

4. Metadata extraction and migration

   - Change the source database to READ ONLY and perform the final roll forward phase
   - Use Data Pump to import the metadata of objects in the tablespace into the destination database
   - Change the tablespace in the destination database to READ WRITE

#### **Diagram**

By migrating a full backup at a specific point in time and the differential data generated after the full backup before the migration date, the downtime can be reduced.

<img src="image-20191217224018152.png" alt="image-20191217224018152" style="zoom:50%;" />



#### **Execution Environment**

Source: 12.1.0.2

Target: 19.3

#### **Steps**

##### **1. Enable Block Change Tracking**

Since we're using incremental backups, enable the Block Change Tracking file (change tracking file). This speeds up backup operations. For incremental backups, only blocks where data has changed are read directly based on this file, reducing backup time.

```sql
ALTER DATABASE ENABLE BLOCK CHANGE TRACKING;
```

##### **2. Take Level 0 Backup**

Check the source-side SCN:

```sql
SQL> select current_scn from v$database;

CURRENT_SCN
-----------
    3450645
```

Take a Level 0 backup. In this example, we're migrating a tablespace called TTS. [You need to verify that the transportable tablespace set is self-contained](https://docs.oracle.com/cd/E57425_01/121/ARPLS/d_tts.htm) as needed.

```sh
rman target /
backup for transport allow inconsistent incremental level 0 format '/home/oracle/rman/tts_level0.bkp' tablespace tts;

Starting backup (start time: 19-12-11)
Using channel ORA_DISK_1
Channel ORA_DISK_1: starting incremental level 0 data file backup set
Channel ORA_DISK_1: specifying data file(s) in backup set
Input data file, file number=00014 name=/u01/app/oracle/oradata/DB121S/datafile/o1_mf_tts_gystzx22_.dbf
Channel ORA_DISK_1: starting piece 1 (19-12-11)

Channel ORA_DISK_1: piece 1 (19-12-11) finished
Piece handle=/home/oracle/rman/tts_level0.bkp tag=TAG20191211T135511 comment=NONE
Channel ORA_DISK_1: backup set complete. Elapsed time: 00:00:01
Backup completed (completion time: 19-12-11)
```

##### **3. Restore from Level 0 Backup on Target Side**

Restore on the target side:

```sh
restore all foreign datafiles to new from backupset '/home/oracle/rman/tts_level0.bkp';

[oracle@dbsrvec2 ~]$ rman target /

Recovery Manager: Release 19.0.0.0.0 - Production on Wed Dec 11 13:46:43 2019
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates. All rights reserved.

Connected to target database: DB19C (DBID=2154771102)

RMAN> restore all foreign datafiles to new from backupset '/home/oracle/rman/tts_level0.bkp';

Starting restore on 19-12-11
Using channel ORA_DISK_1

Channel ORA_DISK_1: starting restore of data file backup set
Channel ORA_DISK_1: specifying data file(s) to restore from backup set
Channel ORA_DISK_1: restoring all foreign files from backup piece
Channel ORA_DISK_1: reading from backup piece /home/oracle/rman/tts_level0.bkp
Channel ORA_DISK_1: restoring foreign file 14 to /u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf
Channel ORA_DISK_1: foreign piece handle /home/oracle/rman/tts_level0.bkp
Channel ORA_DISK_1: backup piece 1 restored
Channel ORA_DISK_1: restore complete. Elapsed time: 00:00:02
Finished restore on 19-12-11
```

If DB_CREATE_FILE_DEST is not set, you'll get an error: "RMAN-05088: DB_CREATE_FILE_DEST is not set."

```sql
ALTER SYSTEM SET DB_CREATE_FILE_DEST = '/u01/app/oracle/oradata/db19c' SCOPE = both;
```

##### **4. Take Incremental Backup**

Check the source SCN again:

```sql
SQL> select current_scn from v$database;

CURRENT_SCN
-----------
    3450702
```

Take a Level 1 incremental backup. The SCN specified here is the SCN obtained at the very beginning.

```sh
backup for transport allow inconsistent incremental from scn 3450645 format '/home/oracle/rman/tts_level1.bkp' tablespace tts;

RMAN> backup for transport allow inconsistent incremental from scn 3450645 format '/home/oracle/rman/tts_level1.bkp' tablespace tts;

Starting backup (start time: 19-12-11)
Using channel ORA_DISK_1
Channel ORA_DISK_1: starting full data file backup set
Channel ORA_DISK_1: specifying data file(s) in backup set
Input data file, file number=00014 name=/u01/app/oracle/oradata/DB121S/datafile/o1_mf_tts_gystzx22_.dbf
Channel ORA_DISK_1: starting piece 1 (19-12-11)
Channel ORA_DISK_1: piece 1 (19-12-11) finished
Piece handle=/home/oracle/rman/tts_level1.bkp tag=TAG20191211T135615 comment=NONE
Channel ORA_DISK_1: backup set complete. Elapsed time: 00:00:01
Backup completed (completion time: 19-12-11)
```

Note that if there are no updates on the source side, the backup will be skipped with a warning:

```sh
RMAN-06755: WARNING: datafile 14: incremental start SCN is too recent; using checkpoint SCN 3304366 instead
Channel ORA_DISK_1: starting full data file backup set
Channel ORA_DISK_1: specifying data file(s) in backup set
Input data file, file number=00014 name=/u01/app/oracle/oradata/DB121S/datafile/o1_mf_tts_gystzx22_.dbf
Datafile 00014: skipped because there are no changes
Channel ORA_DISK_1: backup cancelled because all files were skipped
Backup completed (completion time: 19-12-11)
```

##### **5. Apply Incremental Backup**

Apply the incremental backup to the data files. The data file specified here is the one output when the restore command was executed above.

```sh
recover foreign datafilecopy '/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf' from backupset '/home/oracle/rman/tts_level1.bkp';

RMAN> recover foreign datafilecopy '/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf' from backupset '/home/oracle/rman/tts_level1.bkp';

Starting restore on 19-12-11
Using channel ORA_DISK_1

Channel ORA_DISK_1: starting restore of data file backup set
Channel ORA_DISK_1: specifying data file(s) to restore from backup set
Channel ORA_DISK_1: restoring foreign file /u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf
Channel ORA_DISK_1: reading from backup piece /home/oracle/rman/tts_level1.bkp
Channel ORA_DISK_1: foreign piece handle /home/oracle/rman/tts_level1.bkp
Channel ORA_DISK_1: backup piece 1 restored
Channel ORA_DISK_1: restore complete. Elapsed time: 00:00:01
Finished restore on 19-12-11
```

Repeat the "take incremental backup" and "apply incremental backup" phases at any timing until migration day arrives.

##### **6. Apply Final Incremental Backup and Obtain Metadata**

This is migration day work. Downtime for the source database begins at this point. Set the target TTS tablespace to read-only:

```sql
alter tablespace tts read only;
```

Create the final incremental backup with the tablespace now read-only. Obtain metadata to make the data files transportable to the destination database:

```sh
backup for transport incremental from scn 3450702 format '/home/oracle/rman/tts_last.bkp' tablespace tts DATAPUMP FORMAT '/home/oracle/rman/dp_tts_ts.dmp';

RMAN> backup for transport incremental from scn 3450702 format '/home/oracle/rman/tts_last.bkp' tablespace tts DATAPUMP FORMAT '/home/oracle/rman/dp_tts_ts.dmp';

Starting backup (start time: 19-12-11)
Using channel ORA_DISK_1
Running TRANSPORT_SET_CHECK on specified tablespaces
TRANSPORT_SET_CHECK completed successfully

Exporting metadata for specified tablespaces...
   EXPDP> Starting "SYS"."TRANSPORT_EXP_DB121S_bCex":
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/PLUGTS_BLK
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/TABLE
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/CONSTRAINT/CONSTRAINT
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/INDEX_STATISTICS
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/TABLE_STATISTICS
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/STATISTICS/MARKER
   EXPDP> Processing object type TRANSPORTABLE_EXPORT/POST_INSTANCE/PLUGTS_BLK
   EXPDP> Master table "SYS"."TRANSPORT_EXP_DB121S_bCex" successfully loaded/unloaded
   EXPDP> ******************************************************************************
   EXPDP> Dump file set for SYS.TRANSPORT_EXP_DB121S_bCex is:
   EXPDP>   /u01/app/oracle/product/12.1.0.2/dbhome_1/dbs/backup_tts_DB121S_17308.dmp
   EXPDP> ******************************************************************************
   EXPDP> Transportable tablespace TTS requires the following data files:
   EXPDP>   /u01/app/oracle/oradata/DB121S/datafile/o1_mf_tts_gystzx22_.dbf
   EXPDP> Job "SYS"."TRANSPORT_EXP_DB121S_bCex" successfully completed at Wed Dec 11 14:02:24 2019 elapsed 0 00:00:47
Export completed

...
Backup completed (completion time: 19-12-11)
```

Apply the final backup to the data files:

```sh
recover foreign datafilecopy '/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf' from backupset '/home/oracle/rman/tts_last.bkp';

RMAN> recover foreign datafilecopy '/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf' from backupset '/home/oracle/rman/tts_last.bkp';

Starting restore on 19-12-11
...
Finished restore on 19-12-11
```

Restore the metadata export dump from the final backup set:

```sh
restore dump file datapump destination '/u01/app/oracle/admin/db19c/dpdump' from backupset '/home/oracle/rman/dp_tts_ts.dmp';

RMAN> restore dump file datapump destination '/u01/app/oracle/admin/db19c/dpdump' from backupset '/home/oracle/rman/dp_tts_ts.dmp';

Starting restore on 19-12-11
...
Finished restore on 19-12-11
```

**7. Execute the Transportable Import!**

By importing this metadata into the destination database, the data files we've been carefully recovering (applying) become usable in the destination.

```sh
impdp system/oracle directory=data_pump_dir dumpfile=backup_tts_DB19C_54885.dmp logfile=backup_tts_DB19C_54885.log transport_datafiles='/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf';

[oracle@dbsrvec2 ~]$ impdp system/oracle directory=data_pump_dir dumpfile=backup_tts_DB19C_54885.dmp logfile=backup_tts_DB19C_54885.log transport_datafiles='/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf';

Import: Release 19.0.0.0.0 - Production on Wed Dec 11 14:07:18 2019
Version 19.3.0.0.0

...

ORA-39123: Data Pump transportable tablespace job aborted.
ORA-29342: user TTS does not exist in the database.

Job "SYSTEM"."SYS_IMPORT_TRANSPORTABLE_01" stopped due to fatal error at Wed Dec 11 14:07:22 2019 elapsed 0 00:00:02
```

Create the user. Since the TTS tablespace doesn't exist yet at this point, don't specify a default tablespace:

```sh
SQL> create user tts identified by "oracle";

User created.

SQL> grant dba to tts;

Grant succeeded.
```

Try again:

```sh
[oracle@dbsrvec2 ~]$ impdp system/oracle directory=data_pump_dir dumpfile=backup_tts_DB19C_54885.dmp logfile=backup_tts_DB19C_54885.log transport_datafiles='/u01/app/oracle/oradata/DB19C/datafile/o1_mf_tts_gz1xbopy_.dbf';

Import: Release 19.0.0.0.0 - Production on Wed Dec 11 14:08:56 2019
Version 19.3.0.0.0

...
Job "SYSTEM"."SYS_IMPORT_TRANSPORTABLE_01" successfully completed at Wed Dec 11 14:09:09 2019 elapsed 0 00:00:13
```

The TTS tablespace has been created. Also change the default tablespace for the tts user:

```sh
SQL> select TABLESPACE_NAME from dba_tablespaces;

TABLESPACE_NAME
--------------------------------------------------------------------------------
SYSTEM
SYSAUX
UNDOTBS1
TEMP
USERS
TTS

6 rows selected.

SQL> alter user tts DEFAULT TABLESPACE tts;

User altered.
```

Finally, change the tablespace in the destination to read-write and you're done:

```sql
alter tablespace tts read write;
```

#### **Impressions**

As described above, this method has distinctive advantages compared to other migration methods. While it can't completely replace GoldenGate, it can be a viable option when you want to migrate without additional cost, minimize downtime, or perform a version upgrade.



#### **4. Oracle Zero Downtime Migration**

##### **Introduction**

I was curious about the architecture, internals, and concepts of Oracle's Zero Downtime Migration tool. Initially, I wanted to try it hands-on to see how it felt and whether it actually worked well, then write about it for the Advent Calendar. However, I ran into errors and got stuck, so I'll just summarize the overview. All input information comes from the following manual and whitepaper:

> [https://www.oracle.com/database/technologies/rac/zdm.html](https://www.oracle.com/database/technologies/rac/zdm.html)
>
> [https://docs.oracle.com/en/database/oracle/zero-downtime-migration/](https://docs.oracle.com/en/database/oracle/zero-downtime-migration/)
>
> [https://www.oracle.com/technetwork/database/options/clustering/learnmore/oracle-zdm-wp-5869851.pdf](https://www.oracle.com/technetwork/database/options/clustering/learnmore/oracle-zdm-wp-5869851.pdf)

##### **Oracle Zero Downtime Migration Overview**

There appear to be two main functions:

- Zero Downtime Migration using Data Guard
- Offline (backup and restore) migration

The rough steps for "Zero Downtime Migration using Data Guard" can be seen at the [official page's 8 Simple Automated Steps](https://www.oracle.com/database/technologies/rac/zdm.html):

1. Install & Setup ZDM/Agent (requires a separate Oracle Linux 7+ environment with 100GB+ storage)
2. Start ZDM
3. Connect source database to Object Storage
4. Backup to Object Storage using RMAN
5. Create Data Guard standby (using backup from step 4)
6. Sync with Data Guard
7. Switchover
8. Terminate connections from source and target, clean up source and target environments

"Offline (backup and restore) migration" is a feature designed for Standard Edition databases that cannot use Data Guard. However, details of the offline migration are not well documented in the manual or whitepaper. For offline migration, network connectivity between the source and target databases is not required. There is a "zdm_template_zdmsdb.rsp" file where you choose whether to use Data Guard-based migration or offline (object storage) migration.

The whitepaper clearly states that Data Guard is the underlying technology:

> ZDM automates the entire process of migration, reducing the chance of human errors. ZDM leverages Oracle Database-integrated high availability (HA) technologies such as Oracle Data Guard and follows all MAA best practices that ensures zero to no downtime of production environments

Supported versions are 11.2.0.4 through 19c:

> Oracle ZDM supports the following Oracle Database versions:
>
> - 11.2.0.4
> - 12.1.0.2
> - 12.2.0.1
> - 18c
> - 19c

Since it's a Data Guard-based solution, Oracle Zero Downtime Migration can only migrate between databases of the same version.

> The source and target databases should be in the same database version. Oracle ZDM supports Oracle Databases hosted on Linux operating systems. The source database can be a single instance database migrating to a single instance or a RAC database, or it can also be a RAC One Node / RAC database, migrating to a RAC database.

Just as Standard Edition cannot use Data Guard, Standard Edition migrations with Zero Downtime Migration also require a different approach:

> Oracle ZDM supports Enterprise & Standard Edition Oracle Databases as source databases. Enterprise Edition Databases are migrated leveraging Oracle Data Guard; Standard Edition Databases are migrated in an offline manner using a backup and restore methodology.

Detailed steps are below. Automated execution is possible using the ZDMCLI command:

| **Phase Name**                | **Description**                                                              |
| :---------------------------- | :--------------------------------------------------------------------------- |
| ZDM_GET_SRC_INFO              | Retrieve information about the source database                               |
| ZDM_GET_TGT_INFO              | Retrieve information about the target database                               |
| ZDM_SETUP_SRC                 | Set up the Zero Downtime Migration helper module on the source server        |
| ZDM_SETUP_TGT                 | Set up the Zero Downtime Migration helper module on the target server        |
| ZDM_PREUSERACTIONS            | Execute pre-migration user actions (if any) on the source                    |
| ZDM_PREUSERACTIONS_TGT        | Execute pre-migration user actions (if any) on the target                    |
| ZDM_OBC_INST_SRC              | Install Oracle Database Cloud Backup Module on the source                    |
| ZDM_OBC_INST_TGT              | Install Oracle Database Cloud Backup Module on the target                    |
| ZDM_GEN_RMAN_PASSWD           | Generate a random password to encrypt RMAN backups                           |
| ZDM_BACKUP_FULL_SRC           | Perform a full backup of the source database                                 |
| ZDM_BACKUP_INCREMENTAL_SRC    | Perform an incremental backup of the source database                         |
| ZDM_VALIDATE_SRC              | Run validation on the source                                                 |
| ZDM_VALIDATE_TGT              | Run validation on the target                                                 |
| ZDM_DISCOVER_SRC              | Run database discovery on the source to configure Data Guard                 |
| ZDM_COPYFILES                 | Copy Oracle password file and TDE wallet from source to target               |
| ZDM_OSS_STANDBY_SETUP_TDE_TGT | Copy TDE wallet file from source to target keystore location                 |
| ZDM_PREPARE_TGT               | Prepare target for Data Guard standby creation                               |
| ZDM_CLONE_TGT                 | Create Data Guard standby from cloud backup                                  |
| ZDM_FINALIZE_TGT              | Complete Data Guard standby preparation on target                            |
| ZDM_CONFIGURE_DG_SRC          | Register cloud standby with the source                                       |
| ZDM_SWITCHOVER_SRC            | Initiate switchover action on the source                                     |
| ZDM_SWITCHOVER_TGT            | Complete switchover action on the target                                     |
| ZDM_POSTUSERACTIONS           | Execute post-migration user actions on the source                            |
| ZDM_POSTUSERACTIONS_TGT       | Execute post-migration user actions on the target                            |
| ZDM_CLEANUP_SRC               | Perform cleanup on the source                                                |
| ZDM_CLEANUP_TGT               | Perform cleanup on the target                                                |



##### **Impressions**

Initially, "Zero Downtime Migration" made me think of Oracle GoldenGate, but it turns out it's actually done using Data Guard. The fact that it can only be used with the same version means it can't be used for a "migration with version upgrade" to the cloud, which I see as a drawback. My understanding is that it's simply a tool for cloud migration. I'm curious about the Data Guard mode (sync/async) and how it behaves with apply lag in async mode. Also, looking at the manual, I didn't see any documentation about changes needed to the source database's Data Guard configuration as a prerequisite. Isn't Force Logging mandatory for DG? Since I wasn't able to run it all the way through, I couldn't document the full details — that's something I regret.



#### **Conclusion**

***

Let's use better migration methods to make our lives easier!

I've been hosting on GitHub Pages using a framework called Pelican for the past few months, but it's so inconvenient that I'm eager to migrate my blog to something else.
