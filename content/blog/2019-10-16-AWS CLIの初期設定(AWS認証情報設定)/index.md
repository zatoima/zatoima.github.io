---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS CLIの初期設定(AWS認証情報設定)"
subtitle: ""
summary: " "
tags: ["AWS", "EC2"]
categories: ["AWS", "EC2"]
url: aws-ec2-awscli-setting-credentials.html
date: 2019-10-16
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


## IAMユーザーのアクセスキーを取得

***

事前にIAMのセキュリティ認証情報から`Access key ID`と`Secret access key`を取得します。

<img src="image-20191121220548086.png" alt="image-20191121220548086" style="zoom:50%;" />

## CLIの設定ファイル

***

aws configureコマンドで`Access key ID`と`Secret access key`を設定します。

```sh
[ec2-user@donald-dev-ec2-bastin ~]$ aws configure
AWS Access Key ID [None]: xxxxxxxxxxxxxxxxxxxxx
AWS Secret Access Key [None]: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Default region name [None]: ap-northeast-1
Default output format [None]: text
[ec2-user@donald-dev-ec2-bastin ~]$ 
[ec2-user@donald-dev-ec2-bastin ~]$ ls -l .aws
total 8
-rw------- 1 ec2-user ec2-user  48 Oct 16 00:25 config
-rw------- 1 ec2-user ec2-user 116 Oct 16 00:25 credentials
[ec2-user@donald-dev-ec2-bastin ~]$ 
[ec2-user@donald-dev-ec2-bastin ~]$ cat .aws/config 
[default]
output = text
region = ap-northeast-1
[ec2-user@donald-dev-ec2-bastin ~]$ 
[ec2-user@donald-dev-ec2-bastin ~]$ cat .aws/credentials 
[default]
aws_access_key_id = xxxxxxxxxxxxxxxxxxx
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxx
[ec2-user@donald-dev-ec2-bastin ~]$ 

```



## その他の設定方法

------

- 環境変数( AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN )
- AWS認証情報ファイル( ~/.aws/credentials ) ★←今回の手順
- CLI 設定ファイル( ~/.aws/config )
- 認証情報
- インスタンスプロファイルの認証情報(インスタンスに割り当てられたIAMロール)
