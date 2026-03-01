---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Retrieving Parameter Information for Running GoldenGate Processes"
subtitle: ""
summary: " "
tags: ["GoldenGate"]
categories: ["GoldenGate"]
url: goldengate-gg-process-getparaminfo.html
date: 2019-04-06
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



How to retrieve parameters for running processes. Note that both intentionally set parameters and other default parameters are included in the output.

The manual is available here:

> https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-6D0E4481-BB8A-4B3C-B8E9-2305BC01928E.htm
>
> GETPARAMINFO
>
> GETPARAMINFO queries the runtime parameter values of running instances such as Extract, Replicat, and Manager. You can query one or all parameters and send the output to the console or a text file.

#### MGR Process

```sql
GGSCI (node1.oracle12c.jp) 1> send MGR getparaminfo

Sending GETPARAMINFO request to MANAGER ...

GLOBALS

checkpointtable                      : c##ggs.ggs_ckpt
enablemonitoring                     : <enabled>

/u01/ogg_1/dirprm/mgr.prm

port                                 : 7809
purgeoldextracts                     : /u01/ogg_1/dirdat

Default Values

ptkcaptureprocstats                  : <enabled>
ptkmonitorfrequency                  : 1
ptkprocesscheckfrequency             : 1
checkminutes                         : 10
monitoring_heartbeat_timeout         : 10
  usecheckpoints                     : <enabled>
  minkeepfiles                       : 1
  frequencyminutes                   : 60
repobackupdir                        : dirbkup
repobackupfrequency                  : 0
reponumbackupsbeforefullbackup       : 3


```

#### Capture Process

```sql
GGSCI (node1.oracle12c.jp) 2> send cap01 getparaminfo

Sending GETPARAMINFO request to EXTRACT CAP01 ...

GLOBALS

checkpointtable                      : c##ggs.ggs_ckpt
enablemonitoring                     : <enabled>

/u01/ogg_1/dirprm/cap01.prm

extract                              : CAP01
logallsupcols                        : <enabled>
setenv                               : (ORACLE_HOME=/u01/app/oracle/product/12.1.0/dbhome_1)
setenv                               : (ORACLE_SID=cdb1)
userid                               : c##ggs
  password                           : *******
updaterecordformat                   : COMPACT
ddl                                  : <enabled>
  include                            : <enabled>
                                     : <enabled>
    mapped                           : <enabled>
                                     : <enabled>
    sourcecatalog                    : p_pdb1
                                     : p_pdb2
exttrail                             : ./dirdat/local/lt
table                                : p_pdb1.oracle.*
table                                : p_pdb2.oracle.*
sourcecatalog                        : p_pdb1
table                                : oracle.*
sourcecatalog                        : p_pdb2

Default Values

deletelogrecs                        : <enabled>
fetchoptions                         :
  userowid                           : <enabled>
  usekey                             : <enabled>
  missingrow                         : ALLOW
  usesnapshot                        : <enabled>
  uselatestversion                   : <enabled>
  maxfetchstatements                 : 100
  usediagnostics                     : <disabled>
  detaileddiagnostics                : <disabled>
  diagnosticsonall                   : <disabled>
  nosuppressduplicates               : <enabled>
flushsecs                            : 1
passthrumessages                     : <enabled>

```

#### Data Pump Process

```sql
GGSCI (node1.oracle12c.jp) 3> send dp01 getparaminfo

Sending GETPARAMINFO request to EXTRACT DP01 ...

GLOBALS

checkpointtable                      : c##ggs.ggs_ckpt
enablemonitoring                     : <enabled>

/u01/ogg_1/dirprm/dp01.prm

extract                              : DP01
passthru                             : <enabled>
rmthost                              : node1.oracle12c.jp
  mgrport                            : 7810
rmttrail                             : /u01/ogg_2/dirdat/remote/rt
table                                : p_pdb1.oracle.*
table                                : p_pdb2.oracle.*

Default Values

deletelogrecs                        : <enabled>
fetchoptions                         :
  userowid                           : <enabled>
  usekey                             : <enabled>
  missingrow                         : ALLOW
...
```

#### Replicat Process

```sql
GGSCI (node1.oracle12c.jp) 1> send rep01 getparaminfo

Sending GETPARAMINFO request to REPLICAT REP01 ...

GLOBALS

checkpointtable                      : c##ggs.ggs_ckpt
enablemonitoring                     : <enabled>

/u01/ogg_2/dirprm/rep01.prm

replicat                             : REP01
setenv                               : ("ORACLE_HOME=/u01/app/oracle/product/12.1.0/dbhome_1")
setenv                               : (ORACLE_SID=cdb2)
userid                               : c##ggs@s_pdb1
  password                           : *******
assumetargetdefs                     : <enabled>
discardfile                          : ./dirrpt/REP01.DSC
  purge                              : <enabled>
map                                  : p_pdb1.oracle.*
  target                             : s_pdb1.oracle.*

Default Values

allownoopupdates                     : <disabled>
applynoopupdates                     : <disabled>
auditreps                            : <enabled>
deferapplyinterval                   : 0 FILESEQNO
grouptransops                        : 50
maxdiscardrecs                       : 0
maxsqlstatements                     : 250
ptkcapturebatchsql                   : <enabled>
ptkirstatsfrequency                  : 10
restartcollisions                    : <disabled>
retrydelay                           : 60
warnrate                             : 100
...

```



