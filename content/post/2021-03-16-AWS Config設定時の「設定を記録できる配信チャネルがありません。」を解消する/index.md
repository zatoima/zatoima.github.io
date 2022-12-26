---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS Config設定時の「設定を記録できる配信チャネルがありません。」を解消する"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-config-delivery-channels-error
date: 2022-03-16
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

## 問題

AWS Configで記録を有効化しようとすると「設定を記録できる配信チャネルがありません。」が出力されて有効化出来ないケース

![image-20220314143103696](image-20220314143103696.png)

下記のように、配信チャネルが無い状態になっていると思われるので、配信チャネルを手動作成する。DeliveryChannelsが確かにnullになっている。

```json
[ec2-user@bastin ~]$ aws configservice describe-delivery-channels
{
    "DeliveryChannels": []
}
[ec2-user@bastin ~]$ aws configservice describe-configuration-recorders
{
    "ConfigurationRecorders": [
        {
            "name": "default",
            "roleARN": "arn:aws:iam::xxxxxx:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
            "recordingGroup": {
                "allSupported": true,
                "includeGlobalResourceTypes": true,
                "resourceTypes": []
            }
        }
    ]
}
```

### 解決方法：配信チャネルの作成

配信チャネル作成後にConfigの再設定を行う

```sh
[ec2-user@bastin ~]$ aws configservice put-delivery-channel --delivery-channel name=default,s3BucketName=config-bucket-xxxxxxxxxx --region ap-northeast-1
```

参考

- [put\-delivery\-channel — AWS CLI 1\.22\.73 Command Reference](https://docs.aws.amazon.com/cli/latest/reference/configservice/put-delivery-channel.html)

### 設定確認

```json
[ec2-user@bastin ~]$ aws configservice describe-delivery-channels
{
    "DeliveryChannels": [
        {
            "name": "default",
            "s3BucketName": "config-bucket-xxxxx"
        }
    ]
}
[ec2-user@bastin ~]$ aws configservice describe-configuration-recorders
{
    "ConfigurationRecorders": [
        {
            "name": "default",
            "roleARN": "arn:aws:iam::xxxx:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
            "recordingGroup": {
                "allSupported": true,
                "includeGlobalResourceTypes": true,
                "resourceTypes": []
            }
        }
    ]
}

```

