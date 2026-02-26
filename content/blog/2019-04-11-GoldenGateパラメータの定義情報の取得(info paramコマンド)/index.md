---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGateパラメータの定義情報の取得(info paramコマンド)"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-info-param.html
date: 2019-04-11
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

info paramコマンドを使用するとGoldenGateのパラメータ定義情報を取得可能です。本機能はGoldenGate12.2のバージョンから使用可能です。

マニュアルはこちら

> https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-60208072-8E74-4703-B4FF-31761E6CDDC0.htm#GUID-60208072-8E74-4703-B4FF-31761E6CDDC0
>
> INFO PARAM
>
> INFO PARAMでは、パラメータ定義情報を取得します。名前が複数のレコードに一致した場合、一致したレコードがすべて表示されます。問合せパラメータに子オプションがある場合、各子オプションの名前が「Options」タブにリストされていても、出力には表示されません。オプションのレコード全体を表示するには、parameter.optionという形式の完全名を個別に問い合せる必要があります。

#### **基本的な使い方**

下記のようにパラメータ、及びパラメータのサブ・パラメータの情報を取得することが出来ます。

```sql
GGSCI (dbvgg.jp.oracle.com) 3> info param BATCHSQL

param name  : batchsql
description : Use the BATCHSQL parameter to increase the performance of Replicat. BATCHSQL causes Replicat to organize similar SQL statements into arrays and apply them at an accelerated rate. In its normal mode, Replicat applies one SQL statement at a time.
argument    : no argument
options     : batcherrormode|nobatcherrormode, batchesperqueue, batchtransops
              bypasspkcheck|nobypasspkcheck, bytesperqueue
              checkuniquekeys|nocheckuniquekeys
              errorhandling|noerrorhandling, maxthreadqueuedepth, opsperbatch
              opsperqueue, thread, trace
component(s): REPLICAT
mode(s)     : all Replicat modes
platform(s) : all platforms
versions    :
database(s) : Oracle 8
              Oracle 9i
              Oracle 10g
              Oracle 11g
              Oracle 12c
              Oracle 18c
              Sybase
              DB2LUW 10.5
              DB2LUW 10.1
              DB2LUW 9.5
              DB2LUW 9.7
              Teradata
              Timesten
              DB2 for i
              DB2 for i Remote
              MS SQL
              MS SQL CDC
              Informix
              SQL/MX
              DB2 z/OS
              PostgreSQL
status      : current
mandatory   : false
dynamic     : false
relations   : none


GGSCI (dbvgg.jp.oracle.com) 4> info param BATCHSQL.opsperbatch

param name  : batchsql.opsperbatch
description : Sets the maximum number of row operations that one batch can contain. After OPSPERBATCH is reached, a target transaction is executed.
argument    : integer
default     : 1200
      range : 1 - 100000
options     :
component(s): REPLICAT
mode(s)     : all Replicat modes
platform(s) : all platforms
versions    :
database(s) : Oracle 8
              Oracle 9i
              Oracle 10g
              Oracle 11g
              Oracle 12c
              Oracle 18c
              Sybase
              DB2LUW 10.5
              DB2LUW 10.1
              DB2LUW 9.5
              DB2LUW 9.7
              Teradata
              Timesten
              DB2 for i
              DB2 for i Remote
              MS SQL
              MS SQL CDC
              Informix
              SQL/MX
              DB2 z/OS
              PostgreSQL
status      : current
mandatory   : false
dynamic     : false
relations   : none

```

#### **出力内容**

下記のような出力結果が出力されます。

| No.  | 項目        | 補足                                                         |
| ---- | ----------- | ------------------------------------------------------------ |
| 1    | param name  | パラメータ名                                                 |
| 2    | description | パラメータ説明                                               |
| 3    | argument    | 引数                                                         |
| 4    | options     | サブパラメータ                                               |
| 5    | component   | 対応コンポーネント<br />   (「capture」 or 「data pump」 or 「replicat」) |
| 6    | mode        | Integratedモード or classicモード                            |
| 7    | platform    | 対応プラットフォーム                                         |
| 8    | versions    | 対応バージョン                                               |
| 9    | database    | 対応データベース                                             |
| 10   | status      | current or deprecated                                        |
| 11   | mandatory   | 必須かどうか？                                               |
| 12   | dynamic     | 動的変更が可能か？                                           |
| 13   | relations   |                                                              |

#### **GoldenGateのバージョン間の出力差異を確認する**

GoldenGateの12.3以降のバージョンではSYSLOGパラメータが非推奨に変更されています。この変更がどのように出力結果に影響しているか確認してみます。

下記出力結果の「★」印箇所のように「deprecated」に変更されています。GGのアップデート時にパラメータをチェックするのも良いかもですね。

#### **GoldenGate 12.2.0.1の出力結果**

```sql
[oracle@dbvgg ~]$ ogg1

Oracle GoldenGate Command Interpreter for Oracle
Version 12.2.0.1.170919 OGGCORE_12.2.0.1.0OGGBP_PLATFORMS_171030.0908_FBO
Linux, x64, 64bit (optimized), Oracle 11g on Oct 30 2017 19:19:45
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2017, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> info param syslog

param name  : syslog
description : Use the SYSLOG parameter to control the types of messages that Oracle GoldenGate sends to the system logs on a Windows or UNIX system, or to the SYSOPR message queue on an IBM i system.
argument    : no argument
options     : all, error, info, none, warn
component(s): MGR
              GLOBALS
mode(s)     : none
platform(s) : all platforms
versions    :
    min ver : 11.1.1
database(s) : all supported databases (on the supported platforms).
status      : current ★←「current」
mandatory   : false
dynamic     : false
relations   : none


GGSCI (dbvgg.jp.oracle.com) 2>

```

#### **GoldenGate 18.1の出力結果**

```sql
[oracle@dbvgg ~]$ ogg2

Oracle GoldenGate Command Interpreter for Oracle
Version 18.1.0.0.0 OGGCORE_18.1.0.0.0_PLATFORMS_180928.0432_FBO
Linux, x64, 64bit (optimized), Oracle 18c on Sep 29 2018 07:21:38
Operating system character set identified as UTF-8.

Copyright (C) 1995, 2018, Oracle and/or its affiliates. All rights reserved.



GGSCI (dbvgg.jp.oracle.com) 1> info param syslog

param name  : syslog
description : Use the SYSLOG parameter to control the types of messages that Oracle GoldenGate sends to the system logs on a Windows or UNIX system, or to the SYSOPR message queue on an IBM i system.
argument    : no argument
options     : all, error, info, none, warn
component(s): MGR
              GLOBALS
mode(s)     : none
platform(s) : all platforms
versions    :
    min ver : 11.1.1
database(s) : all supported databases (on the supported platforms).
status      : deprecated ★←「deprecated」に変更されている
mandatory   : false
dynamic     : false
relations   : none


GGSCI (dbvgg.jp.oracle.com) 2>

```