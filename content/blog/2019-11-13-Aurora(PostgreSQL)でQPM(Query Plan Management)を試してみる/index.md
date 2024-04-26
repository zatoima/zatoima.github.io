---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora(PostgreSQL)でQPM(Query Plan Management)を試してみる"
subtitle: ""
summary: " "
tags: ["AWS", "RDS", "Aurora", "PostgreSQL"]
categories: ["AWS", "RDS", "Aurora", "PostgreSQL"]
url: aurora-postgresql-query-plan-management.html
date: 2019-11-13
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


### QPM(Query Plan Management)とは？

***

SQLに実行計画を記録して、その実行計画を固定化、もしくは別環境に実行計画を移行して固定化出来る機能。Oracleで言うところのSPM（SQL Plan Management）になる。Aurora(PostgreSQL)でもこの機能が使えるので実際にやってみる。

##### Query Plan Managementの制御方法

```sql
rds.enable_plan_management = { 0,1} #パラメータグループで設定

apg_plan_mgmt.capture_plan_baselines = { manual, automatic, off }
# automatic : 自動計画取り込み。1回以上実行されたSQLを取り込む
# manual    : 個々のSQLを手動で実行計画を取り込む
# off       : Query Planの取得を無効化

apg_plan_mgmt.use_plan_baselines = { true, false }
# true  : 取得したQuery Planを使用して実行計画を固定化する
# false : 取得したQuery Planを使用しない。
```

### 環境、及びシナリオ説明

***

開発環境から本番環境への実行計画の移行を想定。

- 本番環境DB名：prod
- 開発環境DB名：dev

開発環境で実行したfull scan(seq scan)となる実行計画を本番環境に移行して非効率な実行計画を再現する。

### パラメータグループ変更（dev/prod環境）

***

クラスターパラメータグループの `rds.enable_plan_management` を`1`に設定

### 拡張機能の有効化（dev/prod環境）

***

create extensionコマンドでapg_plan_mgmtをインストールする

##### コマンド

```sql
\dx
create extension apg_plan_mgmt;
\dx
```

##### 実行結果

```sql
#実行結果
dev=> \dx
                 List of installed extensions
  Name   | Version |   Schema   |         Description          
---------+---------+------------+------------------------------
 plpgsql | 1.0     | pg_catalog | PL/pgSQL procedural language
(1 row)
dev=> 
dev=> create extension apg_plan_mgmt;    #拡張機能を有効化
CREATE EXTENSION
dev=> \dx
                                        List of installed extensions
     Name      | Version |    Schema     |                            Description           
                 
---------------+---------+---------------+--------------------------------------------------
-----------------
 apg_plan_mgmt | 1.0.1   | apg_plan_mgmt | Amazon Aurora with PostgreSQL compatibility Query #★←apg_plan_mgmtが増えている
 Plan Management
 plpgsql       | 1.0     | pg_catalog    | PL/pgSQL procedural language
(2 rows)
dev=> 
dev=> 
```



### dba_plans表の事前確認（dev/prod環境）

***

apg_plan_mgmt.dba_plans表には当然何も格納されていない。

##### コマンド

```sql
SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
FROM   apg_plan_mgmt.dba_plans
ORDER BY sql_text, plan_created;
```

##### 実行結果

```sql
dev=> SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
dev-> FROM   apg_plan_mgmt.dba_plans
dev-> ORDER BY sql_text, plan_created;
 sql_hash | plan_hash | status | enabled | sql_text 
----------+-----------+--------+---------+----------
(0 rows)
```



### テスト用のテーブル作成（dev/prod環境）

***

テスト用のテーブルを作成する

##### コマンド

```sql
CREATE TABLE t1 AS
SELECT num                         a -- 生成値
      ,'1'                         b -- 定数
      ,to_char(num,'FM00000')      c -- 生成値を利用（IDなどの文字列）
      ,current_timestamp      d 
FROM   generate_series(1,10000) num
;

ALTER TABLE t1 ADD PRIMARY KEY(a);

\d t1
```

##### 実行結果

```sql
dev=> CREATE TABLE t1 AS
dev-> SELECT num                         a -- 生成値
dev->       ,'1'                         b -- 定数
dev->       ,to_char(num,'FM00000')      c -- 生成値を利用（IDなどの文字列）
dev->       ,current_timestamp      d 
dev-> FROM   generate_series(1,10000) num
dev-> ;
SELECT 10000
dev=> 
dev=> ALTER TABLE t1 ADD PRIMARY KEY(a);
ALTER TABLE
dev=> 
dev=> \d t1
                         Table "public.t1"
 Column |           Type           | Collation | Nullable | Default 
--------+--------------------------+-----------+----------+---------
 a      | integer                  |           | not null | 
 b      | text                     |           |          | 
 c      | text                     |           |          | 
 d      | timestamp with time zone |           |          | 
Indexes:
    "t1_pkey" PRIMARY KEY, btree (a)
dev=> 
```



