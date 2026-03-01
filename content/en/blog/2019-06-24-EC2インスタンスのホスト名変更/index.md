---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Changing the EC2 Instance Hostname"
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




## Introduction

------

The prompt displayed when logging into EC2 looks ugly, so I want to explicitly change it. It's slightly different from RHEL 7, so here's a note.

```sh
[ec2-user@ip-10-0-0-9 local]#
```

## Configuration Method

------

##### Change with hostnamectl

```sh
sudo hostnamectl set-hostname --static awsstg-db001
```

##### Edit /etc/cloud/cloud.cfg

Add `preserve_hostname: true` to the cfg file

```sh
sudo vi /etc/cloud/cloud.cfg
~ omitted ~
preserve_hostname: true
```

##### Reboot

```sh
[ec2-user@awsstg-db001 ~]$
[ec2-user@awsstg-db001 ~]$ hostname
awsstg-db001
```



## Reference

------

> AMAZON EC2 LINUX STATIC HOSTNAME RHEL7 CENTOS7 https://aws.amazon.com/jp/premiumsupport/knowledge-center/linux-static-hostname-rhel7-centos7/

------

> Assigning a static hostname to a private Amazon EC2 instance on RHEL, CentOS, or Amazon Linux https://aws.amazon.com/jp/premiumsupport/knowledge-center/linux-static-hostname-rhel-centos-amazon/
