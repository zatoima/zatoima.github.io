---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLレプリケーション間のバージョン制限について"
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


MySQLはレプリケーション間のバージョン制限があり、1バージョンの差異のみ可能。MySQLは論理レプリケーションにも関わらずバージョン制限があることに注意。

> MySQL :: MySQL 5.7 Reference Manual :: 16.4.2 Replication Compatibility Between MySQL Versions https://dev.mysql.com/doc/refman/5.7/en/replication-compatibility.html
>
> MySQL supports replication from one release series to the next higher release series. For example, you can replicate from a master running MySQL 5.6 to a slave running MySQL 5.7, from a master running MySQL 5.7 to a slave running MySQL 8.0, and so on. 

(日本語訳)

> MySQLは、あるリリースシリーズから次のリリースシリーズへのレプリケーションをサポートしています。たとえば、MySQL 5.6を実行しているマスターからMySQL 5.7を実行しているスレーブ、MySQL 5.7を実行しているマスターからMySQL 8.0を実行しているスレーブなどに複製できます。

### 備考：他DB(Oracle、Postgres)のレプリケーションのバージョン制限

Oracle DataGuard（フィジカル・スタンバイ）は同バージョン、Oracle GoldenGateはバージョン制限無し(≒Certification Matrixに依存)

PostgreSQLのストリーミングレプリケーション（物理レプリケーション）は同一バージョンのみ。ロジカルレプリケーション（論理レプリケーション）は他バージョンも可能。
