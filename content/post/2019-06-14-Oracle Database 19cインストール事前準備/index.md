---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Database 19cインストール事前準備"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-pre-install-19c.html
date: 2019-06-14
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


#### はじめに

------

前回の記事でインストールの前提条件であるOracle Linux7.6をインストールしたので、今回は続きをやっていきます。DBインストール、DB構築の事前準備です。

Oracle Database 19c for Linuxのインストールガイドはこちらです。

> Oracle Database Databaseインストレーション・ガイド, 19c for Linux https://docs.oracle.com/cd/F19136_01/ladbi/index.html

#### ホスト名の変更

------

```sh
#ホスト名の変更
hostnamectl set-hostname dbsrv.oracle.jp
```

 ※セッションを抜けて再度ログインする

```sh
[root@localhost ~]# hostnamectl set-hostname dbsrv.oracle.jp
[root@localhost ~]# 
[root@localhost ~]# echo $?
0
[root@localhost ~]# 
```

#### ファイアーウォールの停止

------

```sh
#ファイアーウォールを停止
systemctl status firewalld
systemctl stop firewalld
systemctl status firewalld
#ファイアーウォール停止を恒久化
systemctl disable firewalld
systemctl status firewalld
```

```sh
[root@localhost ~]# 
[root@localhost ~]# systemctl status firewalld
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
   Active: active (running) since 木 2019-06-13 16:41:42 JST; 7min ago
     Docs: man:firewalld(1)
 Main PID: 3423 (firewalld)
    Tasks: 2
   CGroup: /system.slice/firewalld.service
           └─3423 /usr/bin/python -Es /usr/sbin/firewalld --nofork --nopid

 6月 13 16:41:40 localhost.localdomain systemd[1]: Starting firewalld - dynamic firewall daemon...
 6月 13 16:41:42 localhost.localdomain systemd[1]: Started firewalld - dynamic firewall daemon.
[root@localhost ~]# 
[root@localhost ~]# systemctl stop firewalld
[root@localhost ~]# echo $?
0
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# systemctl status firewalld
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
   Active: inactive (dead) since 木 2019-06-13 16:49:06 JST; 4s ago
     Docs: man:firewalld(1)
  Process: 3423 ExecStart=/usr/sbin/firewalld --nofork --nopid $FIREWALLD_ARGS (code=exited, status=0/SUCCESS)
 Main PID: 3423 (code=exited, status=0/SUCCESS)

 6月 13 16:41:40 localhost.localdomain systemd[1]: Starting firewalld - dynamic firewall daemon...
 6月 13 16:41:42 localhost.localdomain systemd[1]: Started firewalld - dynamic firewall daemon.
 6月 13 16:49:05 dbsrv.oracle.jp systemd[1]: Stopping firewalld - dynamic firewall daemon...
 6月 13 16:49:06 dbsrv.oracle.jp systemd[1]: Stopped firewalld - dynamic firewall daemon.
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# systemctl disable firewalld
Removed symlink /etc/systemd/system/multi-user.target.wants/firewalld.service.
Removed symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.
[root@localhost ~]# 
[root@localhost ~]# echo $?
0
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# 
[root@localhost ~]# systemctl status firewalld
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
     Docs: man:firewalld(1)

 6月 13 16:41:40 localhost.localdomain systemd[1]: Starting firewalld - dynamic firewall daemon...
 6月 13 16:41:42 localhost.localdomain systemd[1]: Started firewalld - dynamic firewall daemon.
 6月 13 16:49:05 dbsrv.oracle.jp systemd[1]: Stopping firewalld - dynamic firewall daemon...
 6月 13 16:49:06 dbsrv.oracle.jp systemd[1]: Stopped firewalld - dynamic firewall daemon.
[root@localhost ~]# 
```

#### SELinuxの無効化

------

```sh
-- SELinuxの無効化
vi /etc/selinux/config
cat /etc/selinux/config
[root@localhost ~]# cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
#SELINUX=enforcing
SELINUX=disabled ★←disabledに変更
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted 
```

#### 「oracle-database-preinstall-19c」パッケージの実行

------

yumでパッケージをインストールします。

```sh
yum install -y oracle-database-preinstall-19c
```

