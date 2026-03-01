---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Configuring HugePages for PostgreSQL"
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



Memory is managed in block units called pages, and the default page size for x86 architecture is 4096 bytes. HugePages is a feature that manages memory with larger page sizes (2 MB by default), so the overview is that using huge pages reduces overhead when the shared_buffers value is large.

#### Pre-check

Verify that HugePages is supported by the kernel.

*Build the Linux kernel with `CONFIG_HUGETLBFS` and `CONFIG_HUGETLB_PAGE` configuration options.*

```
grep Huge /proc/meminfo
```

For PostgreSQL, estimate the number of hugepages according to the manual below. There is no script like Oracle's hugepages_settings.sh.

> 18.4. Managing Kernel Resources https://www.postgresql.jp/document/10/html/kernel-resources.html#LINUX-HUGE-PAGES

#### How to Estimate the Required Number of HugePages

```sh
[postgres@postdb ~]$ head -1 $PGDATA/postmaster.pid
5811
[postgres@postdb ~]# grep ^VmPeak /proc/5811/status
VmPeak:	 5565496 kB
[postgres@postdb ~]# grep ^Hugepagesize /proc/meminfo
Hugepagesize:       2048 kB
```

From the above, `5565496kb/2048kb` = `2,717.52734375`, so we can determine that 2718 hugepages are needed.

##### OS-Side Configuration

```sh
sysctl -w vm.nr_hugepages=2718
```

Persist this value by setting it in /etc/sysctl.conf so it is used after a restart.

```
cat "vm.nr_hugepages=2718" >> /etc/sysctl.conf
```

##### Verifying HugePages Allocation

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

##### Set Parameter on the DB Side (postgresql.conf)

```sh
huge_pages=on
```

Verify the parameter just to be sure:

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

### Reference

> 18.4. Managing Kernel Resources https://www.postgresql.jp/document/10/html/kernel-resources.html#LINUX-HUGE-PAGES
