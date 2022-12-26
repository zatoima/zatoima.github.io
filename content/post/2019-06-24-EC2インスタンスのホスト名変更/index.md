---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2インスタンスのホスト名変更"
subtitle: ""
summary: " "
tags: ["AWS","EC2"]
categories: ["AWS","EC2"]
url: aws-ec2-hostname-change.html
date: 2019-06-24
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




## はじめに

------

EC2にログインした時のプロンプト表記が不格好なので明示的に変更したい。REHL7系と少しだけ違うのでメモ。

```sh
[ec2-user@ip-10-0-0-9 local]#
```

## 設定方法

------

##### hostnamectlで変更

```sh
sudo hostnamectl set-hostname --static awsstg-db001
```

##### /etc/cloud/cloud.cfgを編集する

`preserve_hostname: true`をcfgファイル内に記述

```sh
sudo vi /etc/cloud/cloud.cfg
～中略～
preserve_hostname: true
```

##### リブートする

```sh
[ec2-user@awsstg-db001 ~]$
[ec2-user@awsstg-db001 ~]$ hostname
awsstg-db001
```



## 参考

------

> AMAZON EC2 LINUX の静的ホスト名 RHEL7 CENTOS7 HTTPS://AWS.AMAZON.COM/JP/PREMIUMSUPPORT/KNOWLEDGE-CENTER/LINUX-STATIC-HOSTNAME-RHEL7-CENTOS7/

------

> RHEL、Centos、または Amazon Linux 上のプライベート Amazon EC2 インスタンスに静的ホスト名を割り当てる https://aws.amazon.com/jp/premiumsupport/knowledge-center/linux-static-hostname-rhel-centos-amazon/