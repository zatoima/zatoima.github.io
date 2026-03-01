---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ElastiCacheのRedisにベンチマークを実施する"
subtitle: ""
summary: " "
tags: ["AWS","ElastiCache","Redis"]
categories: ["AWS","ElastiCache","Redis"]
url: aws-elasticache-redis-benchmark.html
date: 2020-11-27
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

デフォルトで付属される`redis-benchmark`を使用してElastiCacheのRedisに対してベンチマークをしてみる。

#### マニュアル

> How fast is Redis? – Redis https://redis.io/topics/benchmarks

#### オプション説明

| オプション | オプション補足 | デフォルト値 | 説明                                                         |
| ---------- | -------------- | ------------ | ------------------------------------------------------------ |
| -h         | <hostname>     | 127.0.0.1    | サーバーのホスト名を指定                                     |
| -p         | <port>         | 6379         | サーバポートを指定                                           |
| -s         | <socket>       |              | サーバソケットを指定                                         |
| -c         | <clients>      | 50           | 同時接続数を指定                                             |
| -n         | <requests>     | 100000       | リクエストの数を指定                                         |
| -d         | <size>         | 2            | データサイズのバイトの形式でSET / GETの値を指定              |
| -r         | <keyspacelen>  |              | 実際のオペレーションを想定してランダムなコマンドを発行して、キャッシュミスを誘発する<br />例：100kの可能なキーのうちすべての操作にランダムキーを使用して100万のSET操作を実行する<br />redis-benchmark -t set -r  100000 -n 1000000 |
| -k         |                | 1            | 1=keep alive 0=reconnect                                     |
| -P         |                | 1            | パイプラインを有効化<br />https://redis.io/topics/pipelining |
| -q         |                |              | クエリ/秒の値のみを表示                                      |
| -csv       |                |              | CSV形式で出力。ヘッダーは出力されないので注意                |
| -l         |                |              | ひたすらループ処理                                           |
| -t         | <tests>        |              | カンマで区切られたテストのリストのみを実行     例： -t get,set → get と setコマンドのみ実行 |
| -I         |                |              | アイドルモード                                               |

#### パターン1

デフォルト設定で実施。リクエスト数「100,000」、同時接続数「50」、データサイズ「2バイト」等

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com
```

出力結果

レイテンシのばらつきやレクエストが何秒で完了したか出力

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com
====== PING_INLINE ======
  100000 requests completed in 2.62 seconds
  50 parallel clients
  3 bytes payload
  keep alive: 1

12.45% <= 1 milliseconds
98.95% <= 2 milliseconds
99.54% <= 3 milliseconds
99.75% <= 4 milliseconds
99.90% <= 5 milliseconds
99.97% <= 6 milliseconds
100.00% <= 6 milliseconds
38138.82 requests per second

～省略～
```

#### パターン2

サイレントモードで実施する。クエリ/秒の値のみを表示。

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -q
```

出力結果

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -q
PING_INLINE: 43840.42 requests per second
PING_BULK: 35958.29 requests per second
SET: 37907.50 requests per second
GET: 34293.55 requests per second
INCR: 41288.19 requests per second
LPUSH: 43327.55 requests per second
RPUSH: 43725.41 requests per second
LPOP: 46403.71 requests per second
RPOP: 44943.82 requests per second
SADD: 45085.66 requests per second
HSET: 27563.40 requests per second
SPOP: 34258.31 requests per second
LPUSH (needed to benchmark LRANGE): 31279.32 requests per second
LRANGE_100 (first 100 elements): 30902.35 requests per second
LRANGE_300 (first 300 elements): 15941.34 requests per second
LRANGE_500 (first 450 elements): 12241.40 requests per second
LRANGE_600 (first 600 elements): 9856.10 requests per second
MSET (10 keys): 25766.55 requests per second
```

#### パターン3

クライアント数を「100」に増やし、かつ「set」と「get」コマンドのみ実行する。（サイレントモード）

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -q -t set,get
```

出力結果

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -q -t set,get
SET: 45766.59 requests per second
GET: 42789.90 requests per second
```

#### パターン4

CSVモードで実行

```
redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -t set,get --csv
```

出力結果

```
[ec2-user@bastin ~]$ redis-benchmark -h redistest.xxxxx.0001.apne1.cache.amazonaws.com -p 6379 -c 100 -n 100000 -t set,get --csv
"SET","41562.76"
"GET","38491.14"
```

#### その他

`redis-cli` に`--latency`を付与することでPINGを使用したレイテンシを計測することが出来る。ひたすらサンプルを取り続けるのでCtrl+Cでストップする

```
[ec2-user@bastin ~]$ redis-cli -h redistest.xxxx.0001.apne1.cache.amazonaws.com -p 6379 --latency
min: 0, max: 18, avg: 0.40 (4591 samples)
```

