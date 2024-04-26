---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle GoldenGateの仮想メモリの使い方を整理する"
subtitle: ""
summary: " "
tags: ["GoldenGate","Oracle"]
categories: ["GoldenGate","Oracle"]
url: goldengate-vmemory-use.html
date: 2019-04-20
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

GoldenGateもOS上で動作するミドルウェアなので物理メモリ/仮想メモリを使用します。

GoldenGateはコミットされたトランザクションのみをレプリケートするため、トランザクションのコミットまたはロールバックを受信するまで、*キャッシュ*と呼ばれる`管理仮想メモリー・プール`に各トランザクションの操作を保持する必要があります。ここで述べているのは物理メモリではなく仮想メモリです。ご注意ください。

本記事で明示的に指定していない場合は、メモリという言葉は仮想メモリを指します。

GoldenGateプロセスによって使用される物理メモリーの実際の量は、オペレーティング・システムによって制御されます。

具体的なメモリの使い方と使用されるスワップ容量については本記事では扱いません。

#### **必要な仮想メモリ量について**

仮想メモリの見積もり式は下記の通りマニュアルに記載があります。

> https://docs.oracle.com/cd/E74358_01/gg-winux/GWURF/GUID-B910F3D9-E41C-4335-AC0A-442435481A19.htm
>
> CACHEMGR

```
1. 1つのExtractプロセスおよび1つのReplicatプロセスを起動します。
2. GGSCIを実行します。
3. 実行中の各プロセスのレポート・ファイルを表示し、PROCESS VM AVAIL FROM OS (min)行を探します。
4. 必要な場合、各値を次の整数(GB)に切り上げます。たとえば、1.76GBの場合は2GBに切り上げます。
5. 繰り上げられたExtractの値に、Extractプロセスの数を掛けます。
6. 繰り上げられたReplicatの値に、Replicatプロセスの数を掛けます。
7. 2つの結果に、システム上のOracle GoldenGateプロセスおよびその他のプロセスで必要とする追加スワップ領域を足します。

(PROCESS_VM x number_Extracts) + (PROCESS_VM x number_Replicats) + (swap_for_other_processes) = max_swap_space_on_system

この合計が、これらのプロセスに必要な最大スワップ領域になります。すべてのOracle GoldenGateプロセスが使用する実際の物理メモリー量は、Oracle GoldenGateプロセスではなく、オペレーティング・システムによって制御されます。グローバル・キャッシュ・サイズは、CACHEMGRのCACHESIZEオプションで制御します。
```

#### **仮想メモリ動作**

下記はプロセス起動時にレポートファイルに出力されるメモリの統計値です。

```
CACHEMGR virtual memory values (may have been adjusted)
CACHEPAGEOUTSIZE (default):               4M
PROCESS VM AVAIL FROM OS (min):           2G
CACHESIZEMAX (strict force to disk):   1.74G
```

仮想メモリ上限値を設定したい場合、CACHESIZEパラメータを設定します。これはプロセスがトランザクション・データのキャッシュに使用できる仮想メモリーの弱い制限を示します。これは、PROCESS VM AVAIL FROM OS (min)の値に基づいて動的に決定されます。CACHEMGRのCACHESIZEオプションを使用して制御できます。トランザクション・データのキャッシングにできる仮想メモリー量(キャッシュ・サイズ)の弱い制限を指定するため、トランザクションによってはこのサイズを超えてメモリを使用するケースも存在します。この場合、上限値は上記の統計値で言うところの `CACHESIZEMAX`が上限となります。

次に、PROCESS VM AVAIL FROM OS (min)は、このプロセスが使用可能と判断したおおよその仮想メモリー量を示します。内部的な理由で、この量はオペレーティング・システムによって使用可能と表示される量より少ない場合があります。

CACHESIZEMAX (strict force to disk)は、PROCESS VM AVAIL FROM OSおよびCACHESIZEから導出されます。通常は、現在仮想メモリー・バッファが特定の内部値を超えているトランザクションのみがページングの候補です。メモリー・リクエストの合計がCACHESIZEの値を超えると、キャッシュ・マネージャはディスクに書き込むトランザクションを探し、ページング候補のリストからトランザクションを選択します。ページング候補のトランザクションがすでにディスクにページングされていて、使用中の仮想メモリーがCACHESIZEMAX (strict force to disk)を超えている場合は、追加のバッファを必要とするすべてのトランザクションをページング候補にできます。このような方法で、常に仮想メモリーの可用性が確保されています。

メモリ使用の上限を超える場合 GoldenGateインストール・ディレクトリの`dirtmp`サブディレクトリにトランザクション・データがスワップされます。

ロングトランザクションが実行される場合は設定しているCACHESIZE次第ですが、ディスクにスワップされる可能性が高いでディスク容量にも注意が必要と思われます。

#### **SEND EXTRACT <Capture名>, CACHEMGR CACHESTATSについて**

仮想メモリの使用状況について確認したい場合は下記コマンドを実行します。

多くの情報が出力されますが、「CACHE OBJECT MANAGER statistics」セクションを見てどのようなメモリ動作になっているか確認すれば良いと思います。ファイルキャッシュに関する情報は「CACHE File Caching」で確認可能です。

```
GGSCI (dbvgg.jp.oracle.com as ggs@db112s) 40> SEND EXTRACT c11, CACHEMGR CACHESTATS

Sending CACHEMGR request to EXTRACT C11 ...

CACHE OBJECT MANAGER statistics

CACHE MANAGER VM USAGE
vm current     =      0    vm anon queues =      0
vm anon in use =      0    vm file        =      0
vm used max    =   1.27G   ==> CACHE BALANCED

CACHE CONFIGURATION
cache size            =   1G   cache force paging = 1.74G
buffer min            =  64K   buffer max (soft)  =   4M
pageout eligible size =   4M

================================================================================
RUNTIME STATS FOR SUPERPOOL

CACHE Transaction Stats
trans active    =      0    max concurrent =    238
non-zero total  =      1    trans total    =  42.58K

CACHE File Caching
filecache rqsts        =    129    bytes to disk      =   8.20G
file retrieves         =   2.08K   objs filecached    =      1
queue entries          =    129    queue processed    =    130
queue entry not needed =      0    queue not signaled =      0
fc requesting obj      =      0

CACHE MANAGEMENT
buffer links   =   2.06K  anon gets   =      0
forced unmaps  =     39   cnnbl try   =    200
cached out     =    114

```

想定より多く仮想メモリを使用していることを疑われる場合は`CACHE MANAGER VM USAGE` を優先的に確認するのが良いと思います。

```
CACHE MANAGER VM USAGE
vm current = 1015M vm anon queues = 320M
vm anon in use = 692M vm file = 3M
vm used max = 1G ==> CACHE BALANCED
```

##### **各項目の補足説明**

- vm current : 現在割当てられている仮想メモリサイズ総量(メモリ＋ページング)
- vm anon queues : vm current のうち、フリーなメモリサイズ(使用されなくなったメモリをフリーなメモリとして一旦キューに保持しているサイズ)
- vm anon in use : 現在処理で利用中の仮想メモリサイズ総量
- vm file : 現在ページングしているサイズ
- vm used max : これまでに利用された仮想メモリサイズ総量の最大サイズ