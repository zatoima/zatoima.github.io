---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "アカウントを跨いだ際のS3へのアクセスについて"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-s3-access-iam-bucket-policy
date: 2022-06-28
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



> S3のバケットポリシーでハマったので、S3へのアクセスを許可するPrincipalの設定を整理する | DevelopersIO https://dev.classmethod.jp/articles/summarize-principal-settings-in-s3-bucket-policy/?utm_source=pocket_mylist

| IAMユーザーとS3が同じアカウントか | IAMポリシー  | バケットポリシー（ユーザーArn指定） | バケットポリシー（AWSアカウント指定） | 備考                                                         |
| --------------------------------- | ------------ | ----------------------------------- | ------------------------------------- | ------------------------------------------------------------ |
| **同じ**                          | いずれか必要 | いずれか必要                        | -                                     | IAMポリシーまたはバケットポリシーのどちらかで許可されていればアクセス可能 |
| **異なる**                        | 許可必須     | いずれか必要                        | いずれか必要                          | IAMポリシーとバケットポリシー両方の許可が必要。バケットポリシーはユーザーArnでもAWSアカウント指定でもOK |
