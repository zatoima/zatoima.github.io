---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのpg_dump、pg_restoreについてまとめる"
subtitle: ""
summary: " "
tags: ["PostgreSQL","pg_dump", "pg_restore"]
categories: ["PostgreSQL"]
url: postgresql-about-pg_dump-pg_restore.html
date: 2019-12-03
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



## はじめに

これから何度も調べることになりそうなので、PostgreSQLのpg_dump、pg_restoreについてまとめておく。

スクリプトファイル形式とアーカイブファイル形式でバックアップが可能。それぞれでリストア方式が異なる。

1. スクリプトファイル形式の論理バックアップ  :  psqlでリストア
2. アーカイブファイル形式の論理バックアップ  :  pg_restoreでリストア

## 基本コマンド

### １．スクリプトファイル形式の論理バックアップ

#### データベース単位のバックアップ

​	`mydb`という名前のデータベースをSQLスクリプトファイルにダンプ

```sql
pg_dump mydb > db.sql
```

#### テーブル単位のバックアップ

`mytab`という名前の単一のテーブルをダンプ

```sql
pg_dump -t mytab mydb > db.sql
```

#### リストア

`newdb`というデータベースにdb.sqlの内容をリストア

```
psql -d newdb -f db.sql
```



### ２．アーカイブファイル形式の論理バックアップ

この場合、圧縮されるため、データやデータ型にも依存するが一定のデータが減る。

#### データベース単位のバックアップ

​	`mydb`という名前のデータベースをアーカイブファイル形式にダンプ。

```sql
pg_dump -Fc mydb > db.dump
```

#### テーブル単位のバックアップ

`mytab`という名前の単一のテーブルをアーカイブファイル形式にダンプ

```sql
pg_dump -t mytab -Fc mydb > db.dump
```

#### リストア

`newdb`というデータベースにdb.dumpの内容をリストア

```
pg_restore -d newdb db.dump
```

### 3.コマンドのオプション

##### pg_dump

| 引数（省略系） | 引数                | 説明                                                         |
| -------------- | ------------------- | ------------------------------------------------------------ |
| -a             | --data-only         | データのみをダンプし、スキーマ（データ定義）はダンプしない   |
| -b             | --blobs             | ラージオブジェクトをダンプに含める。     --schema、--table、--schema-onlyが指定された場合を除き、これがデフォルトの動作 |
| -c             | --clean             | データベースオブジェクトを作成するコマンドの前に、データベースオブジェクトを整理（削除）するコマンドを書き出す。スクリプト形式の場合にのみ有効。 |
| -C             | --create            | 初めにデータベース自体を作成するコマンドを出力し、その後、作成したデータベースに接続するコマンドを出力する。スクリプト形式の場合にのみ有効。 |
| -f file        | --file=file         | 出力を指定のファイルに書き出す                               |
| -F format      | --format=format     | p/plain 平文のSQLスクリプトファイルを出力                    |
|                |                     | c/custom  pg_restoreへの入力に適したカスタム形式アーカイブを出力 |
| -s             | --schema-only       | データ定義（スキーマ）のみをダンプし、データはダンプしない   |
| -j njobs       | --jobs=njobs        | njobs個のテーブルを同時にダンプすることによって、並行してダンプを実行 |
| -d dbname      | --dbname=dbname     | 接続するデータベースの名前を指定                             |
| -h host        | --host=host         | サーバが稼働しているマシンのホスト名を指定                   |
| -p port        | --port=port         | サーバが接続を監視するTCPポート                              |
| -U username    | --username=username | 接続ユーザ名を指定                                           |

##### pg_restore

| 引数（省略系） | 引数                | 説明                                                         |
| -------------- | ------------------- | ------------------------------------------------------------ |
| -a             | --data-only         | データのみをダンプし、スキーマ（データ定義）はダンプしない   |
| -c             | --clean             | 再作成前にデータベースオブジェクトを整理（削除）             |
| -C             | --create            | リストア前にデータベースを作成                               |
| -d dbname      | --dbname=dbname     | dbnameデータベースに接続し、このデータベースに直接リストア   |
| -e             | --exit-on-error     | データベースにSQLコマンドを送信中にエラーが発生した場合、処理を終了 |
| -F format      | --format=format     | pg_restoreは形式を自動認識するので、このオプションは必須ではない |
|                |                     | p/plain 平文のSQLスクリプトファイルを出力                    |
|                |                     | c/custom  pg_restoreへの入力に適したカスタム形式アーカイブを出力 |
| -j njobs       | --jobs=njobs        | データのロード、インデックスの作成、制約の作成部分を複数の同時実行ジョブを使用して実行 |
| -s             | --schema-only       | アーカイブ内にあるスキーマ項目の範囲でスキーマ（データ定義）のみをリストアし、データ（テーブルの内容）をリストアしない |
| -h host        | --host=host         | サーバが稼働しているマシンのホスト名を指定                   |
| -p port        | --port=port         | サーバが接続を監視するTCPポート                              |
| -U username    | --username=username | 接続ユーザ名を指定                                           |
| -v             | --verbose           | 冗長モードを指定                                             |

### 4.個人的によく使うコマンド例

AWSのRDS等で使う場合はリモートホストに対して実行することになるので、`-h`オプションが必要。

テーブルのデータのみ pg_dump でexport(カスタムモード)

```sh
pg_dump -h aurorapostgresdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U <ユーザ名> -a -t <Table名> -Fc <DB名> > rds01.custom
```

rds01に接続してインポート前にオブジェクトを削除してインポートする

```sh
pg_restore -v -h aurorapostgresdb.xxxxxxx.ap-northeast-1.rds.amazonaws.com -U <ユーザ名> -c -C -d <DB名> /home/ec2-user/rds01_dump_2.custom
```

スキーマ定義のみインポートする

```sh
pg_restore -v -h rdspostgresql1.xxxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U <ユーザ名> -s -d <DB名> /home/ec2-user/rds01_dump_2.custom
```

データのみインポートする

```sh
pg_restore -v -h aurorapostgresdb.xxxxxxxxxx.ap-northeast-1.rds.amazonaws.com -U <ユーザ名> -a -d <DB名> /home/ec2-user/rds01_dump_2.custom
```

リストア時にパラレルで実行する（8並列で実行）

```
pg_restore -h aurorapgsqlv1.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -j 8 -d tpcc tpcc.dump
```



## 参考

> pg_dump [https://www.postgresql.jp/document/10/html/app-pgdump.html](https://www.postgresql.jp/document/10/html/app-pgdump.html)

> pg_restore [https://www.postgresql.jp/document/10/html/app-pgrestore.html](https://www.postgresql.jp/document/10/html/app-pgrestore.html)

