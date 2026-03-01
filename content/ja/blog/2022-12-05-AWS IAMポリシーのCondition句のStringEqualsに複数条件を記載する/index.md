---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS IAMポリシーのCondition句のStringEqualsに複数条件を記載する"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-iam-policy-condition-multipul
date: 2022-12-05
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

> 参考
> [IAM JSON ポリシー要素: Condition \- AWS Identity and Access Management](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/reference_policies_elements_condition.html)

### OR条件となるIAMポリシー

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::xxxxxxx:user/xxxx-s"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": ["xxxxxxx_SFCRole=2_JVxxxxxxO3Bd/Pr0=","xxxxxxx_SFCRole=2_dxxxxxxiw="]
                }
            }
        }
    ]
}
```

### NGパターン
#### そもそも構文としてNG

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::xxxxxxx:user/xxxx-s"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "xxxxxxx_SFCRole=2_JVxxxxxxO3Bd/Pr0=",
                    "sts:ExternalId": "xxxxxxx_SFCRole=2_dxxxxxxiw="
                }
            }
        }
    ]
}
```

#### 冗長なのでNG

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::xxxxxxx:user/xxxx-s"
			},
			"Action": "sts:AssumeRole",
			"Condition": {
				"StringEquals": {
					"sts:ExternalId": "xxxxxxx_SFCRole=2_JVxxxxxxO3Bd/Pr0="
				}
			}
		},
		{
			"Effect": "Allow",
			"Principal": {
				"AWS": "arn:aws:iam::xxxxxxx:user/bkm20000-s"
			},
			"Action": "sts:AssumeRole",
			"Condition": {
				"StringEquals": {
					"sts:ExternalId": "xxxxxxx_SFCRole=2_dxxxxxxiw="
				}
			}
		}
	]
}
```
