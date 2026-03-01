---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "CloudTrailのデータイベントはマネージメントコンソール上からは確認出来ない"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-cloudtrail-dataevent-athena
date: 2021-11-25
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bottで
---



ハマったことのメモです。

### データイベントとは？

- [20210119\_AWSBlackbelt\_CloudTrail\.pdf](https://d1.awsstatic.com/webinars/jp/pdf/services/20210119_AWSBlackbelt_CloudTrail.pdf)

![image-20211125131604361](image-20211125131604361.png)

### ハマってしまったこと

デフォルトではデータイベントは記録されないという事実は知っていたが、データイベントがマネージメントコンソール上に出力されないという事実を知らず、時間が掛かってしまった。（CloudTrailの情報は普段Athenaで検索するが、この時はマネージメントコンソールのイベント履歴から見ようとして出て来ず、なんで？と思ってた）

マニュアルや公式のガイド的には下記の通り。

> [証跡での管理イベントの記録 \- AWS CloudTrail](https://docs.aws.amazon.com/ja_jp/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html)
>
> CloudTrail の [**イベント履歴**] 機能では、管理イベントのみサポートされています。すべての管理イベントがイベント履歴に表示されるわけではありません。

> [CloudTrail のデータおよび管理イベントについて](https://aws.amazon.com/jp/premiumsupport/knowledge-center/cloudtrail-data-management-events/?utm_source=pocket_mylist)
>
> デフォルトでは、CloudTrail の[データイベント](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#logging-data-events)は無効になっています。追加料金をお支払いいただくことで、ログ記録を有効にできます。データイベントは、データプレーンオペレーションとも呼ばれ、しばしば大量の処理を含みます。データイベントは CloudTrail イベント履歴での表示はできません。
>
> Athena を使用すると、Amazon S3 バケットに保存されているログファイルから、90 日を超えた CloudTrail のデータおよび管理イベントが表示できます

### 解決策

データイベントを見たい場合は、AthenaでCloudTrailを検索しましょう

- [AthenaでCloudTrail の証跡を分析 \| my opinion is my own](https://zatoima.github.io/aws-cloudtrail-athena-analyze-query/)