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

### 前提

- Homebrewがインストールされていること

### インストール

```sh
(base) jimazato@XXXXXXXX ~ % brew search postgresql

==> Formulae
postgresql@10    postgresql@11    postgresql@12    postgresql@13    postgresql@14    postgresql@15    postgresql@9.4   postgresql@9.5   qt-postgresql    postgrest

==> Casks
navicat-for-postgresql

If you meant "postgresql" specifically:
postgresql breaks existing databases on upgrade without human intervention.

See a more specific version to install with:
  brew formulae | grep postgresql@
```

```sh
(base) jimazato@XXXXXXXX ~ % brew install postgresql
Running `brew update --auto-update`...
==> Auto-updated Homebrew!
Updated 4 taps (hashicorp/tap, homebrew/core, homebrew/cask and homebrew/services).
省略
```

### バージョン確認

```sh
(base) jimazato@XXXXXXXX ~ % psql --version
psql (PostgreSQL) 14.7 (Homebrew)
```

Linuxの場合、pgbenchは`postgresql-contrib`のインストールが必要だったが、Homebrewの場合は一緒にインストールされるらしい。

```
(base) jimazato@XXXXXXXX ~ % pgbench --version
pgbench (PostgreSQL) 14.7 (Homebrew)
```

AWSのRDSに接続してpgbench（データ生成のみ）を実施してみる

```sh
(base) jimazato@XXXXXXXX ~ % psql -h xxxx-rds-pgsql.xxxxxx.us-west-1.rds.amazonaws.com -U postgres -d postgres
Password for user postgres:
psql (14.7 (Homebrew), server 13.7)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=> select version();
                                                 version
---------------------------------------------------------------------------------------------------------
 PostgreSQL 13.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 7.3.1 20180712 (Red Hat 7.3.1-12), 64-bit
(1 row)
```

```sh
(base) jimazato@XXXXXXXX ~ % pgbench -r -c 10 -j 10 -t 10 -U postgres -h xxxx-rds-pgsql.xxxxxx.us-west-1.rds.amazonaws.com pgbench
pgbench (14.7 (Homebrew), server 13.7)
starting vacuum...end.
transaction type: <builtin: TPC-B (sort of)>
scaling factor: 10
query mode: simple
number of clients: 10
number of threads: 10
number of transactions per client: 10
number of transactions actually processed: 100/100
latency average = 1095.176 ms
initial connection time = 858.293 ms
tps = 9.130952 (without initial connection time)
statement latencies in milliseconds:
         0.005  \set aid random(1, 100000 * :scale)
         0.002  \set bid random(1, 1 * :scale)
         0.001  \set tid random(1, 10 * :scale)
         0.001  \set delta random(-5000, 5000)
       134.627  BEGIN;
       136.454  UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
       135.479  SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
       145.459  UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
       193.648  UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
       134.604  INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
       135.139  END;

```

