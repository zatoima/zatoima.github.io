---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "SnowflakeのTime Travel"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-timetravel-summary
date: 2022-08-25
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



SnowPro Core 認定試験ガイドの6.2向けの勉強メモ

> Snowflake 認定資格 | Snowflake 【スノーフレイク】 https://www.snowflake.com/certifications/?lang=ja

6.2 Snowflakeによる継続的なデータ保護の概要を説明する。

- Time Travel
- Fail Safe
- データ暗号化
- クローニング

### Time Travelの概要

- テーブル、スキーマ、データベース、について定義された期間の間の任意の時点で履歴データにアクセスできる機能。
  - 通常、テーブルをDROPした場合、バックアップから戻すことが必要となるが、Time Travel機能を使用することで簡単に復元することが出来る
  - テーブルだけではなく、スキーマやデータベース単位と広い論理範囲で戻すことが出来る

- エディションによる戻せる期間の差異
  - Standard：最大1日
  - Enterprise以上：最大90日
- テーブルの種類による戻せる期間の差異
  - Transient及びTemporaryテーブルは最大1日

### 設定方法

設定値の確認

```sql
SHOW PARAMETERS like '%DATA_RETENTION_TIME_IN_DAYS%' in account;
```

アカウントレベルの設定（※危険）

```sql
ALTER ACCOUNT SET DATA_RETENTION_TIME_IN_DAYS=5;
```

テーブル単位の設定

```sql
CREATE TABLE my_table (c1 int) SET DATA_RETENTION_TIME_IN_DAYS=90
ALTER TABLE my_table SET DATA_RETENTION_TIME_IN_DAYS=30
```

### Time Travelの実行方法

復元、クエリ、クローンの3種類がある

#### 復元

```sql
-- データベースの復元
UNDROP DATABASE <name>;
-- スキーマの復元
UNDROP SCHEMA <name>;
-- テーブルの復元
UNDROP TABLE <name>;
```

#### クエリ

標準時からマイナス7時間とした上で、2015年5月1日16時20分時点のmy_tableのデータを取得する

```sql
SELECT * FROM my_table AT(timestamp => 'Fri, 01 May 2015 16:20:00 -0700'::timestamp_tz);
```

10分前の時点のmy_tableのデータを取得する。offsetには秒単位で入れるため、「60秒×10」で10分を表す

```sql
SELECT * FROM my_table AT((offset => -60*10);
```

指定したクエリIDのクエリが実行される前の状態の、my_tableのデータを取得する

```sql
SELECT * FROM my_table BEFORE(statement => '<クエリID>');
```

#### クローニング

指定されたタイムスタンプで表される日付と時刻のテーブルのクローンを作成

```sql
create table restored_table clone my_table
  at(timestamp => 'Sat, 09 May 2015 01:01:00 +0300'::timestamp_tz);
```

現在時刻の1時間前に存在していたスキーマとそのすべてのオブジェクトのクローンを作成

```sql
create schema restored_schema clone my_schema at(offset => -3600);
```

指定されたステートメントの完了前に存在していたデータベースとそのすべてのオブジェクトのクローンを作成

```sql
create database restored_db clone my_db
  before(statement => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');
```

#### Time Travelの使用量について

[TABLE\_STORAGE\_METRICS ビュー — Snowflake Documentation](https://docs.snowflake.com/ja/sql-reference/info-schema/table_storage_metrics.html)

上記ビューから確認が可能

```sql
select
    TABLE_CATALOG,
    TABLE_NAME,
    ((ACTIVE_BYTES / 1024) / 1024) / 1024 as storage_usage_gb,
    ((TIME_TRAVEL_BYTES / 1024) / 1024) / 1024 as timetravel_usage_gb
from
    "INFORMATION_SCHEMA".table_storage_metrics
where
    TABLE_NAME in('T1')
;
```

### 参考

- [Time Travelの理解と使用 — Snowflake Documentation](https://docs.snowflake.com/ja/user-guide/data-time-travel.html)

- [Time TravelおよびFail\-safeのストレージコスト — Snowflake Documentation](https://docs.snowflake.com/ja/user-guide/data-cdp-storage-costs.html)

- [Snowflakeのタイムトラベル関連でよく使いそうなコマンドを試してみた \#SnowflakeDB \| DevelopersIO](https://dev.classmethod.jp/articles/snowflake-timetravel-useful-command/)

- [Snowflakeのタイムトラベル機能であの頃（の状態のデータ）に戻ろう \| DevelopersIO](https://dev.classmethod.jp/articles/snowflake-time-travel/)
