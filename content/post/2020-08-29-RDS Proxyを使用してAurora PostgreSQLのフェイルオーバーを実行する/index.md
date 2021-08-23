---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDS Proxyを使用してAurora PostgreSQLのフェイルオーバーを実行する"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-postgresql-rdsproxy-failover.html
date: 2020-08-29
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



RDS Proxyを触って見つつ、フェイルオーバーがどのくらいで完了するのか、動きを含めて確認してみたいという目的。

従来のクラスタエンドポイントの場合は、DNSを利用してWriter と Readerの切替を実装しているが、RDS Proxyの場合は、アプリケーションとRDS Proxyの接続は維持したままで、DB側のフェイルオーバーを検出してシームレスに接続する。アプリケーションから再接続やDNSのTTLの考慮が不要になる。トランザクション中やクエリ処理中の接続は再接続が必要。

> Amazon RDS Proxy のご紹介
>
> https://pages.awscloud.com/rs/112-TZM-766/images/EV_amazon-rds-aws-lambda-update_Jul28-2020_RDS_Proxy.pdf

というわけでクラスタエンドポイントを使用するパターンとRDS Proxyを使用するパターンでフェイルオーバーや実施してみる。

### パターン1：クラスタエンドポイントで実施パターン

適当に下記スクリプトを実行してタイムスタンプをテーブルに記録してスクリプト実行中に手動フェイルオーバーを実行する。

#### テストスクリプト

1秒ごとにINSERTを実施

```sh
#! /bin/bash

while true
do
  #truncate table record;
  #create table record(id serial,create_at timestamp);
  DATETIME=$(date -u "+%Y-%m-%d %T.%N")
  echo $DATETIME
  psql -q -h a-pgsql.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "insert into record(create_at) VALUES (current_timestamp)" &
  sleep 1
done
```

### フェイルオーバー自体に掛かった時間

約30秒弱でフェイルオーバー自体は完了

| 時間                              | システムノート                                               |
| --------------------------------- | ------------------------------------------------------------ |
| August 29th 2020, 11:44:48 am UTC | Completed failover to DB instance: a-pgsql-instance-1-ap-northeast-1a |
| August 29th 2020, 11:44:23 am UTC | Started cross AZ failover to DB instance: a-pgsql-instance-1-ap-northeast-1a |

#### bashの実行ログ

フェイルオーバーの開始から完了までデータベースが使えなくなるというわけではなく、`11:44:29`から`11:44:40` の約11秒間でフェイルオーバーに伴いエラーが出ている

```sh
2020-08-29 11:44:27.964959626
2020-08-29 11:44:28.966971425
2020-08-29 11:44:29.968957489
WARNING:  terminating connection because of crash of another server process
DETAIL:  The postmaster has commanded this server process to roll back the current transaction and exit, because another server process exited abnormally and possibly corrupted shared memory.
HINT:  In a moment you should be able to reconnect to the database and repeat your command.
psql: SSL SYSCALL error: EOF detected
SSL SYSCALL error: EOF detected
connection to server was lost
2020-08-29 11:44:30.971007776
psql: could not connect to server: Connection refused
	Is the server running on host "a-pgsql.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com" (10.0.3.43) and accepting
	TCP/IP connections on port 5432?
2020-08-29 11:44:31.972952018
2020-08-29 11:44:32.974997039
2020-08-29 11:44:33.977032145
psql: FATAL:  the database system is starting up
FATAL:  the database system is starting up
psql: FATAL:  the database system is starting up
FATAL:  the database system is starting up
psql: FATAL:  the database system is starting up
FATAL:  the database system is starting up
2020-08-29 11:44:34.979111133
ERROR:  cannot execute INSERT in a read-only transaction
2020-08-29 11:44:35.981149831
ERROR:  cannot execute INSERT in a read-only transaction
2020-08-29 11:44:36.983173817
ERROR:  cannot execute INSERT in a read-only transaction
2020-08-29 11:44:37.985163358
ERROR:  cannot execute INSERT in a read-only transaction
2020-08-29 11:44:38.987178155
ERROR:  cannot execute INSERT in a read-only transaction
2020-08-29 11:44:39.989168920
2020-08-29 11:44:40.991212531
2020-08-29 11:44:41.993185159
2020-08-29 11:44:42.995173285
2020-08-29 11:44:43.997177503
2020-08-29 11:44:44.999206797
2020-08-29 11:44:46.001261962
2020-08-29 11:44:47.003287661
2020-08-29 11:44:48.005291195
```

