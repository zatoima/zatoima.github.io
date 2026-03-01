---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing GoldenGate and Building a Replication Environment Between Databases"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-12c-18c-install-implement.html
date: 2019-03-29
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



We will build a replication environment between Oracle Databases using GoldenGate.

The steps to set up replication are as follows, but this article covers steps "1." and "2.":

1. GoldenGate installation

2. GoldenGate environment configuration

3. Data propagation


#### **Environment Configuration**

Due to hardware resource constraints, two databases are created on the same machine. We will build a replication environment between these two databases using GoldenGate.

|                          | Source                               | Target                               |
| ------------------------ | ------------------------------------ | ------------------------------------- |
| DB Version               | 11.2.0.4                             | 18c                                   |
| GoldenGate Version       | 12.2.0.1                             | 18.1.0.0.0                            |
| DB Name                  | db112s                               | db18s                                 |
| PDB Name                 | -                                    | db18p1                                |
| GoldenGate DB User       | ggs                                  | c##ggs                                |
| Propagation User         | ggtest                               | ggtest                                |
| GoldenGate Install Path  | /gg/gg1                              | /gg/gg2                               |
| Capture Process          | c11                                  | -                                     |
| Data Pump Process        | d11                                  | -                                     |
| Replicat Process         | -                                    | r11                                   |
| Capture Process Mode     | Integrated Mode<br />(Integrated Capture) | -                                |
| Replicat Process Mode    | -                                    | Integrated Mode<br />(Integrated Replicat) |
| Other                    | Single instance configuration        |                                       |



#### **Prerequisites**

1. Source and target databases are already installed
2. GoldenGate media files have been downloaded in advance



#### **GoldenGate Installation**

#### **Create GG_HOME**

In this example, we will perform a CUI-based installation. For a GUI-based installation, refer to the following Qiita article:

> GoldenGate Evangelism 2 - GoldenGate Installation - Qiita https://qiita.com/ch0c0bana0/items/a57debf29a8d907e9feb

```sh
su -
mkdir -p /gg/gg1
mkdir -p /gg/gg2
chmod -R 755 /gg
chown -R oracle:oinstall /gg
exit
```



#### **Installing GoldenGate 12cR2 (12.2.0.1)**

#### **Extract Media Files**

```sh
#Command
cd /home/oracle/software/goldengate/12.2.0.1/V100692-01
ls -l
unzip V100692-01.zip
```

```sh
#Execution result
[oracle@dbvgg V100692-01]$
[oracle@dbvgg V100692-01]$ cd /home/oracle/software/goldengate/12.2.0.1/V100692-01
[oracle@dbvgg V100692-01]$ ls -l
Total 464468
-rwxr-xr-x 1 oracle oinstall 475611228  Jul  7 19:15 2017 V100692-01.zip
[oracle@dbvgg V100692-01]$ unzip V100692-01.zip
Archive:  V100692-01.zip
   creating: fbo_ggs_Linux_x64_shiphome/
   creating: fbo_ggs_Linux_x64_shiphome/Disk1/
...omitted...
   creating: fbo_ggs_Linux_x64_shiphome/Disk1/response/
  inflating: fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
  inflating: OGG-12.2.0.1-README.txt
  inflating: OGG-12.2.0.1.1-ReleaseNotes.pdf
[oracle@dbvgg V100692-01]$
```



#### **Edit Response File for Silent Installation**

The marked (★) sections are the modifications. They need to be updated to match your environment.

```sh
cd ./fbo_ggs_Linux_x64_shiphome/Disk1/response
ls -l
vi oggcore.rsp
```

