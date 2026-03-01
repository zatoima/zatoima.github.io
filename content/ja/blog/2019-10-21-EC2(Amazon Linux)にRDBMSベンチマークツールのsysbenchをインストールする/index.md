---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2(Amazon Linux)にRDBMSベンチマークツールのsysbenchをインストールする"
subtitle: ""
summary: " "
tags: ["AWS","EC2"]
categories: ["AWS","EC2"]
url: aws-ec2-sysbench-install-howto.html
date: 2019-10-21
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


### 実行コマンド

***

sysbench は EPEL のリポジトリに存在するので事前にインストールする必要がある。

```sh
sudo -s
wget https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-12.noarch.rpm
rpm -ivh epel-release-7-12.noarch.rpm
yum -y install epel-release

yum -y install sysbench
```



### 実行ログ

***

```sh
[root@donald-dev-ec2-bastin ec2-user]# wget https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-12.noarch.rpm
--2019-10-21 07:47:27--  https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-12.noarch.rpm
Resolving dl.fedoraproject.org (dl.fedoraproject.org)... 209.132.181.25, 209.132.181.23, 209.132.181.24
Connecting to dl.fedoraproject.org (dl.fedoraproject.org)|209.132.181.25|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15264 (15K) [application/x-rpm]
Saving to: ‘epel-release-7-12.noarch.rpm’

100%[==================================================================================================================================================>] 15,264      --.-K/s   in 0.1s    

2019-10-21 07:47:28 (119 KB/s) - ‘epel-release-7-12.noarch.rpm’ saved [15264/15264]

[root@donald-dev-ec2-bastin ec2-user]# ll
total 55692
-rw-r--r--  1 root     root        15264 Sep 18 12:56 epel-release-7-12.noarch.rpm
-rw-rw-r--  1 ec2-user ec2-user  4856388 Oct 16 02:34 function.zip
-rw-r--r--  1 root     root     51434432 Oct  8 04:05 oracle-instantclient18.3-basic-18.3.0.0.0-3.x86_64.rpm
-rw-r--r--  1 root     root       709700 Oct  8 04:08 oracle-instantclient18.3-sqlplus-18.3.0.0.0-3.x86_64.rpm
drwxrwxr-x  3 ec2-user ec2-user       18 Oct  8 04:23 oradiag_ec2-user
drwxrwxr-x 19 ec2-user ec2-user     4096 Oct 16 02:33 package
drwxrwxr-x  3 ec2-user ec2-user       21 Oct 16 00:45 venv
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# rpm -ivh epel-release-7-11.noarch.rpm 
error: open of epel-release-7-11.noarch.rpm failed: No such file or directory
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# rpm -ivh epel-release-7-12.noarch.rpm
warning: epel-release-7-12.noarch.rpm: Header V3 RSA/SHA256 Signature, key ID 352c64e5: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:epel-release-7-12                ################################# [100%]
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# yum -y install epel-release
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
epel/x86_64/metalink                                                                                                                                                 | 6.0 kB  00:00:00     
epel                                                                                                                                                                 | 5.4 kB  00:00:00     
(1/3): epel/x86_64/group_gz                                                                                                                                          |  90 kB  00:00:00     
(2/3): epel/x86_64/updateinfo                                                                                                                                        | 1.0 MB  00:00:00     
(3/3): epel/x86_64/primary_db                                                                                                                                        | 6.9 MB  00:00:00     
186 packages excluded due to repository priority protections
Package epel-release-7-12.noarch already installed and latest version
Nothing to do
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# 
[root@donald-dev-ec2-bastin ec2-user]# yum -y install sysbench
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
186 packages excluded due to repository priority protections
Resolving Dependencies
--> Running transaction check
---> Package sysbench.x86_64 0:1.0.17-2.el7 will be installed
--> Processing Dependency: libck.so.0()(64bit) for package: sysbench-1.0.17-2.el7.x86_64
--> Processing Dependency: libluajit-5.1.so.2()(64bit) for package: sysbench-1.0.17-2.el7.x86_64
--> Running transaction check
---> Package ck.x86_64 0:0.5.2-2.el7 will be installed
---> Package luajit.x86_64 0:2.0.4-3.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================================================================
 Package                                      Arch                                       Version                                             Repository                                Size
============================================================================================================================================================================================
Installing:
 sysbench                                     x86_64                                     1.0.17-2.el7                                        epel                                     152 k
Installing for dependencies:
 ck                                           x86_64                                     0.5.2-2.el7                                         epel                                      26 k
 luajit                                       x86_64                                     2.0.4-3.el7                                         epel                                     343 k

Transaction Summary
============================================================================================================================================================================================
Install  1 Package (+2 Dependent packages)

Total download size: 521 k
Installed size: 1.7 M
Downloading packages:
warning: /var/cache/yum/x86_64/2/epel/packages/ck-0.5.2-2.el7.x86_64.rpm: Header V3 RSA/SHA256 Signature, key ID 352c64e5: NOKEY
Public key for ck-0.5.2-2.el7.x86_64.rpm is not installed
(1/3): ck-0.5.2-2.el7.x86_64.rpm                                                                                                                                     |  26 kB  00:00:00     
(2/3): sysbench-1.0.17-2.el7.x86_64.rpm                                                                                                                              | 152 kB  00:00:00     
(3/3): luajit-2.0.4-3.el7.x86_64.rpm                                                                                                                                 | 343 kB  00:00:00     
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                       2.0 MB/s | 521 kB  00:00:00     
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
Importing GPG key 0x352C64E5:
 Userid     : "Fedora EPEL (7) <epel@fedoraproject.org>"
 Fingerprint: 91e9 7d7c 4a5e 96f1 7f3e 888f 6a2f aea2 352c 64e5
 Package    : epel-release-7-12.noarch (installed)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : luajit-2.0.4-3.el7.x86_64                                                                                                                                                1/3 
  Installing : ck-0.5.2-2.el7.x86_64                                                                                                                                                    2/3 
  Installing : sysbench-1.0.17-2.el7.x86_64                                                                                                                                             3/3 
  Verifying  : ck-0.5.2-2.el7.x86_64                                                                                                                                                    1/3 
  Verifying  : sysbench-1.0.17-2.el7.x86_64                                                                                                                                             2/3 
  Verifying  : luajit-2.0.4-3.el7.x86_64                                                                                                                                                3/3 

Installed:
  sysbench.x86_64 0:1.0.17-2.el7                                                                                                                                                            

Dependency Installed:
  ck.x86_64 0:0.5.2-2.el7                                                                    luajit.x86_64 0:2.0.4-3.el7                                                                   

Complete!
[root@donald-dev-ec2-bastin ec2-user]# 

```