---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "[DBT-06103] The port (1,521) is already in use. When Running DBCA"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-oraerror-DBT06103.html
date: 2019-06-20
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



#### **Introduction**

------

There are many cases where a new listener is created when creating a DB with DBCA, but you may encounter the following error and be unable to proceed to the next screen.

```
[DBT-06103] The port (1,521) is already in use.
```

<img src="images/image-20191121171343673.png" alt="image-20191121171343673" style="zoom:50%;" />

#### **Cause**

------

The cause was that the host's own information was not listed in "/etc/hosts".

By adding the entry as shown below, this error no longer appeared.

```sh
[root@dbsrv ~]# vi /etc/hosts
[root@dbsrv ~]#
[root@dbsrv ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.56.231 dbsrv.oracle.jp dbsrv
```

#### **Reference**

------

[DBT-06103] The port (5,500) is already in use. ACTION: Specify a free port (Document ID 2277154.1)
