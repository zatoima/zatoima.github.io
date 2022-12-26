---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLのInnoDB バッファープールのプリロード"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-buffer-pool-load.html
date: 2019-07-19
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



### はじめに

MySQLのバッファープールのプリロード機能について整理する。※Oracleにはない機能なので気になった

### 関連するシステム変数

```sql
mysql> select version();
+------------+
| version()  |
+------------+
| 5.7.26-log |
+------------+
1 row in set (0.00 sec)

mysql>

mysql> show variables like 'innodb_buffer_pool%';
+-------------------------------------+----------------+
| Variable_name                       | Value          |
+-------------------------------------+----------------+
| innodb_buffer_pool_chunk_size       | 134217728      |
| innodb_buffer_pool_dump_at_shutdown | ON             |
| innodb_buffer_pool_dump_now         | OFF            |
| innodb_buffer_pool_dump_pct         | 25             |
| innodb_buffer_pool_filename         | ib_buffer_pool |
| innodb_buffer_pool_instances        | 1              |
| innodb_buffer_pool_load_abort       | OFF            |
| innodb_buffer_pool_load_at_startup  | ON             |
| innodb_buffer_pool_load_now         | OFF            |
| innodb_buffer_pool_size             | 134217728      |
+-------------------------------------+----------------+
10 rows in set (0.00 sec)
```

##### innodb_buffer_pool_dump_at_shutdown

シャットダウン時にバッファプール上のキャッシュを保持するかどうか。

> https://dev.mysql.com/doc/refman/5.6/ja/innodb-parameters.html#sysvar_innodb_buffer_pool_dump_at_shutdown
> 次回再起動時のウォームアッププロセスの時間を短縮するために、MySQL サーバーのシャットダウン時に、InnoDB のバッファープールにキャッシュされるページを記録するかどうかを指定します。一般に、innodb_buffer_pool_load_at_startup と組み合わせて使用されます。

シャットダウン後に `ib_buffer_pool` が作成されている。

```sql
[mysql@awsstg-db001 mysql]$ ls -l ib_buffer_pool
-rw-r----- 1 mysql mysql 3206 Jun 29 15:07 ib_buffer_pool
[mysql@awsstg-db001 mysql]$
```

このパラメータを設定することでシャットダウンシーケンス時にはエラーログに下記のログが出力される。

```sql
2019-06-27T07:59:52.431613Z 0 [Note] InnoDB: Starting shutdown...
2019-06-27T07:59:52.531945Z 0 [Note] InnoDB: Dumping buffer pool(s) to /var/lib/mysql/ib_buffer_pool
2019-06-27T07:59:52.532242Z 0 [Note] InnoDB: Buffer pool(s) dump completed at 190627  7:59:52
2019-06-27T07:59:54.242932Z 0 [Note] InnoDB: Shutdown completed; log sequence number 616413821
```

##### innodb_buffer_pool_load_at_startup

スタートアップ時に `ib_buffer_pool` を読み込んでバッファプールにプリロードを行う。

> https://dev.mysql.com/doc/refman/5.6/ja/innodb-parameters.html#sysvar_innodb_buffer_pool_load_at_startup
> MySQL サーバーの起動時に、以前に保持されたときと同じページをロードすることで、InnoDB のバッファープールが自動的にウォームアップされるように指定します。一般に、innodb_buffer_pool_dump_at_shutdown と組み合わせて使用されます。

##### innodb_buffer_pool_filename

記録するファイル名を指定

##### innodb_buffer_pool_dump_now/innodb_buffer_pool_load_at_startup

シャットダウンやスタートアップ時ではなくMySQLがオンライン時に任意のタイミングで即時書き出し、及び即時読み込みを行う。

### ib_buffer_poolに保存される情報

`必要なテーブルスペース ID` と `ページ ID`

```sql
[mysql@awsstg-db001 mysql]$ head ib_buffer_pool
0,890
0,889
0,888
0,887
0,886
0,885
0,884
0,883
0,882
0,881
```

> 該当するページを見つけるために必要なテーブルスペース ID とページ ID だけがディスクに保存されます。この情報は、`INNODB_BUFFER_PAGE_LRU` `INFORMATION_SCHEMA` テーブルから取得されます。デフォルトでは、テーブルスペース ID とページ ID のデータは、`InnoDB` データディレクトリに保存される `ib_buffer_pool` という名前のファイル内に保存されます。このファイル名は、`innodb_buffer_pool_filename` 構成パラメータを使用して変更できます。

この情報は `INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU` から取得される模様。

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU LIMIT 1\G
*************************** 1. row ***************************
            POOL_ID: 0
       LRU_POSITION: 0
              SPACE: 30
        PAGE_NUMBER: 11063
          PAGE_TYPE: INDEX
         FLUSH_TYPE: 0
          FIX_COUNT: 0
          IS_HASHED: NO
NEWEST_MODIFICATION: 0
OLDEST_MODIFICATION: 0
        ACCESS_TIME: 2747830684
         TABLE_NAME: `mydb`.`t1`
         INDEX_NAME: PRIMARY
     NUMBER_RECORDS: 648
          DATA_SIZE: 14904
    COMPRESSED_SIZE: 0
         COMPRESSED: NO
             IO_FIX: IO_NONE
             IS_OLD: YES
    FREE_PAGE_CLOCK: 0
1 row in set (0.01 sec)

```