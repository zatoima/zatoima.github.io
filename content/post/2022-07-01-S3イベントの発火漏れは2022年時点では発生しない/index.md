---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "S3イベントの発火漏れは2022年時点では発生しない"
subtitle: ""
summary: " "
tags: ["AWS","S3"]
categories: ["AWS","S3"]
url: aws-s3-event-missing
date: 2022-07-01
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



### 結論

---

結論を表題に書いた通りだが、S3イベントの発火漏れはもはや発生しない。

以前のドキュメントにはS3イベント通知は欠損する可能性があり、ドキュメントにもその旨が記載されているが、2022年時点では下記の通り発生しない。

> https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/NotificationHowTo.html
>
> Amazon S3 イベント通知は、少なくとも 1 回配信されるように設計されています。通常、イベント通知は数秒で配信されますが、1 分以上かかる場合もあります。



少し古い記事だとS3イベントの発火漏れが起きうるとのの記載があり、この仕様改善（？）を書かれた記事があまり無かったのでメモ。

> https://dev.classmethod.jp/articles/s3-event-notification-vs-eventbridge-event-processing-overflow-rate/
>
> https://qiita.com/kkimura/items/92833436349d8fc5ad29