```sh
#oggcore.rsp modifications
####################################################################
## Copyright(c) Oracle Corporation 2014. All rights reserved.     ##
##                                                                ##
## Specify values for the variables listed below to customize     ##
## your installation.                                             ##
##                                                                ##
## Each variable is associated with a comment. The comment        ##
## can help to populate the variables with the appropriate        ##
## values.                                                        ##
##                                                                ##
## IMPORTANT NOTE: This file should be secured to have read       ##
## permission only by the oracle user or an administrator who     ##
## own this installation to protect any sensitive input values.   ##
##                                                                ##
####################################################################

#-------------------------------------------------------------------------------
# Do not change the following system generated value.
#-------------------------------------------------------------------------------
oracle.install.responseFileVersion=/oracle/install/rspfmt_ogginstall_response_schema_v12_1_2


################################################################################
##                                                                            ##
## Oracle GoldenGate installation option and details                          ##
##                                                                            ##
################################################################################

#-------------------------------------------------------------------------------
# Specify the installation option.
# Specify ORA12c for installing Oracle GoldenGate for Oracle Database 12c and
#         ORA11g for installing Oracle GoldenGate for Oracle Database 11g
#-------------------------------------------------------------------------------
INSTALL_OPTION=ORA11g ★<-

#-------------------------------------------------------------------------------
# Specify a location to install Oracle GoldenGate
#-------------------------------------------------------------------------------
SOFTWARE_LOCATION=/gg/gg1 ★<-

#-------------------------------------------------------------------------------
# Specify true to start the manager after installation.
#-------------------------------------------------------------------------------
START_MANAGER=false ★<-

#-------------------------------------------------------------------------------
# Specify a free port within the valid range for the manager process.
# Required only if START_MANAGER is true.
#-------------------------------------------------------------------------------
MANAGER_PORT=

#-------------------------------------------------------------------------------
# Specify the location of the Oracle Database.
# Required only if START_MANAGER is true.
#-------------------------------------------------------------------------------
DATABASE_LOCATION=


################################################################################
##                                                                            ##
## Specify details to Create inventory for Oracle installs                    ##
## Required only for the first Oracle product install on a system.            ##
##                                                                            ##
################################################################################

#-------------------------------------------------------------------------------
# Specify the location which holds the install inventory files.
# This is an optional parameter if installing on
# Windows based Operating System.
#-------------------------------------------------------------------------------
INVENTORY_LOCATION=

#-------------------------------------------------------------------------------
# Unix group to be set for the inventory directory.
# This parameter is not applicable if installing on
# Windows based Operating System.
#-------------------------------------------------------------------------------
UNIX_GROUP_NAME=

```



#### **Install GoldenGate**

```sh
cd /home/oracle/software/goldengate/12.2.0.1/V100692-01/fbo_ggs_Linux_x64_shiphome/Disk1
./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/12.2.0.1/V100692-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
```

```sh
#Execution result
[oracle@dbvgg Disk1]$ ./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/12.2.0.1/V100692-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
Starting Oracle Universal Installer...

Checking Temp space: must be greater than 120 MB.   Actual 28028MB    Passed
Checking swap space: must be greater than 150 MB.   Actual 7855MB    Passed
Preparing to launch Oracle Universal Installer from /tmp/OraInstall2019-03-29_05-24-01PM. Please wait...
The installation session logs are located at:
 /u01/app/oraInventory/logs/installActions2019-03-29_05-24-01PM.log
Oracle GoldenGate Core installation succeeded.
Check '/u01/app/oraInventory/logs/silentInstall2019-03-29_05-24-01PM.log' for more details.
Successfully Setup Software.

[oracle@dbvgg Disk1]$
```



#### **Update OPatch**

```sh
#OPatch update
cd /home/oracle/software/goldengate/12.2.0.1/p6880880
unzip p6880880_112000_Linux-x86-64.zip
cp -Rp ./OPatch/* /gg/gg1/OPatch/
/gg/gg1/OPatch/opatch version
```

```sh
#Execution result
[oracle@dbvgg p6880880]$ /gg/gg1/OPatch/opatch version
OPatch Version: 11.2.0.3.19

OPatch succeeded.
[oracle@dbvgg p6880880]$
```



#### **Apply GoldenGate Patch**

