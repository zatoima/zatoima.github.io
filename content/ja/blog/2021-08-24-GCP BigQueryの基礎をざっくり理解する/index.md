---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GCP BigQueryの基礎をざっくり理解する"
subtitle: ""
summary: " "
tags: ["GCP","BigQuery"]
categories: ["GCP","BigQuery"]
url: gcp-bigquery-google-cloud-overview-basic
date: 2021-08-24
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

AWSで言えば、Athenaのような、、、Redshiftのような、、、Auroraのような、、サービスと理解した

## BigQueryの構成要素

- BigQueryマネージドストレージ
  - スケーラブルなデータ・ストレージ
- BigQuery Analysis
  - Dremelクエリエンジンテクノロジーに基づく並列SQLエンジン

## アーキテクチャ

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=15" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## データ格納方式

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=14" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## データの分散配置

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=17" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## クエリの並列処理

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=19" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## データ型

> https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=ja

## データの持ち方

BigQueryの場合、読み取り量に応じた課金が発生するので、積極的に使うことを検討。

- パーティション分割テーブル
  - パーティションプルーニング、パーティション単位でエクスポート等
- クラスタ化テーブル
  - クラスタリング列に基づいてデータ配置、並び順が調整

## スロット

処理の並列度で、デフォルトだと2000が上限。bigqueryの並列処理の速さはストレージの分散、スロット分散で実現しているが、スロット数がこの上限までスケールするとは限らないことには注意。CPUコア数を指しているわけでは無さそう。

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=50" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

> https://cloud.google.com/bigquery/docs/slots?hl=ja
>
> BigQuery スロットは、BigQuery で SQL クエリを実行するために使用される仮想 CPU です。BigQuery はクエリのサイズと複雑さに応じて、クエリごとに必要なスロットの数を自動的に計算します。

> Google BigQuery の知らない？世界 - Qiita https://qiita.com/AkiQ/items/9c5eefb7953409aa2eda
>
> 前述しましたSlotですが、デフォルトで[プロジェクトに対して最大2,000 Slot与えられます](https://cloud.google.com/bigquery/quotas#queries)。クエリーの爆速はSlot の並列処理により生み出していると言えます。Slotは、BigQuery のその時点で余っているリソースから割り当てるわけです、考えてみたら当たり前ですけど。Slotは基本的にグローバルリソースです。
> ということは、最大2,000 Slot使用できると言っていますが、使いたくても2,000 Slot同時に使用できるとは限らないのです。

## BigQueryの階層構造

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=20" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## コスト最適化に向けて

- BigQuery破産という話題が以前にあったが、大容量に対しての分析クエリになる場合、コスト面を気をつける必要がある
  - BigQuery におけるコスト最適化の ベスト プラクティス | Google Cloud Blog https://cloud.google.com/blog/ja/products/data-analytics/cost-optimization-best-practices-for-bigquery?utm_source=pocket_mylist

## 料金体系

> 料金  | BigQuery: クラウド データ ウェアハウス  | Google Cloud https://cloud.google.com/bigquery/pricing?hl=ja

- クエリ料金
- ストレージ料金

## 他クラウドからのデータ転送

データが無ければ分析基盤があってもどうしようも出来ない。`BigQuery Data Transfer Service for Amazon S3` を使用すると、Amazon S3 から BigQuery への定期的な読み込みジョブを自動的にスケジュール出来る。もちろん逆も然り。

> Amazon S3 転送  | BigQuery Data Transfer Service  | Google Cloud https://cloud.google.com/bigquery-transfer/docs/s3-transfer?hl=ja
>
> 『GCPからAWSへのデータ移動』について考えて＆まとめてみる | DevelopersIO https://dev.classmethod.jp/articles/data-migration-from-gcp-to-aws-matome/#a-4

## 参考

> BigQuery ドキュメント  | Google Cloud https://cloud.google.com/bigquery/docs
