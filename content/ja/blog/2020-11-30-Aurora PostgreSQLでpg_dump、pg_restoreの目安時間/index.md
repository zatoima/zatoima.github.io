---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLのpg_dump、pg_restore目安時間"
subtitle: ""
summary: " "
tags: ["AWS","Aurora",PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-pg_dump_pg_restore_time.html
date: 2020-11-30
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

EC2上の踏み台サーバに対して、Aurora PostgreSQLのデータをpg_dumpして、pg_restoreする時間を計測してみた。インスタンスタイプやディスクサイズ、IOPS指定により、ネットワーク帯域やディスクのIO性能も変わってくるので目安程度に。

#### 結果

| No   | 検証パターン   | DB名     | DBサイズ（GB) | データの中身                                 | 開始時間 | 終了時間 | 所要時間 |
| ---- | -------------- | -------- | ------------- | -------------------------------------------- | -------- | -------- | -------- |
| 1    | pg_dump        | postgres | 729GB         | 青空文庫のテキストデータ                     | 14:31:33 | 19:01:44 | 4:30:11  |
| 2    | ※並列度1で実施 | tpch     | 45GB          | HammerDBのtpc-hのデータ                      | 12:59:44 | 13:34:22 | 0:34:38  |
| 3    |                | tpcc     | 118GB         | HammerDBのtpc-cのデータ                      | 13:43:07 | 14:26:32 | 0:43:25  |
| 4    |                | blob     | 98GB          | byteaにバイナリ（25MBファイル×4000ファイル） | 9:26:14  | 12:38:51 | 3:12:37  |
| 5    | pg_dump        | postgres | 729GB         | 同上                                         | 18:30:26 | 19:59:33 | 1:29:07  |
| 6    | ※並列度8で実施 | tpch     | 45GB          | 同上                                         | 18:11:08 | 18:28:35 | 0:17:27  |
| 7    |                | tpcc     | 118GB         | 同上                                         | 13:16:13 | 13:44:05 | 0:27:52  |
| 8    |                | blob     | 98GB          | 同上                                         | 20:01:51 | 21:04:38 | 1:02:47  |
| 9    | pg_restore     | postgres | 729GB         | 同上                                         | 21:09:34 | 0:26:25  | 3:16:51  |
| 10   | ※並列度8で実施 | tpch     | 45GB          | 同上                                         | 20:58:25 | 21:06:24 | 0:07:59  |
| 11   |                | tpcc     | 118GB         | 同上                                         | 20:46:58 | 20:56:44 | 0:09:46  |
| 12   |                | blob     | 98GB          | 同上                                         | 12:45:23 | 13:07:43 | 0:22:20  |

#### 並列度1のpg_dumpコマンド

```sh
pg_dump -h aurorapgsqlv1.cluster-xxxx.ap-northeast-1.rds.amazonaws.com -U postgres -Fc postgres > postgres.dump
```

#### 並列度8のpg_dumpコマンド

```sh
pg_dump -h aurorapgsqlv1.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -j 8 -U postgres -F d -f /data/postgres postgres
```

#### 並列度8のpg_restoreコマンド

```sh
pg_restore -h aurorapgsqlv1.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -j 8 -d postgres postgres.dump
```

