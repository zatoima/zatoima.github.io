---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "gmailを使用してmetabaseのメール設定（Dashboard subscriptions）を行う"
subtitle: ""
summary: " "
tags: ["metabase"]
categories: ["metabase"]
url: metabase-gmail-email-sent-how-to
date: 2021-09-12
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



metabaseにはダッシュボードを共有するときにSlackやメールを選べるわけですが、メールをgmailで設定するときの設定値、設定方法をまとめておきます。ビジネス用途ではgmailで送信するという需要ないと思います。個人では中々メールサーバ立てるのはめんどくさいと思うのでgmailで出来れば便利かと思います。

### 参考資料

> Dashboard Subscriptions https://www.metabase.com/docs/latest/users-guide/dashboard-subscriptions.html
>
> Setting Up Email https://www.metabase.com/docs/latest/administration-guide/02-setting-up-email.html

### セットアップ画面

![Email Credentials](https://www.metabase.com/docs/latest/administration-guide/images/EmailCredentials.png)

### 入力値

```
SMTPホスト： smtp.gmail.com
SMTPポート： 587
SMTPセキュリティ： TLS
SMTPユーザー名： GMailアカウント（email@gmail.com）
SMTPパスワード：gmailのパスワード
```

### その他設定するところ

上記の入力値をmetabaseから設定すると失敗しました。理由は、gmailからすると安全性の低いアプリと認定されるようです。こちらの記事を確認して、安全性の低いアプリのアクセスを有効化します。一応、念の為に普段使い用のgmailアカウントではなく、送信用のgmailのアカウントを作成しました。

> https://support.google.com/accounts/answer/6010255?hl=ja
>
> 安全性の低いアプリと Google アカウント

![image-20210912163448540](image-20210912163448540.png)

ここまで行うことでメール設定が完了。後は選択項目の通りに設定して、メールを送信する。