#### データベース側に記録された時間

bashで接続エラーがあった`11:44:29`から`11:44:40` あたりのINSERT分が抜けている。十分短いが、、、

```
| 1065 | 2020-08-29 11:44:19.974279 |
| 1066 | 2020-08-29 11:44:20.976299 |
| 1067 | 2020-08-29 11:44:21.984021 |
| 1068 | 2020-08-29 11:44:22.981434 |
| 1069 | 2020-08-29 11:44:23.982408 |
| 1070 | 2020-08-29 11:44:24.984163 |
| 1071 | 2020-08-29 11:44:25.986223 |
| 1072 | 2020-08-29 11:44:26.991738 |
| 1073 | 2020-08-29 11:44:28.024189 |
| 1090 | 2020-08-29 11:44:40.040502 |
| 1091 | 2020-08-29 11:44:41.006773 |
| 1092 | 2020-08-29 11:44:42.012005 |
| 1093 | 2020-08-29 11:44:43.010699 |
| 1094 | 2020-08-29 11:44:44.014737 |
| 1095 | 2020-08-29 11:44:45.089499 |
| 1096 | 2020-08-29 11:44:46.020322 |
| 1097 | 2020-08-29 11:44:47.01858  |
| 1098 | 2020-08-29 11:44:48.024825 |
| 1099 | 2020-08-29 11:44:49.028113 |
| 1100 | 2020-08-29 11:44:50.026786 |
```

### パターン２：RDS Proxyで実施パターン

パターン1と同じ手順でスクリプトを実行してフェイルオーバーに掛かる時間やDBへの接続状況などを見てみる。RDS Proxyのエンドポイントを接続先に指定。

#### スクリプト

```sh
#! /bin/bash

while true
do
  #truncate table record;
  #create table record(id serial,create_at timestamp);
  DATETIME=$(date -u "+%Y-%m-%d %T.%N")
  echo $DATETIME
  psql -q -h proxy-aurora.proxy-xxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "insert into record(create_at) VALUES (current_timestamp)" &
  sleep 0.5
done
```

### フェイルオーバー自体に掛かった時間

約36秒でフェイルオーバーは完了

| 時間                              | システムノート                                               |
| --------------------------------- | ------------------------------------------------------------ |
| August 29th 2020, 12:05:03 pm UTC | Completed failover to DB instance: a-pgsql-instance-1        |
| August 29th 2020, 12:04:39 pm UTC | Started cross AZ failover to DB instance: a-pgsql-instance-1 |

#### bashの実行ログ

フェイルオーバーに伴い`12:04:48`あたりでエラーが出ているが、クラスタエンドポイントを使用したパターン①の検証と異なりエラー自体の傾向が異なる