```sh
#OPatch update
export ORACLE_HOME=/gg/gg1
export PATH=$ORACLE_HOME/OPatch:$PATH

cd /home/oracle/software/goldengate/12.2.0.1/p26849940
unzip p26849940_12201170919_Linux-x86-64.zip
cd 26849940/
/gg/gg1/OPatch/opatch prereq CheckConflictAgainstOHWithDetail -ph ./
$ORACLE_HOME/OPatch/opatch apply -oh $ORACLE_HOME
$ORACLE_HOME/OPatch/opatch lspatches
$ORACLE_HOME/OPatch/opatch lsinventory

```

```sh
#Execution result
[oracle@dbvgg 26849940]$ $ORACLE_HOME/OPatch/opatch apply -oh $ORACLE_HOME

Oracle Interim Patch Installer version 11.2.0.3.19
Copyright (c) 2019, Oracle Corporation.  All rights reserved.


Oracle Home       : /gg/gg1
Central Inventory : /u01/app/oraInventory
   from           : /gg/gg1/oraInst.loc
OPatch version    : 11.2.0.3.19
OUI version       : 11.2.0.3.0
Log file location : /gg/gg1/cfgtoollogs/opatch/opatch2019-03-29_17-36-23PM_1.log

Verifying environment and performing prerequisite checks...
OPatch continues with these patches:   26849940

Do you want to proceed? [y|n]
y
User Responded with: Y
All checks passed.
...
Patch 26849940 successfully applied.
Log file location: /gg/gg1/cfgtoollogs/opatch/opatch2019-03-29_17-36-23PM_1.log

OPatch succeeded.
[oracle@dbvgg 26849940]$
[oracle@dbvgg 26849940]$ $ORACLE_HOME/OPatch/opatch lspatches
26849940;

OPatch succeeded.
[oracle@dbvgg 26849940]$
```



#### **Installing GoldenGate 18c (18.1.0.0.0)**

#### **Extract Media Files**

```sh
#Command
cd /home/oracle/software/goldengate/18.1.0.0/V980002-01
ls -l
unzip V980002-01.zip
```

#### **Edit Response File for Silent Installation**

The marked (★) sections are the modifications.

```sh
cd ./fbo_ggs_Linux_x64_shiphome/Disk1/response
ls -l
vi oggcore.rsp
```

Key changes:

```sh
INSTALL_OPTION=ORA18c ★<-
SOFTWARE_LOCATION=/gg/gg2 ★<-
START_MANAGER=false ★<-
```

#### **Install GoldenGate**

```sh
cd /home/oracle/software/goldengate/18.1.0.0/V980002-01/fbo_ggs_Linux_x64_shiphome/Disk1
./runInstaller -silent -nowait -responseFile /home/oracle/software/goldengate/18.1.0.0/V980002-01/fbo_ggs_Linux_x64_shiphome/Disk1/response/oggcore.rsp
```



#### **Create Trail File Storage Directories**

"/gg/gg1/c11" is the storage directory for Local Trail files generated by the source-side Capture process, and "/gg/gg2/d11" is the storage directory for Remote Trail files generated by Data Pump on the target side.

```sh
mkdir -p /gg/gg1/dirdat/c11 #Storage directory for Local Trail
mkdir -p /gg/gg2/dirdat/d11 #Storage directory for Remote Trail
```



#### **DB Environment Changes (Source Side)**

#### **Create Tablespace**

```sql
. /home/oracle/.oraenv_db112s --load environment variables
sqlplus / as sysdba
create tablespace ggdata datafile '/u01/app/oracle/oradata/DB112S/datafile/ggdata.dbf' size 5G;
```



#### **Create Propagation and GoldenGate Management Users**

```sql
CREATE USER ggs IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;
CREATE USER ggtest IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;

GRANT dba TO ggs;
GRANT dba TO ggtest;
exec dbms_goldengate_auth.grant_admin_privilege('GGS');
```



#### **Change Initialization Parameters / Set Minimum Supplemental Logging**

```sql
-- Pre-check
show parameter enable_goldengate_replication
select name,supplemental_log_data_min from v$database;
select log_mode from v$database;

-- Change initialization parameters
alter system set enable_goldengate_replication=true scope=both;
alter system set streams_pool_size=1250M scope=both SID='*'; -- Integrated Capture requirement

-- Set minimum supplemental logging
alter database add supplemental log data;
alter system switch logfile;

-- Verify changes
show parameter enable_goldengate_replication
select name,supplemental_log_data_min from v$database;
select log_mode from v$database;
exit
```



