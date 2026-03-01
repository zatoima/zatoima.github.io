---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWSのドキュメントの更新履歴をgithubで確認してRSSフィードを取得"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-docs-guthub-commit-log.html
date: 2020-09-04
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

### 

今更ながらAWSのドキュメントがgithubから確認出来ることを知った。2018年にオープンソースになった模様。

> AWS ドキュメントがオープンソースになり、GitHub でご利用可能に | Amazon Web Services ブログ https://aws.amazon.com/jp/blogs/news/aws-documentation-is-now-open-source-and-on-github/

下記のURLからユーザガイドや開発者ガイドのリポジトリにアクセスすることが出来る。

> https://github.com/awsdocs

![image-20200903144451541](image-20200903144451541.png)

例えばAuroraのユーザガイドのリポジトリはこちら。

> https://github.com/awsdocs/amazon-aurora-user-guide

githubなのでcommitのログも確認出来るし、具体的にどこの部分が変わったか、というのも見ることが出来る。

> https://github.com/awsdocs/amazon-aurora-user-guide/commit/f83c1cce2f8fa9bbb7bc4c72ac2233c381f9bd84

![image-20200903144632795](image-20200903144632795.png)

GitHubは色々なatomフィードを出力出来るのでRSSに登録しといて、更新があれば確認してみる、というような使い方も出来る。例えば、Auroraのユーザガイドのcommitログのフィードは下記となる。リポジトリ名をそれぞれのものに変えることで気にあるリポジトリの更新を受け取ることが出来るのでこういう使い方も。

> https://github.com/awsdocs/amazon-aurora-user-guide/commits/master.atom

私はFeedlyを使っているが、こんな感じに通知が飛んでくる。

![image-20200903145022613](image-20200903145022613.png)



