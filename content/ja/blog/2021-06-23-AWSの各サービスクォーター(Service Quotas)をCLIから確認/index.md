---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWSの各サービスクォーター(Service Quotas)をCLIから確認"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-service-quotas-limit-cli
date: 2021-06-23
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



### サービス一覧とサービスコードを確認する

```sh
aws service-quotas list-services --output table
```

```sh
--------------------------------------------------------------------------------------------------------
|                                             ListServices                                             |
+------------------------------------------------------------------------------------------------------+
||                                              Services                                              ||
|+--------------------------+-------------------------------------------------------------------------+|
||        ServiceCode       |                               ServiceName                               ||
|+--------------------------+-------------------------------------------------------------------------+|
||  AWSCloudMap             |  AWS Cloud Map                                                          ||
||  access-analyzer         |  Access Analyzer                                                        ||
||  acm                     |  AWS Certificate Manager (ACM)                                          ||
||  acm-pca                 |  AWS Certificate Manager Private Certificate Authority (ACM PCA)        ||
||  airflow                 |  Amazon Managed Workflows for Apache Airflow                            ||
||  amplify                 |  AWS Amplify                                                            ||
||  apigateway              |  Amazon API Gateway                                                     ||
||  appflow                 |  Amazon AppFlow                                                         ||
||  application-autoscaling |  Application Auto Scaling                                               ||
||  appmesh                 |  AWS App Mesh                                                           ||
||  apprunner               |  AWS App Runner                                                         ||
||  appstream2              |  Amazon AppStream 2.0                                                   ||
||  appsync                 |  AWS AppSync                                                            ||
||  athena                  |  Amazon Athena                                                          ||
||  auditmanager            |  AWS Audit Manager                                                      ||

```

### サービスクォーターを確認

`list-service-quotas`を使用する。指定されたAWSサービスに適用されたクォータ値を一覧表示する。

パラメータの補足↓

- Adjustable：上限緩和が可能かどうか（ハードリミットかソフトリミットかが確認可能）

```sh
aws service-quotas list-service-quotas --service-code athena --output table
```

```sh
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|                                                                                     ListServiceQuotas                                                                                    |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
||                                                                                         Quotas                                                                                         ||
|+------------+--------------+-----------------------------------------------------------------------+-------------+--------------------+--------------+----------------+-------+---------+|
|| Adjustable | GlobalQuota  |                               QuotaArn                                |  QuotaCode  |     QuotaName      | ServiceCode  |  ServiceName   | Unit  |  Value  ||
|+------------+--------------+-----------------------------------------------------------------------+-------------+--------------------+--------------+----------------+-------+---------+|
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1:0123456789:athena/L-3CE0BBA0  |  L-3CE0BBA0 |  DDL query limit   |  athena      |  Amazon Athena |  None |  20.0   ||
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1:0123456789:athena/L-56A94400  |  L-56A94400 |  DDL query timeout |  athena      |  Amazon Athena |  None |  600.0  ||
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1:0123456789:athena/L-FC5F6546  |  L-FC5F6546 |  DML query limit   |  athena      |  Amazon Athena |  None |  30.0   ||
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1:0123456789:athena/L-E80DC288  |  L-E80DC288 |  DML query timeout |  athena      |  Amazon Athena |  None |  30.0   ||
|+------------+--------------+-----------------------------------------------------------------------+-------------+--------------------+--------------+----------------+-------+---------+|
```

### サービスクォーターのデフォルト値を確認

`list-aws-default-service-quotas`はデフォルト値のみを出力する。上限緩和等で値が変更された場合の結果は反映されないので注意。`QuotaArn`にもアカウント番号が出てこないところを見ると各アカウントで同じ結果になるものと思われる。

```sh
aws service-quotas list-aws-default-service-quotas --service-code athena --output table
```

```sh
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|                                                                          ListAWSDefaultServiceQuotas                                                                         |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
||                                                                                   Quotas                                                                                   ||
|+------------+--------------+-----------------------------------------------------------+-------------+--------------------+--------------+----------------+-------+---------+|
|| Adjustable | GlobalQuota  |                         QuotaArn                          |  QuotaCode  |     QuotaName      | ServiceCode  |  ServiceName   | Unit  |  Value  ||
|+------------+--------------+-----------------------------------------------------------+-------------+--------------------+--------------+----------------+-------+---------+|
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1::athena/L-3CE0BBA0  |  L-3CE0BBA0 |  DDL query limit   |  athena      |  Amazon Athena |  None |  20.0   ||
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1::athena/L-56A94400  |  L-56A94400 |  DDL query timeout |  athena      |  Amazon Athena |  None |  600.0  ||
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1::athena/L-FC5F6546  |  L-FC5F6546 |  DML query limit   |  athena      |  Amazon Athena |  None |  30.0   ||
||  True      |  False       |  arn:aws:servicequotas:ap-northeast-1::athena/L-E80DC288  |  L-E80DC288 |  DML query timeout |  athena      |  Amazon Athena |  None |  30.0   ||
|+------------+--------------+-----------------------------------------------------------+-------------+--------------------+--------------+----------------+-------+---------+|

```

### CSV形式で抽出したい時

```sh
aws service-quotas list-services | jq -r '.Services[] | [.ServiceCode, .ServiceName] | @csv'
aws service-quotas list-service-quotas --service-code athena | jq -r '.Quotas[] | [.ServiceCode, .ServiceName, .QuotaName, .Value, .Unit, .Adjustable] | @csv'
aws service-quotas list-aws-default-service-quotas --service-code athena | jq -r '.Quotas[] | [.ServiceCode, .ServiceName, .QuotaName, .Value, .Unit, .Adjustable] | @csv'
```

### 参考

> AWS のサービスクォータ - AWS 全般のリファレンス https://docs.aws.amazon.com/ja_jp/general/latest/gr/aws_service_limits.html
>
> list-service-quotas — AWS CLI1.19.97コマンドリファレンス https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-service-quotas.html
>
> list-aws-default-service-quotas — AWS CLI 1.19.97 Command Reference https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-aws-default-service-quotas.html
>
> AWS CLI を使用してサービスクォータの引き上げをリクエストする https://aws.amazon.com/jp/premiumsupport/knowledge-center/request-service-quota-increase-cli/