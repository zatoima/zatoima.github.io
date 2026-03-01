---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Permission Error When Trying to Restore an EC2 Instance with AWS Backup"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-backup-ec2-restore-error
date: 2022-09-08
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

### Error Message

```
You are not authorized to perform this operation. Please consult the permissions associated with your AWS Backup role(s), and refer to the AWS Backup documentation for more details. Encoded authorization failure message: <omitted>
```

Decode using `aws sts decode-authorization-message --encoded-message <error message>`.

### Decoded Message

```json
{
    "DecodedMessage": "{\"allowed\":false,\"explicitDeny\":false,\"matchedStatements\":{\"items\":[]},\"failures\":{\"items\":[]},\"context\":{\"principal\":{\"id\":\"AROAR23YLZYEOUMEHOE2O:AWSBackup-AWSBackupROLEEC2\",\"arn\":\"arn:aws:sts::xxxxxxxxxxxxx:assumed-role/AWSBackupROLEEC2/AWSBackup-AWSBackupROLEEC2\"},\"action\":\"iam:PassRole\",\"resource\":\"arn:aws:iam::xxxxxxxxxxxxx:role/IAM_ROLE_EC2_Access\",\"conditions\":{\"items\":[{\"key\":\"aws:Region\",\"values\":{\"items\":[{\"value\":\"ap-northeast-1\"}]}},{\"key\":\"aws:Service\",\"values\":{\"items\":[{\"value\":\"ec2\"}]}},{\"key\":\"aws:Resource\",\"values\":{\"items\":[{\"value\":\"role/IAM_ROLE_EC2_Access\"}]}},{\"key\":\"iam:RoleName\",\"values\":{\"items\":[{\"value\":\"IAM_ROLE_EC2_Access\"}]}},{\"key\":\"aws:Type\",\"values\":{\"items\":[{\"value\":\"role\"}]}},{\"key\":\"aws:Account\",\"values\":{\"items\":[{\"value\":\"xxxxxxxxxxxxx\"}]}},{\"key\":\"aws:ARN\",\"values\":{\"items\":[{\"value\":\"arn:aws:iam::xxxxxxxxxxxxx:role/IAM_ROLE_EC2_Access\"}]}}]}}}"
}
```

An error appears to be occurring related to `iam:PassRole`.

As described in the articles below, an additional policy needs to be attached.

- [Troubleshooting Encoded Authorization Failure Messages When Restoring an Amazon EC2 Instance Using AWS Backup](https://aws.amazon.com/premiumsupport/knowledge-center/aws-backup-encoded-authorization-failure/)
- [How to Fix Errors When Restoring from AWS Backup While EC2 Can Be Restored from AMI | DevelopersIO](https://dev.classmethod.jp/articles/tsnote-backup-restore-role/)

> When examining the target EC2, an IAM role was attached.
> In this case, when restoring, a new IAM role needs to be attached.
> Therefore, when restoring from AWS Backup, the "AWS Backup role" needs to be granted "PassRole permission for the role to be attached to EC2" as follows.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::111122223333:role/*",
            "Effect": "Allow"
        }
    ]
}
```
