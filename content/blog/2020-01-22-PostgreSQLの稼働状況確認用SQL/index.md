---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLの稼働状況確認用SQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-monitoring-sql.html
date: 2020-01-22
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

DB稼働状況の監視と性能解析用のツールは数あれど、やはりSQLを使った状況確認の機会は多いので、PostgreSQLの稼働状況確認時に使用するSQLをまとめた。必要に応じてまた都度追加していきたい。

 PostgreSQL 10.11のバージョンでSQLの確認を実施済。バージョンが上がるにつれて便利なシステムカタログが増えているので最新バージョンを触ってみたい。

#### バージョン

```sql
postgres=# select version();
                                                 version                                                  
----------------------------------------------------------------------------------------------------------
 PostgreSQL 10.11 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-39), 64-bit
(1 row)
```

#### commit数/rollback数の確認

```sql
SELECT datname, xact_commit, xact_rollback FROM pg_stat_database;
```

#### DB単位のキャッシュヒット率の確認

```sql
SELECT datname, round(blks_hit*100/(blks_hit+blks_read), 2) AS cache_hit_ratio
FROM pg_stat_database WHERE blks_read > 0;
```

#### TBL単位のキャッシュヒット率の確認

```sql
SELECT relname, round(heap_blks_hit*100/(heap_blks_hit+heap_blks_read), 2)
AS cache_hit_ratio FROM pg_statio_user_tables
WHERE heap_blks_read > 0 ORDER BY cache_hit_ratio;
```

#### INDEX単位のキャッシュヒット率の確認

```sql
SELECT relname, indexrelname, round(idx_blks_hit*100/(idx_blks_hit+idx_blks_read), 2)
AS cache_hit_ratio FROM pg_statio_user_indexes
WHERE idx_blks_read > 0 ORDER BY cache_hit_ratio;
```

#### 表スキャンあたりの読み取り行数の確認

```sql
SELECT relname, seq_scan, seq_tup_read, seq_tup_read/seq_scan AS tup_per_read FROM pg_stat_user_tables
WHERE seq_scan > 0 ORDER BY tup_per_read DESC;
```

#### HOT更新の比率の確認

```sql
SELECT relname, n_tup_upd, n_tup_hot_upd, round(n_tup_hot_upd*100/n_tup_upd, 2) AS hot_upd_ratio
FROM pg_stat_user_tables WHERE n_tup_upd > 0 ORDER BY hot_upd_ratio;
```

#### 稼働しているプロセスの確認

```sql
SELECT pid, datname, usename, state, backend_type FROM pg_stat_activity;
```

#### 実行されているSQLの確認

```sql
SELECT pid, query_start, substr(query, 0, 50) FROM pg_stat_activity WHERE state='active' ORDER BY query_start;
```

#### WALアーカイブの確認

```sql
select * from pg_stat_archiver;
```

#### デットロック回数の確認

```sql
SELECT datname,deadlocks FROM pg_stat_database where datname = 'pgbench';
```

#### デットロック状況の確認

```sql
SELECT l.pid, l.granted, d.datname, l.locktype, relation, relation::regclass, transactionid, l.mode 
FROM pg_locks l LEFT JOIN pg_database d ON  l.database = d.oid 
WHERE l.pid != pg_backend_pid() 
ORDER BY l.pid ;
```

#### 長時間かかっている処理を確認

```sql
SELECT pid, state, wait_event, wait_event_type, (NOW() - xact_start)::INTERVAL(3) AS tx_duration, (NOW() - query_start)::INTERVAL(3) AS sql_duration, query 
FROM pg_stat_activity 
WHERE pid <> pg_backend_pid() ;
```

#### チェックポイント

```sql
SELECT
    checkpoints_timed,
    checkpoints_req,
    checkpoint_write_time,
    checkpoint_sync_time,
    buffers_checkpoint
FROM
    pg_stat_bgwriter;
```

#### VACUUM

last_vacuum, last_autovacuum でVACUUM, 自動VACUUMがいつ実行されたか、n_dead_tupで不要なタプルが何行削除されたか

```sql
SELECT relname,n_live_tup,n_dead_tup,last_autovacuum,autovacuum_count
FROM pg_stat_user_tables;
```

#### ANALYZE

```sql
SELECT relname,last_analyze,last_autoanalyze,analyze_count,autoanalyze_count
FROM pg_stat_user_tables;
```

#### 一時ファイルの書き出し

```sql
select datname,temp_files,temp_bytes from pg_stat_database;
```

#### トータルの実行時間が長いSQL/実行回数が多いSQLを確認。pg_stat_statementsの事前設定が必要。

```sql
SELECT datname, SUBSTRING(query, 1, 40) AS query, calls, TRUNC( total_time::NUMERIC, 3 ) AS total_time 
FROM pg_stat_statements LEFT OUTER JOIN pg_database ON  pg_stat_statements.dbid = pg_database.oid 
WHERE datname = 'pgbench' 
ORDER BY total_time DESC 
LIMIT 5 ;
```

#### データベースのサイズを確認

```sql
select pg_size_pretty(pg_database_size('pgbench'));
```

#### テーブルのサイズを確認
```sql
select pg_relation_size('pgbench');
```

#### テーブルとインデックスのサイズ合計を確認
```sql
select pg_total_relation_size('pgbench');
```

