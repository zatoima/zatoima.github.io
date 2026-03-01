---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS BackupでEC2を復元しようとしたときの権限不足エラー"
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



### エラーメッセージ

```
You are not authorized to perform this operation. Please consult the permissions associated with your AWS Backup role(s), and refer to the AWS Backup documentation for more details. Encoded authorization failure message: <省略>
```

`aws sts decode-authorization-message --encoded-message <エラーメッセージ>`でデコードする。

### Decodeメッセージ

```json
{
    "DecodedMessage": "{\"allowed\":false,\"explicitDeny\":false,\"matchedStatements\":{\"items\":[]},\"failures\":{\"items\":[]},\"context\":{\"principal\":{\"id\":\"AROAR23YLZYEOUMEHOE2O:AWSBackup-AWSBackupROLEEC2\",\"arn\":\"arn:aws:sts::xxxxxxxxxxxxx:assumed-role/AWSBackupROLEEC2/AWSBackup-AWSBackupROLEEC2\"},\"action\":\"iam:PassRole\",\"resource\":\"arn:aws:iam::xxxxxxxxxxxxx:role/IAM_ROLE_EC2_Access\",\"conditions\":{\"items\":[{\"key\":\"aws:Region\",\"values\":{\"items\":[{\"value\":\"ap-northeast-1\"}]}},{\"key\":\"aws:Service\",\"values\":{\"items\":[{\"value\":\"ec2\"}]}},{\"key\":\"aws:Resource\",\"values\":{\"items\":[{\"value\":\"role/IAM_ROLE_EC2_Access\"}]}},{\"key\":\"iam:RoleName\",\"values\":{\"items\":[{\"value\":\"IAM_ROLE_EC2_Access\"}]}},{\"key\":\"aws:Type\",\"values\":{\"items\":[{\"value\":\"role\"}]}},{\"key\":\"aws:Account\",\"values\":{\"items\":[{\"value\":\"xxxxxxxxxxxxx\"}]}},{\"key\":\"aws:ARN\",\"values\":{\"items\":[{\"value\":\"arn:aws:iam::xxxxxxxxxxxxx:role/IAM_ROLE_EC2_Access\"}]}}]}}}"
}
```

`iam:PassRole`系でエラーが起きているようだ。

下記記事の通り、追加のポリシーをアタッチする必要がある。

- [AWS Backup を使用して Amazon EC2 インスタンスを復元するときに表示されるエンコードされた認可エラーメッセージのトラブルシューティング](https://aws.amazon.com/jp/premiumsupport/knowledge-center/aws-backup-encoded-authorization-failure/)
- [EC2 の AMI からは復元できるが、AWS Backup から復元しようとするとエラーになった際の対処方法 \| DevelopersIO](https://dev.classmethod.jp/articles/tsnote-backup-restore-role/)

>対象の EC2 を確認すると、IAM ロールがアタッチされていました。
>この場合には復元する際に、新たに IAM ロールをアタッチする必要があります。
>そのため、AWS Backup から復元する場合には、「AWS Backup 用のロール」に以下のように「EC2 にアタッチするロールを PassRole できる」権限を追加する必要があります。

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

