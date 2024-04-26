---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "expdp時にFLASHBACK_SCNを使用した場合のインスタンス化SCNについて"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-flashbackscn-instantiationSCN.html
date: 2019-03-30
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

GoldenGateにはインスタンス化SCNという機能があります。この機能を使用するとDatapumpを使用したシステム無停止の初期移行が簡単に出来ます。

詳細は下記のqiita記事がわかりやすいのでご確認ください。

インスタンス化SCNを使ってお手軽初期移行 - Qiita https://qiita.com/kurouuuron/items/118afdc6b6d15d46e7dd

> Oracle Datapump との連携を強化した、GoldenGateの初期移行用の機能。
>
> 一言でいえば、Datapumpを使用したシステム無停止の初期移行が簡単にできる、という機能。
>
> もう少し言えば、Flashback_scnやHandlecollisionsなどの初期移行で考慮すべきポイントを考慮せずによくしてくれた機能。
>
> 実際の挙動としては、Datapumpでexpdpした際に、その表はどのSCNまで反映し終わっているか、というデータを内部的に付与してくれて、impdpしたらReplicatがそのSCN以降のデータから自動で当ててくれる、というもの。

この記事にもあるようにGoldenGate12.2以上でadd trandataを実行した場合にpreparescnがデフォルトで付与されるためDatapumpでexpdpした際に、その表はどのSCNまで反映し終わっているか、というデータを内部的に付与してくれます。

#### **環境の前提**

add trandata preparecsn noneを指定した場合の動作になります。

none以外を設定した場合は下記の内容は異なる場合がありますのでご注意ください。

#### **add trandata preparescn noneをした場合の動作**

[マニュアル](https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-D3FD004B-81E4-4185-92D3-812834A5DEFC.htm)に記載があるとおり、この場合はインスタンス化の準備は行われません。

**ソース側でのエクスポート**

```sh
[oracle@xxxxxxxx1p ~]$ expdp ggtest/xxxxxx DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES

Export: Release 11.2.0.4.0 - Production on 日 3月 3 16:47:00 2019

Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

接続先: Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, Real Application Clusters, Automatic Storage Management, OLAP,
Data Mining and Real Application Testing options
FLASHBACKでは、データベース整合性が自動的に維持されます。
"GGTEST"."SYS_EXPORT_TABLE_01"を起動しています: ggtest DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES
BLOCKSメソッドを使用して見積り中です...
オブジェクト型TABLE_EXPORT/TABLE/TABLE_DATAの処理中です
BLOCKSメソッドを使用した見積り合計: 384 KB
. . "GGTEST"."T10"                              288.6 KB   10000行がエクスポートされました
マスター表"GGTEST"."SYS_EXPORT_TABLE_01"は正常にロード/アンロードされました
******************************************************************************
GGTEST.SYS_EXPORT_TABLE_01に設定されたダンプ・ファイルは次のとおりです:
  /home/oracle/t10.dmp
ジョブ"GGTEST"."SYS_EXPORT_TABLE_01"が日 3月 3 16:47:04 2019 elapsed 0 00:00:02で正常に完了しました

```

#### **ターゲット側のインポート**

```sh
[oracle@xxxxxx ~]$ impdp ggtest/xxxxxx@xxxxxxxx1 DIRECTORY=homedir DUMPFILE=t10.dmp tables=t10

Import: Release 18.0.0.0.0 - Production on 日 3月 3 16:48:33 2019
Version 18.4.0.0.0

Copyright (c) 1982, 2018, Oracle and/or its affiliates.  All rights reserved.

接続先: Oracle Database 18c Enterprise Edition Release 18.0.0.0.0 - Production
マスター表"GGTEST"."SYS_IMPORT_TABLE_01"は正常にロード/アンロードされました
"GGTEST"."SYS_IMPORT_TABLE_01"を起動しています: ggtest@xxxxxxxx1 DIRECTORY=homedir DUMPFILE=t10.dmp tables=t10
オブジェクト型TABLE_EXPORT/TABLE/TABLE_DATAの処理中です
. . "GGTEST"."T10"                              288.6 KB   10000行がインポートされました
ジョブ"GGTEST"."SYS_IMPORT_TABLE_01"が日 3月 3 16:48:45 2019 elapsed 0 00:00:09で正常に完了しました
```

#### **インスタンス化SCNの確認**