#### 各テーブルごとのサイズ/タプル数をチェックする
```sql
SELECT pgn.nspname, relname, pg_size_pretty(relpages::bigint * 8 * 1024) AS size, CASE WHEN relkind = 
't' THEN (SELECT pgd.relname FROM pg_class pgd WHERE pgd.reltoastrelid = pg.oid) WHEN nspname = 
'pg_toast' AND relkind = 'i' THEN (SELECT pgt.relname FROM pg_class pgt WHERE SUBSTRING(pgt.relname 
FROM 10) = REPLACE(SUBSTRING(pg.relname FROM 10), '_index', '')) ELSE (SELECT pgc.relname FROM 
pg_class pgc WHERE pg.reltoastrelid = pgc.oid) END::varchar AS refrelname, CASE WHEN nspname = 
'pg_toast' AND relkind = 'i' THEN (SELECT pgts.relname FROM pg_class pgts WHERE pgts.reltoastrelid = 
(SELECT pgt.oid FROM pg_class pgt WHERE SUBSTRING(pgt.relname FROM 10) = REPLACE(SUBSTRING(pg.relname 
FROM 10), '_index', ''))) END AS relidxrefrelname, relfilenode, relkind, reltuples::bigint, relpages 
FROM pg_class pg, pg_namespace pgn WHERE pg.relnamespace = pgn.oid AND pgn.nspname NOT IN 
('information_schema', 'pg_catalog') ORDER BY relpages DESC; 
```

#### 各テーブルの行長を取得
```sql
select tablename, attname, avg_width from pg_stats;
```

#### 各テーブル（列単位）の統計情報を確認（pg_statビューを使用）
```sql
SELECT * FROM pg_stats WHERE tablename = 'xxxxxxx';
```

#### DMLごとの実行回数を取得
```sql
select relname, n_tup_ins as insert_cnt, n_tup_upd as update_cnt, n_tup_del as delete_cnt from pg_stat_user_tables;
```

#### ディスクソートの実行回数を取得
```sql
select datname, temp_files, pg_size_pretty(temp_bytes) as temp_bytes, pg_size_pretty(round(temp_bytes/temp_files,2)) as temp_file_size
from pg_stat_database
where temp_files > 0;
```

#### 大量の行を読み取っている表スキャンを確認
```sql
select relname, seq_scan, seq_tup_read,seq_tup_read/seq_scan as tup_per_read 
from pg_stat_user_tables
where seq_scan > 0 order by tup_per_read desc;
```

#### dead tupleが多いテーブルを確認
```sql
select relname, n_live_tup, n_dead_tup,round(n_dead_tup*100/(n_dead_tup+n_live_tup), 2)  as dead_ratio,pg_size_pretty(pg_relation_size(relid))
from pg_stat_user_tables
where n_live_tup > 0
order by dead_ratio desc;
```

#### IOに関する情報取得
```sql
select * from pg_statio_all_tables;
```

#### SQLの総実行回数、総実行時間を確認する(pg_stat_statements)
```sql
select substr(query, 0, 160) as query, calls
  ,(total_time / 1000)::numeric(10,3) as total_time_sec
  ,(mean_time / 1000)::numeric(10,3) as avg_time_sec
  ,(min_time / 1000)::numeric(10,3) as min_time_sec
 ,(max_time / 1000)::numeric(10,3) as max_time_sec
from pg_stat_statements
order by total_time desc
limit 10;
```

#### vaccumの進捗状況を確認
```sql
select v.pid, v.datname, c.relname, v.phase, v.heap_blks_total, v.heap_blks_scanned, v.heap_blks_vacuumed, v.index_vacuum_count, v.max_dead_tuples, v.num_dead_tuples 
from pg_stat_progress_vacuum as v join pg_class as c on  v.relid = c.relfilenode ;
```

#### テーブルのoidを確認
```sql
select relid,relname from pg_stat_all_tables;
```

#### アクセス頻度の多いテーブル
```sql
select 
    relname,
    coalesce(seq_tup_read,0)+coalesce(idx_tup_fetch,0)+
    coalesce(n_tup_ins,0)+coalesce(n_tup_upd,0)+coalesce(n_tup_del,0) as total,
    coalesce(seq_tup_read,0)+coalesce(idx_tup_fetch,0) as select,
    coalesce(n_tup_ins,0) as insert,
    coalesce(n_tup_upd,0) as update,
    coalesce(n_tup_del,0) as delete
from pg_stat_user_tables
order by total desc;
```

#### I/O回数＆キャッシュヒット率
```sql
select *,(heap_blks_hit*100) / (heap_blks_read+heap_blks_hit) as ritu 
from pg_statio_all_tables 
where heap_blks_hit >= 1 
order by ritu;
```

#### インデックス毎のアクセスに関する統計情報を確認
```sql
select * from pg_stat_all_indexes;
```

#### パラメータ一覧と反映タイミング
```sql
SELECT name,setting,unit,context FROM pg_settings;

internal：変更不可(構築時設定確認用)
postmaster：サーバ起動時
sighup：設定ファイルの再読み込み
backend：セッション確立時に決定
superuser：スーパユーザ権限で動的変更可能
user：一般ユーザで動的変更可能
```

#### 参考：

> 稼動統計情報を活用しよう by Let's Postgres
> PGECons 2018年度WG3活動報告書 性能トラブル調査編
> ［改訂新版］内部構造から学ぶPostgreSQL 設計・運用計画の鉄則
> PostgreSQL徹底入門 第4版
> 参考資料ダウンロード(LPI-JAPAN OSS-DB) OSS-DB Exam Gold技術解説無料セミナー

