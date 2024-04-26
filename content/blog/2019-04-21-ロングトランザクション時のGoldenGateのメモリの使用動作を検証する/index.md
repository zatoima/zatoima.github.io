---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ロングトランザクション時のGoldenGateのメモリの使用動作を検証する"
subtitle: ""
summary: " "
tags: ["GoldenGate"]
categories: ["GoldenGate"]
url: goldengate-longtransaction-memoryuse.html
date: 2019-04-21
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

以前、下記記事でGoldenGateのメモリの使い方について整理しました。

> Oracle GoldenGateの仮想メモリの使い方を整理する - zato logger https://www.zatolog.com/entry/goldengate-vmemory-use

実際にロングトランザクションを実行してどのようにメモリを使用するのかを見える化したいと思います。

#### **事前準備**

#### **CACHESIZEについて**

ソース側のCaptureに設定するCACHESIZEは「1GB」を設定しています。

#### **情報取得対象**

下記情報を1分ごとに取得するため簡易的なスクリプトを配置します。

取得する情報はこちらです。

| 取得先/取得コマンド                           | 取得情報                   |
| --------------------------------------------- | -------------------------- |
| v$sysstat                                     | REDO生成量                 |
| SEND EXTRACT <Capture名>, CACHEMGR CACHESTATS | キャッシュマネージャー統計 |
| info exttrail ./dirdat/c11/lt                 | Trailファイル情報          |

#### **情報取得スクリプト**

1回しか使わないので雑です。

```sh
#!/bin/bash

. "/home/oracle/.oraenv_db112s"

while :
do
    date
    sqlplus / as sysdba << EOF
        set pages 2000 lin 2000
        col name for a20
        select * from v\$sysstat where name = 'redo size';
    exit

    EOF

    /gg/gg1/ggsci << EOF
    info exttrail ./dirdat/c11/lt
    SEND EXTRACT c11, CACHEMGR CACHESTATS
    exit
    EOF

    ls -lth /gg/gg1/BR/C11/stale
    ls -lth /gg/gg1/dirtmp

    sleep 60
done
```

#### **ソース側で流すトランザクション**

一度もcommitせず、「20,000,000(2000万件)」ひたすらInsertを行います。貧弱な環境なのでUNDO表領域が枯渇やアーカイブログ領域やデータファイルのパンクの可能性がありますがトライしてみます。

```sql
create table memtest(a number primary key,b varchar2(30));

declare
v_c1 number;
v_c2 varchar2(30);
begin
dbms_random.seed(uid);
for i in 1..20000000
loop
v_c1 := i;
v_c2 := dbms_random.string('x', 16);
insert into reptest (a, b) values (v_c1, v_c2);
end loop;
commit;
end;
/
```



#### **実行結果**

`REDO更新量`、及び`vm current(MB`)、`byte to disk(MB)`をグラフ化しました。

<img src="images/image-20191121164246512.png" alt="image-20191121164246512" style="zoom:50%;" />

1. CHCHESIZEの1GBを上限に「vm current」が推移している。

   先日まとめた資料に`CACHESIZE`の上限値は弱い制限であり、トランザクションによっては`CACHEMAXSIZE`まで使用する可能性があると記載しました。今回のケースでは同様のトランザクション傾向のためこの弱い制限以上に仮想メモリを使用することは無さそうでした。

2. REDO生成量の「7~8割」がディスクのdirtmpにスワップしている。

   約30分更新し続けており、`REDO更新量(MB)`は右肩上がりです。それに合わせて`bytes to disk(MB)`も追従する形で右肩上がりとなっています。

   今回のケースでは約10GBのREDO生成量のロングトランザクションでしたが、実際の業務では大量バッチ更新等が行われる可能性があり、大量のREDO更新が見込まれます。どのくらいスワップ用のディレクトリを確保すべきか改めて考える必要があると思います。

3. 更新完了後の「vm current」が0に減っている

   ロングトランザクションが完了してcommitが発行後に`vm current(MB)`の値が0になっています。確保されていた仮想メモリが開放されていることがわかります。ちなみに過去どのくらいの仮想メモリを使用したかの最大値を知りたい場合は「vm used max」で確認が出来ます。

