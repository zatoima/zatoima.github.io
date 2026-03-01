---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Procedure for Creating GoldenGate Classic Replicat (Non-Integrated Replicat)"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-classic-replicat-create.html
date: 2019-04-10
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



In another article, I described the process configuration procedure for Integrated Replicat. However, Classic Replicat (non-integrated Replicat) is also used frequently, so here are the steps.

The difference in procedures is that the command arguments (options) change, and a checkpoint table needs to be created. Since the internal behavior is quite different, this should be noted separately.

#### **Create Classic Replicat Process on Target Side**

#### **Create Parameter File**

```sh
. /home/oracle/.oraenv_db18s --load environment variables
cd /gg/gg2
./ggsci

#Create parameter file
edit param r21

Set the following parameters:
----
REPLICAT R21
USERID c##ggs@db18p1,  PASSWORD oracle
DISCARDFILE ./dirrpt/r21.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY

BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;
----

view param r21
```



#### **Create Replicat Process**

```sh
#DB login
dblogin userid c##ggs@db18p1,password oracle

#Create Replicat process
add replicat r21, exttrail ./dirdat/d11/rt, CHECKPOINTTABLE c##ggs.ggs_ckpt

#Create checkpoint table
ADD CHECKPOINTTABLE c##ggs.ggs_ckpt
INFO CHECKPOINTTABLE c##ggs.ggs_ckpt
```

```sh
#Execution Result
GSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 4> add replicat r11, exttrail ./dirdat/d11/rt, CHECKPOINTTABLE c##ggs.ggs_ckpt
REPLICAT added.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 5> add checkpointtable
ERROR: Missing checkpoint table specification.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 6>

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 6> ADD CHECKPOINTTABLE c##ggs.ggs_ckpt
Logon catalog name DB18P1 will be used for table specification DB18P1.c##ggs.ggs_ckpt.

Successfully created checkpoint table DB18P1.c##ggs.ggs_ckpt.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 7> info checkpointtable c##ggs.ggs_ckpt
Logon catalog name DB18P1 will be used for table specification DB18P1.c##ggs.ggs_ckpt.

Checkpoint table DB18P1.c##ggs.ggs_ckpt created 2019-04-03 10:33:15.

```



The manual for creating each process is available here:

> https://docs.oracle.com/cd/E74358_01/gg-winux/GIORA/GUID-7065CF34-FD9A-4652-A34A-AE9F6BD3C87E.htm
>
> \> Adding a Replicat Group

When using Classic Replicat, it is also important to understand the checkpoint table. Please refer to the manual:

> https://docs.oracle.com/cd/E74358_01/gg-winux/GIORA/GUID-B3EFA08D-145B-4806-B7E2-B8AE409C651C.htm#GUID-B3EFA08D-145B-4806-B7E2-B8AE409C651C
>
> \> Creating a Checkpoint Table (Non-Integrated Replicat Only)
>
> https://docs.oracle.com/cd/E74358_01/gg-winux/GWUAD/GUID-D1ED9CCF-C81C-4CE2-8EAB-E4C8C7BDF58C.htm
>
> \> Oracle GoldenGate Checkpoint Table
