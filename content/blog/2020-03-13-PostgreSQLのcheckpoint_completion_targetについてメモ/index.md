---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのcheckpoint_completion_targetについてメモ"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-checkpoint_completion_target.html
date: 2020-03-13
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



PostgreSQLの`checkpoint_completion_target`についてメモ。

> 19.5. ログ先行書き込み（WAL） https://www.postgresql.jp/document/10/html/runtime-config-wal.html#GUC-CHECKPOINT-TIMEOUT
>
> checkpoint_completion_target
>
> チェックポイントの完了目標をチェックポイント間の総時間の割合として指定します。 デフォルトは0.5です。 このパラメータはpostgresql.confファイル、または、サーバのコマンドラインでのみ設定可能です。

```sh
postgres=# show checkpoint_completion_target;
 checkpoint_completion_target 
------------------------------
 0.5
(1 row)
```

一方、`checkpoint_timeout`というパラメータがありデフォルトでは5分が設定されている。自動的WALチェックポイント間の最大間隔を秒単位で指定できるパラメータである。

このcheckpoint_completion_targetはcheckpoint_timeoutで設定された"割合"の時間を使ってcheckpointをしていくという動きをして負荷を分散する。あくまで目安程度となるらしい。

```sh
postgres=# show checkpoint_timeout;
 checkpoint_timeout 
--------------------
 5min
(1 row)
```

デフォルトの通り、`checkpoint_timeout`が5分で`checkpoint_completion_target`が0.5の場合は約2.5分（あくまで目安）掛けてダーティーページをディスクに書き込んでいくという処理となる。

つまり、checkpoint_completion_targetを低くした場合はcheckpointでダーティーページをディクスに書き込む際の負荷が高くなることが予想され、checkpoint_completion_targetを高くした場合(=時間を掛ける)は、クラッシュリカバリ時に処理をするWALファイルが増える。

更新が多くcheckpointの負荷が気になる場合はcheckpoint_completion_targetをデフォルトの0.5から「0.6~0.9」に引き上げることを考慮。