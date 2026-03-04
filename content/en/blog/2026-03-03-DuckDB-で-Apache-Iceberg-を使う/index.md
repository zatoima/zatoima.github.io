---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Using Apache Iceberg with DuckDB"
subtitle: ""
summary: "A hands-on verification of the DuckDB v1.4.4 Iceberg extension, covering table reading with iceberg_scan, metadata inspection with iceberg_snapshots and iceberg_metadata, time travel, and CREATE TABLE, INSERT, UPDATE, and DELETE operations via a REST catalog."
tags: ["DuckDB", "Iceberg", "Data Lake", "Analytics Platform"]
categories: ["Data Platform"]
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

## Introduction

[Apache Iceberg](https://iceberg.apache.org/) is an open table format designed for large-scale analytical workloads, providing features such as schema management, time travel, and partition management.

DuckDB added write support for Iceberg tables via its Iceberg extension starting with v1.4.0, and extended support to UPDATE and DELETE operations in v1.4.2. This means DuckDB alone can now handle the entire lifecycle of Iceberg tables.

In this article, I use DuckDB v1.4.4 to verify the following:

- Reading tables with `iceberg_scan()`
- Inspecting metadata with `iceberg_snapshots()` / `iceberg_metadata()`
- Time travel using `snapshot_from_id` / `snapshot_from_timestamp`
- CREATE TABLE / INSERT / UPDATE / DELETE via a REST catalog

For official documentation, see [Iceberg Extension – DuckDB](https://duckdb.org/docs/stable/core_extensions/iceberg/overview).

## Setting Up the Iceberg Extension

```sql
INSTALL iceberg;
LOAD iceberg;
```

The extension is automatically downloaded on first run. If already installed, `LOAD iceberg;` is all you need.

The available functions are as follows:

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

## Reading Tables with iceberg_scan

For test data, I created a local Iceberg table using PyIceberg and inserted fruit pricing data in two batches.

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

In DuckDB, you read the table by specifying the path to the metadata JSON file.

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

Standard SQL syntax works as-is.

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

## Inspecting Snapshots and Metadata

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

Two snapshots were recorded, corresponding to the two `append()` calls.

### iceberg_metadata()

This function lets you inspect details at the data file level.

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

The Parquet files corresponding to each snapshot are registered with an ADDED status. This reveals Iceberg's internal structure: a hierarchy of snapshots, manifests, and data files.

```text
Iceberg Table
└── metadata/
    ├── 00000-....metadata.json   ← Table definition
    ├── 00001-....metadata.json   ← Snapshot 1
    ├── 00002-....metadata.json   ← Snapshot 2 (latest)
    ├── snap-xxxx.avro            ← Manifest list
    └── xxxx-m0.avro              ← Manifest (data file listing)
data/
    ├── 00000-0-xxxx.parquet      ← Batch 1 (5 rows)
    └── 00000-0-yyyy.parquet      ← Batch 2 (3 rows)
```

## Time Travel

### Specifying a Snapshot with snapshot_from_id

```sql
-- Snapshot 1 (5 rows)
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

While the latest snapshot contains 8 rows, this query retrieved the 5 rows from the state at snapshot 1.

### Specifying a Timestamp with snapshot_from_timestamp

```sql
-- Specify a point in time before the second INSERT
SELECT * FROM iceberg_scan(
    '/tmp/iceberg_test/warehouse/default/products/metadata/00002-...metadata.json',
    snapshot_from_timestamp='2026-03-02 07:09:33.530'
)
ORDER BY id;
```

You can time travel by specifying a timestamp without needing to look up the snapshot ID. The most recent snapshot at or before the specified timestamp is used.

## Connecting to a REST Catalog and Write Operations

Write operations require an Iceberg REST catalog. Here, I used [tabulario/iceberg-rest](https://github.com/databricks/iceberg-rest-image) running locally for verification.

```bash
docker run -d --name iceberg-rest \
  -p 8181:8181 \
  -v /tmp/iceberg_warehouse:/tmp/iceberg_warehouse \
  -e CATALOG_WAREHOUSE=/tmp/iceberg_warehouse \
  tabulario/iceberg-rest:latest
```

To connect from DuckDB, specify `TYPE ICEBERG` and `ENDPOINT` in the `ATTACH` statement.

```sql
LOAD iceberg;

ATTACH '' AS iceberg_rest (
    TYPE ICEBERG,
    ENDPOINT 'http://localhost:8181',
    AUTHORIZATION_TYPE NONE
);
```

Once connected, you can operate on tables using standard DuckDB SQL syntax.

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

### UPDATE / DELETE (v1.4.2 and later)

```sql
-- Update the price
UPDATE iceberg_rest.demo.sales SET amount = 2600.00 WHERE order_id = 1;

-- Delete by region
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

The two rows in the West region were deleted, and the Laptop's amount was updated from 2400.0 to 2600.0.

{{< callout "info" >}}
UPDATE and DELETE are only supported on non-partitioned, non-sorted tables. Running these operations on a partitioned table will result in an error.
{{< /callout >}}

### Checking Snapshots After Operations

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

Three snapshots were recorded, corresponding to the INSERT, UPDATE, and DELETE operations. Using `snapshot_from_id`, you can revert to the state before any of these operations.

```sql
-- State right after INSERT (5 rows, amount=2400)
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

## Summary

Here is a summary of the Iceberg extension capabilities verified with DuckDB v1.4.4.

| Operation | Function / Syntax | Notes |
|-----------|------------------|-------|
| Read | `iceberg_scan()` | Specify metadata JSON path |
| Snapshot listing | `iceberg_snapshots()` | File path or table reference |
| Data file inspection | `iceberg_metadata()` | Manifest and Parquet file listing |
| Time travel (by ID) | `snapshot_from_id=` | Parameter of iceberg_scan |
| Time travel (by time) | `snapshot_from_timestamp=` | Parameter of iceberg_scan |
| Create table | `CREATE TABLE` | Via REST catalog, v1.4.0+ |
| Insert data | `INSERT INTO` | Via REST catalog, v1.4.0+ |
| Update | `UPDATE` | Via REST catalog, v1.4.2+ |
| Delete | `DELETE` | Via REST catalog, v1.4.2+ |

Read operations work without a REST catalog by specifying a direct path to the metadata JSON. Write operations require a connection to a REST catalog. On AWS, [Amazon S3 Tables](https://aws.amazon.com/s3/features/tables/) and [Amazon SageMaker Lakehouse](https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/lakehouse.html) can be used as Iceberg REST catalogs.

## References

{{< linkcard "https://duckdb.org/docs/stable/core_extensions/iceberg/overview" >}}

{{< linkcard "https://duckdb.org/2025/11/28/iceberg-writes-in-duckdb" >}}

{{< linkcard "https://duckdb.org/docs/stable/core_extensions/iceberg/iceberg_rest_catalogs" >}}