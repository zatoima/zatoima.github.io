---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "M1 MacにPostgreSQLをインストールする"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-mac-install-postgresql-homebrew
date: 2023-02-10
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

Homebrewがすでにシステムにインストールされていることを前提としている。Homebrewはオープンソースソフトウェアのパッケージ管理システムで、簡単なコマンドを使ってさまざまなソフトウェアのインストールやアップデートが可能となる。

### 1. PostgreSQLのインストール

最初に、インストール可能なPostgreSQLのバージョンを確認するため、以下のコマンドを実行する。

```sh
(base) jimazato@XXXXXXXX ~ % brew search postgresql
```

このコマンドを実行すると、利用可能なPostgreSQLのバージョン一覧が表示される。特定のバージョンを指定せずに最新バージョンをインストールする場合は、次のコマンドを実行する。

```sh
(base) jimazato@XXXXXXXX ~ % brew install postgresql
```

このコマンドはHomebrewの自動アップデートを実行した後、PostgreSQLをインストールする。

### 2. インストールバージョンの確認

インストールが完了したら、以下のコマンドでPostgreSQLのバージョンを確認することができる。

```sh
(base) jimazato@XXXXXXXX ~ % psql --version
```

これでPostgreSQLのバージョンが表示され、正しくインストールされたことが確認できる。また、Linuxでは`postgresql-contrib`のインストールが必要だが、Homebrewではpgbenchが一緒にインストールされるので注意する。

```sh
(base) jimazato@XXXXXXXX ~ % pgbench --version
```

### 3. AWSのRDSに接続してpgbenchを利用

PostgreSQLが正しくインストールされたら、AWSのRDSに接続して、pgbenchを使ってパフォーマンステスト（データ生成のみ）を行うことができる。pgbenchはPostgreSQLの性能評価ツールで、事前に大量のテストデータを作成したり、一定の負荷をかけて性能を評価することができる。

まずは、RDSに接続するためのコマンドを以下に示す。

```sh
(base) jimazato@XXXXXXXX ~ % psql -h xxxx-rds-pgsql.xxxxxx.us-west-1.rds.amazonaws.com -U postgres -d postgres
```

接続が成功すると、以下のようなメッセージが表示される。

```
psql (14.7 (Homebrew), server 13.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.
```

次に、pgbenchを利用してパフォーマンステストを実行する。以下のコマンドを使用する。

```sh
(base) jimazato@XXXXXXXX ~ % pgbench -r -c 10 -j 10 -t 10 -U postgres -h xxxx-rds-pgsql.xxxxxx.us-west-1.rds.amazonaws.com pgbench
```

これでテストが実行され、その結果が表示される。これらの情報を活用して、RDSのPostgreSQLのパフォーマンスを評価できる。

