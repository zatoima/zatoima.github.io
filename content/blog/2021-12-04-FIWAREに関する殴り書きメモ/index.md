---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "FIWAREに関する殴り書きメモ"
subtitle: ""
summary: " "
tags: ["fiware"]
categories: ["fiware"]
url: fiware-about-memo
date: 2021-12-04
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



### FIWARE とは何か

分野横断的なデータ流通に主眼を置いたデータ管理基盤となり、スマートシティのための都市OSとも呼ばれる。

データ管理基盤と言われている通り、ただのインフラではなく、データマネジメントで必要と言われる多くの要素をコンポーネント単位に構築出来るようだ。

コアコンポーネントやデータカタログを扱うCKAN、データ可視化のためのGrafana等も使える模様。IoTデバイスからデータを受け取って可視化する機能もある。データのやり取りを行う中心はコンテキストブローカーであり、Pub/Sub的なデータのやり取りを行うことが出来る。担当するのはOrionというコンポーネントの模様。

結果的に都市に関する情報の生成、収集、公開、消費というのが出来る代物。都市を強調しているのは何故だろうか？

### 意義

都市OSに限らず、システム間連携は統一的な規格がないことが問題になりうる。また、米国はビックプラットフォーマーが存在し、データの囲い込みが行われつつある一方、欧州や日本等はオープンソースやFIWAREにおけるNGSI等の規格を使うことでエコシステムを作ろうとしているという見方もあるようだ。データを収集・蓄積するために規格を統一し、エコシステムを作って共栄していくことを目指す

エコシステムという言葉：複数の企業が商品開発や事業活動などでパートナーシップを組み、互いの技術や資本を生かしながら、業界の枠や国境を超えて広く共存共栄していく仕組み

### FIWAREで実現出来ること

- 相互運用
- データ流通
- 拡張性

データ活用やデータを扱う際にはDMBOKが参考になるが、DMBOKではデータガバナンスに関連する分野としてメタデータ管理やデータ連携、相互運用性、データモデリング、データアーキテクチャ等が記載されている。このあたりに対しても一部が有効らしい。様々なシステムと連携する場合は、どのようにデータを連携するか、フォーマットやファイル形式はどうするかのデータモデリング等を考える必要があるが、FIWAREではある程度決まったフレームワークで処理出来るように決まっている。

- NGSIデータモデル
- オープンAPI
- 共通API

NGSI（Next Generation Service Interfaces）という国際標準規格を使ってデータのやり取りを行うこととなるが、（珍しく？）日本によって策定されたようだ。（標準化自体は欧州の団体）

データ連携のためのインターフェースとデータ格納時のデータモデルを定義している。データモデルでは「エンティティ（実体）」と、その属性情報であるコンテキスト情報から構成され、異なるアプリケーション同士でのデータ連携を行えるようにしている。データのセマンティクスは FIWARE Data Modelsとなる。

### 学ぶためには

正直調べてみてもよくわからないので、手っ取り早く学ぶために下記のチュートリアルをやったりした方が良さそう

https://github.com/FIWARE/tutorials.Getting-Started/blob/master/README.ja.md

### 参考

- [官民データ活用共通プラットフォームの取り組み](https://www.sci-japan.or.jp/vc-files/member/secure/speakers/20201130.pdf?utm_source=pocket_mylist)
- [誰でもできるスマートシティ向けOSS : FIWAREのはじめかた](https://www.slideshare.net/ShunsukeKikuchi1/oss-fiware?utm_source=pocket_mylist)
- [NGSI v2 まとめ \- Qiita](https://qiita.com/NKGWM/items/603bc49da608a12d257d)
- [SIPサイバー/アーキテクチャ構築及び実証研究の成果公表](https://www8.cao.go.jp/cstp/stmain/a-1-1_200318.pdf)