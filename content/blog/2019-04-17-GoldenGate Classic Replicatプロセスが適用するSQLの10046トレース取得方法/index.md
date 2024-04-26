---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGate Classic Replicatプロセスが適用するSQLの10046トレース取得方法"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-classic-replicat-trace.html
date: 2019-04-17
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

GoldenGateのReplicatプロセスが適用するSQLの調査をする場面があります。SQLの性能調査の場合はSQLトレースを取得して解析という流れになると思いますが、DB層からの操作ではGoldenGateセッション単位での設定は出来ないので、DB単位で設定する必要があります。

一方、GoldenGateにはSQLEXECというパラメータが用意されてありますので、こちらをReplicatプロセスのパラメータ・ファイルに記載することでReplicatが適用するSQLのみ10046トレースが取得が可能です。

> SQLEXEC https://docs.oracle.com/cd/E51849_01/gg-winux/GWURF/gg_parameters156.htm
>
> `SQLEXEC`パラメータでは、Oracle GoldenGate処理の範囲でストアド・プロシージャ、問合せまたはデータベース・コマンドを実行します。`SQLEXEC`により、Oracle GoldenGateはデータベースと直接通信し、データベースによってサポートされている処理を実行できます。

#### **設定方法**

```sh
～省略～
REPORTCOUNT EVERY 10 MINUTES, RATE

SQLEXEC  "ALTER  SESSION  SET  TRACEFILE_IDENTIFIER='GG_DEBUG'"
SQLEXEC  "alter session set events '10046 trace name context forever,level 12'"

BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;
～省略～
```

※この方法で10046トレースが取得できるのはClassic Replicatの場合のみです。Integrated Replicatでは他の方法を使用してSQL性能情報を取得する必要があります。

#### **実行結果**

TRACEFILE_IDENTIFIERで「GG_DEBUG」を付与しているため、トレースファイルには「GG_DEBUG」がついたファイルが生成されます。

```sh
[oracle@dbvgg trace]$ pwd
/u01/app/oracle/diag/rdbms/db18s/db18s/trace
[oracle@dbvgg trace]$ ls -ltr | tail
-rw-r----- 1 oracle oinstall    1737  4月  3 10:49 2019 db18s_m000_3762.trm
-rw-r----- 1 oracle oinstall    8661  4月  3 10:49 2019 db18s_m000_3762.trc
-rw-r----- 1 oracle oinstall    1160  4月  3 10:49 2019 db18s_dbrm_3705.trm
-rw-r----- 1 oracle oinstall    4775  4月  3 10:49 2019 db18s_dbrm_3705.trc
-rw-r----- 1 oracle oinstall    1646  4月  3 10:50 2019 db18s_m003_4089.trm
-rw-r----- 1 oracle oinstall    7495  4月  3 10:50 2019 db18s_m003_4089.trc
-rw-r----- 1 oracle oinstall    1894  4月  3 10:50 2019 db18s_m002_4087.trm
-rw-r----- 1 oracle oinstall   11111  4月  3 10:50 2019 db18s_m002_4087.trc
-rw-r----- 1 oracle oinstall  234008  4月  3 10:50 2019 db18s_ora_5208_GG_DEBUG.trm
-rw-r----- 1 oracle oinstall 1339711  4月  3 10:50 2019 db18s_ora_5208_GG_DEBUG.trc
[oracle@dbvgg trace]$
```