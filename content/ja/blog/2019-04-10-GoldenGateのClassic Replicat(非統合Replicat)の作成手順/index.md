---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGateのClassic Replicat(非統合Replicat)の作成手順"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-classic-replicat-create.html
date: 2019-04-10
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



他記事でIntegrated Replicat(統合Replicat)のプロセス構成手順は記載しました。ただ、Classic Replicat（非統合Replicat）も使用することが多いので手順を記載します。

手順の違いはコマンドの引数（オプション）が変わるということとチェックポイント表の作成が必要ということです。内部的な動作は多く変わっているのでそこは別途注意が必要かと思います。

#### **ターゲット側にてClassic Replicatプロセスを作成**

#### **パラメータファイル作成**

```sh
. /home/oracle/.oraenv_db18s --環境変数の読み込み
cd /gg/gg2
./ggsci

#パラメータ作成
edit param r21

下記パラメータを設定する
----
REPLICAT R21
USERID c##ggs@db18p1,  PASSWORD oracle
DISCARDFILE ./dirrpt/r21.dsc, APPEND, MEGABYTES 500
DISCARDROLLOVER AT 2:00 ON SUNDAY
REPORTROLLOVER AT 2:00 ON SUNDAY

BATCHSQL
MAP ggtest.* ,TARGET db18p1.ggtest.*;
----

view param r21
```



#### **Replicatプロセスの作成**

```sh
#DBログイン
dblogin userid c##ggs@db18p1,password oracle

#Replicatプロセスの作成
add replicat r21, exttrail ./dirdat/d11/rt, CHECKPOINTTABLE c##ggs.ggs_ckpt

#チェックポイントファイルの作成
ADD CHECKPOINTTABLE c##ggs.ggs_ckpt
INFO CHECKPOINTTABLE c##ggs.ggs_ckpt
```

```sh
#実行結果
GSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 4> add replicat r11, exttrail ./dirdat/d11/rt, CHECKPOINTTABLE c##ggs.ggs_ckpt
REPLICAT added.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 5> add checkpointtable
ERROR: Missing checkpoint table specification.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 6>

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 6> ADD CHECKPOINTTABLE c##ggs.ggs_ckpt
Logon catalog name DB18P1 will be used for table specification DB18P1.c##ggs.ggs_ckpt.

Successfully created checkpoint table DB18P1.c##ggs.ggs_ckpt.

GGSCI (dbvgg.jp.oracle.com as c##ggs@db18s/DB18P1) 7> info checkpointtable c##ggs.ggs_ckpt
Logon catalog name DB18P1 will be used for table specification DB18P1.c##ggs.ggs_ckpt.

Checkpoint table DB18P1.c##ggs.ggs_ckpt created 2019-04-03 10:33:15.

```



各プロセスの作成手順のマニュアルはこちらです。

> https://docs.oracle.com/cd/E74358_01/gg-winux/GIORA/GUID-7065CF34-FD9A-4652-A34A-AE9F6BD3C87E.htm
>
> \> Replicatグループの追加

Classic Replicatを使用する場合はチェックポイント表の理解も重要です。こちらのマニュアルの記載をご参照ください。

> https://docs.oracle.com/cd/E74358_01/gg-winux/GIORA/GUID-B3EFA08D-145B-4806-B7E2-B8AE409C651C.htm#GUID-B3EFA08D-145B-4806-B7E2-B8AE409C651C
>
> \> チェックポイント表の作成(非統合Replicatのみ)
>
> https://docs.oracle.com/cd/E74358_01/gg-winux/GWUAD/GUID-D1ED9CCF-C81C-4CE2-8EAB-E4C8C7BDF58C.htm
>
> \> Oracle GoldenGateチェックポイント表