#### **DB Environment Changes (Target Side)**

#### **Create Tablespace**

```sql
. /home/oracle/.oraenv_db18s --load environment variables
sqlplus / as sysdba
create tablespace ggdata datafile '/u01/app/oracle/oradata/DB18S/ggdata.dbf' size 1G;
alter session set container=db18p1;
create tablespace ggdata datafile '/u01/app/oracle/oradata/DB18S/db18p1/ggdata.dbf' size 5G;

```



#### **Create Propagation and GoldenGate Management Users (Target)**

```sql
alter session set container=cdb$root;
show con_name
CREATE USER c##ggs IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;
alter session set container=db18p1;
show con_name
CREATE USER ggtest IDENTIFIED BY oracle DEFAULT TABLESPACE ggdata;

alter session set container=cdb$root;
GRANT DBA TO c##ggs container=all;
exec dbms_goldengate_auth.grant_admin_privilege('C##GGS');

alter session set container=db18p1;
GRANT DBA TO ggtest;
exec dbms_goldengate_auth.grant_admin_privilege('C##GGS');
```



#### **GoldenGate Environment Configuration**

#### **Create Subdirectories Under GG_HOME**

Supplemental logging is configured on the source side.

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1
./ggsci
create subdirs
exit

cd /gg/gg2
./ggsci
create subdirs
exit
```



#### **Configure Schema-Level Supplemental Logging**

Supplemental logging is configured on the source side.

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1
./ggsci
dblogin userid ggs@db112s, password oracle
add schematrandata ggtest
```



#### **Create GG Parameter Files**

GoldenGate parameter files must be created for each process. GLOBALS and MGR parameters exist on both source and target sides, so they need to be created on both sides.

#### **GLOBALS Parameter (Source Side)**

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1

./ggsci
EDIT PARAMS GLOBALS

#Specify the following in vi editor:
SYSLOG NONE
GGSCHEMA ggs
NODUPMSGSUPPRESSION

view params GLOBALS
```



#### **MGR Parameter (Source Side)**

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1

./ggsci
EDIT PARAMS MGR

# MGR file settings
PORT 7809

AUTOSTART EXTRACT c11
AUTOSTART EXTRACT d11
AUTORESTART EXTRACT c11, RETRIES 2, WAITMINUTES 1, RESETMINUTES 60
AUTORESTART EXTRACT d11, RETRIES 5, WAITMINUTES 1, RESETMINUTES 60

-- Trail file maintenance settings
PURGEOLDEXTRACTS ./dirdat/c11/*,  USECHECKPOINTS, MINKEEPDAYS 1

view params GLOBALS

```



#### **Capture Parameter (Source Side)**

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1

./ggsci
EDIT PARAMS C11

# CAPTURE file settings
EXTRACT c11
USERID ggs@db112s,PASSWORD oracle
EXTTRAIL ./dirdat/c11/lt
CACHEMGR CACHESIZE 4GB
DISCARDFILE ./dirrpt/c11.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY
DDL INCLUDE ALL
DDLOPTIONS CAPTUREGLOBALTEMPTABLE,REPORT
TRANLOGOPTIONS INTEGRATEDPARAMS (MAX_SGA_SIZE 1250, PARALLELISM 2)

TABLE ggtest.* ;

view params MGR

```



#### **Data Pump Parameter (Source Side)**

Since this is replication between two databases on the same host, "localhost" is set for RMTHOST. In a normal scenario, the hostname or IP address of the target server would be specified.

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1

./ggsci
EDIT PARAMS d11

# Data Pump file settings
EXTRACT d11
PASSTHRU
RMTHOST localhost,  MGRPORT 7810
RMTTRAIL ./dirdat/d11/rt

TABLE ggtest.*;

view params c11

```



#### **GLOBALS Parameter (Target Side)**

