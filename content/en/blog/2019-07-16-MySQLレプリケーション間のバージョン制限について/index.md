---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Version Restrictions Between MySQL Replication Instances"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-replication-version.html
date: 2019-07-16
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


MySQL has version restrictions between replication instances, and only one version difference is allowed. Note that MySQL has version restrictions even for logical replication.

> MySQL :: MySQL 5.7 Reference Manual :: 16.4.2 Replication Compatibility Between MySQL Versions https://dev.mysql.com/doc/refman/5.7/en/replication-compatibility.html
>
> MySQL supports replication from one release series to the next higher release series. For example, you can replicate from a master running MySQL 5.6 to a slave running MySQL 5.7, from a master running MySQL 5.7 to a slave running MySQL 8.0, and so on.

### Note: Version Restrictions for Other DBs (Oracle, Postgres) Replication

Oracle DataGuard (Physical Standby) requires the same version. Oracle GoldenGate has no version restrictions (approximately dependent on the Certification Matrix).

PostgreSQL streaming replication (physical replication) requires the same version. Logical replication allows different versions.
