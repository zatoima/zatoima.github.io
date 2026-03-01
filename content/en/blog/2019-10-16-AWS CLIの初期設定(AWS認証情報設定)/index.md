---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Initial AWS CLI Setup (AWS Credentials Configuration)"
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


## Get IAM User Access Key

***

Obtain the `Access key ID` and `Secret access key` from IAM security credentials in advance.

<img src="image-20191121220548086.png" alt="image-20191121220548086" style="zoom:50%;" />

## CLI Configuration File

***

Use the aws configure command to set the `Access key ID` and `Secret access key`.

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



## Other Configuration Methods

------

- Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
- AWS credentials file (~/.aws/credentials) ★ ← This procedure
- CLI configuration file (~/.aws/config)
- Credentials
- Instance profile credentials (IAM role assigned to the instance)
