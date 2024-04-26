---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでpg_dumpした場合の圧縮率"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: aws-postgresql-pg_dump_zip.html
date: 2020-11-26
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

表題の件を検証。カスタムファイル（圧縮）で出力されるよう`-Fc`オプションを付与。こんな感じになりました。int、string主体だと圧縮率は高め。

| No   | 検証パターン | DB名     | DBサイズ（GB) | データの中身                                 | ダンプファイルの容量（GB） | 圧縮率 |
| ---- | ------------ | -------- | ------------- | -------------------------------------------- | -------------------------- | ------ |
| 1    | pg_dump      | postgres | 729GB         | 青空文庫のテキストデータ                     | 66                         | 9%     |
| 2    |              | tpch     | 45GB          | HammerDBのtpc-hのデータ                      | 9.9                        | 22%    |
| 3    |              | tpcc     | 118GB         | HammerDBのtpc-cのデータ                      | 34                         | 29%    |
| 4    |              | blob     | 98GB          | byteaにバイナリ（25MBファイル×4000ファイル） | 108                        | 110%   |



