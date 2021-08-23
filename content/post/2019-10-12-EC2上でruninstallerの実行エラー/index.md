---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EC2上でruninstallerの実行エラー"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "Oracle"]
categories: ["AWS", "EC2", "Oracle"]
url: aws-oracle-ec2-runinstaller-error.html
date: 2019-10-12
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


xclockやxeyesを使用できるように設定したにも関わらずruninstaller実行時にエラーになる。

設定した手順は下記の通り。

> AWS EC2でX Window Systemをセットアップする - zato logger [https://www.zatolog.com/entry/aws-ec2-xwindow](https://www.zatolog.com/entry/aws-ec2-xwindow)

```bash
[oracle@db121s-dev-ec2-oracle database]$ ./runInstaller 
Starting Oracle Universal Installer...

Checking Temp space: must be greater than 500 MB.   Actual 75212 MB    Passed
Checking swap space: 0 MB available, 150 MB required.    Failed <<<<
Checking monitor: must be configured to display at least 256 colors
    >>> Could not execute auto check for display colors using command /usr/bin/xdpyinfo. Check if the DISPLAY variable is set.    Failed <<<<

Some requirement checks failed. You must fulfill these requirements before

continuing with the installation,

Continue? (y/n) [n] y
```



### 理由1:Checking swap space: 0 MB available, 150 MB required. Failed <<<<

---

公式Linux AMIの初期構成にはswapパーティションが無いのでスワップ領域を設定する必要がある。

詳細は下記手順やマニュアルを参照。

> Amazon EC2 インスタンスのスワップ領域としてメモリを割り当てるためのスワップファイルの使用 [https://aws.amazon.com/jp/premiumsupport/knowledge-center/ec2-memory-swap-file/](https://aws.amazon.com/jp/premiumsupport/knowledge-center/ec2-memory-swap-file/)
> Amazon EC2(Linux)のswap領域ベストプラクティス ｜ DevelopersIO [https://dev.classmethod.jp/cloud/ec2linux-swap-bestpractice/](https://dev.classmethod.jp/cloud/ec2linux-swap-bestpractice/)
> インスタンスストアスワップボリューム - Amazon Elastic Compute Cloud [https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html)

### 理由2:Checking monitor: must be configured to display at least 256 colors >>> Could not execute auto check for display colors using command /usr/bin/xdpyinfo. Check if the DISPLAY variable is set. Failed <<<<

---

こちらはxdpyinfo自体がインストールされてなかったので、yumでインストール。「DISPLAY変数」と出たらXmingやサーバ側のX11転送の問題かと思いこんでいた…。xdpyinfoがインストールされていないだけという単純な問題