###  SQLの実行、及び実行capture（dev環境）

***

実行計画が**<u>full scan(seq scan)</u>**になるSQLと、**<u>Index Scan</u>**になるSQLを実行。この時、**<u>full scan(seq scan)</u>**になるSQLの実行計画だけを手動で取り込む。

この例では「Plan Hash: -52705300」が`apg_plan_mgmt.dba_plans`表に取り込まれているのがわかる。

##### コマンド

```sql
SET apg_plan_mgmt.capture_plan_baselines = manual; #実行計画の手動取り込みを有効化

explain (hashes true) select count(*) from t1 where a > 1;

SET apg_plan_mgmt.capture_plan_baselines = off;  #実行計画の手動取り込みを停止

explain (hashes true) select count(*) from t1 where a > 9999;

SET apg_plan_mgmt.capture_plan_baselines = off;
 
SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
FROM   apg_plan_mgmt.dba_plans
ORDER BY sql_text, plan_created;
```

##### 実行結果

```sql
#実行ログ
dev=> SET apg_plan_mgmt.capture_plan_baselines = manual;
SET
dev=> 
dev=> explain (hashes true) select count(*) from t1 where a > 1;
                          QUERY PLAN                          
--------------------------------------------------------------
 Aggregate  (cost=214.00..214.01 rows=1 width=8)
   ->  Seq Scan on t1  (cost=0.00..189.00 rows=10000 width=0)
         Filter: (a > 1)
 SQL Hash: -1895827505, Plan Hash: -52705300
(4 rows)
dev=> 
dev=> 
dev=> SET apg_plan_mgmt.capture_plan_baselines = off;
SET
dev=> 
dev=> 
dev=> 
dev=> explain (hashes true) select count(*) from t1 where a > 9999;
                                 QUERY PLAN                                  
-----------------------------------------------------------------------------
 Aggregate  (cost=8.30..8.31 rows=1 width=8)
   ->  Index Only Scan using t1_pkey on t1  (cost=0.29..8.30 rows=1 width=0)
         Index Cond: (a > 9999)
 Plan Hash: 1222455040
(4 rows)
dev=> 
dev=> SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
dev-> FROM   apg_plan_mgmt.dba_plans
dev-> ORDER BY sql_text, plan_created;
  sql_hash   | plan_hash |  status  | enabled |               sql_text               
-------------+-----------+----------+---------+--------------------------------------
 -1895827505 | -52705300 | Approved | t       | select count(*) from t1 where a > 1; #★←実行計画が取り込まれている
(1 row)
dev=> 
dev=> 
dev=> 
```



### エクスポート用のテーブル作成(dev)

***

```sql
CREATE TABLE plans_copy AS SELECT * FROM apg_plan_mgmt.plans;
```



### pg_dumpを使用してエクスポートする(dev)

***

```sql
export PGPASSWORD=xxxxxx
pg_dump -U postgres -h aurora-postgres-cluster-dev.cluster-xxxxxxxx.ap-northeast-1.rds.amazonaws.com -t plans_copy -Ft dev > plans_copy.tar

#必要に応じて不要になった中間テーブルを削除する
--DROP TABLE plans_copy;
```



### 別DBでインポート(prod)

***

```sql
pg_restore -U postgres -h aurora-postgres-cluster-prod.cluster-xxxxxxxxx.ap-northeast-1.rds.amazonaws.com -t plans_copy -Ft plans_copy.tar -d prod
```

### インポート確認、及びマージ(prod)

***

このあたりのマニュアルを参考に実行計画のマージを行います。

> 実行計画の維持 - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Optimize.Maintenance.html#AuroraPostgreSQL.Optimize.Maintenance.ExportingImporting
>
> > 計画のエクスポートおよびインポート

##### コマンド

```sql
INSERT INTO apg_plan_mgmt.plans SELECT * FROM plans_copy
 ON CONFLICT ON CONSTRAINT plans_pkey
 DO UPDATE SET
 status = EXCLUDED.status,
 enabled = EXCLUDED.enabled,
 last_used = CASE WHEN EXCLUDED.last_used > plans.last_used 
 THEN EXCLUDED.last_used ELSE plans.last_used END, 
 estimated_startup_cost = EXCLUDED.estimated_startup_cost,
 estimated_total_cost = EXCLUDED.estimated_total_cost,
 planning_time_ms = EXCLUDED.planning_time_ms,
 execution_time_ms = EXCLUDED.execution_time_ms,
-- estimated_rows = EXCLUDED.estimated_rows,
-- actual_rows = EXCLUDED.actual_rows,
 total_time_benefit_ms = EXCLUDED.total_time_benefit_ms, 
 execution_time_benefit_ms = EXCLUDED.execution_time_benefit_ms;
 
#管理計画を共有メモリにリロードする
SELECT apg_plan_mgmt.reload(); -- refresh shared memory
DROP TABLE plans_copy;

-- 確認
SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
FROM   apg_plan_mgmt.dba_plans
ORDER BY sql_text, plan_created;
```

