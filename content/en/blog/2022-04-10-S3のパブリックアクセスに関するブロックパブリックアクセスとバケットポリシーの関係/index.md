---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "The Relationship Between Block Public Access and Bucket Policy for S3 Public Access"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-s3-public-access-about-message-policy
date: 2022-04-10
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

### Introduction

I checked the following four statuses for S3 public access and will summarize them.

1. Private bucket and objects
2. Objects can be made public
3. Public
4. Authenticated users of this account only

### 1. Private Bucket and Objects

When in the following state, `Private bucket and objects` is displayed:

- Block public access is ON
- No explicit access permitted in the bucket policy

![image-20220410113831656](image-20220410113831656.png)

![image-20220410113846723](image-20220410113846723.png)

![image-20220410113946431](image-20220410113946431.png)

### 2. Objects Can Be Made Public

When in the following state, `Objects can be made public` is displayed. At first I thought this meant public access was possible, but it seems an explicit bucket policy change is required. Even though the Japanese text implies public access is possible, access is actually not possible.

- Block public access is OFF
- No explicit access permitted in the bucket policy

![image-20220410114103815](image-20220410114103815.png)

![image-20220410114139965](image-20220410114139965.png)

![image-20220410114043581](image-20220410114043581.png)

![image-20220410114335717](image-20220410114335717.png)

### 3. Public

When in the following state, `Public` is displayed:

- Block public access is OFF
- Explicit access is permitted in the bucket policy

Example:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-public-test-1/*"
            ]
        }
    ]
}
```

![image-20220410115015587](image-20220410115015587.png)

![image-20220410115053992](image-20220410115053992.png)

![image-20220410115223332](image-20220410115223332.png)

### 4. Authenticated Users of This Account Only

When in the following state, `Authenticated users of this account only` is displayed:

- Block public access is ON
- Explicit access is permitted in the bucket policy

![image-20220410115420705](image-20220410115420705.png)

![image-20220410115359315](image-20220410115359315.png)