preparescn noneのため、この場合はインスタンスSCN化されていません。

```sh
SQL> select source_database,source_object_owner,source_object_name,instantiation_scn from  DBA_APPLY_INSTANTIATED_OBJECTS where SOURCE_OBJECT_NAME='T10';

行が選択されていません
```

#### **expdp時にFLASHBACK_SCNを使用した場合**

ここでようやく表題の件ですが、このケースはtrandata時にpreparecsn noneに設定した場合においてもインスタンス化SCNがexpdp時に設定される動作のようです。

#### **エクスポート時のコマンド**

ここで特定時点のFLASHBACK_SCNを指定します。

```sh
[oracle@xxxxxxxx1p ~]$ expdp ggtest/xxxxxx DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES FLASHBACK_SCN=25587768

Export: Release 11.2.0.4.0 - Production on 日 3月 3 16:59:04 2019

Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

接続先: Oracle Database 11g Enterprise Edition Release 11.2.0.4.0 - 64bit Production
With the Partitioning, Real Application Clusters, Automatic Storage Management, OLAP,
Data Mining and Real Application Testing options
FLASHBACKでは、データベース整合性が自動的に維持されます。
"GGTEST"."SYS_EXPORT_TABLE_01"を起動しています: ggtest DIRECTORY=homedir DUMPFILE=t10.dmp TABLES=t10 CONTENT=DATA_ONLY REUSE_DUMPFILES=YES FLASHBACK_SCN=25587768
BLOCKSメソッドを使用して見積り中です...
オブジェクト型TABLE_EXPORT/TABLE/TABLE_DATAの処理中です
BLOCKSメソッドを使用した見積り合計: 384 KB
. . "GGTEST"."T10"                              288.6 KB   10000行がエクスポートされました
マスター表"GGTEST"."SYS_EXPORT_TABLE_01"は正常にロード/アンロードされました
******************************************************************************
GGTEST.SYS_EXPORT_TABLE_01に設定されたダンプ・ファイルは次のとおりです:
  /home/oracle/t10.dmp
ジョブ"GGTEST"."SYS_EXPORT_TABLE_01"が日 3月 3 16:59:08 2019 elapsed 0 00:00:02で正常に完了しました

```



FLASHBACK_SCN を指定してexpdpしたdmpファイルをimpdpした場合、 DBA_APPLY_INSTANTIATED_OBJECTS は INSTANTIATION_SCNが設定されています。

```sh
SQL> select source_database,source_object_owner,source_object_name,instantiation_scn from  DBA_APPLY_INSTANTIATED_OBJECTS where SOURCE_OBJECT_NAME='T10';
SOURCE_DATABASE   SOURCE_OBJECT_OWNER   SOURCE_OBJECT_NAME     INSTANTIATION_SCN
xxxxxxx           GGTEST                T10                             25587768 ←★INSTANTIATION_SCNが設定されている
```

#### **まとめ**

add trandata時にpreparecsn noneを設定した場合においてもexpdp時にFLASHBACK_SCNを使用した場合はインスタンス化SCNが設定されるという動作になります。

この動作についてですが、streamsのマニュアルに記載があります。合わせてご確認ください。

> https://docs.oracle.com/cd/E16338_01/server.112/b61352/instant.htm#CIHBDFJE
>
> エクスポート中、Oracle Data Pumpでは、データベース・オブジェクトごとにエクスポートされたデータおよび手続き型操作が特定の時点で一貫性を持つように、自動的にOracle Flashbackが使用されます。Oracle Streams環境でインスタンス化を実行する場合は、ある程度の一貫性が必要です。データ・ポンプ・エクスポート・ユーティリティを使用すると、Oracle Streamsのインスタンス化についてこの一貫性を確保できます。
>
> Oracle Streamsのインスタンス化のみでなく、他の用途にもエクスポート・ダンプ・ファイルを使用しており、その用途がデータ・ポンプのデフォルトのエクスポートで得られる一貫性より厳密な一貫性要件を伴う場合は、Oracle Streamsのインスタンス化にデータ・ポンプ・エクスポート・ユーティリティ・パラメータ`FLASHBACK_SCN`または`FLASHBACK_TIME`を使用できます。たとえば、エクスポートに外部キー制約を持つオブジェクトが含まれている場合、より厳密な一貫性が要求される場合があります。