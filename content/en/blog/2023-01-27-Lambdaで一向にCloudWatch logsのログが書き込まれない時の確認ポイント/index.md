---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "What to Check When CloudWatch Logs Are Not Being Written from Lambda"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-lambda-cloudwatch-logs-not-write
date: 2023-01-27
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

Getting this error and logs are not being written at all.

![image-20230127162101389](image-20230127162101389.png)

### Cause

The role from another Lambda function was being reused, and the CloudWatch Logs write destination was configured specifically for that other Lambda function. This can be resolved by modifying the IAM policy or creating a new policy.
