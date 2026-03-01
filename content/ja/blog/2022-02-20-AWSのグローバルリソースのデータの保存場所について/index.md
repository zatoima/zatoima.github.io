---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWSのグローバルリソースのデータの保存場所について"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-global-resource-data
date: 2022-02-20
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



国内に情報は留めておきたいという要件があった場合において、グローバルリソースはどうなるのか？という点をメモ。

### 1.グローバルリソース

グローバルリソースや例えばRoute53 、WAF 、CloudFront、IAM を指す。IAMはグローバルリソースで一つのリージョンに限らずにデータが複製される旨が記載がある。東京リージョンだけに留めたい場合においてもこのようなグローバル・サービスでは困難な場合がある。（とはいえ、保管される情報はログやメトリクスが主なのでその情報が海外リージョンに保管される場合、何が問題か？ということは整理する必要がある）

> https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/introduction.html  
>
> IAM には、他の多くの AWS サービスと同様、結果整合性があります。IAM は、世界中の Amazon のデータセンター内の複数のサーバーにデータを複製することにより、高可用性を実現します。

#### グローバルリソース関連（エッジサービス含む）

- CloudTrailイベント

- CloudWatchメトリクス

- route53クエリログやWAFログ等

- CloudFrontのSSL証明書

- 請求メトリクスデータ

- AWS Healthグローバルイベント

### 2.実は海外リージョンでしか使えない機能

リージョナルサービスだが、特定機能を使う場合には海外リージョンが使われてしまうパターン。これは他にも間違いなくある。

- Cognito ユーザープールのイベントデータ
- CognitoのEメール設定リージョン
- SESの受信

### マニュアルの抜粋箇所

随時見つけたら追記していきたいが、各サービスでバージニアリージョンだったり海外リージョンを経由してサービス提供が行われる機能をメモしていく。

| サービス   | 分類                                   | マニュアル抜粋                                               | URL                                                          |
| ---------- | -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| CloudWatch | 請求メトリクスデータ                   | 請求メトリクスデータは米国東部 (バージニア北部)  リージョンに保存され、世界全体の請求額として表されます。このデータには、使用した AWS のサービス別の予想請求額と AWS  全体の予想請求額が含まれています。 | https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html |
| CloudTrail | CloudTrailイベント                     | ほとんどのグローバルサービスの場合、イベントは米国東部  (バージニア北部) リージョンで発生しているものとしてログに記録されますが、一部のグローバルサービスイベントは米国東部 (オハイオ) リージョンや米国西部  (オレゴン) リージョンなどのその他のリージョンで発生しているものとしてログに記録されます。 | https://docs.aws.amazon.com/ja_jp/awscloudtrail/latest/userguide/cloudtrail-concepts.html |
| CloudFront | CloudFront証明書                       | Amazon CloudFront で ACM 証明書を使用するには、米国東部 (バージニア北部) リージョン  の証明書をリクエスト (またはインポート) していることを確認します。CloudFront ディストリビューションに関連づけられたこのリージョンの ACM  証明書は、このディストリビューションに設定されたすべての地域に分配されます。 | https://docs.aws.amazon.com/ja_jp/acm/latest/userguide/acm-regions.html |
| CloudFront | CloudFront メトリクス                  | CloudWatch API から CloudFront メトリクスを取得するには、米国東部 (バージニア北部) リージョン  (us-east-1) を使用する必要があります。また、各メトリクスの特定の値とタイプも知っておく必要があります。 | https://docs.aws.amazon.com/ja_jp/AmazonCloudFront/latest/DeveloperGuide/programming-cloudwatch-metrics.html |
| Route53    | Route 53 メトリクス                    | 現在のリージョンを米国東部  (バージニア北部) に変更します。それ以外のリージョンを現在のリージョンとして選択した場合、Route 53 のメトリクスは利用できません。 | https://docs.aws.amazon.com/ja_jp/Route53/latest/DeveloperGuide/monitoring-health-checks.html |
| AWS Health | AWS Healthグローバルイベント           | グローバルイベントを受信するには、米国東部 (バージニア北部) リージョンのルールを作成する必要があります。 | https://docs.aws.amazon.com/ja_jp/health/latest/ug/cloudwatch-events-health.html |
| Cognito    | E メール設定リージョン                 | 使用する Amazon SES  設定リージョンを決定するときは、次のリージョンから選択する必要があります: us-east-1、us-west-2、または eu-west-1。 | https://docs.aws.amazon.com/ja_jp/cognito/latest/developerguide/user-pool-email.html |
| Cognito    | Cognito ユーザープールのイベントデータ | Amazon Cognito ユーザープールで Amazon Pinpoint  分析が使用される場合、イベントデータは米国東部 (バージニア北部) リージョンにルーティングされます。 | https://docs.aws.amazon.com/ja_jp/cognito/latest/developerguide/security-cognito-regional-data-considerations.html |
