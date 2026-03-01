---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2で使用できるRHELのAMI一覧"
subtitle: ""
summary: " "
tags: ["AWS","EC2"]
categories: ["AWS","EC2"]
url: aws-ec2-available-rhel-ami-version.html
date: 2020-05-22
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

こちらを参考にRHEL 7とRHEL 8のAMIの調査方法をメモ

> 【小ネタ】Red Hat Enterprise LinuxのAMIの調べ方 – サーバーワークスエンジニアブログ http://blog.serverworks.co.jp/tech/2019/06/18/post-71160/

### RHEL 7

```
[ec2-user@bastin ~]$ aws ec2 describe-images --owners 309956199498 --query 'Images[*].[CreationDate,Name,ImageId]' --filters "Name=name,Values=RHEL-7.?*GA*x86*" --region ap-northeast-1 --output table | sort -r

|                                            DescribeImages                                            |
|  2020-02-26T17:20:13.000Z |  RHEL-7.8_HVM_GA-20200225-x86_64-1-Hourly2-GP2  |  ami-038a794b902fa0afc |
|  2019-07-24T09:17:45.000Z |  RHEL-7.7_HVM_GA-20190723-x86_64-1-Hourly2-GP2  |  ami-0dc41c7805e171046 |
|  2019-02-06T00:23:09.000Z |  RHEL-7.6_HVM_GA-20190128-x86_64-0-Hourly2-GP2  |  ami-00b95502a4d51a07e |
|  2018-10-17T14:14:10.000Z |  RHEL-7.6_HVM_GA-20181017-x86_64-0-Hourly2-GP2  |  ami-08419d23bf91152e4 |
|  2018-03-23T21:14:36.000Z |  RHEL-7.5_HVM_GA-20180322-x86_64-1-Hourly2-GP2  |  ami-6b0d5f0d          |
|  2017-08-08T15:45:51.000Z |  RHEL-7.4_HVM_GA-20170808-x86_64-2-Hourly2-GP2  |  ami-30ef0556          |
|  2017-07-24T15:55:34.000Z |  RHEL-7.4_HVM_GA-20170724-x86_64-1-Hourly2-GP2  |  ami-3901e15f          |
|  2016-10-26T22:33:03.000Z |  RHEL-7.3_HVM_GA-20161026-x86_64-1-Hourly2-GP2  |  ami-5de0433c          |
|  2015-11-12T21:11:15.000Z |  RHEL-7.2_HVM_GA-20151112-x86_64-1-Hourly2-GP2  |  ami-0dd8f963          |
|  2015-02-26T16:34:39.000Z |  RHEL-7.1_HVM_GA-20150225-x86_64-1-Hourly2-GP2  |  ami-b1b458b1          |
|  2015-02-16T16:17:50.000Z |  RHEL-7.0_HVM_GA-20150209-x86_64-1-Hourly2-GP2  |  ami-e532d3e5          |
|  2014-10-20T14:13:11.000Z |  RHEL-7.0_HVM_GA-20141017-x86_64-1-Hourly2-GP2  |  ami-35556534          |
|  2014-05-28T20:36:35.000Z |  RHEL-7.0_GA_HVM-x86_64-3-Hourly2               |  ami-87206d86          |
+---------------------------+-------------------------------------------------+------------------------+
+---------------------------+-------------------------------------------------+------------------------+
--------------------------------------------------------------------------------------------------------
```

### RHEL 8

```
[ec2-user@bastin ~]$ aws ec2 describe-images --owners 309956199498 --query 'Images[*].[CreationDate,Name,ImageId]' --filters "Name=name,Values=RHEL-8.?*x86*" --region ap-northeast-1 --output table | sort -r
|                                              DescribeImages                                              |
|  2020-04-23T15:39:00.000Z |  RHEL-8.2.0_HVM-20200423-x86_64-0-Hourly2-GP2       |  ami-07dd14faa8a17fb3e |
|  2020-01-14T22:28:26.000Z |  RHEL-8.2.0_HVM_BETA-20191219-x86_64-0-Hourly2-GP2  |  ami-0f3a7097e011d9532 |
|  2019-10-30T10:14:36.000Z |  RHEL-8.1.0_HVM-20191029-x86_64-0-Hourly2-GP2       |  ami-0302fadfb901ae198 |
|  2019-09-23T20:01:56.000Z |  RHEL-8.0_HVM-20190920-x86_64-0-Hourly2-GP2         |  ami-0c45b9b8b241f629f |
|  2019-07-21T19:37:12.000Z |  RHEL-8.1.0_HVM_BETA-20190701-x86_64-0-Hourly2-GP2  |  ami-0c09ca180274c253a |
|  2019-06-19T19:55:31.000Z |  RHEL-8.0.0_HVM-20190618-x86_64-1-Hourly2-GP2       |  ami-09f31cc5d5eecca1a |
|  2019-05-20T22:19:27.000Z |  RHEL-8.0.0_HVM-20190520-x86_64-1-Hourly2-GP2       |  ami-0c3b878cc19d12d6c |
|  2019-04-26T20:05:27.000Z |  RHEL-8.0.0_HVM-20190426-x86_64-1-Hourly2-GP2       |  ami-03c6a4362c5fb8c61 |
|  2018-11-13T21:36:49.000Z |  RHEL-8.0_HVM_BETA-20181113-x86_64-1-Hourly2-GP2    |  ami-0d938ac9c11076133 |
+---------------------------+-----------------------------------------------------+------------------------+
+---------------------------+-----------------------------------------------------+------------------------+
------------------------------------------------------------------------------------------------------------

```

