---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS RDSインスタンスを停止する際の注意事項"
subtitle: ""
summary: " "
tags: ["AWS", "RDS"]
categories: ["AWS", "RDS"]
url: aws-rds-stop-cautions.html
date: 2019-07-14
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



### はじめに

RDSの下記マニュアルを見ていていくつかハマるポイントがあるな、と感じたのでメモ。

> 一時的に Amazon RDS DB インスタンスを停止する - Amazon Relational Database Service https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/USER_StopInstance.html

### 停止時間の最大日数

最大1週間のみ停止が可能。**停止したから永続的に課金されない**というわけではないので注意。

> DB インスタンスは最大 7 日間停止できます。DB インスタンスを手動で起動しないで 7 日間が経過すると、DB インスタンスは自動的に起動します。

### 停止可能なDBエンジン

一通りのDBエンジンは停止が出来る。

> MariaDB
>
> Microsoft SQL Server
>
> MySQL
>
> Oracle
>
> PostgreSQL

ただ、`マルチ AZ 設定の Amazon RDS for SQL Server DB インスタンスは停止できません。`と記載されている通り、マルチAZのSQL Serverの運用は注意。

### 制約事項

> リードレプリカが含まれているか、リードレプリカである DB インスタンスは停止できません。
>
> マルチ AZ 設定の Amazon RDS for SQL Server DB インスタンスは停止できません。
>
> 停止された DB インスタンスを変更することはできません。
>
> 停止された DB インスタンスに関連付けられているオプショングループを削除することはできません。
>
> 停止した DB インスタンスに関連付けられている DB パラメータグループを削除することはできません。

##### 停止された DB インスタンスを変更することはできません。

これは停止してインスタンスタイプをアップグレードしたい、と言った場合、停止中には出来ません、とのこと。

##### リードレプリカが含まれているか、リードレプリカである DB インスタンスは停止できません。

開発環境ならまだしも本番環境の場合はリードレプリカを使うシステム構成が多いのでこの制約事項のために停止運用が出来ないシステムは多く存在しそう。

### まとめ

バッファキャッシュ、共有プール(Oracle)やInnoDB バッファプール(MySQL)等は当然DBの再起動が入るとキャッシュから消えてしまう。（MySQLのInnoDB バッファープールのプリロードを使う等すれば良いかもしれない）

SQLの性能にはバッファキャッシュや共有プールが非常に重要になってくるので性能や運用管理よりもコストを重視する(開発環境)などの理由が明確にある場合にのみRDSの停止運用をすべき。少なくともDB on EC2の運用とは別の考え方が必要。

### 参考

> RDSを本番環境で停止運用しないほうが良い理由について – サーバーワークスエンジニアブログ http://blog.serverworks.co.jp/tech/2019/06/26/stopdbinstance/