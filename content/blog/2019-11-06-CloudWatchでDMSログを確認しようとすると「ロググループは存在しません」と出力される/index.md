---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "CloudWatchでDMSログを確認しようとすると「ロググループは存在しません」と出力される"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-cloudwatchlogs-dms-log-error.html
date: 2019-11-06
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


### エラー内容

***

<img src="images/image-20191121221355387.png" alt="image-20191121221355387" style="zoom:50%;" />

上記の右下の「ログの表示」ボタンをクリックした場合、CloudWatch Logsに移動しますが、移動後の画面でエラーが発生しました。

```sh
ロググループは存在しません
ロググループ dms-tasks-dev-oracle-to-aurora-v2 が見つかりませんでした。このロググループが正しく作成されたことを確認し再試行してください。
```

### エラー原因

***

上記に記載がありますが、こちらが原因となっていました。ログを確認するためには、下記が必要です。

1. dms-cloudwatch-logs-role IAM ロールが作成されていること
2. 正しいアクセス許可ポリシーが設定されていること
3. AWS DMS がロールを引き受けるための正しい信頼関係が設定されていること

普通は AWS DMS コンソールを使用して最初の AWS DMS タスクを作成したときに自動的に作成されるみたいです。

### 対応方法

***

下記のどちらかを参照して実行ください。

> CloudWatch Logs が AWS DMS タスクに表示されない場合のトラブルシューティング https://aws.amazon.com/jp/premiumsupport/knowledge-center/dms-cloudwatch-logs-not-appearing/

> AWS CLI と AWS DMS API で使用する IAM ロールを作成する - AWS DATABASE MIGRATION SERVICE HTTPS://DOCS.AWS.AMAZON.COM/JA_JP/DMS/LATEST/USERGUIDE/CHAP_SECURITY.APIROLE.HTML