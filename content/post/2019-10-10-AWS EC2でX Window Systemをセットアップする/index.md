---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS EC2でX Window Systemをセットアップする"
subtitle: ""
summary: " "
tags: ["AWS", "EC2", "Oracle"]
categories: ["AWS", "EC2", "Oracle"]
url: aws-ec2-xwindow.html
date: 2019-10-10
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

Oracle Databaseをインストール（DBCA）する際にX Window System環境が必要だったのでEC2上でXが動くように設定。EC上でX Window System環境を動作させるのは手間な印象があったが、いくつかのパッケージをyumでインストールするだけで実施が可能だった。

### 前提バージョン

```sh
[ec2-user@bastin ~]$ cat /etc/os-release
NAME="Amazon Linux"
VERSION="2"
ID="amzn"
ID_LIKE="centos rhel fedora"
VERSION_ID="2"
PRETTY_NAME="Amazon Linux 2"
ANSI_COLOR="0;33"
CPE_NAME="cpe:2.3:o:amazon:amazon_linux:2"
HOME_URL="https://amazonlinux.com/"
[ec2-user@bastin ~]$ cat /etc/image-id
image_name="amzn2-ami-hvm"
image_version="2"
image_arch="x86_64"
image_file="INCOMPLETE-amzn2-ami-hvm-2.0.20191116.0-x86_64.xfs.gpt"
image_stamp="ec6f-62ed"
image_date="20191118225945"
recipe_name="amzn2 ami"
recipe_id="cd573903-ca89-ecf8-cb7f-1320-48ba-1a6d-730da3c5"
[ec2-user@bastin ~]$ 
```

### クライアント側(Windows側)にxmingをインストール

> ダウンロードファイル一覧 - Xming X Server for Windows - OSDN https://ja.osdn.net/projects/sfnet_xming/releases/

### xorg関連パッケージをインストール

- xorg-x11-xauth.x86_64
- xorg-x11-server-utils.x86_64

```sh
sudo yum -y install xorg-x11-xauth.x86_64 xorg-x11-server-utils.x86_64
```

### xeyesで確認

```sh
sudo yum -y install xeyes
xeyes
```

### 補足

#### 設定ファイル

/etc/ssh/sshd_configの「X11Forwarding」がyesとなっているか

### SSHターミナルの設定

#### Teratermの場合

Teratermの[設定]-[SSH転送]にて「SSHポート転送」というウィンドウが表示されるので、その中の「Xクライアントアプリケーションの転送」にチェックを入れる。

#### [Xshell](https://www.netsarang.com/en/xshell/)の場合

X11Forwarding先を設定する

#### ユーザ

実行ユーザにも注意(※ su or su - したユーザでは挙動が違った記憶が、、、、。曖昧。)