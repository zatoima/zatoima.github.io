---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLのIO料金について"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-aurora-cost-io-input-output.html
date: 2021-06-04
lastmod : 2022-02-02
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

Auroraのコストは大きく下記の4つに分類される。RDS PostgreSQL等の他のRDBMS系のデータベースサービスはIO料金が掛からず、それもあってかAuroraのIO料金は見積もりにも見落としがちとなる。（IO料金についてはインスタンス料金の数％から高くても10％に収まる感触を持っているが、データベースの使い方によっては高い料金になる可能性もある。）

1. インスタンス料金
2. データベースストレージ
3. IO料金
4. データ転送量

詳細は下記をご参照。クローニングやグローバルデータベースの利用料については使い方によるので省略。

> 料金 - Amazon Aurora | AWS https://aws.amazon.com/jp/rds/aurora/pricing/

東京リージョンのIO料金については`0.24USD/100 万リクエスト`となる。また、各データページで最大 4KB の変更に対して 1 回の I/O オペレーションを課金される。仮に秒間2000IOPS発生するワークロードあった場合の月額費用は下記で計算される。（なお、秒間2,000IOPSというワークロードはあくまでも目安として。）

```
1,000 Reads/Second + 1,000 Writes/Second = 2,000 Number of I/Os per second
2,000 I/Os per second x 730 hours x 60 minutes x 60 Seconds = 5,256,000,000 Number of I/Os per month
5,256,000,000 x 0.00000024 USD = 1,261.44 USD (I/O Rate Cost)
```

なお、料金自体はPricing Calculatorで計算出来る。

- [AWS Pricing Calculator](https://calculator.aws/#/createCalculator/AuroraPostgreSQL)
  - https://calculator.aws/#/createCalculator/AuroraPostgreSQL

AuroraのIO料金が高いときには下記を確認する。

- CloudWatchで`Billed IOPS`を確認する
  - スパイクしている際にどんなオペレーションをやっているか確認してIO量を減らせないか確認する
    - pg_dump、バッチ処理、フルスキャン等
- `Performance Insights `で `IO: DataFileRead` や `IO:DataFilePrefetch` あたりが発生しているSQLを確認する
- バッファキャッシュヒット率を確認する
  - データファイルI/Oが発生しているのでオンメモリになるようにパラメータを調整

IO料金を下げるためのアクションとしては下記が中心となる

- メモリを大きくしてオンメモリで処理出来るようにする
- フルスキャン系のSQLをチューニングする
- インデックスやパーティションを使って不要なIOを削減する

### 追記（2022/02/02)

次の記事も参考になる、というか2022年1月に公式から出たAWS Database Blogをしっかり読んだ方が良い。

・[Planning I/O in Amazon Aurora \| AWS Database Blog](https://aws.amazon.com/jp/blogs/database/planning-i-o-in-amazon-aurora/)