```sh
[oracle@dbsrv ~]$ su -
パスワード:
最終ログイン: 2019/06/13 (木) 17:10:03 JST日時 pts/0
[root@dbsrv ~]# yum install -y oracle-database-preinstall-19c
読み込んだプラグイン:langpacks, ulninfo
ol7_UEKR5                                                                                                                                                            | 2.5 kB  00:00:00     
ol7_latest                                                                                                                                                           | 2.7 kB  00:00:00     
(1/5): ol7_UEKR5/x86_64/updateinfo                                                                                                                                   |  27 kB  00:00:00     
(2/5): ol7_latest/x86_64/group                                                                                                                                       | 810 kB  00:00:00     
(3/5): ol7_UEKR5/x86_64/primary_db                                                                                                                                   | 3.9 MB  00:00:00     
(4/5): ol7_latest/x86_64/updateinfo                                                                                                                                  | 938 kB  00:00:01     
(5/5): ol7_latest/x86_64/primary_db                                                                                                                                  |  24 MB  00:00:01     
依存性の解決をしています
--> トランザクションの確認を実行しています。
---> パッケージ oracle-database-preinstall-19c.x86_64 0:1.0-1.el7 を インストール
--> 依存性の処理をしています: ksh のパッケージ: oracle-database-preinstall-19c-1.0-1.el7.x86_64
--> 依存性の処理をしています: libaio-devel のパッケージ: oracle-database-preinstall-19c-1.0-1.el7.x86_64
--> トランザクションの確認を実行しています。
---> パッケージ ksh.x86_64 0:20120801-139.0.1.el7 を インストール
---> パッケージ libaio-devel.x86_64 0:0.3.109-13.el7 を インストール
--> 依存性解決を終了しました。

依存性を解決しました

============================================================================================================================================================================================
 Package                                                   アーキテクチャー                  バージョン                                         リポジトリー                           容量
============================================================================================================================================================================================
インストール中:
 oracle-database-preinstall-19c                            x86_64                            1.0-1.el7                                          ol7_latest                             18 k
依存性関連でのインストールをします:
 ksh                                                       x86_64                            20120801-139.0.1.el7                               ol7_latest                            883 k
 libaio-devel                                              x86_64                            0.3.109-13.el7                                     ol7_latest                             12 k

トランザクションの要約
============================================================================================================================================================================================
インストール  1 パッケージ (+2 個の依存関係のパッケージ)

総ダウンロード容量: 913 k
インストール容量: 3.2 M
Downloading packages:
警告: /var/cache/yum/x86_64/7Server/ol7_latest/packages/libaio-devel-0.3.109-13.el7.x86_64.rpm: ヘッダー V3 RSA/SHA256 Signature、鍵 ID ec551f03: NOKEY   ]  0.0 B/s |    0 B  --:--:-- ETA 
libaio-devel-0.3.109-13.el7.x86_64.rpm の公開鍵がインストールされていません
(1/3): libaio-devel-0.3.109-13.el7.x86_64.rpm                                                                                                                        |  12 kB  00:00:00     
(2/3): ksh-20120801-139.0.1.el7.x86_64.rpm                                                                                                                           | 883 kB  00:00:00     
(3/3): oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm                                                                                                           |  18 kB  00:00:00     
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
合計                                                                                                                                                        2.0 MB/s | 913 kB  00:00:00     
file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle から鍵を取得中です。
Importing GPG key 0xEC551F03:
 Userid     : "Oracle OSS group (Open Source Software group) <build@oss.oracle.com>"
 Fingerprint: 4214 4123 fecf c55b 9086 313d 72f9 7b74 ec55 1f03
 Package    : 7:oraclelinux-release-7.6-1.0.15.el7.x86_64 (@anaconda/7.6)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  インストール中          : ksh-20120801-139.0.1.el7.x86_64                                   1/3 
  インストール中          : libaio-devel-0.3.109-13.el7.x86_64                                2/3 
  インストール中          : oracle-database-preinstall-19c-1.0-1.el7.x86_64                   3/3 
  検証中                  : libaio-devel-0.3.109-13.el7.x86_64                               1/3 
  検証中                  : ksh-20120801-139.0.1.el7.x86_64                                  2/3 
  検証中                  : oracle-database-preinstall-19c-1.0-1.el7.x86_64                  3/3 

インストール:
  oracle-database-preinstall-19c.x86_64 0:1.0-1.el7                                                                                                                                         

依存性関連をインストールしました:
  ksh.x86_64 0:20120801-139.0.1.el7                                                           libaio-devel.x86_64 0:0.3.109-13.el7                                                          

完了しました!
[root@dbsrv ~]# 

```

