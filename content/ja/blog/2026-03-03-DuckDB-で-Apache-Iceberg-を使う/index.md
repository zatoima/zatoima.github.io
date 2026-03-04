---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "DuckDB で Apache Iceberg を使う"
subtitle: ""
summary: "DuckDB v1.4.4 の Iceberg 拡張機能を使い、iceberg_scan によるテーブル読み込み、iceberg_snapshots・iceberg_metadata によるメタデータ確認、タイムトラベル、REST カタログ経由での CREATE TABLE・INSERT・UPDATE・DELETE を実際に動かして検証した記録である。"
tags: ["DuckDB", "Iceberg", "データレイク", "分析基盤"]
categories: ["データ基盤"]
url: duckdb-apache-iceberg-extension
date: 2026-03-03
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

[Apache Iceberg](https://iceberg.apache.org/) はオープンテーブルフォーマットの一つで、大規模な分析ワークロードに向けたスキーマ管理、タイムトラベル、パーティション管理などの機能を提供する。

DuckDB は v1.4.0 から Iceberg 拡張機能でテーブルへの書き込みをサポートし、v1.4.2 では UPDATE・DELETE まで対応した。DuckDB だけで Iceberg テーブルのライフサイクル全体を扱えるようになった。

本記事では DuckDB v1.4.4 を使い、以下を検証する。

- `iceberg_scan()` によるテーブルの読み込み
- `iceberg_snapshots()` / `iceberg_metadata()` によるメタデータ確認
- `snapshot_from_id` / `snapshot_from_timestamp` によるタイムトラベル
- REST カタログ経由での CREATE TABLE / INSERT / UPDATE / DELETE

公式ドキュメントは [Iceberg Extension – DuckDB](https://duckdb.org/docs/stable/core_extensions/iceberg/overview) を参照。

## Iceberg 拡張のセットアップ

```sql
INSTALL iceberg;
LOAD iceberg;
```

初回実行時に自動ダウンロードされる。インストール済みであれば `LOAD iceberg;` のみで使える。

利用可能な関数は以下の通り。

```sql
SELECT function_name, function_type
FROM duckdb_functions()
WHERE function_name LIKE 'iceberg%'
ORDER BY function_name;
```

```text
┌──────────────────────────┬───────────────┐
│      function_name       │ function_type │
├──────────────────────────┼───────────────┤
│ iceberg_metadata         │ table         │
│ iceberg_scan             │ table         │
│ iceberg_snapshots        │ table         │
│ iceberg_table_properties │ table         │
│ iceberg_to_ducklake      │ table         │
└──────────────────────────┴───────────────┘
```

## iceberg_scan でテーブルを読み込む

検証用データとして PyIceberg でローカルに Iceberg テーブルを作成し、果物の価格データを 2 回に分けて投入した。

```python
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, IntegerType, StringType, DoubleType
import pyarrow as pa

catalog = SqlCatalog(
    'local',
    **{
        'uri': 'sqlite:////tmp/iceberg_test/catalog.db',
        'warehouse': 'file:///tmp/iceberg_test/warehouse',
    }
)

schema = Schema(
    NestedField(field_id=1, name='id',       field_type=IntegerType(), required=True),
    NestedField(field_id=2, name='name',     field_type=StringType()),
    NestedField(field_id=3, name='price',    field_type=DoubleType()),
    NestedField(field_id=4, name='category', field_type=StringType()),
)

table = catalog.create_table('default.products', schema=schema)

# 1 回目（スナップショット 1）
pa_schema = pa.schema([
    pa.field('id', pa.int32(), nullable=False),
    pa.field('name', pa.string()),
    pa.field('price', pa.float64()),
    pa.field('category', pa.string()),
])
table.append(pa.table({
    'id':       pa.array([1, 2, 3, 4, 5], type=pa.int32()),
    'name':     pa.array(['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry']),
    'price':    pa.array([1.50, 0.80, 3.00, 5.00, 8.00]),
    'category': pa.array(['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit']),
}, schema=pa_schema))

# 2 回目（スナップショット 2）
table.append(pa.table({
    'id':       pa.array([6, 7, 8], type=pa.int32()),
    'name':     pa.array(['Fig', 'Grape', 'Honeydew']),
    'price':    pa.array([4.50, 2.20, 6.80]),
    'category': pa.array(['Fruit', 'Fruit', 'Melon']),
}, schema=pa_schema))
```

DuckDB からはメタデータファイルの JSON パスを指定して読み込む。

```sql
LOAD iceberg;

SELECT * FROM iceberg_scan(
    '/tmp/iceberg_test/warehouse/default/products/metadata/00002-ce5e4a45-0c63-4322-9af4-9f0416977efd.metadata.json'
)
ORDER BY id;
```

```text
┌───────┬────────────┬────────┬──────────┐
│  id   │    name    │ price  │ category │
│ int32 │  varchar   │ double │ varchar  │
├───────┼────────────┼────────┼──────────┤
│     1 │ Apple      │    1.5 │ Fruit    │
│     2 │ Banana     │    0.8 │ Fruit    │
│     3 │ Cherry     │    3.0 │ Fruit    │
│     4 │ Date       │    5.0 │ Fruit    │
│     5 │ Elderberry │    8.0 │ Fruit    │
│     6 │ Fig        │    4.5 │ Fruit    │
│     7 │ Grape      │    2.2 │ Fruit    │
│     8 │ Honeydew   │    6.8 │ Melon    │
└───────┴────────────┴────────┴──────────┘
```

通常の SQL 構文をそのまま使える。

```sql
SELECT category, COUNT(*) AS count, ROUND(AVG(price), 2) AS avg_price, MAX(price) AS max_price
FROM iceberg_scan('/tmp/iceberg_test/warehouse/default/products/metadata/00002-...metadata.json')
GROUP BY category
ORDER BY category;
```

```text
┌──────────┬───────┬───────────┬───────────┐
│ category │ count │ avg_price │ max_price │
├──────────┼───────┼───────────┼───────────┤
│ Fruit    │     7 │      3.57 │       8.0 │
│ Melon    │     1 │       6.8 │       6.8 │
└──────────┴───────┴───────────┴───────────┘
```

## スナップショットとメタデータの確認

### iceberg_snapshots()

```sql
SELECT sequence_number, snapshot_id, timestamp_ms
FROM iceberg_snapshots('/tmp/iceberg_test/warehouse/default/products/metadata/00002-...metadata.json');
```

```text
┌─────────────────┬─────────────────────┬─────────────────────────┐
│ sequence_number │     snapshot_id     │      timestamp_ms       │
├─────────────────┼─────────────────────┼─────────────────────────┤
│               1 │ 6271676225834788955 │ 2026-03-02 07:09:33.521 │
│               2 │ 6235383406797039698 │ 2026-03-02 07:09:33.546 │
└─────────────────┴─────────────────────┴─────────────────────────┘
```

2 回の `append()` に対応して 2 つのスナップショットが記録されている。

### iceberg_metadata()

データファイルレベルの詳細を確認できる。

```sql
SELECT manifest_sequence_number, status, file_path, file_format, record_count
FROM iceberg_metadata('/tmp/iceberg_test/warehouse/default/products/metadata/00002-...metadata.json')
ORDER BY manifest_sequence_number;
```

```text
┌──────────────────────────┬─────────┬─────────────────────────────────────────────────────────────────────────┬─────────────┬──────────────┐
│ manifest_sequence_number │ status  │                              file_path                                  │ file_format │ record_count │
├──────────────────────────┼─────────┼─────────────────────────────────────────────────────────────────────────┼─────────────┼──────────────┤
│                        1 │ ADDED   │ file:///tmp/.../data/00000-0-92d0c825-...parquet                        │ PARQUET     │            5 │
│                        2 │ ADDED   │ file:///tmp/.../data/00000-0-ca64ef58-...parquet                        │ PARQUET     │            3 │
└──────────────────────────┴─────────┴─────────────────────────────────────────────────────────────────────────┴─────────────┴──────────────┘
```

各スナップショットに対応する Parquet ファイルが ADDED ステータスで登録されている。Iceberg の内部構造が確認でき、スナップショット→マニフェスト→データファイルの階層になっていることがわかる。

```text
Iceberg テーブル
└── metadata/
    ├── 00000-....metadata.json   ← テーブル定義
    ├── 00001-....metadata.json   ← スナップショット 1
    ├── 00002-....metadata.json   ← スナップショット 2（最新）
    ├── snap-xxxx.avro            ← マニフェストリスト
    └── xxxx-m0.avro              ← マニフェスト（データファイル一覧）
data/
    ├── 00000-0-xxxx.parquet      ← バッチ 1（5 行）
    └── 00000-0-yyyy.parquet      ← バッチ 2（3 行）
```

## タイムトラベル

### snapshot_from_id でスナップショット指定

```sql
-- スナップショット 1 時点（5 行）
SELECT * FROM iceberg_scan(
    '/tmp/iceberg_test/warehouse/default/products/metadata/00002-...metadata.json',
    snapshot_from_id=6271676225834788955
)
ORDER BY id;
```

```text
┌───────┬────────────┬────────┬──────────┐
│  id   │    name    │ price  │ category │
├───────┼────────────┼────────┼──────────┤
│     1 │ Apple      │    1.5 │ Fruit    │
│     2 │ Banana     │    0.8 │ Fruit    │
│     3 │ Cherry     │    3.0 │ Fruit    │
│     4 │ Date       │    5.0 │ Fruit    │
│     5 │ Elderberry │    8.0 │ Fruit    │
└───────┴────────────┴────────┴──────────┘
```

最新は 8 行だが、スナップショット 1 時点の 5 行が取得できた。

### snapshot_from_timestamp でタイムスタンプ指定

```sql
-- 2 回目の INSERT 前の時点を指定
SELECT * FROM iceberg_scan(
    '/tmp/iceberg_test/warehouse/default/products/metadata/00002-...metadata.json',
    snapshot_from_timestamp='2026-03-02 07:09:33.530'
)
ORDER BY id;
```

スナップショット ID を調べなくても、タイムスタンプ指定でタイムトラベルできる。指定したタイムスタンプ以前の最新スナップショットが使われる。

## REST カタログへの接続と書き込み操作

書き込み操作には Iceberg REST カタログが必要になる。ここでは [tabulario/iceberg-rest](https://github.com/databricks/iceberg-rest-image) をローカルで起動して検証した。

```bash
docker run -d --name iceberg-rest \
  -p 8181:8181 \
  -v /tmp/iceberg_warehouse:/tmp/iceberg_warehouse \
  -e CATALOG_WAREHOUSE=/tmp/iceberg_warehouse \
  tabulario/iceberg-rest:latest
```

DuckDB から接続するには `ATTACH` に `TYPE ICEBERG` と `ENDPOINT` を指定する。

```sql
LOAD iceberg;

ATTACH '' AS iceberg_rest (
    TYPE ICEBERG,
    ENDPOINT 'http://localhost:8181',
    AUTHORIZATION_TYPE NONE
);
```

接続後は通常の DuckDB と同じ SQL 構文でテーブルを操作できる。

### CREATE TABLE / INSERT

```sql
CREATE SCHEMA IF NOT EXISTS iceberg_rest.demo;

CREATE TABLE iceberg_rest.demo.sales (
    order_id INTEGER,
    product  VARCHAR,
    quantity INTEGER,
    amount   DOUBLE,
    region   VARCHAR
);

INSERT INTO iceberg_rest.demo.sales VALUES
    (1, 'Laptop',    2, 2400.00, 'East'),
    (2, 'Mouse',    10,  150.00, 'West'),
    (3, 'Keyboard',  5,  375.00, 'East'),
    (4, 'Monitor',   3, 1200.00, 'North'),
    (5, 'Headset',   8,  480.00, 'West');

SELECT * FROM iceberg_rest.demo.sales ORDER BY order_id;
```

```text
┌──────────┬──────────┬──────────┬────────┬─────────┐
│ order_id │ product  │ quantity │ amount │ region  │
├──────────┼──────────┼──────────┼────────┼─────────┤
│        1 │ Laptop   │        2 │ 2400.0 │ East    │
│        2 │ Mouse    │       10 │  150.0 │ West    │
│        3 │ Keyboard │        5 │  375.0 │ East    │
│        4 │ Monitor  │        3 │ 1200.0 │ North   │
│        5 │ Headset  │        8 │  480.0 │ West    │
└──────────┴──────────┴──────────┴────────┴─────────┘
```

### UPDATE / DELETE（v1.4.2 以降）

```sql
-- 価格変更
UPDATE iceberg_rest.demo.sales SET amount = 2600.00 WHERE order_id = 1;

-- 地域を条件に削除
DELETE FROM iceberg_rest.demo.sales WHERE region = 'West';

SELECT * FROM iceberg_rest.demo.sales ORDER BY order_id;
```

```text
┌──────────┬──────────┬──────────┬────────┬─────────┐
│ order_id │ product  │ quantity │ amount │ region  │
├──────────┼──────────┼──────────┼────────┼─────────┤
│        1 │ Laptop   │        2 │ 2600.0 │ East    │
│        3 │ Keyboard │        5 │  375.0 │ East    │
│        4 │ Monitor  │        3 │ 1200.0 │ North   │
└──────────┴──────────┴──────────┴────────┴─────────┘
```

West リージョンの 2 行が削除され、Laptop の amount が 2400.0 から 2600.0 に更新された。

{{< callout "info" >}}
UPDATE / DELETE は非パーティション・非ソートのテーブルのみサポート。パーティション化されたテーブルに対して実行するとエラーになる。
{{< /callout >}}

### 操作後のスナップショット確認

```sql
SELECT sequence_number, snapshot_id, timestamp_ms
FROM iceberg_snapshots(iceberg_rest.demo.sales)
ORDER BY sequence_number;
```

```text
┌─────────────────┬─────────────────────┬─────────────────────────┐
│ sequence_number │     snapshot_id     │      timestamp_ms       │
├─────────────────┼─────────────────────┼─────────────────────────┤
│               1 │ 3015870820437673917 │ 2026-03-02 07:12:20.701 │
│               2 │ 8210928633681103167 │ 2026-03-02 07:12:27.015 │
│               3 │ 7873958590094721501 │ 2026-03-02 07:12:32.734 │
└─────────────────┴─────────────────────┴─────────────────────────┘
```

INSERT・UPDATE・DELETE の 3 操作に対応して 3 つのスナップショットが記録されている。`snapshot_from_id` を使えば各操作前の状態に戻れる。

```sql
-- INSERT 直後の状態（5 行、amount=2400）
SELECT * FROM iceberg_scan(iceberg_rest.demo.sales, snapshot_from_id=3015870820437673917)
ORDER BY order_id;
```

```text
┌──────────┬──────────┬──────────┬────────┬─────────┐
│ order_id │ product  │ quantity │ amount │ region  │
├──────────┼──────────┼──────────┼────────┼─────────┤
│        1 │ Laptop   │        2 │ 2400.0 │ East    │
│        2 │ Mouse    │       10 │  150.0 │ West    │
│        3 │ Keyboard │        5 │  375.0 │ East    │
│        4 │ Monitor  │        3 │ 1200.0 │ North   │
│        5 │ Headset  │        8 │  480.0 │ West    │
└──────────┴──────────┴──────────┴────────┴─────────┘
```

## まとめ

DuckDB v1.4.4 での Iceberg 拡張機能の動作確認結果をまとめる。

| 操作 | 関数 / 構文 | 備考 |
|------|------------|------|
| 読み込み | `iceberg_scan()` | メタデータ JSON パス指定 |
| スナップショット一覧 | `iceberg_snapshots()` | ファイルパスまたはテーブル参照 |
| データファイル確認 | `iceberg_metadata()` | マニフェスト・Parquet ファイル一覧 |
| タイムトラベル（ID） | `snapshot_from_id=` | iceberg_scan のパラメータ |
| タイムトラベル（時刻） | `snapshot_from_timestamp=` | iceberg_scan のパラメータ |
| テーブル作成 | `CREATE TABLE` | REST カタログ経由、v1.4.0 以降 |
| データ挿入 | `INSERT INTO` | REST カタログ経由、v1.4.0 以降 |
| 更新 | `UPDATE` | REST カタログ経由、v1.4.2 以降 |
| 削除 | `DELETE` | REST カタログ経由、v1.4.2 以降 |

読み取りはメタデータ JSON への直接パス指定で REST カタログなしに使える。書き込みには REST カタログへの接続が必要になる。AWS の場合は [Amazon S3 Tables](https://aws.amazon.com/s3/features/tables/) や [Amazon SageMaker Lakehouse](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/lakehouse.html) が Iceberg REST カタログとして利用できる。

## 参考資料

{{< linkcard "https://duckdb.org/docs/stable/core_extensions/iceberg/overview" >}}

{{< linkcard "https://duckdb.org/2025/11/28/iceberg-writes-in-duckdb" >}}

{{< linkcard "https://duckdb.org/docs/stable/core_extensions/iceberg/iceberg_rest_catalogs" >}}
