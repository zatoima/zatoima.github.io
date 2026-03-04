---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflake クラウドサービス利用料の仕組みと最適化"
subtitle: ""
summary: "Snowflake のクラウドサービス（Cloud Services）レイヤーの仕組みと課金ルールを解説する。1日のCS消費がVWクレジットの10%を超えた場合のみ超過分が課金される「10%ルール」の詳細、METERING_DAILY_HISTORY・WAREHOUSE_METERING_HISTORY・QUERY_HISTORYを使った費用追跡クエリ、および削減優先順位を整理する。"
tags: ["Snowflake", "コスト管理"]
categories: ["Snowflake"]
url: snowflake-cloud-services-billing
date: 2026-03-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false
---

## はじめに

Snowflake の利用明細を見ると、ウェアハウスのコンピュートとは別に「クラウドサービス（Cloud Services）」というクレジット消費が記録されている。これが何者で、どういう条件で課金され、どう追跡・削減するかを整理する。

公式ドキュメント: [Understanding compute cost](https://docs.snowflake.com/en/user-guide/cost-understanding-compute) / [Optimizing cloud services for cost](https://docs.snowflake.com/en/user-guide/cost-optimize-cloud-services)

---

## クラウドサービスレイヤーとは

Snowflake のアーキテクチャは大きく3層に分かれる。

```
┌────────────────────────────────────────────┐
│        Cloud Services Layer                │  ← 今回の対象
│  認証 / メタデータ管理 / クエリコンパイル      │
│  アクセス制御 / トランザクション管理           │
├────────────────────────────────────────────┤
│        Compute Layer（仮想ウェアハウス）      │  ← クエリ・DML実行
├────────────────────────────────────────────┤
│        Storage Layer                       │  ← データ永続化
└────────────────────────────────────────────┘
```

クラウドサービスレイヤーは、ユーザーが明示的にウェアハウスを起動しなくても、Snowflake が内部的に常時稼働させているコンポーネントになる。主な役割は以下のとおり。

| 機能 | 内容 |
|------|------|
| 認証・認可 | ログイン検証、ロール解決、行ポリシー評価 |
| メタデータ管理 | テーブル定義、パーティション情報、統計情報の管理 |
| クエリコンパイル | SQL のパース、最適化プラン生成、プルーニング |
| トランザクション管理 | ACID 保証、スナップショット管理 |

---

## 10%ルール（Cloud Services Adjustment）

### 課金の仕組み

クラウドサービスのクレジット消費は**常に発生**するが、課金（請求）されるのは一定の条件を超えた場合のみとなる。

> **1日（UTC）のクラウドサービス消費量が、同日の仮想ウェアハウス消費量の10%を超えた場合のみ、超過分が課金される。**

超過分のみが課金される仕組みを「Cloud Services Adjustment（調整）」と呼ぶ。METERING_DAILY_HISTORY ビューの `CREDITS_ADJUSTMENT_CLOUD_SERVICES` 列が負の値で記録され、その分だけ差し引かれる。

{{< callout "info" >}}
サーバーレスコンピュート（Snowpipe、Automatic Clustering 等）は、この10%調整の計算対象外となる。調整に使われるのは**仮想ウェアハウスのクレジットのみ**。
{{< /callout >}}

### 計算例

公式ドキュメントの具体例を以下に示す。

| 日付 | VW使用クレジット | CS使用クレジット | 調整額（10%以下は全額控除） | 課金クレジット |
|------|----------------|----------------|--------------------------|-------------|
| Nov 1 | 100 | 20 | −10 | 110 |
| Nov 2 | 120 | 10 | −10 | 120 |
| Nov 3 | 80 | 5 | −5 | 80 |
| Nov 4 | 100 | 13 | −10 | 103 |
| **合計** | **400** | **48** | **−35** | **413** |

- Nov 1: CS=20 > VW×10%=10 → 超過10クレジット分が課金。調整額は −10
- Nov 2: CS=10 < VW×10%=12 → CS が10%未満 → 調整額は −10（CS全額控除）
- Nov 3: CS=5 < VW×10%=8 → 全額調整。調整額は −5（CS全額控除）
- Nov 4: CS=13 > VW×10%=10 → 超過3クレジット分が課金。調整額は −10

---

## クラウドサービス費用が発生するユースケース

以下のいずれも、仮想ウェアハウスを**使わずに**クラウドサービスのみでリソースを消費するパターンになる。

| パターン | 発生原因 | 推奨対策 |
|---------|---------|---------|
| COPYコマンドの低選択性 | S3ファイル一覧取得はCSのみで実行 | S3バケットに日付プレフィックスを付与し、対象ファイルを絞る |
| 高頻度DDL・クローニング | CREATE/DROP/CLONE はメタデータ操作のみ | クローンの粒度を見直す（スキーマ全体→テーブル単位へ） |
| 高頻度の単純クエリ | `SELECT 1`、`SELECT CURRENT_SESSION()` の大量実行 | JDBC ドライバの `getSessionId()` メソッドを使ってキャッシュ活用 |
| INFORMATION_SCHEMA の高頻度クエリ | I_Sクエリはウェアハウス不使用 | `ACCOUNT_USAGE` スキーマへ切り替える |
| 高頻度SHOWコマンド | アプリ・サードパーティツールがメタデータを頻繁に取得 | ツール側のポーリング頻度を見直す |
| 単一行INSERT・細粒度スキーマ | 小さいメタデータ操作の積み重ね | バルクロードに変更。マルチテナントはスキーマ共有 + `customer_id` クラスタリングへ |
| 複雑なSQLクエリ | JOINが多い、`IN` 句に大きなリスト | コンパイル時間が長いクエリを見直す |

---

## 操作別クラウドサービス消費量の実測

実際に各種操作を実行し、`INFORMATION_SCHEMA.QUERY_HISTORY` でCS消費量を計測した。以下はその結果だ。

### CS のみで完結する操作（ウェアハウス不使用）

`bytes_scanned = 0` となり、仮想ウェアハウスを起動せずにCS単独で処理される操作の一覧。

| カテゴリ | 操作例 | CS消費量（実測） | 備考 |
|--------|-------|--------------|------|
| セッション関数 | `SELECT 1` | 0.000006〜0.000014 | 最小コストのCS操作 |
| コンテキスト関数 | `SELECT CURRENT_SESSION()`, `CURRENT_USER()` | 0.000007〜0.000009 | セッション情報の参照 |
| SHOW コマンド（軽量） | `SHOW TABLES`, `SHOW SCHEMAS` | 0.000005〜0.000018 | オブジェクト数に比例 |
| SHOW コマンド（重量） | `SHOW GRANTS TO ROLE SYSADMIN` | **0.001902** | 権限エントリ数が多いと増加 |
| DESC / DESCRIBE | `DESC TABLE`, `DESC STREAM` | 0.000006〜0.000028 | オブジェクト構造の参照 |
| USE 文 | `USE DATABASE`, `USE SCHEMA` | 0.000005〜0.000013 | コンテキスト切り替え |
| ALTER SESSION | `ALTER SESSION SET/UNSET` | 0.000007〜0.000008 | セッションパラメータ変更 |
| CREATE TABLE | `CREATE OR REPLACE TABLE` | 0.000020〜0.000031 | DDL はすべてCS操作 |
| CREATE SEQUENCE | `CREATE SEQUENCE` | 0.000012 | シーケンスのメタデータ登録 |
| CREATE STREAM | `CREATE STREAM ... ON TABLE` | **0.000069** | Streamオブジェクト作成 |
| CLONE（テーブル） | `CREATE TABLE ... CLONE` | **0.000164** | メタデータのコピーのみ |
| CLONE（スキーマ） | `CREATE SCHEMA ... CLONE` | **0.000458** | テーブルクローンの3倍近く |
| ALTER TABLE（カラム操作） | `ADD COLUMN / DROP COLUMN` | 0.000010〜0.000018 | スキーマ変更のみ |
| Stream メタデータ参照 | `SELECT metadata$action FROM stream` | 0.000026 | Stream変更追跡メタデータ |
| SYSTEM$ 関数 | `SYSTEM$STREAM_HAS_DATA(...)` | 0.000009 | Streamの変更有無チェック |
| シーケンス NEXTVAL | `SELECT seq.NEXTVAL` | 0.000008〜0.000009 | 採番のたびにCS消費 |
| Time Travel（メタデータのみ） | `SELECT COUNT(*) ... AT(OFFSET => -60)` | 0.000007 | 過去スナップショットのカウント |
| INFORMATION_SCHEMA（軽量） | `SELECT ... FROM I_S.TABLES` | 0.000026〜0.000034 | テーブル・カラム定義の参照 |
| INFORMATION_SCHEMA（重量） | 結果件数が多いクエリ | **0.000614** | 返却行数に比例して増加 |

{{< callout "info" >}}
CLONE のCS消費はスキーマ全体 > テーブル単体の順に大きくなる。スキーマクローン（0.000458）はテーブルクローン（0.000164）の約3倍のCS消費となった。バックアップ用途でスキーマクローンを頻繁に実行するパターンは注意が必要となる。
{{< /callout >}}

### 結果キャッシュの挙動

同一クエリを2回実行した際の比較。

| 実行回 | bytes_scanned | CS消費量 | 実行時間 | 判定 |
|------|-------------|---------|---------|------|
| 1回目（ウェアハウス計算） | 4,096 bytes | 0.000009 | 83ms | WAREHOUSE_COMPUTE |
| 2回目（結果キャッシュ） | 0 bytes | 0.000007 | **44ms** | RESULT_CACHE_HIT |

結果キャッシュヒット時もCS消費はゼロにはならない。これはCSがキャッシュを管理・提供する処理自体にCSリソースを使うためだ。消費量は初回の約78%程度で、完全に消えるわけではない点に留意する。キャッシュヒットの特徴は `bytes_scanned = 0` かつ `rows_produced > 0` の組み合わせで判別できる。

```sql
-- 結果キャッシュヒットかどうかを判別するクエリ
SELECT
    query_type,
    LEFT(query_text, 80)                  AS query_snippet,
    ROUND(credits_used_cloud_services, 8) AS cs_credits,
    bytes_scanned,
    rows_produced,
    CASE
        WHEN bytes_scanned = 0 AND rows_produced > 0 THEN 'RESULT_CACHE_HIT'
        WHEN bytes_scanned > 0 AND rows_produced > 0 THEN 'WAREHOUSE_COMPUTE'
        ELSE 'CS_ONLY_METADATA'
    END AS access_type
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    DATEADD('minute', -30, CURRENT_TIMESTAMP),
    NULL, 200
))
WHERE query_type = 'SELECT'
ORDER BY start_time DESC;
```

---

## クラウドサービス費用の追跡方法

### 1. 日次課金サマリー（METERING_DAILY_HISTORY）

`SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY` ビューで、日ごとのCS使用量と調整後の実課金量を確認できる。

```sql
-- 過去1ヶ月のCS課金サマリー（課金量が多い日順）
SELECT
    usage_date,
    credits_used_cloud_services,
    credits_adjustment_cloud_services,
    credits_used_cloud_services + credits_adjustment_cloud_services AS billed_cloud_services
FROM snowflake.account_usage.metering_daily_history
WHERE usage_date >= DATEADD(month, -1, CURRENT_TIMESTAMP())
    AND credits_used_cloud_services > 0
ORDER BY 4 DESC;
```

実行結果：

| USAGE_DATE | CREDITS_USED_CLOUD_SERVICES | CREDITS_ADJUSTMENT_CLOUD_SERVICES | BILLED_CLOUD_SERVICES |
|------------|---------------------------|-----------------------------------|-----------------------|
| 2026-02-21 | 0.010796945 | -0.0107969450 | 0 |
| 2026-02-17 | 0.009336666 | -0.0093366660 | 0 |
| 2026-02-27 | 0.006565000 | -0.0065650000 | 0 |
| 2026-02-23 | 0.006603055 | -0.0066030550 | 0 |
| 2026-02-04 | 0.012600552 | -0.0126005520 | 0 |

すべての行で `billed_cloud_services = 0` になっている。CS消費量と調整額が完全に一致しており、VWの10%以内に収まっているため追加課金が発生していない状態だ。調整の仕組みが正常に機能している例として読み取れる。

主要列の意味：

| 列名 | 説明 |
|------|------|
| `CREDITS_USED_CLOUD_SERVICES` | その日の実際のCS消費量 |
| `CREDITS_ADJUSTMENT_CLOUD_SERVICES` | 調整額（負の値。最大で10%分） |
| `CREDITS_BILLED` | 実際に請求されるクレジット合計 |

### 2. ウェアハウス別の分析（WAREHOUSE_METERING_HISTORY）

CSの割合が高いウェアハウスを特定することで、問題のある処理を絞り込める。

```sql
-- CS割合が高いウェアハウスを特定
SELECT
    warehouse_name,
    SUM(credits_used)                AS credits_used,
    SUM(credits_used_cloud_services) AS credits_used_cloud_services,
    ROUND(
        SUM(credits_used_cloud_services) / NULLIF(SUM(credits_used), 0) * 100,
        2
    )                                AS pct_cloud_services
FROM snowflake.account_usage.warehouse_metering_history
WHERE TO_DATE(start_time) >= DATEADD(month, -1, CURRENT_TIMESTAMP())
    AND credits_used_cloud_services > 0
GROUP BY 1
ORDER BY 4 DESC;
```

実行結果：

| WAREHOUSE_NAME | CREDITS_USED | CREDITS_USED_CLOUD_SERVICES | PCT_CLOUD_SERVICES |
|---------------|-------------|----------------------------|-------------------|
| CLOUD_SERVICES_ONLY | 0.008040553 | 0.008040553 | 100.00 |
| COMPUTE_WH | 6.615521114 | 0.273854438 | 4.14 |
| RETAIL_WH | 0.046300557 | 0.001300557 | 2.81 |

`CLOUD_SERVICES_ONLY` は Snowflake が仮想ウェアハウスを介さずに実行する処理（DDL、メタデータ操作等）を計上する擬似ウェアハウスで、CS割合が必ず100%になる。`COMPUTE_WH` は 4.14%、`RETAIL_WH` は 2.81% とともに10%未満に収まっており、追加課金は発生していない。

`PCT_CLOUD_SERVICES` が 10% を大きく超えているウェアハウスが出た場合、前節のパターンに該当する処理が動いている可能性が高い。

### 3. クエリタイプ別の分析（QUERY_HISTORY）

どの種類の操作がCSを多く消費しているか確認する。

```sql
-- 過去7日間のクエリタイプ別CS消費量
SELECT
    query_type,
    ROUND(SUM(credits_used_cloud_services), 6) AS cs_credits,
    COUNT(1)                                   AS num_queries
FROM snowflake.account_usage.query_history
WHERE start_time >= TIMESTAMPADD(day, -7, CURRENT_TIMESTAMP)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

実行結果：

| QUERY_TYPE | CS_CREDITS | NUM_QUERIES |
|-----------|-----------|-------------|
| SELECT | 0.062068 | 1205 |
| DROP | 0.002595 | 115 |
| CALL | 0.000925 | 577 |
| SHOW | 0.000596 | 281 |
| INSERT | 0.000555 | 18 |
| CREATE_TABLE | 0.000434 | 11 |
| DROP_ROLE | 0.000376 | 15 |
| CREATE | 0.000319 | 46 |
| USE | 0.000169 | 20 |
| UPDATE | 0.000089 | 22 |

SELECT が CS消費の大半を占めており、DROP（テーブル削除等のDDL）と SHOW がそれに続く。281件の SHOW に対してクレジット消費は 0.000596 と軽微だが、アプリが頻繁にメタデータを取得する構成では件数がこの数十倍規模になることもある。

### 4. Snowsight での確認

Snowsight の **Admin > Cost Management** からグラフィカルに確認できる。サービスタイプや期間でフィルタリングでき、クエリを書かずに傾向を把握するのに適している。

---

## 補足

### INFORMATION_SCHEMA と ACCOUNT_USAGE の違い

追跡クエリを書く際、スキーマ選択で挙動が変わる点に注意が必要となる。

| 比較項目 | INFORMATION_SCHEMA | ACCOUNT_USAGE |
|---------|-------------------|---------------|
| データ取得方法 | クラウドサービスのみ | 仮想ウェアハウスを使用 |
| CS消費への影響 | 高頻度実行時に増加 | ウェアハウスに計上 |
| データ反映速度 | リアルタイム | 最大180分のレイテンシ |
| 保持期間 | 7日〜6ヶ月 | 最大365日 |

モニタリング用途では `ACCOUNT_USAGE` を使うのがコスト面で有利なケースが多い。

### METERING_DAILY_HISTORY の注意点

- ビューのレイテンシは最大**180分（3時間）**
- `CREDITS_USED_CLOUD_SERVICES` 列のレイテンシは最大**6時間**（`WAREHOUSE_METERING_HISTORY` 側）
- 月次請求と照合する際は、セッションのタイムゾーンを UTC に設定してから参照する

```sql
ALTER SESSION SET TIMEZONE = UTC;
```

### コスト削減の優先順位

実際の対策として効果が出やすい順に並べると以下のようになる。

1. **INFORMATION_SCHEMA → ACCOUNT_USAGE への切り替え** — コード変更だけで対応可能
2. **高頻度 SHOW コマンドの削減** — ツール設定の見直しで対応
3. **単一行 INSERT のバルク化** — アーキテクチャ変更が必要だが効果大
4. **COPY コマンドの S3 バケット構造見直し** — 段階的に対応可能

---

## まとめ

- クラウドサービスレイヤーは認証・メタデータ管理・クエリコンパイルを担い、常時クレジットを消費する
- 課金は「1日のCS消費がVWの10%を超えた場合の超過分のみ」という仕組みで、多くの場合は調整が効く
- `METERING_DAILY_HISTORY`・`WAREHOUSE_METERING_HISTORY`・`QUERY_HISTORY` の3つのビューで段階的に原因を特定できる
- CS費用が高い場合はまず「高頻度のSHOW/INFORMATION_SCHEMAクエリ」と「単一行INSERT」を疑う

## 参考資料

{{< linkcard "https://docs.snowflake.com/en/user-guide/cost-understanding-compute" >}}

{{< linkcard "https://docs.snowflake.com/en/user-guide/cost-optimize-cloud-services" >}}

{{< linkcard "https://docs.snowflake.com/en/user-guide/cost-exploring-compute" >}}

{{< linkcard "https://docs.snowflake.com/en/sql-reference/account-usage/metering_daily_history" >}}
