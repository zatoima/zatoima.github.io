---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ユーザデータを使用してEC2作成時にApacheを自動インストール"
subtitle: ""
summary: " "
tags: ["AWS","EC2"]
categories: ["AWS","EC2"]
url: aws-ec2-userdata-apache-install.html
date: 2020-08-31
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



### ユーザデータとは？

Linuxインスタンスの初期起動時に実行するコマンドを指す。デフォルトでは初期起動時のみですが、再起動時に毎回実行するということも出来る模様。

> https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/user-data.html
>
> Amazon EC2 でインスタンスを起動するとき、起動後にそのインスタンスにユーザーデータを渡し、一般的な自動設定タスクを実行したり、スクリプトを実行したりできます。2 つのタイプのユーザーデータを Amazon EC2 に渡すことができます。

### ユーザデータの設定方法

`ステップ 3: インスタンスの詳細の設定` の `高度な詳細`欄にユーザデータを指定する欄があります。

![image-20200830172722192](image-20200830172722192.png)

ユーザデータには下記を指定。yum update、Apacheのインストールから権限変更などを実施。

```sh
#!/bin/bash
yum update -y
amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
yum install -y httpd mariadb-server
systemctl start httpd
systemctl enable httpd
usermod -a -G apache ec2-user
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;
echo `hostname` > /var/www/html/index.html
```

後はこの状態で他のEC2作成と同じように進めることでインスタンス作成時にApacheインストールまで実施される。セキュリティグループなどの設定は割愛します。