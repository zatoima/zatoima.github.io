---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "DBCA実行時の[DBT-06103] The port (1,521) is already in use.について"
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



#### **はじめに**

------

DBCAでDB作成する際にリスナーを新規で作成するケースは多くあると思いますが、

下記エラーで次の画面に進めないことがあります。

```
[DBT-06103] The port (1,521) is already in use.
```

<img src="images/image-20191121171343673.png" alt="image-20191121171343673" style="zoom:50%;" />

#### **原因**

------

「/etc/hosts」に自ホストの情報が記載されていないことが原因でした。

下記のように記載することでこのエラーは出力しないようになりました。

```sh
[root@dbsrv ~]# vi /etc/hosts
[root@dbsrv ~]# 
[root@dbsrv ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.56.231 dbsrv.oracle.jp dbsrv
```

#### **参考**

------

[DBT-06103] The port (5,500) is already in use. ACTION: Specify a free port (ドキュメントID 2277154.1)