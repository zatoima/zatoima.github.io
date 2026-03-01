---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Verifying the Behavior of GoldenGate 12.3's New Parallel Replicat Feature"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-parallel-replicat-try.html
date: 2019-04-29
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

In the previous article, I summarized Parallel Replicat.

In this article, I will check how to set up, view processes, and examine log output using actual hardware.

The process to be created this time is an "Integrated Parallel Replicat". Note that "Non-Integrated Parallel Replicat" requires a different procedure.

#### **Creating an Integrated Parallel Replicat Process**

Add the "parallel" clause to the process. When using integrated mode, you must also specify the "checkpointtable" clause, which was not needed previously.

```sh
GGSCI (dbvm1) 8> dblogin userid c##ggs@db18p1sv,password oracle
Successfully logged into database DB18P1.

GGSCI (dbvm1 as c##ggs@db18c2/DB18P1) 9> ADD REPLICAT r99,integrated,parallel EXTTRAIL
./dirdat/d11/rt checkpointtable c##ggs.ggckpt
REPLICAT (Parallel) added.

GGSCI (dbvm1 as c##ggs@db18c2/DB18P1) 11> info r99
REPLICAT R99 Initialized 2018-11-03 17:17 Status STOPPED
INTEGRATED
Parallel
Checkpoint Lag 00:00:00 (updated 00:00:08 ago)
Log Read Checkpoint File ./dirdat/d11/rt000000000
First Record RBA 0

```

#### **Integrated Parallel Replicat Parameters**

In this parameter file, `MAP_PARALLELISM`, `MIN_APPLY_PARALLELISM`, and `MAX_APPLY_PARALLELISM` are parameters specific to Integrated Parallel Replicat.

```sh
REPLICAT r99
USERID c##ggs@db18p1, PASSWORD oracle

DISCARDFILE ./dirrpt/r99.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY

MAP_PARALLELISM 3
MIN_APPLY_PARALLELISM 2
MAX_APPLY_PARALLELISM 8
-- BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;

```

#### **ggserr.log When Starting Integrated Parallel Replicat**

```sh
2018-11-03T17:18:08.892+0900 INFO OGG-00987 Oracle GoldenGate Command Interpreter for Oracle: GGSCI command (oracle): start r99.
2018-11-03T17:18:08.905+0900 INFO OGG-00963 Oracle GoldenGate Manager for Oracle, mgr.prm: Command received from GGSCI on host [192.168.56.127]:47418 (START REPLICAT R99 ).
2018-11-03T17:18:08.934+0900 INFO OGG-00975 Oracle GoldenGate Manager for Oracle, mgr.prm: REPLICAT R99 starting.
2018-11-03T17:18:09.170+0900 INFO OGG-03059 Oracle GoldenGate Delivery for Oracle, r99.prm: Operating system character set identified as UTF-8.
2018-11-03T17:18:09.170+0900 INFO OGG-02695 Oracle GoldenGate Delivery for Oracle, r99.prm: ANSI SQL parameter syntax is usedfor parameter parsing.
2018-11-03T17:18:09.244+0900 INFO OGG-01360 Oracle GoldenGate Delivery for Oracle, r99.prm: REPLICAT is running in Parallel Integrated mode.
2018-11-03T17:18:11.117+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Applier with pid 32,269.
2018-11-03T17:18:11.125+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Applier with pid 32,270.
2018-11-03T17:18:11.137+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Mapper with pid 32,272.
2018-11-03T17:18:11.539+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Applier with pid 32,271.
2018-11-03T17:18:11.668+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Mapper with pid 32,285.
2018-11-03T17:18:11.668+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Applier with pid 32,286.
2018-11-03T17:18:11.766+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Mapper with pid 32,287.
2018-11-03T17:18:11.766+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Applier with pid 32,288.
2018-11-03T17:18:12.298+0900 INFO OGG-00995 Oracle GoldenGate Delivery for Oracle, r99.prm: REPLICAT R99A00 starting.

```

#### **ggserr.log While Integrated Parallel Replicat Is Running**

Applier processes increase and decrease according to load. The number of Applier processes specified by `MIN_APPLY_PARALLELISM` is always maintained.

```sh
2018-11-03T17:46:44.808+0900 INFO OGG-06067 Oracle GoldenGate Delivery for Oracle, r99.prm: Spawned Applier with pid 17,035.
2018-11-03T17:46:48.465+0900 INFO OGG-02530 Oracle GoldenGate Delivery for Oracle, r99.prm.backup: Integrated replicat successfully attached to inbound server OGG$R99.
2018-11-03T17:51:54.641+0900 INFO OGG-06073 Oracle GoldenGate Delivery for Oracle, r99.prm: Removed Applier with pid 15,777.
2018-11-03T17:53:09.738+0900 INFO OGG-06073 Oracle GoldenGate Delivery for Oracle, r99.prm: Removed Applier with pid 15,780.
2018-11-03T17:54:24.872+0900 INFO OGG-06073 Oracle GoldenGate Delivery for Oracle, r99.prm: Removed Applier with pid 15,782.
2018-11-03T17:55:39.986+0900 INFO OGG-06073 Oracle GoldenGate Delivery for Oracle, r99.prm: Removed Applier with pid 15,783.
```

#### **OS Process Information for Integrated Parallel Replicat**

From the OS level, you can confirm that processes named "R99Axx" and "R99Mxx" are running.

```sh
oracle 32190 25849 0 17:17 pts/2 00:00:00 tail -f ggserr.log
oracle 32259 26592 1 17:18 ? 00:00:01 /gg/gg181/replicat PARAMFILE /gg/gg181/dirprm/r99.prm REPORTFILE /gg/gg181/dirrpt/R99.rpt PROCESSID R99
oracle 32269 32259 0 17:18 ? 00:00:00 /gg/gg181/replicat PARAMFILE /gg/gg181/dirprm/r99.prm REPORTFILE /gg/gg181/dirrpt/R99.rpt PROCESSID R99A00 THREADID 0 PARAMCRC 3975171
oracle 32270 32259 0 17:18 ? 00:00:00 /gg/gg181/replicat PARAMFILE /gg/gg181/dirprm/r99.prm REPORTFILE /gg/gg181/dirrpt/R99.rpt PROCESSID R99A01 THREADID 1 PARAMCRC 3975171
oracle 32271 32259 0 17:18 ? 00:00:00 /gg/gg181/replicat PARAMFILE /gg/gg181/dirprm/r99.prm REPORTFILE /gg/gg181/dirrpt/R99.rpt PROCESSID R99A02 THREADID 2 PARAMCRC 3975171
oracle 32272 32259 0 17:18 ? 00:00:00 /gg/gg181/replicat PARAMFILE /gg/gg181/dirprm/r99.prm REPORTFILE /gg/gg181/dirrpt/R99.rpt PROCESSID R99M00 THREADID 0 PARAMCRC 3975171
oracle 32275 27681 0 17:18 ? 00:00:00 oracledb112n1 (DESCRIPTION=(LOCAL=YES)(ADDRESS=(PROTOCOL=beq)))
root 32277 2 0 17:18 ? 00:00:00 [kworker/u8:2]
```
