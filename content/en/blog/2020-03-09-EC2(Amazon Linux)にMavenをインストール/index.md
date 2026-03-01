---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Installing Maven on EC2 (Amazon Linux)"
subtitle: ""
summary: " "
tags: ["AWS","EC2","Maven"]
categories: ["AWS","EC2","Maven"]
url: aws-ec2-maven-install.html
date: 2020-03-09
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



I needed Maven to build a Java source project on GitHub, so here are my installation notes.

### Commands

```sh
sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
mvn --version
```

### Example Execution

```sh
[ec2-user@bastin]$ sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
--2020-02-24 04:47:19--  http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo
Resolving repos.fedorapeople.org (repos.fedorapeople.org)... 152.19.134.199, 2610:28:3090:3001:5054:ff:fea7:9474
Connecting to repos.fedorapeople.org (repos.fedorapeople.org)|152.19.134.199|:80... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo [following]
--2020-02-24 04:47:20--  https://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo
Connecting to repos.fedorapeople.org (repos.fedorapeople.org)|152.19.134.199|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 445
Saving to: '/etc/yum.repos.d/epel-apache-maven.repo'

100%[==================================================================================================================================================>] 445         --.-K/s   in 0s

2020-02-24 04:47:20 (24.6 MB/s) - '/etc/yum.repos.d/epel-apache-maven.repo' saved [445/445]

[ec2-user@bastin]$ sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
[ec2-user@bastin]$ sudo yum install -y apache-maven
Loaded plugins: langpacks, priorities, update-motd
epel-apache-maven                                                                                                                                                    | 3.3 kB  00:00:00
epel-apache-maven/x86_64/primary_db                                                                                                                                  | 5.0 kB  00:00:01
Resolving Dependencies
--> Running transaction check
---> Package apache-maven.noarch 0:3.5.2-1.el6 will be installed
--> Processing Dependency: java-1.7.0-openjdk-devel for package: apache-maven-3.5.2-1.el6.noarch
--> Running transaction check
---> Package java-1.7.0-openjdk-devel.x86_64 1:1.7.0.241-2.6.20.0.amzn2.0.2 will be installed
--> Processing Dependency: java-1.7.0-openjdk = 1:1.7.0.241-2.6.20.0.amzn2.0.2 for package: 1:java-1.7.0-openjdk-devel-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64
--> Running transaction check
---> Package java-1.7.0-openjdk.x86_64 1:1.7.0.241-2.6.20.0.amzn2.0.2 will be installed

(... dependency resolution output omitted ...)

Complete!
[ec2-user@bastin]$
[ec2-user@bastin]$ mvn --version
Apache Maven 3.5.2 (138edd61fd100ec658bfa2d307c43b76940a5d7d; 2017-10-18T07:58:13Z)
Maven home: /usr/share/apache-maven
Java version: 1.8.0_222, vendor: Oracle Corporation
Java home: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.222.b10-0.amzn2.0.1.x86_64/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "4.14.152-127.182.amzn2.x86_64", arch: "amd64", family: "unix"
[ec2-user@bastin]$
[ec2-user@bastin]$

[ec2-user@bastin]$
```

### Reference

> Install Maven with Yum on Amazon Linux https://gist.github.com/sebsto/19b99f1fa1f32cae5d00
