---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "About the Data Storage Location of AWS Global Resources"
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



Notes on what happens with global resources when there is a requirement to keep information within Japan.

### 1. Global Resources

Global resources refer to things like Route53, WAF, CloudFront, and IAM. IAM is a global resource, and there is documentation stating that data is replicated across regions beyond a single region. If you want to limit data to only the Tokyo region, some global services may make this difficult. (That said, the information stored is mainly logs and metrics, so you would need to organize what the actual problem is if such information is stored in overseas regions.)

> https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/introduction.html
>
> IAM, like many other AWS services, is eventually consistent. IAM achieves high availability by replicating data across multiple servers within Amazon data centers around the world.

#### Global Resource Related (Including Edge Services)

- CloudTrail events

- CloudWatch metrics

- Route53 query logs, WAF logs, etc.

- CloudFront SSL certificates

- Billing metric data

- AWS Health global events

### 2. Features That Are Actually Only Available in Overseas Regions

Patterns where a regional service routes through an overseas region for a specific feature. There are certainly more examples beyond these.

- Cognito user pool event data
- Cognito email configuration region
- SES receiving

### Excerpts from the Manual

I will add to this as I find more, noting features that use US Virginia or other overseas regions for service delivery.

| Service    | Classification                           | Manual Excerpt                                               | URL                                                          |
| ---------- | ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| CloudWatch | Billing metric data                      | Billing metric data is stored in the US East (N. Virginia) Region and represents charges for your entire AWS account. This data includes the estimated charges for each AWS service you use and the estimated overall total AWS charges. | https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html |
| CloudTrail | CloudTrail events                        | For most global services, events are logged as occurring in US East (N. Virginia) Region, but some global service events are logged as occurring in other regions, such as US East (Ohio) or US West (Oregon). | https://docs.aws.amazon.com/ja_jp/awscloudtrail/latest/userguide/cloudtrail-concepts.html |
| CloudFront | CloudFront certificates                  | To use an ACM certificate with Amazon CloudFront, make sure you request (or import) the certificate in the US East (N. Virginia) Region. ACM certificates in this region that are associated with a CloudFront distribution are distributed to all geographic locations configured for that distribution. | https://docs.aws.amazon.com/ja_jp/acm/latest/userguide/acm-regions.html |
| CloudFront | CloudFront metrics                       | To get CloudFront metrics from the CloudWatch API, you must use the US East (N. Virginia) Region (us-east-1). You also need to know the specific values and types for each metric. | https://docs.aws.amazon.com/ja_jp/AmazonCloudFront/latest/DeveloperGuide/programming-cloudwatch-metrics.html |
| Route53    | Route 53 metrics                         | Change the current region to US East (N. Virginia). If you select any other region as the current region, Route 53 metrics won't be available. | https://docs.aws.amazon.com/ja_jp/Route53/latest/DeveloperGuide/monitoring-health-checks.html |
| AWS Health | AWS Health global events                 | To receive global events, you must create a rule in the US East (N. Virginia) Region. | https://docs.aws.amazon.com/ja_jp/health/latest/ug/cloudwatch-events-health.html |
| Cognito    | Email configuration region               | When determining the Amazon SES configuration region to use, you must choose from the following regions: us-east-1, us-west-2, or eu-west-1. | https://docs.aws.amazon.com/ja_jp/cognito/latest/developerguide/user-pool-email.html |
| Cognito    | Cognito user pool event data             | When Amazon Cognito user pools uses Amazon Pinpoint analytics, event data is routed to the US East (N. Virginia) Region. | https://docs.aws.amazon.com/ja_jp/cognito/latest/developerguide/security-cognito-regional-data-considerations.html |
