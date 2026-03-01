---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Checking AWS Service Quotas via CLI"
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



### List Services and Service Codes

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

### Check Service Quotas

Use `list-service-quotas` to list the quota values applied to the specified AWS service.

Parameter notes:

- Adjustable: Whether the limit can be increased (indicates whether it is a hard limit or soft limit)

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

### Check Default Service Quota Values

`list-aws-default-service-quotas` outputs only the default values. Note that it does not reflect values changed by limit increase requests. The fact that no account number appears in the `QuotaArn` suggests the results are the same across all accounts.

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

### Exporting as CSV

```sh
aws service-quotas list-services | jq -r '.Services[] | [.ServiceCode, .ServiceName] | @csv'
aws service-quotas list-service-quotas --service-code athena | jq -r '.Quotas[] | [.ServiceCode, .ServiceName, .QuotaName, .Value, .Unit, .Adjustable] | @csv'
aws service-quotas list-aws-default-service-quotas --service-code athena | jq -r '.Quotas[] | [.ServiceCode, .ServiceName, .QuotaName, .Value, .Unit, .Adjustable] | @csv'
```

### References

> AWS Service Quotas - AWS General Reference https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html
>
> list-service-quotas - AWS CLI 1.19.97 Command Reference https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-service-quotas.html
>
> list-aws-default-service-quotas - AWS CLI 1.19.97 Command Reference https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-aws-default-service-quotas.html
>
> Request a Service Quota Increase Using the AWS CLI https://aws.amazon.com/premiumsupport/knowledge-center/request-service-quota-increase-cli/
