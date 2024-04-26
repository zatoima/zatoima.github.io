---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのauto_explainで特定クエリの実行計画を出力する"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-about-auto_explain.html
date: 2020-03-03
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

contribモジュールにauto_explain という特定の条件にマッチしたクエリの実行計画をログに出力する拡張機能がありますので使ってみます。スロークエリの監視と改善を行う場合に有効な拡張機能だと思います。	

auto_explainはcontribモジュールの一つなので必要に応じてcontribのインストールも実施が必要です。

```sh
sudo yum -y install postgresql10-devel postgresql10-contrib
```

### バージョンについて

```sh
postgres=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

### pg_buffercacheの設定

`postgresql.conf`に下記のパラメータを設定します。`auto_explain.log_min_duration`にて指定した秒数以上のクエリの実行計画がサーバログに出力されます。ここの設定値は要件に応じて変更する必要があります。ここでは1秒以上としています。

```sh
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = '1'
auto_explain.log_analyze=on
auto_explain.log_buffers=on
auto_explain.log_verbose=on
```

#### 関連パラメータ

| パラメータ                    | 説明                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| auto_explain.log_min_duration | 実行計画がログに記録されるようになる、ミリ秒単位の最小の文実行時間 |
| auto_explain.log_analyze      | EXPLAIN出力ではなく、EXPLAIN ANALYZE出力を行う。極端に性能上のマイナスの影響が起こり得る。 |
| auto_explain.log_buffers      | 実行計画のログを取得するときに、バッファ使用統計を出力するかどうかを制御。EXPLAINのBUFFERSオプションと同じ |
| auto_explain.log_timing       | 実行計画のログが取得されたときに、ノード毎の時間的調整情報を出力するかどうかを制 |
| auto_explain.log_triggers     | 実行計画のログを記録するときに、トリガ実行の統計を含める     |
| auto_explain.log_verbose      | 冗長な詳細が出力されるかどうかを制御します。 EXPLAINのVERBOSEオプションと同じ。 |

## 使用方法

クエリを実行します。10000件入っているテーブルを直積結合して件数をカウントしています。auto_explain.log_min_duration以上掛かるSQLである必要があります。

```
select count(*) from t1,t2;
```

2パターン実行しました。

### パターン1.)

- shared_preload_libraries = 'auto_explain'
- auto_explain.log_min_duration = '1'

```sh
2020-03-02 09:22:53.837 UTC [27039] LOG:  duration: 6715.237 ms  plan:
	Query Text: select count(*) from t1,t2;
	Aggregate  (cost=1500353.00..1500353.01 rows=1 width=8)
	  ->  Nested Loop  (cost=0.00..1250353.00 rows=100000000 width=0)
	        ->  Seq Scan on t1  (cost=0.00..164.00 rows=10000 width=0)
	        ->  Materialize  (cost=0.00..214.00 rows=10000 width=0)
	              ->  Seq Scan on t2  (cost=0.00..164.00 rows=10000 width=0)
```

### パターン2.)

- shared_preload_libraries = 'auto_explain'
- auto_explain.log_min_duration = '1'
- auto_explain.log_analyze=on
- auto_explain.log_buffers=on
- auto_explain.log_verbose=on

```sh
2020-03-02 09:36:56.407 UTC [27217] LOG:  duration: 399369.613 ms  plan:
	Query Text: select count(*) from t1,t2;
	Aggregate  (cost=1500353.00..1500353.01 rows=1 width=8) (actual time=399369.587..399369.588 rows=1 loops=1)
	  Output: count(*)
	  Buffers: shared hit=128
	  ->  Nested Loop  (cost=0.00..1250353.00 rows=100000000 width=0) (actual time=0.020..297204.066 rows=100000000 loops=1)
	        Buffers: shared hit=128
	        ->  Seq Scan on public.t1  (cost=0.00..164.00 rows=10000 width=0) (actual time=0.007..18.548 rows=10000 loops=1)
	              Output: t1.a, t1.b, t1.c, t1.d
	              Buffers: shared hit=64
	        ->  Materialize  (cost=0.00..214.00 rows=10000 width=0) (actual time=0.002..10.057 rows=10000 loops=10000)
	              Buffers: shared hit=64
	              ->  Seq Scan on public.t2  (cost=0.00..164.00 rows=10000 width=0) (actual time=0.005..11.372 rows=10000 loops=1)
	                    Buffers: shared hit=64
```

パターン2の方が多くの情報が出力されます。ただ、auto_explain.log_analyze はマニュアルに、`このパラメータが有効の場合、計画ノードごとの時間的調整は事実上ログされるまで如何に時間が掛かろうと、全ての実行文に対して引き起こります。 極端に性能上のマイナスの影響が起こり得ます。 `と記載があります。今回は「6715.237 ms」と「399369.613 ms」という実行時間の差異が発生しました。ログ取得の影響で本番環境のクエリに影響を与えるのを本末転倒だと思うので`auto_explain.log_analyze`の設定にはご注意ください。

### 参考

> F.4. auto_explain https://www.postgresql.jp/document/10/html/auto-explain.html