---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "\"Log Group Does Not Exist\" Error When Trying to View DMS Logs in CloudWatch"
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


### Error Details

***

<img src="images/image-20191121221355387.png" alt="image-20191121221355387" style="zoom:50%;" />

When clicking the "View Logs" button in the lower right of the above screen, it navigates to CloudWatch Logs, but an error occurred on the redirected screen.

```sh
Log group does not exist
Log group dms-tasks-dev-oracle-to-aurora-v2 was not found. Please verify that this log group was created correctly and try again.
```

### Error Cause

***

As described above, the following were the causes. To check logs, the following are required:

1. The dms-cloudwatch-logs-role IAM role must be created
2. The correct access permission policy must be configured
3. The correct trust relationship must be configured for AWS DMS to assume the role

Normally, it appears to be automatically created when you create your first AWS DMS task using the AWS DMS console.

### Resolution

***

Please refer to and follow one of the options below.

> Troubleshooting When CloudWatch Logs Don't Appear for AWS DMS Tasks https://aws.amazon.com/jp/premiumsupport/knowledge-center/dms-cloudwatch-logs-not-appearing/

> Creating IAM Roles for Use with AWS CLI and AWS DMS API - AWS DATABASE MIGRATION SERVICE HTTPS://DOCS.AWS.AMAZON.COM/JA_JP/DMS/LATEST/USERGUIDE/CHAP_SECURITY.APIROLE.HTML
