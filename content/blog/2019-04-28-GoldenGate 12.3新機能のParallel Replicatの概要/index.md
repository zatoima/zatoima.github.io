---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGate 12.3新機能のParallel Replicatの概要"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-parallel-replicat-overview.html
date: 2019-04-28
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

従来のReplicatのモードは「Classic Replicat」と「Integrated Replicat」の2つでした。GoldenGateの12.3以降のバージョンからReplicatの新モードであるParalell Replicatが登場しました。この新しい特徴を確認する限り従来のモードで実現出来なかったこと（特に性能問題）を解決出来るのでは、と感じています。

本記事では、概略レベルを整理して、次回の記事で具体的な動作を確認したいと思います。

#### **概要**

- Parallel Replicatは、毎秒最大100万回以上の適用率を達成する、非常にスケーラブルな適用エンジンを備えています。

- Integrated Replicatよりも5倍高速

- 単一の大きなトランザクションを並行して適用

- データベース外での依存関係計算と並列処理

- 単一の大規模トランザクションを並列化する機能

- 大規模トランザクションを並列化している間も依存関係が考慮

- トランザクション分割サイズ（レコード数）を指定するSPLIT_TRANS_RECSパラメータによって制御される機能。 デフォルトは100,000です。

  > 参考
  >
  > http://www.oracle-scn.com/oracle-goldengate-parallel-replicat/

Classic Replicat、及びIntegrated Replicatの場合、大規模なトランザクション（数千万件を更新後に1度だけcommitされる場合等）はレプリケーション遅延が起こりやすい処理でした。

上記の「単一の大規模トランザクションを並列化する機能」や「Integrated Replicatよりも5倍高速」という製品メッセージが事実であれば性能的に高速化が見込めます。

#### **プロセス概略**

マッパーはパラレルに動作し、証跡の読取り、証跡レコードのマッピング、マップされたレコードの統合Replicat LCR形式への変換、および後続の処理のためのマージャへのLCRの送信を実行します。

マスター・プロセスにはコレータとスケジューラの2つのスレッドがあります。コレータはマスターからマップされたトランザクションを受け取り、依存関係の計算のために証跡の順序に戻します。スケジューラがトランザクション間の依存関係を計算し、トランザクションを独立したバッチにグループ化し、ターゲット・データベースに適用するためにバッチをアプライアに送信します。

別モードの統合Replicatの場合はこのプロセスが「Reader」となっており、パラレルではなくシリアルです。

<img src="images/image-20191121164644456.png" alt="image-20191121164644456" style="zoom:50%;" />

#### 参考

こちらはIntegrated Repliatの場合です。Applierがパラレル化されるのは同一ですが、Applier以前のアーキテクチャが大きく違います。

<img src="images/image-20191121164655589.png" alt="image-20191121164655589" style="zoom:50%;" />

#### **プロセス作成方法**

従来通りプロセス自体はADD Replicatコマンドで作成します。

```sh
ggsci > ADD REPLOCAT R1 ,　INTEGRATED ,　PARALLEL ,　EXTTRAIL　./dirdat/ra　checkpointtable ggadmin.ggs_checkpoint
```

#### **使用するパラメータ**

| パラメータ                                     | 説明                                                         |
| :--------------------------------------------- | :----------------------------------------------------------- |
| `MAP_PARALLELISM`                              | マッパーの数を構成します。これは証跡ファイルを読み取るために使用されるスレッドの数を制御します。最小値は`1`、最大値は`100`、デフォルトは`2`です。 |
| `APPLY_PARALLELISM`                            | アプライアの数を構成します。これは変更を適用するために使用されるターゲット・データベースの接続の数を制御します。デフォルト値は4です。 |
| `MIN_APPLY_PARALLELISM``MAX_APPLY_PARALLELISM` | 並列化の適用が自動チューニングされます。最小値と最大値を設定して、Replicatが並列化を自動的に調整する範囲を定義できます。デフォルト値はありません。`APPLY_PARALLELISM`と同時に使用*しないでください*。 |
| `SPLIT_TRANS_REC`                              | 大きなトランザクションを指定のサイズのピースに分割して、パラレルに適用するように指定します。ピース間の依存関係は保持されます。デフォルトでは無効です。 |
| `COMMIT_SERIALIZATION`                         | `FULL`直列化モードのコミットを有効にし、証跡の順序でトランザクションを強制的にコミットします。 |
| **高度なパラメータ**                           |                                                              |
| `LOOK_AHEAD_TRANSACTIONS`                      | トランザクションをバッチ化するときに、スケジューラがどの程度先まで対象にするかを制御します。デフォルト値は10000です。 |
| `CHUNK_SIZE`                                   | 並列Replicatで、どの程度の大きさのトランザクションを大きいトランザクションとみなすかを制御します。並列Replicatは、このサイズより大きいトランザクションを検出すると、そのトランザクションをシリアライズするためにパフォーマンスが低下します。ただし、この値を大きくすると、並列Replicatによって消費されるメモリーも増加します。 |

#### **その他注意事項**

•Integrated Parallel Replicatの場合、COMMIT_SERIALIZATIONのFULLモードはサポートされていません。使用できるモードはデフォルトのDEPENDENTになります。

•DBのバージョンはターゲットが12.2以降である必要があります。

•並列Replicatは完全なメタデータを持つ証跡からのデータ・レプリケーションのみをサポートします。したがって、ソース側はGG12.2以降のバージョンを使用する必要があります。