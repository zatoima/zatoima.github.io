---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_hba.confのメモ"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-pg-hba-conf.html
date: 2019-08-27
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


### 「pg_hba.conf」ファイルの書式

```
パターン1 : local データベース名 ユーザ名 認証方式
パターン2 : host データベース名 ユーザ名 IPアドレス サブネットマスク 認証方式
パターン3 : host データベース名 ユーザ名 CIDRアドレス 認証方式
```

##### 接続方式

クライアントが認証する接続方式を指定

| 接続方式 | 内容             |
| -------- | ---------------- |
| host     | TCP/IP接続       |
| local    | UNIXドメイン接続 |

##### DB名

接続先のデータベース名を指定。複数を指定する場合はカンマ区切り。allは全てのデータベースが対象。

##### ユーザ名

接続するユーザ名を指定。複数を指定する場合はカンマ区切り。allは全てのユーザが対象。

##### IPアドレスとサブネット

接続方式が「host」の場合のみ。クライアントのIPアドレスの範囲を指定する。

##### クライアント認証の設定例

| 認証方式 | 内容                                           |
| -------- | ---------------------------------------------- |
| trust    | 常に許可                                       |
| reject   | 常に拒否                                       |
| md5      | MD5で暗号化されたパスワード認証を行う          |
| password | 暗号化されていない平文でのパスワード認証を行う |

### その他

クライアント認証の判定はレコードの上から順に行われ、一致していればその行で指定されている方式で認証する。認証ができれば接続が許可され、認証できなければ接続は拒否される。認証に成功もしくは失敗した場合、次に続くレコードは確認しない。