```sh
. /home/oracle/.oraenv_db18s --load environment variables
cd /gg/gg2

./ggsci
EDIT PARAM GLOBALS

GGSCHEMA c##ggs
NODUPMSGSUPPRESSION

view params GLOBALS

```



#### **MGR Parameter (Target Side)**

```sh
. /home/oracle/.oraenv_db18s --load environment variables
cd /gg/gg2

./ggsci
EDIT PARAMS MGR

# MGR file settings
PORT 7810

AUTOSTART REPLICAT r11
AUTORESTART REPLICAT r11, RETRIES 2, WAITMINUTES 1, RESETMINUTES 60

-- Trail file maintenance settings
PURGEOLDEXTRACTS ./dirdat/d11/*,  USECHECKPOINTS, MINKEEPDAYS 1


```



#### **Replicat Parameter (Target Side)**

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg2

./ggsci
EDIT PARAMS R11

REPLICAT r11
USERID c##ggs@db18p1, PASSWORD oracle
DBOPTIONS INTEGRATEDPARAMS(PARALLELISM 4,MAX_PARALLELISM 4)

DISCARDFILE ./dirrpt/r11.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY

DDL INCLUDE ALL
DDLOPTIONS CAPTUREGLOBALTEMPTABLE,REPORT
REPORTCOUNT EVERY 10 MINUTES, RATE

BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;

```



#### **Create GoldenGate Processes**

#### **Create Source-Side Processes**

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1
./ggsci

#DB login
dblogin userid ggs@db112s,password oracle

#Create and add Capture process
REGISTER EXTRACT c11 DATABASE
add extract c11, integrated,tranlog, begin now
add exttrail  ./dirdat/c11/lt, extract c11, megabytes 500

#Create and add Data Pump process
add extract d11, exttrailsource ./dirdat/c11/lt
add rmttrail ./dirdat/d11/rt, extract d11

#Verify
info all
```



#### **Create Target-Side Processes**

When the Replicat applies to a PDB, the connection descriptor specified in the dblogin command must point to the PDB (not CDB$ROOT).

Also, the register command is required for Integrated Capture, but it is not needed for Integrated Replicat (it is issued internally).

```sh
. /home/oracle/.oraenv_db18s --load environment variables
cd /gg/gg2
./ggsci

#DB login
dblogin userid c##ggs@db18p1,password oracle

#Create Replicat process
ADD REPLICAT r11,integrated EXTTRAIL ./dirdat/d11/rt

#Check status
info all
```



#### **Start GoldenGate Processes**

The Data Pump process on the source side communicates with the MGR process on the target side. Therefore, the target-side MGR process must be started first, so start from the target side.

#### **Start Target-Side Processes**

```sh
. /home/oracle/.oraenv_db18s --load environment variables
cd /gg/gg1
./ggsci

#Start command
start mgr

# Since autostart is configured in mgr parameters, starting the replicat process separately is not needed.
#start r11

#Check status
info all
```



#### **Start Source-Side Processes**

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1
./ggsci

#Start command
start mgr
# Since autostart is configured in mgr parameters, starting capture and data pump processes separately is not needed.
# start c11
# start d11

#Check status
info all
```



#### **Appendix**

#### **Handling OGG-02912 Error**

When using **DB 11.2 with GG 12.2 (Integrated Capture)**, OGG-02912 may occur at initial startup causing the Capture process to ABEND. (This depends on the PSU/BP applied.)

This error occurs because the Trail file format changed starting from Oracle GoldenGate 12.2. (It occurs when the LogMiner-related functions on the database side are not compatible.)

```text
ERROR OGG-02912 Patch 17030189 is required on your Oracle mining database for trail format RELEASE 12.2 or later.
```

If this error occurs, you can resolve it either by applying "Patch 17030189" as mentioned in the error message, or by running "prvtlmpg.plb" located under the GG_HOME directory.

```sh
. /home/oracle/.oraenv_db112s --load environment variables
cd /gg/gg1
sqlplus / as sysdba
@prvtlmpg.plb
```
