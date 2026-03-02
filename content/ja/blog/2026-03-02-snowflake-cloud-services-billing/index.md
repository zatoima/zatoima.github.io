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

実行結果のイメージ：

| USAGE_DATE | CREDITS_USED_CLOUD_SERVICES | CREDITS_ADJUSTMENT_CLOUD_SERVICES | BILLED_CLOUD_SERVICES |
|------------|---------------------------|-----------------------------------|-----------------------|
| 2026-03-01 | 15.234 | -10.000 | 5.234 |
| 2026-02-28 | 8.120 | -8.120 | 0.000 |
| 2026-02-27 | 12.500 | -10.000 | 2.500 |

`billed_cloud_services` が 0 の行は、その日のCS消費がVWの10%以内に収まっており課金されていないことを意味する。

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

実行結果のイメージ：

| WAREHOUSE_NAME | CREDITS_USED | CREDITS_USED_CLOUD_SERVICES | PCT_CLOUD_SERVICES |
|---------------|-------------|----------------------------|-------------------|
| ANALYTICS_WH | 45.200 | 9.800 | 21.68 |
| ETL_WH | 120.500 | 18.200 | 15.10 |
| ADHOC_WH | 30.100 | 2.500 | 8.31 |

`PCT_CLOUD_SERVICES` が 10% を大きく超えているウェアハウスは、前節のパターンに該当する処理が動いている可能性が高い。

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

実行結果のイメージ：

| QUERY_TYPE | CS_CREDITS | NUM_QUERIES |
|-----------|-----------|-------------|
| SELECT | 0.024500 | 15823 |
| COPY | 0.018200 | 342 |
| INSERT | 0.009100 | 5621 |
| SHOW | 0.005800 | 12045 |
| CREATE_TABLE | 0.001200 | 87 |

`SHOW` クエリの件数が多く CS 消費が高い場合、サードパーティツールが頻繁にメタデータを取得していると考えられる。

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
