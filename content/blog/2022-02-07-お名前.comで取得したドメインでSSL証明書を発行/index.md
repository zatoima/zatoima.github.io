---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "お名前.comで取得したドメインを使用してACMでSSL証明書を発行する"
subtitle: ""
summary: " "
tags: ["AWS","ACM"]
categories: ["AWS","ACM"]
url: aws-acm-ssl-certigication-setting
date: 2022-02-07
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, B
---

表題の通り、お名前.comで取得したドメインを使用してACMでSSL証明書を発行する際のメモ。

### ACMからパブリック証明書をリクエスト

![image-20220112134641278](image-20220112134641278.png)

ドメイン名と検証方法を入力

![image-20220112134754419](image-20220112134754419.png)

証明書の発行中。しばらく待機する

![image-20220112134832140](image-20220112134832140.png)

証明書の詳細画面に移動して、「CSVにエクスポート」を選択して手元にダウンロードしておく。後続の手順で参照。

![image-20220112135511287](image-20220112135511287.png)

お名前.comに移動して「DNSレコードを設定する」に移動

![image-20220112135631643](image-20220112135631643.png)

対象ドメインを選択して次へ

![image-20220112135711384](image-20220112135711384.png)

DNSレコード設定を利用する

![image-20220112135824174](image-20220112135824174.png)

ACMの画面から下記のようなCSVをダウンロードしているはずなのでここから下記を入力する

![image-20220112140655648](image-20220112140655648.png)

| ホスト名    | TYPE  | VALUE        |
| ----------- | ----- | ------------ |
| Domain Name | CNAME | Record Value |

入力して追加する

![image-20220112140548910](image-20220112140548910.png)

ページ下部の設定はデフォルトのままチェックを付ける

![image-20220112140711412](image-20220112140711412.png)

設定するをクリック

![image-20220112140751547](image-20220112140751547.png)

完了となる

![image-20220112140823966](image-20220112140823966.png)

数時間から24時間程度と書かれているのでDNSの伝搬に時間が掛かるので気長に待つ。

https://help.onamae.com/answer/8081

![image-20220112141220725](image-20220112141220725.png)

数十分でステータスが発行済に変更になった

![image-20220112142634611](image-20220112142634611.jpg)

### 参考

検証を保留中の ACM 証明書の解決 https://aws.amazon.com/jp/premiumsupport/knowledge-center/acm-certificate-pending-validation/
