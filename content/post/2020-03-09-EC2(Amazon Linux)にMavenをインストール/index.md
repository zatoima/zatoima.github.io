---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2(Amazon Linux)にMavenをインストール"
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



github上のjavaソースのbuildにmavenが必要だったので、インストールメモ。

### コマンド

```sh
sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
mvn --version
```

### 実行例

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
Saving to: ‘/etc/yum.repos.d/epel-apache-maven.repo’

100%[==================================================================================================================================================>] 445         --.-K/s   in 0s      

2020-02-24 04:47:20 (24.6 MB/s) - ‘/etc/yum.repos.d/epel-apache-maven.repo’ saved [445/445]

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
--> Processing Dependency: java-1.7.0-openjdk-headless = 1:1.7.0.241-2.6.20.0.amzn2.0.2 for package: 1:java-1.7.0-openjdk-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64
--> Processing Dependency: libpulse.so.0(PULSE_0)(64bit) for package: 1:java-1.7.0-openjdk-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64
--> Processing Dependency: libpulse.so.0()(64bit) for package: 1:java-1.7.0-openjdk-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64
--> Running transaction check
---> Package java-1.7.0-openjdk-headless.x86_64 1:1.7.0.241-2.6.20.0.amzn2.0.2 will be installed
--> Processing Dependency: libgconf-2.so.4()(64bit) for package: 1:java-1.7.0-openjdk-headless-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64
---> Package pulseaudio-libs.x86_64 0:10.0-3.amzn2.0.2 will be installed
--> Processing Dependency: libsndfile.so.1(libsndfile.so.1.0)(64bit) for package: pulseaudio-libs-10.0-3.amzn2.0.2.x86_64
--> Processing Dependency: libsndfile.so.1()(64bit) for package: pulseaudio-libs-10.0-3.amzn2.0.2.x86_64
--> Processing Dependency: libasyncns.so.0()(64bit) for package: pulseaudio-libs-10.0-3.amzn2.0.2.x86_64
--> Running transaction check
---> Package GConf2.x86_64 0:3.2.6-8.amzn2.0.2 will be installed
--> Processing Dependency: libpolkit-gobject-1.so.0()(64bit) for package: GConf2-3.2.6-8.amzn2.0.2.x86_64
--> Processing Dependency: libdbus-glib-1.so.2()(64bit) for package: GConf2-3.2.6-8.amzn2.0.2.x86_64
---> Package libasyncns.x86_64 0:0.8-7.amzn2.0.2 will be installed
---> Package libsndfile.x86_64 0:1.0.25-10.amzn2.0.2 will be installed
--> Processing Dependency: libvorbisenc.so.2()(64bit) for package: libsndfile-1.0.25-10.amzn2.0.2.x86_64
--> Processing Dependency: libvorbis.so.0()(64bit) for package: libsndfile-1.0.25-10.amzn2.0.2.x86_64
--> Processing Dependency: libogg.so.0()(64bit) for package: libsndfile-1.0.25-10.amzn2.0.2.x86_64
--> Processing Dependency: libgsm.so.1()(64bit) for package: libsndfile-1.0.25-10.amzn2.0.2.x86_64
--> Processing Dependency: libFLAC.so.8()(64bit) for package: libsndfile-1.0.25-10.amzn2.0.2.x86_64
--> Running transaction check
---> Package dbus-glib.x86_64 0:0.100-7.2.amzn2 will be installed
---> Package flac-libs.x86_64 0:1.3.0-5.amzn2.0.2 will be installed
---> Package gsm.x86_64 0:1.0.13-11.amzn2.0.2 will be installed
---> Package libogg.x86_64 2:1.3.0-7.amzn2.0.2 will be installed
---> Package libvorbis.x86_64 1:1.3.3-8.amzn2.0.2 will be installed
---> Package polkit.x86_64 0:0.112-22.amzn2.1 will be installed
--> Processing Dependency: polkit-pkla-compat for package: polkit-0.112-22.amzn2.1.x86_64
--> Processing Dependency: libmozjs-17.0.so(mozjs_17.0)(64bit) for package: polkit-0.112-22.amzn2.1.x86_64
--> Processing Dependency: libmozjs-17.0.so()(64bit) for package: polkit-0.112-22.amzn2.1.x86_64
--> Running transaction check
---> Package mozjs17.x86_64 0:17.0.0-20.amzn2.0.1 will be installed
---> Package polkit-pkla-compat.x86_64 0:0.1-4.amzn2.0.2 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================================================================
 Package                                             Arch                           Version                                                 Repository                                 Size
============================================================================================================================================================================================
Installing:
 apache-maven                                        noarch                         3.5.2-1.el6                                             epel-apache-maven                         8.1 M