「/etc/sysctl.conf」が変更されているはずです。

```sh
[root@dbsrv ~]# cat /etc/sysctl.conf
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).

# oracle-database-preinstall-19c setting for fs.file-max is 6815744
fs.file-max = 6815744

# oracle-database-preinstall-19c setting for kernel.sem is '250 32000 100 128'
kernel.sem = 250 32000 100 128

# oracle-database-preinstall-19c setting for kernel.shmmni is 4096
kernel.shmmni = 4096

# oracle-database-preinstall-19c setting for kernel.shmall is 1073741824 on x86_64
kernel.shmall = 1073741824

# oracle-database-preinstall-19c setting for kernel.shmmax is 4398046511104 on x86_64
kernel.shmmax = 4398046511104

# oracle-database-preinstall-19c setting for kernel.panic_on_oops is 1 per Orabug 19212317
kernel.panic_on_oops = 1

# oracle-database-preinstall-19c setting for net.core.rmem_default is 262144
net.core.rmem_default = 262144

# oracle-database-preinstall-19c setting for net.core.rmem_max is 4194304
net.core.rmem_max = 4194304

# oracle-database-preinstall-19c setting for net.core.wmem_default is 262144
net.core.wmem_default = 262144

# oracle-database-preinstall-19c setting for net.core.wmem_max is 1048576
net.core.wmem_max = 1048576

# oracle-database-preinstall-19c setting for net.ipv4.conf.all.rp_filter is 2
net.ipv4.conf.all.rp_filter = 2

# oracle-database-preinstall-19c setting for net.ipv4.conf.default.rp_filter is 2
net.ipv4.conf.default.rp_filter = 2

# oracle-database-preinstall-19c setting for fs.aio-max-nr is 1048576
fs.aio-max-nr = 1048576

# oracle-database-preinstall-19c setting for net.ipv4.ip_local_port_range is 9000 65500
net.ipv4.ip_local_port_range = 9000 65500
```

#### ユーザ・グループの追加

------

今回はRAC環境ではなくシングル環境なのでRAC環境用のユーザはコメントアウトしています。

```sh
groupadd -g 54321 oinstall
groupadd -g 54322 dba
groupadd -g 54323 oper
#groupadd -g 54324 backupdba
#groupadd -g 54325 dgdba
#groupadd -g 54326 kmdba
#groupadd -g 54327 asmdba
#groupadd -g 54328 asmoper
#groupadd -g 54329 asmadmin
#groupadd -g 54330 racdba

useradd -u 54321 -g oinstall -G dba,oper oracle
```

```sh
cat /etc/passwd

[root@dbsrv ~]# cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin

～中略～

tcpdump:x:72:72::/:/sbin/nologin
oracle:x:1000:1000:oracle:/home/oracle:/bin/bash
vboxadd:x:988:1::/var/run/vboxadd:/bin/false
[root@dbsrv ~]# 

```

#### ディレクトリ作成

------

```sh
#mkdir -p /u01/app/grid
mkdir -p /u01/app/oracle
mkdir -p /u01/app/oraInventory
#mkdir -p /u01/app/19.3.0.0/grid
mkdir -p /u01/app/oracle/product/19.3.0.0/dbhome_1
#chown -R grid:oinstall /u01
chown -R oracle:oinstall /u01/app/oracle
chmod -R 775 /u01 
```

#### /etc/hostsの変更

------

```sh
[root@dbsrv ~]# vi /etc/hosts
[root@dbsrv ~]# 
[root@dbsrv ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.56.231 dbsrv.oracle.jp dbsrv

[root@dbsrv ~]# 
```

#### 次回

------

<s>次回はOracle Database 19cのインストールを行う予定です。</s>

Oracle Database 19cのインストールは下記にまとめました。

> Oracle Database 19cインストール | my opinion is my own https://zatoima.github.io/oracle-19c-install-single.html