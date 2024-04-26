---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ハードウェア専有インスタンス (Dedicated Instance) とAmazon EC2 Dedicated Hostの違い"
subtitle: ""
summary: " "
tags: ["AWS","EC2","SAP勉強"]
categories: ["AWS","EC2","SAP勉強"]
url: aws-ec2-dedicated-instance-host.html
date: 2020-10-03
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

いつもこの2つの機能差異を忘れてしまうのでメモ。

2011/3からあるハードウェア専有インスタンスで実施出来なかった多くのことが2015年11月くらいから使える`Amazon EC2 Dedicated Host`で出来るようになっている。Dedicated Hosts では、物理サーバーに配置されたインスタンスの状況に関する可視性と制御がユーザ側が実施でできるためオンプレミスのサーバー限定のソフトウェアライセンスを使用でき、コンプライアンスを遵守出来る。

> https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html#dedicated-hosts-dedicated-instances

| 項目                                 | Dedicated Host                                               | ハードウェア専有インスタンス |
| :----------------------------------- | :----------------------------------------------------------- | ---------------------------- |
| 請求                                 | ホストごとの請求                                             | インスタンスごとの請求       |
| ソケット、コア、ホスト ID の可視性   | ソケットと物理コアの数が見える                               | 可視性なし                   |
| ホストおよびインスタンスアフィニティ | インスタンスを同じ物理サーバーに徐々にデプロイし続けることができる | サポート外                   |
| ターゲットを絞ったインスタンスの配置 | インスタンスを物理サーバーに配置する方法についての可視性と制御が高い | サポート外                   |
| インスタンスの自動復旧               | サポート対象。詳細については、「[ホスト復旧](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/dedicated-hosts-recovery.html)」を参照してください。 | サポート対象                 |
| 自分のライセンス使用 (BYOL)          | サポート対象                                                 | サポート外                   |

<iframe src="//www.slideshare.net/slideshow/embed_code/key/7rWkQ7hG6lGY2K?startSlide=52" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/20190305-aws-black-belt-online-seminar-amazon-ec2" title="20190305 AWS Black Belt Online Seminar Amazon EC2" target="_blank">20190305 AWS Black Belt Online Seminar Amazon EC2</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>



<iframe src="//www.slideshare.net/slideshow/embed_code/key/7rWkQ7hG6lGY2K?startSlide=53" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/20190305-aws-black-belt-online-seminar-amazon-ec2" title="20190305 AWS Black Belt Online Seminar Amazon EC2" target="_blank">20190305 AWS Black Belt Online Seminar Amazon EC2</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>