Installing for dependencies:
 GConf2                                              x86_64                         3.2.6-8.amzn2.0.2                                       amzn2-core                                1.0 M
 dbus-glib                                           x86_64                         0.100-7.2.amzn2                                         amzn2-core                                103 k
 flac-libs                                           x86_64                         1.3.0-5.amzn2.0.2                                       amzn2-core                                168 k
 gsm                                                 x86_64                         1.0.13-11.amzn2.0.2                                     amzn2-core                                 30 k
 java-1.7.0-openjdk                                  x86_64                         1:1.7.0.241-2.6.20.0.amzn2.0.2                          amzn2-core                                255 k
 java-1.7.0-openjdk-devel                            x86_64                         1:1.7.0.241-2.6.20.0.amzn2.0.2                          amzn2-core                                9.2 M
 java-1.7.0-openjdk-headless                         x86_64                         1:1.7.0.241-2.6.20.0.amzn2.0.2                          amzn2-core                                 26 M
 libasyncns                                          x86_64                         0.8-7.amzn2.0.2                                         amzn2-core                                 26 k
 libogg                                              x86_64                         2:1.3.0-7.amzn2.0.2                                     amzn2-core                                 24 k
 libsndfile                                          x86_64                         1.0.25-10.amzn2.0.2                                     amzn2-core                                152 k
 libvorbis                                           x86_64                         1:1.3.3-8.amzn2.0.2                                     amzn2-core                                204 k
 mozjs17                                             x86_64                         17.0.0-20.amzn2.0.1                                     amzn2-core                                1.4 M
 polkit                                              x86_64                         0.112-22.amzn2.1                                        amzn2-core                                171 k
 polkit-pkla-compat                                  x86_64                         0.1-4.amzn2.0.2                                         amzn2-core                                 39 k
 pulseaudio-libs                                     x86_64                         10.0-3.amzn2.0.2                                        amzn2-core                                651 k

Transaction Summary
============================================================================================================================================================================================
Install  1 Package (+15 Dependent packages)

