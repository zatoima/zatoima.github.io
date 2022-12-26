---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWSのエンコードされたエラーメッセージを見る方法"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-encode-error-message-how-to-confirm
date: 2022-09-15
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

![image-20220906200656012](image-20220906200656012.png)

`aws sts decode-authorization-message`を使う

```json
[ec2-user@bastin ~]$ aws sts decode-authorization-message --encoded-message CVOAvQdSoEIR4<省略>
{
    "DecodedMessage": "{\"allowed\":false,\"explicitDeny\":false,\"matchedStatements\":{\"items\":[]},\"failures\":{\"items\":[]},\"context\":{\"principal\":{\"id\":\"AROAR23YLZYEOUMEHOE2O:AWSBackup-AWSBackupROLEEC2\",\"arn\":\"arn:aws:sts::xxxxxx:assumed-role/AWSBackupROLEEC2/AWSBackup-AWSBackupROLEEC2\"},\"action\":\"iam:PassRole\",\"resource\":\"arn:aws:iam::xxxxxx:role/IAM_ROLE_EC2_Access\",\"conditions\":{\"items\":[{\"key\":\"aws:Region\",\"values\":{\"items\":[{\"value\":\"ap-northeast-1\"}]}},{\"key\":\"aws:Service\",\"values\":{\"items\":[{\"value\":\"ec2\"}]}},{\"key\":\"aws:Resource\",\"values\":{\"items\":[{\"value\":\"role/IAM_ROLE_EC2_Access\"}]}},{\"key\":\"iam:RoleName\",\"values\":{\"items\":[{\"value\":\"IAM_ROLE_EC2_Access\"}]}},{\"key\":\"aws:Type\",\"values\":{\"items\":[{\"value\":\"role\"}]}},{\"key\":\"aws:Account\",\"values\":{\"items\":[{\"value\":\"xxxxxx\"}]}},{\"key\":\"aws:ARN\",\"values\":{\"items\":[{\"value\":\"arn:aws:iam::xxxxxx:role/IAM_ROLE_EC2_Access\"}]}}]}}}"

```

