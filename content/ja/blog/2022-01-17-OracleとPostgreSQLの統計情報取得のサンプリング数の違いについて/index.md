---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "OracleとPostgreSQLの統計情報取得のサンプリング数の違いについて"
subtitle: ""
summary: " "
tags: ["Oracle","PostgreSQL"]
categories: ["Oracle","PostgreSQL"]
url: oracle-postgresql-dbms-stats-analyze-sampling
date: 2022-01-17
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

統計情報取得というのはDBエンジンに関係なく、オプティマイザ（プランナ）の適切な実行計画生成のためには必要不可欠な仕組みであるが、サンプリング数と精度はトレードオフの関係にある。サンプリング数が多いと統計情報取得に掛かる時間が長くなってしまうし、データの母数に対してサンプルが少ないと統計情報の精度が落ち、結果として最適な実行計画が生成されないかもしれない。

OracleとPostgreSQLの統計情報取得を比較してみたところ圧倒的にPostgreSQLの統計情報の取得時間が短かったので、その理由について簡単にメモしておく。結論として両者デフォルトの場合、PostgreSQLの方はある程度サンプリング数は固定化されているのに対してOracleの場合はAUTO_SAMPLE_SIZEでテーブルサイズによってサンプリング数が増減する。この違いによって取得時間も大きく変わってきているようだ。（あくまで原因の一つ。）

### Oracleの場合

DBMS_STATSパッケージのESTIMATE_PERCENTパラメータで指定する。デフォルトはAUTO_SAMPLE_SIZEで自動でOracle側が最適なサンプリング数を算出してくれる。大きなテーブルはサンプリング数が多くなり、小さいテーブルはサンプリング数が小さくなる。"100%のサンプリングの精度"、"10%サンプリングの所要時間"を両立とあるので素晴らしい機能だと思う。統計的にもそれだけ取れば精度として十分なんだろう。

- PL/SQLパッケージおよびタイプ・リファレンス

> https://docs.oracle.com/cd/F19136_01/arpls/DBMS_STATS.html#GUID-7D7442B5-B060-40E9-AA18-2085E527C3B1
>
> サンプリングする行のパーセントが決定されます。
>
> 有効範囲は0.000001から100です。定数DBMS_STATS.AUTO_SAMPLE_SIZEを使用すると、最適な統計を生成するための適切なサンプル・サイズをデータベースで決定できるようになります。これはデフォルトです。

- Oracle Database 19cにおけるオプティマイザ統計収集のベスト・プラクティス

> https://www.oracle.com/technetwork/jp/database/bi-datawarehousing/twp-bp-for-stats-gather-19c-5324205-ja.pdf

> ESTIMATE_PERCENTパラメータは、統計を計算するために使用される行の割合を決定します。もっとも正確な統計は、表のすべての行が処理される（つまりサンプルが100 %の）ときに収集され、通常は算出された統計と呼ばれます。Oracle Database 11gでは、確定的な統計を実現するハッシュ・ベースの新しいサンプリング・アルゴリズムが導入されました。この新たなアプローチでは、最大 で10 %のサンプルのコストで、100 %のサンプルに近い正確性を実現します。

### PostgreSQLの場合

サンプリング量はデフォルト 30,000 レコード（ MAX(列の STATISTICS 値)× 300 レコード）

STATISTICS 値は下記で決まる。

- default_statistics_targetパラメーター（デフォルト:100)
- テーブルの各カラムに対して実施するALTER TABLEコマンドのSET STATISTICS文
- 式として定義されたインデックス列に対するALTER INDEXコマンドのSET STATISTICS文

大きめのテーブルに対してanalyzeコマンドにオプションverboseを付与して実行してみる。`30000 rows in sample`や`scanned 30000 of 163935 pages`とある。

```sql
postgres=> show default_statistics_target;
 default_statistics_target 
---------------------------
 100
(1 row)

postgres=> select count(*) from pgbench_accounts;
  count   
----------
 10000000
(1 row)

postgres=> 
postgres=> analyze verbose pgbench_accounts;
INFO:  analyzing "public.pgbench_accounts"
INFO:  "pgbench_accounts": scanned 30000 of 163935 pages, containing 1830000 live rows and 0 dead rows; 30000 rows in sample, 10000035 estimated total rows
ANALYZE
postgres=> 
postgres=> select count(*) from pgbench_branches;
 count 
-------
   100
(1 row)

postgres=> analyze verbose pgbench_branches;
INFO:  analyzing "public.pgbench_branches"
INFO:  "pgbench_branches": scanned 1 of 1 pages, containing 100 live rows and 0 dead rows; 100 rows in sample, 100 estimated total rows
ANALYZE
```

数億行等で列値にバリエーションが多い場合はこのサンプル数では適切な実行計画が導き出されない可能性がもちろんある。こういう場合はdefault_statistics_targetパラメーター等（特定列のみサンプリング数を多くすることも出来るので詳細にチューニングしたい場合はそちらの方が良いかもしれない）を調整してサンプリング数を多くする必要がある。当然サンプリング数を多くすると時間が掛かってしまうのでトレードオフに注意すること。

マニュアルの該当箇所はこちら。

> ANALYZE https://www.postgresql.jp/document/13/html/sql-analyze.html
>
> 巨大なテーブルでは、`ANALYZE`は、全ての行を検査するのではなく、テーブルの中からランダムにサンプルを取り出して使用します。 これによって、非常に巨大なテーブルであっても短時間で解析することが可能です。 しかし、このようにして得られた統計情報はおおよそのものでしかなく、テーブルの内容に変更がなくても`ANALYZE`を実行する度に変化することに注意してください。 これにより、[EXPLAIN](https://www.postgresql.jp/document/13/html/sql-explain.html)が表示する、プランナの推定コストも多少変化する可能性があります。 稀に、このような不確定要素のせいで、プランナが`ANALYZE`を実行した後に異なる問い合わせ計画を選択してしまうことがあります。 これを防止するには、以下に示すように`ANALYZE`で収集される統計情報の量を増やしてください。
>
> 設定パラメータ変数[default_statistics_target](https://www.postgresql.jp/document/13/html/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET)を調整するか、もしくは`ALTER TABLE ... ALTER COLUMN ... SET STATISTICS`([ALTER TABLE](https://www.postgresql.jp/document/13/html/sql-altertable.html)参照)を使用して列単位の統計目標を列毎に設定することで、解析の範囲を制御することができます。 目標値として設定するのは、典型的な値のリストにおけるエントリ数の最大値と度数分布のビンの最大数です。 デフォルトの目標値は100です。 しかし、この値は、プランナの推定精度と`ANALYZE`の処理時間、`pg_statistic`の占める容量とのトレードオフによって大きくも小さくも調整されることがあります。 目標値を0に設定すると、その列に関する統計情報の収集は無効になります。 決して`WHERE`句、`GROUP BY`句、`ORDER BY`句に使用されない列に対しては、このような設定が有用です。 プランナにとってそのような列の統計情報は不要だからです。

### 参考

- Best Practices for Gathering Optimizer Statistics with Oracle Database 19c https://www.oracle.com/technetwork/jp/database/bi-datawarehousing/twp-bp-for-stats-gather-19c-5324205-ja.pdf?utm_source=pocket_mylist
- Oracle Statistics Concepts https://www.oracle.com/technetwork/jp/database/bi-datawarehousing/twp-stats-concepts-19c-5324209-ja.pdf?utm_source=pocket_mylist
- 書籍：内部構造から学ぶPostgreSQL 設計・運用計画の鉄則
