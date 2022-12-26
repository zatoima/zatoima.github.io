---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "pgbenchで任意のSQLを使って負荷掛け"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-pgbench-performance-sql-test
date: 2021-06-16
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



### 実行するSQL

```
cat << EOF > query.sql
<SQL文をここに書く>
EOF
```

### pgbenchを使った並列実行

この場合はクライアント数が5、スレッド数5で100回SQLを実行するパターン。

```
pgbench -r -c 5 -j 5 -n -t 100 -f query.sql -U awsuser -h aurora-postgresql.xxxxxx.ap-northeast-1.redshift.amazonaws.com -d postgres -p 5439
```

### 各オプションの説明

> pgbench https://www.postgresql.jp/document/12/html/pgbench.html

```
-j threads --jobs=threads
pgbench内のワーカスレッド数

-r --report-latencies
ベンチマーク完了後の各コマンドにおけるステートメント毎の平均レイテンシ(クライアントから見た実行時間)を報告

-c clients --client=clients
模擬するクライアント数、つまり、同時に実行されるデータベースセッション数

-f filename --file=filename
実行するSQLを指定する

-t transactions --transactions=transactions
各クライアントが実行するトランザクション数。 デフォルトは10。
```

