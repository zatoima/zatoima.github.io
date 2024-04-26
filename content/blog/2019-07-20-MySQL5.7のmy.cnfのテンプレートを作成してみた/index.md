---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQL5.7のmy.cnfのテンプレートを作成してみた"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-myconf-setting-template.html
date: 2019-07-20
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


MySQLのどのシステム変数をmy.cnfに指定するかを明示的にするためにテンプレートを作成しました。

要件や環境(メモリ値、ディレクトリ構成、ディスク性能（HDD or SSD）)に応じて変更する部分が多々ありますのでご注意ください。

※適宜追加、修正していく予定。

### バージョン想定

`MySQL 5.7` を想定しています。

```sql
mysql> select version();
+------------+
| version()  |
+------------+
| 5.7.26-log |
+------------+
1 row in set (0.00 sec)
```

### my.cnfテンプレート

```sql
[mysqld]
# 環境に応じてチューニングが必須

# #################
# Common
# #################

# オートコミット機能を無効化
# init_connectで指定したSQL文はSUPER権限を持ったユーザに対しては実行されない
init_connect='SET AUTOCOMMIT=0'

# パスワードのチェックを無効化する
validate-password=OFF

# バイナリログを有効化
log-bin

# サーバID
server_id=1

# データディレクトリ
datadir=/var/lib/mysql

# ソケット・ファイル
socket=/var/lib/mysql/mysql.sock

# キャラクタセットの指定
character_set_server=utf8mb4

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

# mysqld.logファイルの指定
log-error=/var/log/mysqld.log

# mysqld.pidファイルの指定
pid-file=/var/run/mysqld/mysqld.pid


# #################
# innodb
# #################

# InnoDBデータファイルのパス
innodb_data_file_path = ibdata1:1G:autoextend

# InnoDBテーブルスペース自動拡張サイズ
innodb_autoextend_increment = 64

# InnoDBのデータとインデックスをキャッシュするバッファのサイズ(推奨は物理メモリの8割)
innodb_buffer_pool_size=300M

# コミットされていないトランザクションのためのバッファのサイズ。innodb_buffer_pool_sizeの25%程度(最大でも64MB)
# データインポート時やデータの洗替え時などは32M等に設定する
innodb_log_buffer_size=8M

# innodb_buffer_pool_sizeをいくつのインスタンスに分けるか指定。バッファサイズが大きい場合は分割することを推奨
# innodb_buffer_pool_instances=8

# InnoDBの更新ログを記録するディスク上のファイルサイズ(innodb_buffer_pool_sizeの4分の1程度)
innodb_log_file_size=1G

# データやインデックスを共有ではなくテーブル個別に保存する
innodb_file_per_table=1

# OSのキャッシュをバイパスするかどうかを制御する
# InnoDBとOSのファイルシステムキャッシュの両方にあるという「ダブルバッファリング」を防止するためにO_DIRECTを使用する
innodb_flush_method=O_DIRECT

# バッファプール上で変更されたデータをディスクに書き出す場合に、近隣のページをまとめて1回のI/Oで書き出す仕組み(SSDの場合は無効化が推奨)
innodb_flush_neighbors=0

# 未コミットのトランザクション情報をキャッシュするメモリ上の領域。ラージトランザクションを実行してキャッシュから溢れて一時表を作成するケースにチューニングすることで有効
binlog_cache_size=32768

# 変更をREDOログに同期するタイミングを制御。ACIDが不要な場合に0 or 2を設定して高速化を図る。
innodb_flush_log_at_trx_commit=1

# ダブルライトバッファの無効化
# データインポート時のみ指定(通常時は指定しない)
# skip_innodb_doublewrite

# InnoDBの書込み要求に使用されるバックグラウンドスレッドの数
innodb_write_io_threads = 8

# InnoDBの読取り要求に使用されるバックグラウンドスレッドの数
innodb_read_io_threads = 8

# InnoDB で使用できる全体的な I/O容量(IOPS値が妥当)。SSD、HDDで変更すべき
innodb_io_capacity=200

# innodb_io_capacity の変更に合わせて変更（設定しない場合、デフォルト値が innodb_io_capacity の 2 倍。下限2000）
innodb_io_capacity_max=2000


# #################
# query cache
# #################

# クエリキャッシュのブロックサイズ
query_cache_min_res_unit=4096

# クエリキャッシュ最大サイズ
query_cache_limit=16M

# クエリキャッシュで使用するメモリサイズ
query_cache_size=128M

# クエリキャッシュのタイプ(0:off, 1:ON SELECT SQL_NO_CACHE以外, 2:DEMAND SELECT SQL_CACHEのみ)
query_cache_type=2

# #################
# slow query log
# #################

# スロークエリの出力設定
slow_query_log=ON

# スロークエリと判定する秒数
long_query_time=3

# スロークエリログの場所(あらかじめ作成しておく必要あり)
slow_query_log_file=/var/log/slow.log

# #################
# replication
# #################

# GTID有効
gtid_mode=on

# GTID利用時に必須となる設定（GTIDの一貫性を担保できないSQLの実行を禁止）
enforce_gtid_consistency=on

# #################
# thread buffer
# #################

# インデックス未使用でのJOIN時に使用するバッファ
join_buffer_size=256K

# フルスキャンのレコードバッファ
read_buffer_size=1M

# ソート時に使用されるバッファ
sort_buffer_size=4M

# キーを使用したソートで読み込まれた行がキャッシュされるバッファ
read_rnd_buffer_size=2M


# #################
# etc
# #################

# クライアントからサーバーに送信できるパケットの最大長
max_allowed_packet=8M

# MEMORYテーブルの最大サイズ。このサイズを超えたMEMORYテーブルはディスク上に作成
max_heap_table_size=16M

# スレッド毎に作成される一時的なテーブルの最大サイズ。スレッドバッファ
tmp_table_size=16M

# スレッドキャッシュ保持最大数
thread_cache_size=100

# コネクションタイムアウト時間
wait_timeout=30

# テーブルキャッシュ値。本値を変更する際はopen_files_limitも合わせて引き上げる必要がある。
# open_files_limitはOS側がmysqldプロセスに対して許可するファイルディスクリプタ上限を制御。
table_open_cache=2000

# テーブル定義キャッシュ。テーブル定義（.frmファイル）をキャッシュし、テーブルをオープンする際に高速化
table_definition_cache=1400

# 送受信するパケットを格納するパケットメッセージバッファサイズの初期値
net_buffer_length=16384

```

### 参考

##### 参考ブログ1

> (帰ってきた)InnoDBパフォーマンス最適化の基礎 | Yakst https://yakst.com/ja/posts/65

##### 参考ブログ2

> MySQLをインストールしたら、必ず確認すべき10の設定 | Yakst https://yakst.com/ja/posts/200

##### 参考ブログ3

> MySQL関連のパラメータ(主にInnoDB)について - hiroi10のブログ http://hiroi10.hatenablog.com/entry/20151210/1449731029

##### 参考書籍1

[asin:4774170208:detail]

##### 参考書籍2

[asin:B01N0R2BL2:detail]




