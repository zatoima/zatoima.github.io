---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "About Instantiation SCN When Using FLASHBACK_SCN with expdp"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-flashbackscn-instantiationSCN.html
date: 2019-03-30
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

GoldenGate has a feature called Instantiation SCN. This feature makes it easy to perform zero-downtime initial migration using Data Pump.

For details, please refer to the following Qiita article which explains it clearly:

Instantiation SCN for Easy Initial Migration - Qiita https://qiita.com/kurouuuron/items/118afdc6b6d15d46e7dd

> A GoldenGate feature for initial migration that enhances integration with Oracle Data Pump.
>
> In brief, it enables zero-downtime initial migration using Data Pump.
>
> More specifically, it handles considerations for initial migration such as Flashback_scn and Handlecollisions automatically.
>
> In practice, when expdp is run with Data Pump, it internally attaches data indicating which SCN has been applied for each table, and after impdp, the Replicat automatically applies data from that SCN onwards.

As mentioned in this article, when add trandata is executed with GoldenGate 12.2 or higher, preparescn is attached by default, so when expdp is run with Data Pump, it internally attaches data indicating which SCN has been applied for each table.

#### **Environment Assumption**

The behavior described is for when `add trandata preparecsn none` is specified.

Please note that if a value other than none is set, the behavior described below may differ.

#### **Behavior When add trandata preparescn none is Set**

As described in the [manual](https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-D3FD004B-81E4-4185-92D3-812834A5DEFC.htm), in this case instantiation preparation is not performed.

**Export on the Source Side**

```sh
[oracle@xxxxxxxx1p ~]$ expdp ggtest/xxxxxx DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES

Export: Release 11.2.0.4.0 - Production on Sun Mar 3 16:47:00 2019

Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, Real Application Clusters, Automatic Storage Management, OLAP,
Data Mining and Real Application Testing options
FLASHBACK automatically enabled to preserve database integrity.
Starting "GGTEST"."SYS_EXPORT_TABLE_01":  ggtest DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES
Estimating with BLOCKS method...
Processing object type TABLE_EXPORT/TABLE/TABLE_DATA
Total estimation using BLOCKS method: 384 KB
. . exported "GGTEST"."T10"                              288.6 KB   10000 rows
Master table "GGTEST"."SYS_EXPORT_TABLE_01" successfully loaded/unloaded
******************************************************************************
Dump file set for GGTEST.SYS_EXPORT_TABLE_01 is:
  /home/oracle/t10.dmp
Job "GGTEST"."SYS_EXPORT_TABLE_01" successfully completed at Sun Mar 3 16:47:04 2019 elapsed 0 00:00:02

```

#### **Import on the Target Side**

```sh
[oracle@xxxxxx ~]$ impdp ggtest/xxxxxx@xxxxxxxx1 DIRECTORY=homedir DUMPFILE=t10.dmp tables=t10

Import: Release 18.0.0.0.0 - Production on Sun Mar 3 16:48:33 2019
Version 18.4.0.0.0

Copyright (c) 1982, 2018, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 18c Enterprise Edition Release 18.0.0.0.0 - Production
Master table "GGTEST"."SYS_IMPORT_TABLE_01" successfully loaded/unloaded
Starting "GGTEST"."SYS_IMPORT_TABLE_01": ggtest@xxxxxxxx1 DIRECTORY=homedir DUMPFILE=t10.dmp tables=t10
Processing object type TABLE_EXPORT/TABLE/TABLE_DATA
. . imported "GGTEST"."T10"                              288.6 KB   10000 rows
Job "GGTEST"."SYS_IMPORT_TABLE_01" successfully completed at Sun Mar 3 16:48:45 2019 elapsed 0 00:00:09
```

#### **Check Instantiation SCN**

Since preparescn is set to none, there is no instantiation SCN in this case.

```sh
SQL> select source_database,source_object_owner,source_object_name,instantiation_scn from  DBA_APPLY_INSTANTIATED_OBJECTS where SOURCE_OBJECT_NAME='T10';

no rows selected
```

#### **When FLASHBACK_SCN is Used with expdp**

This is the main topic of this article. Even when trandata is set with preparecsn none, it appears that the instantiation SCN is set during expdp when FLASHBACK_SCN is used.

#### **Export Command**

Here, a specific FLASHBACK_SCN point-in-time is specified.

```sh
[oracle@xxxxxxxx1p ~]$ expdp ggtest/xxxxxx DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES FLASHBACK_SCN=25587768

Export: Release 11.2.0.4.0 - Production on Sun Mar 3 16:59:04 2019

...

. . exported "GGTEST"."T10"                              288.6 KB   10000 rows
Master table "GGTEST"."SYS_EXPORT_TABLE_01" successfully loaded/unloaded
Job "GGTEST"."SYS_EXPORT_TABLE_01" successfully completed at Sun Mar 3 16:59:08 2019 elapsed 0 00:00:02

```



When a dump file exported with FLASHBACK_SCN is imported with impdp, DBA_APPLY_INSTANTIATED_OBJECTS has INSTANTIATION_SCN set.

```sh
SQL> select source_database,source_object_owner,source_object_name,instantiation_scn from  DBA_APPLY_INSTANTIATED_OBJECTS where SOURCE_OBJECT_NAME='T10';
SOURCE_DATABASE   SOURCE_OBJECT_OWNER   SOURCE_OBJECT_NAME     INSTANTIATION_SCN
xxxxxxx           GGTEST                T10                             25587768 <-★INSTANTIATION_SCN is set
```

#### **Summary**

Even when preparecsn none is set during add trandata, the instantiation SCN is set when FLASHBACK_SCN is used during expdp.

For this behavior, there is documentation in the Streams manual. Please refer to it as well.

> https://docs.oracle.com/cd/E16338_01/server.112/b61352/instant.htm#CIHBDFJE
>
> During export, Oracle Data Pump automatically uses Oracle Flashback to ensure that the data and procedural operations exported for each database object are consistent as of a specific point in time. When performing instantiation in an Oracle Streams environment, a certain level of consistency is required. Using the Data Pump export utility ensures this consistency for Oracle Streams instantiation.
>
> If you are also using the export dump file for purposes other than Oracle Streams instantiation, and those purposes involve stricter consistency requirements than the consistency provided by the default Data Pump export, you can use the Data Pump export utility parameter `FLASHBACK_SCN` or `FLASHBACK_TIME` for Oracle Streams instantiation. For example, stricter consistency may be required if the export includes objects with foreign key constraints.
