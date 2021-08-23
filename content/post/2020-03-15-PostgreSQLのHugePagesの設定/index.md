---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのHugePagesの設定"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-hugepages-setting.html
date: 2020-03-15
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



メモリはpagesとよばれるブロック単位で管理されており、x86 アーキテクチャのデフォルトページサイズは 4096 バイト。HugePage は、それよりも大きなページサイズ (デフォルトで 2 MB) で管理する機能であるためshared_buffersの値が大きい場合に、huge pagesを使用するとオーバーヘッドが減少するというのが概要。

#### 事前確認

カーネルでHugePagesがサポートされているかどうかを確認。

※`CONFIG_HUGETLBFS`および`CONFIG_HUGETLB_PAGE`構成オプションを使用してLinuxカーネルを構築

```
 grep Huge /proc/meminfo
```

PostgreSQLの場合は、下記マニュアルに従いhugepages数を見積もる。Oracleみたくhugepages_settings.sh的なものはない。

> 18.4. カーネルリソースの管理 https://www.postgresql.jp/document/10/html/kernel-resources.html#LINUX-HUGE-PAGES

#### 必要なHugePages数の見積もり方法

```sh
[postgres@postdb ~]$ head -1 $PGDATA/postmaster.pid
5811
[postgres@postdb ~]# grep ^VmPeak /proc/5811/status
VmPeak:	 5565496 kB
[postgres@postdb ~]# grep ^Hugepagesize /proc/meminfo
Hugepagesize:       2048 kB
```

上記より、`5565496kb/2048kb` = `2,717.52734375‬`となり、2718のhugepagesが必要と判断できる。

##### OS側の設定

```sh
sysctl -w vm.nr_hugepages=2718
```

再起動後にもこの数値を使用するように/etc/sysctl.confに設定して永続化する。

```
cat "vm.nr_hugepages=2718" >> /etc/sysctl.conf
```

##### hugepagesの割当の確認

```sh
grep Huge /proc/meminfo

[postgres@postdb ~]$ grep Huge /proc/meminfo
AnonHugePages:         0 kB
ShmemHugePages:        0 kB
HugePages_Total:    2718
HugePages_Free:     2638
HugePages_Rsvd:     2511
HugePages_Surp:        0
Hugepagesize:       2048 kB
[postgres@postdb ~]$ 
```

##### DB側にてパラメータセット（postgresql.conf）

```sh
huge_pages=on
```

念のためにパラメータ確認

```sh
[postgres@postdb data]$ psql
psql (10.11)
Type "help" for help.

postgres=# 
postgres=# show huge_pages;
 huge_pages 
------------
 on
(1 row)
```

### 参考

> 18.4. カーネルリソースの管理 https://www.postgresql.jp/document/10/html/kernel-resources.html#LINUX-HUGE-PAGES