```sh
2020-08-29 12:04:30.095671574
2020-08-29 12:04:31.097629856
2020-08-29 12:04:32.099684736
2020-08-29 12:04:33.101745645
2020-08-29 12:04:34.103755036
2020-08-29 12:04:35.105731120
2020-08-29 12:04:36.107736230
2020-08-29 12:04:37.109709993
2020-08-29 12:04:38.111698832
2020-08-29 12:04:39.113675005
2020-08-29 12:04:40.115698907
2020-08-29 12:04:41.117673464
2020-08-29 12:04:42.119682149
2020-08-29 12:04:43.121650566
2020-08-29 12:04:44.123618407
2020-08-29 12:04:45.125820156
2020-08-29 12:04:46.127808056
2020-08-29 12:04:47.129771043
2020-08-29 12:04:48.131772090
WARNING:  terminating connection because of crash of another server process
DETAIL:  The postmaster has commanded this server process to roll back the current transaction and exit, because another server process exited abnormally and possibly corrupted shared memory.
HINT:  In a moment you should be able to reconnect to the database and repeat your command.
SSL connection has been closed unexpectedly
connection to server was lost
WARNING:  terminating connection because of crash of another server process
DETAIL:  The postmaster has commanded this server process to roll back the current transaction and exit, because another server process exited abnormally and possibly corrupted shared memory.
HINT:  In a moment you should be able to reconnect to the database and repeat your command.
SSL connection has been closed unexpectedly
connection to server was lost
2020-08-29 12:04:49.133763120
2020-08-29 12:04:50.135776827
2020-08-29 12:04:51.137775212
2020-08-29 12:04:52.139811209
2020-08-29 12:04:53.141852628
2020-08-29 12:04:54.143861363
2020-08-29 12:04:55.145887875
2020-08-29 12:04:56.147877446
2020-08-29 12:04:57.149851817
2020-08-29 12:04:58.151858291
2020-08-29 12:04:59.153685252
2020-08-29 12:05:00.155651975
2020-08-29 12:05:01.157824634
2020-08-29 12:05:02.159847039
2020-08-29 12:05:03.161849475
2020-08-29 12:05:04.163848675
2020-08-29 12:05:05.165860863
2020-08-29 12:05:06.167913253
2020-08-29 12:05:07.169922306
2020-08-29 12:05:08.171957895
2020-08-29 12:05:09.173986169
2020-08-29 12:05:10.175984477
2020-08-29 12:05:11.177993763
2020-08-29 12:05:12.180028575
2020-08-29 12:05:13.182031977
2020-08-29 12:05:14.184081473

```

#### データベース側に記録された時間

`12:04:46`から`12:04:53`の間で更新が止まっていますが、約7秒で切り替わったことが分かる

```
| 1170 | 2020-08-29 12:04:39.156067 |
| 1171 | 2020-08-29 12:04:40.240195 |
| 1172 | 2020-08-29 12:04:41.161005 |
| 1173 | 2020-08-29 12:04:42.189308 |
| 1174 | 2020-08-29 12:04:43.318342 |
| 1175 | 2020-08-29 12:04:44.227378 |
| 1176 | 2020-08-29 12:04:45.167466 |
| 1177 | 2020-08-29 12:04:46.247739 |
| 1189 | 2020-08-29 12:04:53.329366 |
| 1190 | 2020-08-29 12:04:53.339468 |
| 1191 | 2020-08-29 12:04:53.353239 |
| 1192 | 2020-08-29 12:04:53.380346 |
| 1193 | 2020-08-29 12:04:53.391141 |
| 1194 | 2020-08-29 12:04:54.204525 |
| 1195 | 2020-08-29 12:04:55.284926 |
| 1196 | 2020-08-29 12:04:56.199496 |
| 1197 | 2020-08-29 12:04:57.222213 |
| 1198 | 2020-08-29 12:04:58.297598 |
| 1199 | 2020-08-29 12:04:59.192773 |
| 1200 | 2020-08-29 12:05:00.26938  |
| 1201 | 2020-08-29 12:05:01.217964 |
| 1202 | 2020-08-29 12:05:02.418454 |
| 1203 | 2020-08-29 12:05:03.212937 |
| 1204 | 2020-08-29 12:05:04.231207 |
| 1205 | 2020-08-29 12:05:05.202887 |
| 1206 | 2020-08-29 12:05:06.243436 |
| 1207 | 2020-08-29 12:05:07.221574 |
| 1208 | 2020-08-29 12:05:08.230837 |
| 1209 | 2020-08-29 12:05:09.218686 |
| 1210 | 2020-08-29 12:05:10.228458 |
| 1211 | 2020-08-29 12:05:11.28525  |

```

何回か同じような検証を行った場合も RDS Proxy に掛かる時間は短かった。次はRDS Proxy を使用してLamdbaのコネクションプール的な使い方について整理したい。

### 参考資料

> Amazon RDS Proxy を使用したアプリケーションの可用性の向上 | Amazon Web Services ブログ https://aws.amazon.com/jp/blogs/news/improving-application-availability-with-amazon-rds-proxy/

> RDS Proxyを使うとDB接続処理は早くなるのか？ | Developers.IO https://dev.classmethod.jp/articles/rds-proxy-connect-benchmark/