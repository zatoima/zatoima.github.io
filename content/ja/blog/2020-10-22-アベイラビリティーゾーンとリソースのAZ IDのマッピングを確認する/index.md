---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "アベイラビリティーゾーンのZoneNameとZoneIdのマッピングを確認する"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-availabilityzone-mapping-zonename-zoneid.html
date: 2020-10-22
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

アベイラビリティーゾーンには ZoneName と  ZoneIdという概念があり、マニュアルに記載がある通り、アカウントごとでは異なるということのメモ。例えば、`ap-northeast-1a`は`ZoneId`が`apne1-az4`のアカウントもあれば、`apne1-az1`であるアカウントもあるということ。この仕様がないとリソースが`ap-northeast-1a`に集中してしまうことになりそう。

> リソースの AZ ID - AWS Resource Access Manager https://docs.aws.amazon.com/ja_jp/ram/latest/userguide/working-with-az-ids.html
>
> リソースがリージョンの複数のアベイラビリティーゾーンに分散されるようにするために、アベイラビリティーゾーンは各アカウントの名前に個別にマッピングされます。たとえば、お客様の AWS アカウントのアベイラビリティーゾーン `us-east-1a` は別の AWS アカウントのアベイラビリティーゾーン `us-east-1a` と同じ場所にはない可能性があります。

> リージョンとゾーン - Amazon Elastic Compute Cloud https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
>
> アカウント間でアベイラビリティーゾーンを調整するには、アベイラビリティーゾーンの一意で一貫性のある識別子である *AZ ID* を使用する必要があります。たとえば、`use1-az1` は、`us-east-1` リージョンの AZ ID で、すべての AWS アカウントで同じ場所になります。
>
> AZ ID を表示すると、アカウント間でリソースの場所を区別できます。たとえば、AZ ID `use-az2` のアベイラビリティーゾーンにあるサブネットを別のアカウントと共有する場合、このサブネットは AZ ID が同じく `use-az2` であるアベイラビリティーゾーンのそのアカウントでも利用できます。各 VPC とサブネットの AZ ID は Amazon VPC コンソールに表示されます。

このコマンド(`aws ec2 describe-availability-zones`)で確認することが可能。自アカウントの場合のZoneIDは下記の通りだった。

| ZoneName        | ZoneId    |
| --------------- | --------- |
| ap-northeast-1a | apne1-az4 |
| ap-northeast-1c | apne1-az1 |
| ap-northeast-1d | apne1-az2 |

```
[ec2-user@bastin ~]$ aws ec2 describe-availability-zones
{
    "AvailabilityZones": [
        {
            "OptInStatus": "opt-in-not-required", 
            "Messages": [], 
            "ZoneId": "apne1-az4", 
            "GroupName": "ap-northeast-1", 
            "State": "available", 
            "NetworkBorderGroup": "ap-northeast-1", 
            "ZoneName": "ap-northeast-1a", 
            "RegionName": "ap-northeast-1"
        }, 
        {
            "OptInStatus": "opt-in-not-required", 
            "Messages": [], 
            "ZoneId": "apne1-az1", 
            "GroupName": "ap-northeast-1", 
            "State": "available", 
            "NetworkBorderGroup": "ap-northeast-1", 
            "ZoneName": "ap-northeast-1c", 
            "RegionName": "ap-northeast-1"
        }, 
        {
            "OptInStatus": "opt-in-not-required", 
            "Messages": [], 
            "ZoneId": "apne1-az2", 
            "GroupName": "ap-northeast-1", 
            "State": "available", 
            "NetworkBorderGroup": "ap-northeast-1", 
            "ZoneName": "ap-northeast-1d", 
            "RegionName": "ap-northeast-1"
        }
    ]
}
[ec2-user@bastin ~]$ 
[ec2-user@bastin ~]$ aws ec2 describe-availability-zones --region ap-northeast-1  | jq -c '.AvailabilityZones[] | {RegionName: .RegionName, ZoneName: .ZoneName, ZoneId: .ZoneId}'
{"RegionName":"ap-northeast-1","ZoneName":"ap-northeast-1a","ZoneId":"apne1-az4"}
{"RegionName":"ap-northeast-1","ZoneName":"ap-northeast-1c","ZoneId":"apne1-az1"}
{"RegionName":"ap-northeast-1","ZoneName":"ap-northeast-1d","ZoneId":"apne1-az2"}
[ec2-user@bastin ~]$ 
```



