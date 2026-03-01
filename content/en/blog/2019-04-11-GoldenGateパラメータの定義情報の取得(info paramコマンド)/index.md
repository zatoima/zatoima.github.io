---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Getting GoldenGate Parameter Definition Information (info param Command)"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-info-param.html
date: 2019-04-11
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

The info param command can be used to retrieve GoldenGate parameter definition information. This feature is available from GoldenGate version 12.2.

Manual:

> https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-60208072-8E74-4703-B4FF-31761E6CDDC0.htm#GUID-60208072-8E74-4703-B4FF-31761E6CDDC0
>
> INFO PARAM
>
> INFO PARAM retrieves parameter definition information. If the name matches multiple records, all matching records are displayed. If a queried parameter has child options, they are not displayed in the output even if listed in the "Options" tab. To view the full record for an option, you must query the complete name individually in the form parameter.option.

#### **Basic Usage**

You can retrieve information about parameters and their sub-parameters as shown below.

```sql
GGSCI (dbvgg.jp.oracle.com) 3> info param BATCHSQL

param name  : batchsql
description : Use the BATCHSQL parameter to increase the performance of Replicat. BATCHSQL causes Replicat to organize similar SQL statements into arrays and apply them at an accelerated rate. In its normal mode, Replicat applies one SQL statement at a time.
argument    : no argument
options     : batcherrormode|nobatcherrormode, batchesperqueue, batchtransops
              bypasspkcheck|nobypasspkcheck, bytesperqueue
              checkuniquekeys|nocheckuniquekeys
              errorhandling|noerrorhandling, maxthreadqueuedepth, opsperbatch
              opsperqueue, thread, trace
component(s): REPLICAT
mode(s)     : all Replicat modes
platform(s) : all platforms
versions    :
database(s) : Oracle 8
              Oracle 9i
              Oracle 10g
              Oracle 11g
              Oracle 12c
              Oracle 18c
              Sybase
              DB2LUW 10.5
              DB2LUW 10.1
              DB2LUW 9.5
              DB2LUW 9.7
              Teradata
              Timesten
              DB2 for i
              DB2 for i Remote
              MS SQL
              MS SQL CDC
              Informix
              SQL/MX
              DB2 z/OS
              PostgreSQL
status      : current
mandatory   : false
dynamic     : false
relations   : none


GGSCI (dbvgg.jp.oracle.com) 4> info param BATCHSQL.opsperbatch

param name  : batchsql.opsperbatch
description : Sets the maximum number of row operations that one batch can contain. After OPSPERBATCH is reached, a target transaction is executed.
argument    : integer
default     : 1200
      range : 1 - 100000
options     :
component(s): REPLICAT
mode(s)     : all Replicat modes
platform(s) : all platforms
versions    :
database(s) : Oracle 8
              ...
status      : current
mandatory   : false
dynamic     : false
relations   : none

```

#### **Output Contents**

The output contains the following fields:

| No.  | Field       | Description                                                    |
| ---- | ----------- | -------------------------------------------------------------- |
| 1    | param name  | Parameter name                                                 |
| 2    | description | Parameter description                                          |
| 3    | argument    | Arguments                                                      |
| 4    | options     | Sub-parameters                                                 |
| 5    | component   | Supported components (capture, data pump, or replicat)         |
| 6    | mode        | Integrated mode or classic mode                                |
| 7    | platform    | Supported platforms                                            |
| 8    | versions    | Supported versions                                             |
| 9    | database    | Supported databases                                            |
| 10   | status      | current or deprecated                                          |
| 11   | mandatory   | Is it required?                                                |
| 12   | dynamic     | Can it be changed dynamically?                                 |
| 13   | relations   |                                                                |

#### **Checking Output Differences Between GoldenGate Versions**

In GoldenGate versions 12.3 and later, the SYSLOG parameter was changed to deprecated. Let's see how this change is reflected in the output.

As shown by the ★ marks in the output below, it has been changed to "deprecated". It might be a good idea to check parameters when upgrading GG.

#### **Output Result for GoldenGate 12.2.0.1**

```sql
[oracle@dbvgg ~]$ ogg1

Oracle GoldenGate Command Interpreter for Oracle
Version 12.2.0.1.170919 OGGCORE_12.2.0.1.0OGGBP_PLATFORMS_171030.0908_FBO
Linux, x64, 64bit (optimized), Oracle 11g on Oct 30 2017 19:19:45
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2017, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> info param syslog

param name  : syslog
description : Use the SYSLOG parameter to control the types of messages that Oracle GoldenGate sends to the system logs on a Windows or UNIX system, or to the SYSOPR message queue on an IBM i system.
argument    : no argument
options     : all, error, info, none, warn
component(s): MGR
              GLOBALS
mode(s)     : none
platform(s) : all platforms
versions    :
    min ver : 11.1.1
database(s) : all supported databases (on the supported platforms).
status      : current ★← "current"
mandatory   : false
dynamic     : false
relations   : none


GGSCI (dbvgg.jp.oracle.com) 2>

```

#### **Output Result for GoldenGate 18.1**

```sql
[oracle@dbvgg ~]$ ogg2

Oracle GoldenGate Command Interpreter for Oracle
Version 18.1.0.0.0 OGGCORE_18.1.0.0.0_PLATFORMS_180928.0432_FBO
Linux, x64, 64bit (optimized), Oracle 18c on Sep 29 2018 07:21:38
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2018, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> info param syslog

param name  : syslog
description : Use the SYSLOG parameter to control the types of messages that Oracle GoldenGate sends to the system logs on a Windows or UNIX system, or to the SYSOPR message queue on an IBM i system.
argument    : no argument
options     : all, error, info, none, warn
component(s): MGR
              GLOBALS
mode(s)     : none
platform(s) : all platforms
versions    :
    min ver : 11.1.1
database(s) : all supported databases (on the supported platforms).
status      : deprecated ★← Changed to "deprecated"
mandatory   : false
dynamic     : false
relations   : none


GGSCI (dbvgg.jp.oracle.com) 2>

```
