---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS認定データベース – 専門知識(DBS-C01)の合格体験記"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-certified-database-specialty.html
date: 2020-10-28
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

結構前ですが、AWS認定データベース – 専門知識（AWS Certified Database - Specialty） に合格しました。データベースのお仕事が多いので、こういった資格で知識やスキルの裏付け出来るのは大変嬉しいです。これでデータベースの資格はOracle Master Gold、OSS-DB Goldと合わせて3種類となりました。

この資格が2020年5月にリリースされてまだそこまで月日が経っておらず、当時のメモをブログ公開していなかったので、これから受ける方たちの参考になればと思い私の勉強方法を書いておきます。

### 試験の概要

https://aws.amazon.com/jp/certification/certified-database-specialty/

- 時間：180分
- 問題数：65問
- 合格点：75%以上

### 勉強方法

##### 1.まずは最初の第一歩で試験ガイドを流し読む

https://d1.awsstatic.com/ja_JP/training-and-certification/docs-database-specialty/AWS-Certified-Database-Specialty_Exam-Guide.pdf

##### 2.下記サービスのBlackBelt資料を読み込む。

PDF資料を読むよりも、Youtubeの字幕あり、速度2倍をオススメします。目と耳で頭に入れた方が定着度があるような気が

##### 重要高

- Relational Database Service (RDS)
- Aurora with MySQL Compatibility
- Aurora with PostgreSQL Compatibility
- DynamoDB
- CloudFormation
- Key Management Service

##### 重要度中～低

- ElastiCache
- DocumentDB
- Neptune
- Redshift

##### 3.AWS Certified Database - Specialtyの試験対策のE-Learningが無料で受講可

試験ガイドに記載されているセクションごとに講義が用意されています。

https://www.aws.training/Details/eLearning?id=47245

##### 4.問題傾向を把握

https://devopspages.io/aws-certified-database-specialty-exam-guide/

http://drawing-hisa.seesaa.net/article/473054025.html

##### 5.実機で触りまくる

Aurora、RDS、DynamoDBの機能についてはマニュアルをベースにほとんど触りました。Aurora グローバルデータベース、Aurora Serverless、Aurora クローニング、監査…こんな機能実際にはまだ使わないのでは？というのも出題されますのでこちらのサービスに関しては重点的にやった方が良い気がします

##### 6. 有料問題集を購入して解く

私はこちらの問題集を解きました。試験問題や傾向に慣れる上で良かったかな、と思います。ちょっとDynamoDBの問題数が多いかな、と思いましたが。

https://www.whizlabs.com/learn/course/aws-certified-database-specialty/

##### 7.模擬試験を解く

この試験には模擬試験も用意されているので受験前の総チェックとして受験してみました。私は受験前に60%の得点率でこれはやばい！と思っていました。

##### 出題傾向

私が受験した時の出題傾向は体感的にこんな感じでした

| No   | サービス               | 配分 |
| ---- | ---------------------- | ---- |
| 1    | RDS/Aurora             | 40%  |
| 2    | DynamoDB               | 15%  |
| 3    | DMS/SCT                | 15%  |
| 4    | Key Management Service | 5%   |
| 5    | Redshift               | 5%   |
| 5    | トラブルシューティング | 5%   |
| 6    | その他                 | 15%  |

### 最後に

今回が初めてのAWSの専門資格系(Specialty)の取得だったので取得出来た時は凄く嬉しかったです。ただ、そこまで難しいとは思えず、このSpecialty資格を取ったからと言って専門性の証明になるわけではなく、この分野の一通りの知識を持っています、という程度なのかな、と思いました。資格はその分野の第一歩に過ぎないみたいなことを誰かが言っていてそのとおりだな、と。

