---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2上のRHEL上にOracle Database 12cR1をインストールする場合の事前準備"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "Oracle"]
categories: ["AWS", "EC2", "Oracle"]
url: aws-oracle-ec2-pre-install_1.html
date: 2019-10-13
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



### はじめに

作業メモのようなものです。

### 前提事項

ECのインスタンスタイプはt2.large

RHEL7.6にインストール

CUIではなくGUIでインストールする

runinstallerの実行までの手順

### 必要パッケージのインストール

    sudo -s
    export LANG=C
    
    yum -y install wget
    cd /etc/yum.repos.d
    wget https://public-yum.oracle.com/public-yum-ol7.repo
    curl -k https://public-yum.oracle.com/RPM-GPG-KEY-oracle-ol7 -o /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
    yum install oracle-rdbms-server-12cR1-preinstall

### ネットワーク、SELINUXの設定変更

---

    vi /etc/sysconfig/network
    HOSTNAME=dbsrvec2
    /etc/init.d/network restart
    
    cat /etc/selinux/config
    vi /etc/selinux/config
     SELINUX=disabled
    
    vi /etc/hosts
     x.xxx.181.3 dbsrvec2

### **グループ作成、及びユーザの設定変更**

    groupadd -g 54321 oinstall
    groupadd -g 1101 oper
    groupadd -g 1102 backupdba
    groupadd -g 1103 dgdba
    groupadd -g 1104 kmdba
    groupadd -g 1105 dba
    useradd -u 54321 -g oinstall -G oinstall,oper,backupdba,dgdba,kmdba,dba -d /home/oracle oracle
    
    usermod -u 54321 -g oinstall -G oinstall,oper,backupdba,dgdba,kmdba,dba oracle
    passwd oracle

### 必要なディレクトリの作成

    mkdir -p /u01/app/oracle
    chown -R oracle:oinstall /u01/app/oracle
    chmod -R 775 /u01
    
    cd /u01/app
    mkdir oraInventory
    chown oracle:oinstall oraInventory/

### **GUIでインストールするための設定**

    -- クライアント側(Windows側)にxmingをインストール
    ダウンロードファイル一覧 - Xming X Server for Windows - OSDN https://ja.osdn.net/projects/sfnet_xming/releases/
    
    -- xorgをインストール
    yum -y install xorg-x11-xauth.x86_64 xorg-x11-server-utils.x86_64
    
    -- xeyesで確認
    yum -y install xeyes
    xeyes
    
    -- runinstaller/dbcaでxdpyinfoを使用するのでinstall
    yum -y install xdpyinfo

### **スワップファイルの作成**

    sudo dd if=/dev/zero of=/swapfile bs=1G count=4
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    swapon -s
    vi /etc/fstab
    /swapfile swap swap defaults 0 0

### **runintallerの実行**

    ./runinstaller
    ～省略～
