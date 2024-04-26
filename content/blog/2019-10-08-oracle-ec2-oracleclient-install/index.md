---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2にOracle ClientをインストールしてRDS(Oracle)に接続する"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "Oracle"]
categories: ["AWS", "EC2", "Oracle"]
url: oracle-ec2-oracleclient-install.html
date: 2019-10-08
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


## 手順

### 1. Oracle Clientのbasicとsqlplusをインストール

#### basic

```sh
sudo -s
#rpmファイルをcurlコマンドで取得
curl -o oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm
#rpmファイルをインストール
yum -y localinstall oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm
```

#### sqlplus

```sh
sudo -s
#rpmファイルをcurlコマンドで取得
curl -o oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm
#rpmファイルをインストール
yum -y localinstall oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm
```

### 環境変数の設定

```sh
export LD_LIBRARY_PATH=/usr/lib/oracle/18.3/client64/lib:$LD_LIBRARY_PATH
export PATH=/usr/lib/oracle/18.3/client64/bin:$PATH
```

### 接続

```sql
#sqlplus 'user_name@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=dns_name)(PORT=port))(CONNECT_DATA=(SID=database_name)))'

sqlplus 'oracle@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db112s.cm678nkt5thr.ap-northeast-1.rds.amazonaws.com)(PORT=1521))(CONNECT_DATA=(SID=oradb)))'
```

> Oracle データベースエンジンを実行している DB インスタンスへの接続 - Amazon Relational Database Service https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/USER_ConnectToOracleInstance.html



## 実行ログ

```sh
[root@ip-10-0-0-170 ec2-user]# curl -o oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 49.0M  100 49.0M    0     0  16.1M      0  0:00:03  0:00:03 --:--:-- 16.1M
[root@ip-10-0-0-170 ec2-user]# 
[root@ip-10-0-0-170 ec2-user]# yum -y localinstall oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
Examining oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm: oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64
Marking oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package oracle-instantclient18.3-basic.x86_64 0:18.3.0.0.0-3 will be installed
--> Finished Dependency Resolution
amzn2-core/2/x86_64                                                                                                                                                  | 2.4 kB  00:00:00     

Dependencies Resolved

============================================================================================================================================================================================
 Package                                           Arch                      Version                           Repository                                                              Size
============================================================================================================================================================================================
Installing:
 oracle-instantclient18.3-basic                    x86_64                    18.3.0.0.0-3                      /oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64                    220 M

Transaction Summary
============================================================================================================================================================================================
Install  1 Package

Total size: 220 M
Installed size: 220 M
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64                                                                                                                       1/1 
  Verifying  : oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64                                                                                                                       1/1 

Installed:
  oracle-instantclient18.3-basic.x86_64 0:18.3.0.0.0-3                                                                                                                                      

Complete!
[root@ip-10-0-0-170 ec2-user]# 
[root@ip-10-0-0-170 ec2-user]# 
[root@ip-10-0-0-170 ec2-user]# 
[root@ip-10-0-0-170 ec2-user]# curl -o oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  693k  100  693k    0     0   379k      0  0:00:01  0:00:01 --:--:--  379k
[root@ip-10-0-0-170 ec2-user]# 
[root@ip-10-0-0-170 ec2-user]# 
[root@ip-10-0-0-170 ec2-user]# yum -y localinstall oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
Examining oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm: oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64
Marking oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package oracle-instantclient18.3-sqlplus.x86_64 0:18.3.0.0.0-3 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================================================================
 Package                                            Arch                     Version                          Repository                                                               Size
============================================================================================================================================================================================
Installing:
 oracle-instantclient18.3-sqlplus                   x86_64                   18.3.0.0.0-3                     /oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64                   3.1 M

Transaction Summary
============================================================================================================================================================================================
Install  1 Package

Total size: 3.1 M
Installed size: 3.1 M
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64                                                                                                                     1/1 
  Verifying  : oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64                                                                                                                     1/1 

Installed:
  oracle-instantclient18.3-sqlplus.x86_64 0:18.3.0.0.0-3                                                                                                                                    

Complete!
[root@ip-10-0-0-170 ec2-user]# 

[ec2-user@ip-10-0-0-170 ~]$ export LD_LIBRARY_PATH=/usr/lib/oracle/18.3/client64/lib:$LD_LIBRARY_PATH
[ec2-user@ip-10-0-0-170 ~]$ 
[ec2-user@ip-10-0-0-170 ~]$ 
[ec2-user@ip-10-0-0-170 ~]$ export PATH=/usr/lib/oracle/18.3/client64/bin:$PATH
[ec2-user@ip-10-0-0-170 ~]$ 
[ec2-user@ip-10-0-0-170 ~]$ sqlplus 'oracle@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db112s.cm678nkt5thr.ap-northeast-1.rds.amazonaws.com)(PORT=1521))(CONNECT_DATA=(SID=oradb)))'

SQL*Plus: Release 18.0.0.0.0 - Production on Tue Oct 8 04:30:33 2019
Version 18.3.0.0.0

Copyright (c) 1982, 2018, Oracle.  All rights reserved.

Enter password: 

Connected to:
Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, Oracle Label Security, OLAP, Data Mining
and Real Application Testing options

SQL> 
SQL> 

```

## 参考

> [Oracle Cloud][AWS] EC2にOracle ClientをインストールしてOCI Database(DBaaS)に接続してみた - IT Edge Blog https://itedge.stars.ne.jp/oracle-cloud-ec2-dbaas/
>
> Oracle データベースエンジンを実行している DB インスタンスへの接続 - Amazon Relational Database Service https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/USER_ConnectToOracleInstance.html