この時、estimated_rows、actual_rowsをコメントアウトする必要あり。実際にはない行らしい。マニュアルの誤記？

```sql
ERROR:  column excluded.actual_rows does not exist
LINE 13:  actual_rows = EXCLUDED.actual_rows,
```

##### 実行結果

```sql
prod=> INSERT INTO apg_plan_mgmt.plans SELECT * FROM plans_copy
prod->  ON CONFLICT ON CONSTRAINT plans_pkey
prod->  DO UPDATE SET
prod->  status = EXCLUDED.status,
prod->  enabled = EXCLUDED.enabled,
prod->  last_used = CASE WHEN EXCLUDED.last_used > plans.last_used 
prod->  THEN EXCLUDED.last_used ELSE plans.last_used END, 
prod->  estimated_startup_cost = EXCLUDED.estimated_startup_cost,
prod->  estimated_total_cost = EXCLUDED.estimated_total_cost,
prod->  planning_time_ms = EXCLUDED.planning_time_ms,
prod->  execution_time_ms = EXCLUDED.execution_time_ms,
prod-> -- estimated_rows = EXCLUDED.estimated_rows,
prod-> -- actual_rows = EXCLUDED.actual_rows,
prod->  total_time_benefit_ms = EXCLUDED.total_time_benefit_ms, 
prod->  execution_time_benefit_ms = EXCLUDED.execution_time_benefit_ms;
INSERT 0 2
prod=> 
prod=> 
prod=> SELECT apg_plan_mgmt.reload();
 reload 
--------
      0
(1 row)
prod=> 
prod=> 
prod=> DROP TABLE plans_copy;
DROP TABLE
prod=> 
prod=> 
prod=> 
prod=> 
prod=> SELECT sql_hash, plan_hash, status, enabled, sql_text::varchar(100)
prod-> FROM   apg_plan_mgmt.dba_plans
prod-> ORDER BY sql_text, plan_created;
  sql_hash   | plan_hash  |   status   | enabled |                sql_text                 
-------------+------------+------------+---------+-----------------------------------------
 -1895827505 |  -52705300 | Approved   | t       | select count(*) from t1 where a > 1;
(2 rows)
prod=> 
prod=> 
prod=> 

```

### SQLの実行

今回はindex scanとなるところをfullscanを選択させているケース。

##### コマンド

```sql
-- SQLのテスト
SET apg_plan_mgmt.use_plan_baselines = true;
explain (hashes true) select count(*) from t1 where a > 9999;
SET apg_plan_mgmt.use_plan_baselines = false;
```

##### 実行結果

```sql
prod=> SET apg_plan_mgmt.use_plan_baselines = true;
prod=> 
prod=> explain (hashes true) select count(*) from t1 where a > 9999;
                                   QUERY PLAN                                    
---------------------------------------------------------------------------------
 Aggregate  (cost=189.00..189.01 rows=1 width=8)
   ->  Seq Scan on t1  (cost=0.00..189.00 rows=1 width=0)
         Filter: (a > 9999)
 Note: An Approved plan was used instead of the minimum cost plan.
 SQL Hash: -1895827505, Plan Hash: -52705300, Minimum Cost Plan Hash: 1222455040
(5 rows)
prod=> SET apg_plan_mgmt.use_plan_baselines = false;
SET

```

今回の例ではwhere文でデータ取得件数を絞っているのでindex scanが実行プランとしては正しい。ただ、QPMで`select count(*) from t1 where a > 1;`の実行計画が取り込まれており、この実行計画はFullscan(SeqScan)となる。敢えて非効率な実行計画を選択させたパターン。

実際にログ上にも`Note: An Approved plan was used instead of the minimum cost plan.`と記載がありもっとコストのよい実行計画があるぞーと言っている。

> prod=> explain (hashes true) select count(*) from t1 where a > 9999;
>
> QUERY PLAN                                    
>
> Aggregate  (cost=189.00..189.01 rows=1 width=8)
> ->  Seq Scan on t1  (cost=0.00..189.00 rows=1 width=0)
>    Filter: (a > 9999)
> Note: An Approved plan was used instead of the minimum cost plan.
> SQL Hash: -1895827505, Plan Hash: -52705300, Minimum Cost Plan Hash: 1222455040

### 参考

***

> 実行計画の維持 - Amazon Aurora https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Optimize.Maintenance.html
>
> Amazon Aurora PostgreSQL でのクエリ計画管理のユースケース | Amazon Web Services ブログ https://aws.amazon.com/jp/blogs/news/use-cases-for-query-plan-management-in-amazon-aurora-postgresql/