Total download size: 47 M
Installed size: 159 M
Downloading packages:
(1/16): dbus-glib-0.100-7.2.amzn2.x86_64.rpm                                                                                                                         | 103 kB  00:00:00     
(2/16): GConf2-3.2.6-8.amzn2.0.2.x86_64.rpm                                                                                                                          | 1.0 MB  00:00:00     
(3/16): gsm-1.0.13-11.amzn2.0.2.x86_64.rpm                                                                                                                           |  30 kB  00:00:00     
(4/16): flac-libs-1.3.0-5.amzn2.0.2.x86_64.rpm                                                                                                                       | 168 kB  00:00:00     
(5/16): java-1.7.0-openjdk-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64.rpm                                                                                                   | 255 kB  00:00:00     
(6/16): java-1.7.0-openjdk-devel-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64.rpm                                                                                             | 9.2 MB  00:00:00     
(7/16): libasyncns-0.8-7.amzn2.0.2.x86_64.rpm                                                                                                                        |  26 kB  00:00:00     
(8/16): libogg-1.3.0-7.amzn2.0.2.x86_64.rpm                                                                                                                          |  24 kB  00:00:00     
(9/16): libsndfile-1.0.25-10.amzn2.0.2.x86_64.rpm                                                                                                                    | 152 kB  00:00:00     
(10/16): libvorbis-1.3.3-8.amzn2.0.2.x86_64.rpm                                                                                                                      | 204 kB  00:00:00     
(11/16): mozjs17-17.0.0-20.amzn2.0.1.x86_64.rpm                                                                                                                      | 1.4 MB  00:00:00     
(12/16): polkit-0.112-22.amzn2.1.x86_64.rpm                                                                                                                          | 171 kB  00:00:00     
(13/16): polkit-pkla-compat-0.1-4.amzn2.0.2.x86_64.rpm                                                                                                               |  39 kB  00:00:00     
(14/16): pulseaudio-libs-10.0-3.amzn2.0.2.x86_64.rpm                                                                                                                 | 651 kB  00:00:00     
(15/16): java-1.7.0-openjdk-headless-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64.rpm                                                                                         |  26 MB  00:00:00     
(16/16): apache-maven-3.5.2-1.el6.noarch.rpm                                                                                                                         | 8.1 MB  00:00:04     
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                       9.8 MB/s |  47 MB  00:00:04     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : 2:libogg-1.3.0-7.amzn2.0.2.x86_64                                                                                                                                       1/16 
  Installing : 1:libvorbis-1.3.3-8.amzn2.0.2.x86_64                                                                                                                                    2/16 
  Installing : flac-libs-1.3.0-5.amzn2.0.2.x86_64                                                                                                                                      3/16 
  Installing : mozjs17-17.0.0-20.amzn2.0.1.x86_64                                                                                                                                      4/16 
  Installing : polkit-0.112-22.amzn2.1.x86_64                                                                                                                                          5/16 
  Installing : polkit-pkla-compat-0.1-4.amzn2.0.2.x86_64                                                                                                                               6/16 
  Installing : gsm-1.0.13-11.amzn2.0.2.x86_64                                                                                                                                          7/16 
  Installing : libsndfile-1.0.25-10.amzn2.0.2.x86_64                                                                                                                                   8/16 
  Installing : dbus-glib-0.100-7.2.amzn2.x86_64                                                                                                                                        9/16 
  Installing : GConf2-3.2.6-8.amzn2.0.2.x86_64                                                                                                                                        10/16 
  Installing : 1:java-1.7.0-openjdk-headless-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64                                                                                                      11/16 
  Installing : libasyncns-0.8-7.amzn2.0.2.x86_64                                                                                                                                      12/16 
  Installing : pulseaudio-libs-10.0-3.amzn2.0.2.x86_64                                                                                                                                13/16 
  Installing : 1:java-1.7.0-openjdk-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64                                                                                                               14/16 
  Installing : 1:java-1.7.0-openjdk-devel-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64                                                                                                         15/16 
  Installing : apache-maven-3.5.2-1.el6.noarch                                                                                                                                        16/16 
  Verifying  : libasyncns-0.8-7.amzn2.0.2.x86_64                                                                                                                                       1/16 
  Verifying  : polkit-0.112-22.amzn2.1.x86_64                                                                                                                                          2/16 
  Verifying  : 1:libvorbis-1.3.3-8.amzn2.0.2.x86_64                                                                                                                                    3/16 
  Verifying  : GConf2-3.2.6-8.amzn2.0.2.x86_64                                                                                                                                         4/16 
  Verifying  : 1:java-1.7.0-openjdk-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64                                                                                                                5/16 
  Verifying  : apache-maven-3.5.2-1.el6.noarch                                                                                                                                         6/16 
  Verifying  : dbus-glib-0.100-7.2.amzn2.x86_64                                                                                                                                        7/16 
  Verifying  : 1:java-1.7.0-openjdk-headless-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64                                                                                                       8/16 
  Verifying  : pulseaudio-libs-10.0-3.amzn2.0.2.x86_64                                                                                                                                 9/16 
  Verifying  : 2:libogg-1.3.0-7.amzn2.0.2.x86_64                                                                                                                                      10/16 
  Verifying  : polkit-pkla-compat-0.1-4.amzn2.0.2.x86_64                                                                                                                              11/16 
  Verifying  : flac-libs-1.3.0-5.amzn2.0.2.x86_64                                                                                                                                     12/16 
  Verifying  : libsndfile-1.0.25-10.amzn2.0.2.x86_64                                                                                                                                  13/16 
  Verifying  : gsm-1.0.13-11.amzn2.0.2.x86_64                                                                                                                                         14/16 
  Verifying  : mozjs17-17.0.0-20.amzn2.0.1.x86_64                                                                                                                                     15/16 
  Verifying  : 1:java-1.7.0-openjdk-devel-1.7.0.241-2.6.20.0.amzn2.0.2.x86_64                                                                                                         16/16 

Installed:
  apache-maven.noarch 0:3.5.2-1.el6                                                                                                                                                         

Dependency Installed:
  GConf2.x86_64 0:3.2.6-8.amzn2.0.2                                 dbus-glib.x86_64 0:0.100-7.2.amzn2                       flac-libs.x86_64 0:1.3.0-5.amzn2.0.2                          
  gsm.x86_64 0:1.0.13-11.amzn2.0.2                                  java-1.7.0-openjdk.x86_64 1:1.7.0.241-2.6.20.0.amzn2.0.2 java-1.7.0-openjdk-devel.x86_64 1:1.7.0.241-2.6.20.0.amzn2.0.2
  java-1.7.0-openjdk-headless.x86_64 1:1.7.0.241-2.6.20.0.amzn2.0.2 libasyncns.x86_64 0:0.8-7.amzn2.0.2                      libogg.x86_64 2:1.3.0-7.amzn2.0.2                             
  libsndfile.x86_64 0:1.0.25-10.amzn2.0.2                           libvorbis.x86_64 1:1.3.3-8.amzn2.0.2                     mozjs17.x86_64 0:17.0.0-20.amzn2.0.1                          
  polkit.x86_64 0:0.112-22.amzn2.1                                  polkit-pkla-compat.x86_64 0:0.1-4.amzn2.0.2              pulseaudio-libs.x86_64 0:10.0-3.amzn2.0.2                     

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

### 参考

> Install Maven with Yum on Amazon Linux https://gist.github.com/sebsto/19b99f1fa1f32cae5d00