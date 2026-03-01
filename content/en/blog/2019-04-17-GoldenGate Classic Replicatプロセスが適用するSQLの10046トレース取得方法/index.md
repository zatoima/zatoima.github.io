---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Get 10046 Trace for SQL Applied by GoldenGate Classic Replicat Process"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-classic-replicat-trace.html
date: 2019-04-17
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

There are situations where you need to investigate the SQL applied by GoldenGate's Replicat process. For SQL performance investigations, the typical approach is to collect a SQL trace and analyze it. However, since you cannot configure SQL tracing at the GoldenGate session level from the database layer, you need to set it at the database level.

On the other hand, GoldenGate provides the SQLEXEC parameter. By adding it to the Replicat process parameter file, you can collect a 10046 trace only for the SQL that Replicat applies.

> SQLEXEC https://docs.oracle.com/cd/E51849_01/gg-winux/GWURF/gg_parameters156.htm
>
> The SQLEXEC parameter executes stored procedures, queries, or database commands within the scope of Oracle GoldenGate processing. SQLEXEC enables Oracle GoldenGate to communicate directly with the database and perform operations supported by the database.

#### **Configuration Method**

```sh
～omitted～
REPORTCOUNT EVERY 10 MINUTES, RATE

SQLEXEC  "ALTER  SESSION  SET  TRACEFILE_IDENTIFIER='GG_DEBUG'"
SQLEXEC  "alter session set events '10046 trace name context forever,level 12'"

BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;
～omitted～
```

Note: This method for obtaining 10046 trace only works with Classic Replicat. For Integrated Replicat, you need to use other methods to obtain SQL performance information.

#### **Execution Result**

Since we added "GG_DEBUG" with TRACEFILE_IDENTIFIER, trace files with "GG_DEBUG" in the name are generated.

```sh
[oracle@dbvgg trace]$ pwd
/u01/app/oracle/diag/rdbms/db18s/db18s/trace
[oracle@dbvgg trace]$ ls -ltr | tail
-rw-r----- 1 oracle oinstall    1737 Apr  3 10:49 2019 db18s_m000_3762.trm
-rw-r----- 1 oracle oinstall    8661 Apr  3 10:49 2019 db18s_m000_3762.trc
-rw-r----- 1 oracle oinstall    1160 Apr  3 10:49 2019 db18s_dbrm_3705.trm
-rw-r----- 1 oracle oinstall    4775 Apr  3 10:49 2019 db18s_dbrm_3705.trc
-rw-r----- 1 oracle oinstall    1646 Apr  3 10:50 2019 db18s_m003_4089.trm
-rw-r----- 1 oracle oinstall    7495 Apr  3 10:50 2019 db18s_m003_4089.trc
-rw-r----- 1 oracle oinstall    1894 Apr  3 10:50 2019 db18s_m002_4087.trm
-rw-r----- 1 oracle oinstall   11111 Apr  3 10:50 2019 db18s_m002_4087.trc
-rw-r----- 1 oracle oinstall  234008 Apr  3 10:50 2019 db18s_ora_5208_GG_DEBUG.trm
-rw-r----- 1 oracle oinstall 1339711 Apr  3 10:50 2019 db18s_ora_5208_GG_DEBUG.trc
[oracle@dbvgg trace]$
```
