---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora（PostgreSQL）へのSSL接続について"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-ssl-connect.html
date: 2020-07-02
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

### 事前準備

> https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Security.html
>
> SSL 接続ステータスを調べる

##### 拡張機能のインストール

```sql
create extension sslinfo;
```

##### SSLの使用有無の確認

```sql
select ssl_is_used();
select ssl_cipher();
```

### SSL無しで接続

```sh
[ec2-user@bastin ~]$ export PGSSLMODE=disable
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postgres
psql (11.5, server 11.7)
Type "help" for help.

postgres=> select ssl_is_used();
 ssl_is_used 
-------------
 f
(1 row)
```

### SSL有りで接続

RDSは作成時にSSL証明書が自動的に用意されており、RDSへの接続は基本的にSSLが有効化されている。ログインプロンプトでもSSLが使用されていることが確認可能。

```sh
[ec2-user@bastin ~]$ psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postgres
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=> select ssl_is_used();
 ssl_is_used 
-------------
 t
(1 row)

postgres=> select ssl_cipher();
         ssl_cipher          
-----------------------------
 ECDHE-RSA-AES256-GCM-SHA384
(1 row)

```

SSL接続を有効化したい場合は`rds.force_ssl`を「0」から「1」に変更する。

### なりすまし防止、改ざん防止のために証明書を検証

ルート証明書を取得してなりすまし防止、改ざん防止のための検証を行う必要がある。検証を行う意味としては下記を参照。

> SSLって何？意味や仕組みをわかりやすく解説！ | さくらのSSL https://ssl.sakura.ad.jp/column/ssl/
>
> 改ざん防止となりすましの防止については、SSLサーバー証明書の「認証局」という組織の存在が重要になります。暗号化自体は認証局が無くても実現可能ですが、認証局はサーバーでもパソコンでもない第三者機関であり、「○○.jpを名乗るこのサイトは本当に○○.jpですよ」と保証してくれる組織です。
>
> 認証局が発行する「ルート証明書」というものはパソコンやスマートフォン内に保存され、サーバーから送られてくるSSLサーバー証明書と中間CA証明書が、本当にルート証明書と関連付けられた証明書（認証局が発行した証明書）であるかを検証します。ルート証明書はパソコン本体に入っており、悪意のある第三者が改ざんすることは難しいため、このような仕組みになっています。当然、不正なルート証明書をインストールして不正なSSLサーバー証明書を正当化しようとする悪意のある攻撃も存在します。
>
> 証明書の種類によっては「○○.jpとは、株式会社○○が運営しているサイトですよ」と運営組織を保証してくれる場合もあります（OV/EV認証）。銀行のホームページにアクセスして鍵アイコンをクリックすると会社名が表示されるのはEV証明書という特殊なSSLサーバー証明書を利用しているからです。

##### ルート証明書を取得

```sh
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
psql "host=aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com sslmode=verify-full sslrootcert=rds-combined-ca-bundle.pem user=postgres dbname=postgres"
```

##### 検証成功時

`psql`の引数として`sslrootcert`,`sslmode`を指定している。

```sh
[ec2-user@bastin ~]$ psql "host=aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com sslmode=verify-full sslrootcert=rds-combined-ca-bundle.pem user=postgres dbname=postgres"
psql (11.5, server 11.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.
```

下記の様に環境変数に設定することでも問題無し。

```sh
export PGSSLMODE=verify-full
export PGSSLROOTCERT=rds-combined-ca-bundle.pem
psql -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -d postgres
```

##### 検証失敗時

```sh
[ec2-user@bastin ~]$ psql "host=aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com sslmode=verify-full sslrootcert=dummy.pem user=postgres dbname=postgres"
psql: could not read root certificate file "dummy.pem": no SSL error reported
[ec2-user@bastin ~]$ 
```

### 参考

> Amazon Aurora PostgreSQL でのセキュリティ - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Security.html
>
> SSL/TLS 証明書の更新 - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.SSL-certificate-rotation.html