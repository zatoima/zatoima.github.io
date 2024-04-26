---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "フル・トランスポータブル表領域実施時にORA-31633、ORA-01647で失敗する"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-full-tts-oraerror.html
date: 2019-04-12
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

フル・トランスポータブル・エクスポート/インポート機能を使用すると、データベース全体を異なるデータベース・インスタンスに移動できます。

データベース全体のデータを移行できるので、移行先のデータベースでインデックスや各種オブジェクト（プロシージャ・パッケージ…etc）を別途作成する必要がありません。

また、トランスポータブル表領域（TTS）と同様にデータファイルは物理コピーが可能ですので、中間ファイル作成等の操作が必要ありません。Data Pumpと比較すると高速な手法と言えます。（メタデータは別途エクスポートが必要です。）

下記のホワイトペーパーも合わせてご確認ください。

> https://www.oracle.com/technetwork/jp/database/enterprise-edition/full-transportable-wp-12c-1973971-ja.pdf
>
> \> Oracle Database 12c：フル・トランスポータブル・エクスポート/インポート

#### **手順概要**

> 1) ソース・データベースで、各ユーザー定義表領域を読取り専用モードにし、データベースをエクスポートします。
>
> ・次のパラメータが指定された値に設定されていることを確認します。
>   TRANSPORTABLE=ALWAYS
>   FULL=Y
> ・ソース・データベースがOracle Database 11g リリース2 (11.2.0.3)またはOracle Database 11g以上の
> データベースである場合、VERSIONパラメータを12以上に設定する必要があります。
> ・ソース・データベースに暗号化された表領域、または暗号化された列を含む表が格納された表領域が含まれている場合は、ENCRYPTION_PWD_PROMPT=YESを指定するか、ENCRYPTION_PASSWORDパラメータを指定する必要があります。
> ・エクスポート・ダンプ・ファイルには、ユーザー定義表領域に格納されたオブジェクトのメタデータ、および管理表領域(SYSTEMやSYSAUXなど)に格納されたユーザー定義オブジェクトのメタデータとデータの両方が含まれています。



#### **エラー内容**

上記の手順概要の通り、ユーザ表領域を読み取り専用にして`TRANSPORTABLE=ALWAYS`、及び`FULL=Y`を指定してexpdpを実行したところ`ORA-31633`、及び`ORA-01647`が発生してエラーになります。

```sh
[oracle@dbvop]$ expdp DPUSR/oracle full=y transportable=always directory=dp_dir dumpfile=full_tts.dmp encryption_password=oracle logfile=full_tts_export.log

Export: Release 12.1.0.2.0 - Production on 水 3月 13 15:04:08 2019

Copyright (c) 1982, 2014, Oracle and/or its affiliates.  All rights reserved.

接続先: Oracle Database 12c Enterprise Edition Release 12.1.0.2.0 - 64bit Production
With the Partitioning, Real Application Clusters, Oracle Label Security, OLAP,
Advanced Analytics, Oracle Database Vault and Real Application Testing options
ORA-31626: ジョブが存在しません
ORA-31633: マスター表"DPUSR.SYS_EXPORT_FULL_07"を作成できません
ORA-06512: "SYS.DBMS_SYS_ERROR", 行95
ORA-06512: "SYS.KUPV$FT", 行1048
ORA-01647: 表領域'USERS'は読取り専用です。領域を割当てできません
```

#### **原因**

下記マニュアルの制限に引っ掛かったことが原因と考えられます。

> https://docs.oracle.com/cd/E57425_01/121/SUTIL/GUID-206EC89B-5E43-4CCF-8B78-2C7F91FC5D7D.htm
>
> TRANSPORT_TABLESPACES
>
> エクスポートを実行するユーザーのデフォルトの表領域を、転送対象となっている表領域のいずれかに設定することはできません。

ホワイトペーパーやマニュアルの手順では「system」ユーザで実行されており、systemユーザのデフォルト表領域は「SYSAUX」となります。

今回はData Pump専用の`DPUSR`で実行していました。このユーザは、「ユーザ表領域」をデフォルト表領域に設定していたため、エラーになりました。

#### **回避方法**

下記2つのどちらかです。

1. SYSやSYSTEMユーザで実行する
2. Data Pump専用のDPUSRのデフォルト表領域を一時的に「SYSAUX」に変更する