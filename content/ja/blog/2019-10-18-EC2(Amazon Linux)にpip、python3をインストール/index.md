---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2(Amazon Linux)にpip、python3をインストール"
subtitle: ""
summary: " "
tags: ["Python", "EC2"]
categories: ["Python", "EC2"]
url: aws-ec2-install-python3.html
date: 2019-10-18
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



### 0.コマンド

pip は Python 3.4 以降では Python 本体に同梱されるようなっているのでpip3の個別のインストールは不要。

```sh
sudo yum install -y python3
```

### python3をインストール

```sh
[postgres@postdb ~]$ sudo yum install python3 -y
Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
amzn2-core                                                                                                                                                           | 2.4 kB  00:00:00     
46 packages excluded due to repository priority protections
Resolving Dependencies
--> Running transaction check
---> Package python3.x86_64 0:3.7.6-1.amzn2.0.1 will be installed
--> Processing Dependency: python3-libs(x86-64) = 3.7.6-1.amzn2.0.1 for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Processing Dependency: python3-setuptools for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Processing Dependency: python3-pip for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Processing Dependency: libpython3.7m.so.1.0()(64bit) for package: python3-3.7.6-1.amzn2.0.1.x86_64
--> Running transaction check
---> Package python3-libs.x86_64 0:3.7.6-1.amzn2.0.1 will be installed
---> Package python3-pip.noarch 0:9.0.3-1.amzn2.0.2 will be installed
---> Package python3-setuptools.noarch 0:38.4.0-3.amzn2.0.6 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

============================================================================================================================================================================================
 Package                                           Arch                                  Version                                            Repository                                 Size
============================================================================================================================================================================================
Installing:
 python3                                           x86_64                                3.7.6-1.amzn2.0.1                                  amzn2-core                                 71 k
Installing for dependencies:
 python3-libs                                      x86_64                                3.7.6-1.amzn2.0.1                                  amzn2-core                                9.1 M
 python3-pip                                       noarch                                9.0.3-1.amzn2.0.2                                  amzn2-core                                1.9 M
 python3-setuptools                                noarch                                38.4.0-3.amzn2.0.6                                 amzn2-core                                617 k

Transaction Summary
============================================================================================================================================================================================
Install  1 Package (+3 Dependent packages)

Total download size: 12 M
Installed size: 50 M
Downloading packages:
(1/4): python3-3.7.6-1.amzn2.0.1.x86_64.rpm                                                                                                                          |  71 kB  00:00:00     
(2/4): python3-libs-3.7.6-1.amzn2.0.1.x86_64.rpm                                                                                                                     | 9.1 MB  00:00:00     
(3/4): python3-setuptools-38.4.0-3.amzn2.0.6.noarch.rpm                                                                                                              | 617 kB  00:00:00     
(4/4): python3-pip-9.0.3-1.amzn2.0.2.noarch.rpm                                                                                                                      | 1.9 MB  00:00:00     
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                                                        47 MB/s |  12 MB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
** Found 1 pre-existing rpmdb problem(s), 'yum check' output follows:
pgdg-redhat-repo-42.0-5.noarch has missing requires of /etc/redhat-release
  Installing : python3-pip-9.0.3-1.amzn2.0.2.noarch                                                                                                                                     1/4 
  Installing : python3-3.7.6-1.amzn2.0.1.x86_64                                                                                                                                         2/4 
  Installing : python3-setuptools-38.4.0-3.amzn2.0.6.noarch                                                                                                                             3/4 
  Installing : python3-libs-3.7.6-1.amzn2.0.1.x86_64                                                                                                                                    4/4 
  Verifying  : python3-setuptools-38.4.0-3.amzn2.0.6.noarch                                                                                                                             1/4 
  Verifying  : python3-pip-9.0.3-1.amzn2.0.2.noarch                                                                                                                                     2/4 
  Verifying  : python3-3.7.6-1.amzn2.0.1.x86_64                                                                                                                                         3/4 
  Verifying  : python3-libs-3.7.6-1.amzn2.0.1.x86_64                                                                                                                                    4/4 

Installed:
  python3.x86_64 0:3.7.6-1.amzn2.0.1                                                                                                                                                        

Dependency Installed:
  python3-libs.x86_64 0:3.7.6-1.amzn2.0.1                     python3-pip.noarch 0:9.0.3-1.amzn2.0.2                     python3-setuptools.noarch 0:38.4.0-3.amzn2.0.6                    

Complete!
[postgres@postdb ~]$ 
[postgres@postdb ~]$ pip3 --version
pip 9.0.3 from /usr/lib/python3.7/site-packages (python 3.7)
[postgres@postdb ~]$ 
[postgres@postdb ~]$ 
[postgres@postdb ~]$ python3 --version
Python 3.7.6
[postgres@postdb ~]$ 

```

