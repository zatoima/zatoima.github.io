---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora(PostgreSQL)へのpsql接続時にパスワードを省略する方法"
subtitle: ""
summary: " "
tags: ["AWS", "Aurora", "PostgreSQL"]
categories: ["AWS", "Aurora", "PostgreSQL"]
url: aws-aurora-postgres-password.html
date: 2019-11-08
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


Aurora(PostgreSQL)ではなく、PostgreSQLのお話。

###  **方法**1: '.pgpass' にパスワードを記載する

***

ホームディレクトリに'.pgpass'ファイルを作成してこちらにパスワードを記載。

##### .pgpassの書式

```
ホスト名:ポート:データベース:ユーザ:パスワード
例）192.168.1.**:5432:dbname:dbuser:password
```

##### .pgpassの作成

```sh
vi $HOME/.pgpass
aurorapostdb.xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com:5432:aurorapostdb:master:postgres

chmod 600 $HOME/.pgpass

[ec2-user@donald-dev-ec2-bastin ~]$ psql -h aurorapostdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U master -d aurorapostdb
psql (10.4, server 10.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

aurorapostdb=>
```

権限を変更しない場合、WARNINGが出る。

> WARNING: password file "/home/ec2-user/.pgpass" has group or world access; permissions should be u=rw (0600) or less

### 方法2:環境変数に記載する

***

```sh
export PGPASSWORD=postgres
psql -h aurorapostdb.xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U master -d aurorapostdb

[ec2-user@donald-dev-ec2-bastin ~]$ export PGPASSWORD=xxxxxxxx
[ec2-user@donald-dev-ec2-bastin ~]$ psql -h aurorapostdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U master -d aurorapostdb
psql (10.4, server 10.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

aurorapostdb=> 
```

### 参考

***

> 33.14. 環境変数 https://www.postgresql.jp/document/10/html/libpq-envars.html

> 33.15. パスワードファイル https://www.postgresql.jp/document/10/html/libpq-pgpass.html