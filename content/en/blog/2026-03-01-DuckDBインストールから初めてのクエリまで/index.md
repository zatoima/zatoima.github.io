---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Getting Started with DuckDB Installation"
subtitle: ""
summary: "A guide to installing DuckDB v1.4.4 from scratch using both the CLI and Python API. Covers pip/curl installation, dot commands, in-memory vs file DB switching, direct CSV querying, and fetchdf/pl retrieval methods."
tags: ["DuckDB", "Installation", "SQL", "Python"]
categories: ["DuckDB", "Data Analysis"]
url: duckdb-install-quickstart
date: 2026-03-01
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

## Introduction

A guide to getting started with [DuckDB](https://duckdb.org/) from scratch. Using both the CLI and Python API, we'll walk through installation, basic operations, and CSV file analysis. All execution results shown in this article are actual outputs.

## Installation

### Python Package (Easiest Method)

```bash
pip install duckdb
```

No additional dependencies are needed — this is all it takes. After installation, you can immediately execute SQL from Python.

### CLI Binary

You can also download the binary directly from the official releases.

```bash
# Linux (x86_64)
curl -L https://github.com/duckdb/duckdb/releases/latest/download/duckdb_cli-linux-amd64.zip -o duckdb.zip
unzip duckdb.zip

# Linux (ARM64)
curl -L https://github.com/duckdb/duckdb/releases/latest/download/duckdb_cli-linux-arm64.zip -o duckdb.zip
unzip duckdb.zip && chmod +x duckdb && sudo mv duckdb /usr/local/bin/

# macOS (Homebrew)
brew install duckdb
```

Version check:

```bash
$ duckdb --version
v1.4.4 (Andium) 6ddac802ff
```

## CLI Basic Operations

The DuckDB CLI operates in REPL mode.

```bash
$ duckdb              # In-memory mode
$ duckdb mydb.duckdb  # File DB mode (persistent)
```

After startup, a `D` prompt appears where you can directly enter SQL.

```sql
D SELECT 'Hello, DuckDB!' AS greeting;
┌────────────────┐
│    greeting    │
│    varchar     │
├────────────────┤
│ Hello, DuckDB! │
└────────────────┘

D SELECT current_date AS today, version() AS ver;
┌────────────┬─────────┐
│   today    │   ver   │
│    date    │ varchar │
├────────────┼─────────┤
│ 2026-03-01 │ v1.4.4  │
└────────────┴─────────┘
```

You can also execute one-liners using the `-c` option.

```bash
$ duckdb -c "SELECT 'Hello, DuckDB!' AS greeting;"
```

### Useful Dot Commands

| Command | Description |
|---------|-------------|
| `.help` | Show help |
| `.tables` | List tables |
| `.schema table_name` | Show schema |
| `.mode markdown` | Switch output to Markdown table format |
| `.timer on` | Display query execution time |
| `.output file.csv` | Write results to a file |
| `.quit` | Exit |

## In-Memory DB vs File DB

DuckDB operates in two modes.

```
In-memory mode: duckdb
  → Data is lost when the process exits
  → Suitable for temporary analysis and experiments

File mode: duckdb mydb.duckdb
  → Data is persisted in a .duckdb file
  → Can be used as a reusable database
```

Here's an example of working with a file DB.

```bash
$ duckdb /tmp/demo.duckdb -c "
CREATE TABLE IF NOT EXISTS events (id INTEGER, ts TIMESTAMP, value DOUBLE);
INSERT INTO events VALUES (1, NOW(), 3.14), (2, NOW(), 2.71);
SELECT * FROM events;
"
```

**Output:**

```
┌───────┬────────────────────────────┬────────┐
│  id   │             ts             │ value  │
│ int32 │         timestamp          │ double │
├───────┼────────────────────────────┼────────┤
│     1 │ 2026-03-01 23:06:08.892993 │   3.14 │
│     2 │ 2026-03-01 23:06:08.892993 │   2.71 │
└───────┴────────────────────────────┴────────┘
```

## Basic Table Operations

```sql
-- Create a table
CREATE TABLE users (id INTEGER, name VARCHAR, score DOUBLE);

-- Insert multiple rows at once
INSERT INTO users VALUES
    (1, 'Alice',   95.5),
    (2, 'Bob',     87.0),
    (3, 'Charlie', 92.3);

-- Retrieve sorted results
SELECT * FROM users ORDER BY score DESC;
```

**Output:**

```
┌───────┬─────────┬────────┐
│  id   │  name   │ score  │
│ int32 │ varchar │ double │
├───────┼─────────┼────────┤
│     1 │ Alice   │   95.5 │
│     3 │ Charlie │   92.3 │
│     2 │ Bob     │   87.0 │
└───────┴─────────┴────────┘
```

Aggregation queries are also intuitive to write.

```sql
SELECT AVG(score) AS avg_score FROM users;
-- 91.6
```

## Reading CSV Files

One of DuckDB's biggest strengths is the ability to query CSV files directly. `read_csv_auto` automatically infers headers and types.

```sql
-- Query directly without importing as a table
SELECT * FROM read_csv_auto('sales.csv');
```

The following sales.csv (8 rows) was aggregated by category.

```
date,category,amount
2024-01-15,Electronics,12500
2024-01-22,Books,3200
...
```

```sql
SELECT
    category,
    COUNT(*)            AS count,
    SUM(amount)         AS total,
    AVG(amount)::INTEGER AS avg
FROM read_csv_auto('sales.csv')
GROUP BY category
ORDER BY total DESC;
```

**Output:**

```
┌─────────────┬───────┬────────┬───────┐
│  category   │ count │ total  │  avg  │
│   varchar   │ int64 │ int128 │ int32 │
├─────────────┼───────┼────────┼───────┤
│ Electronics │     3 │  37200 │ 12400 │
│ Books       │     3 │  12000 │  4000 │
│ Food        │     2 │   7800 │  3900 │
└─────────────┴───────┴────────┴───────┘
```

Parquet files can be read the same way using `read_parquet('file.parquet')`. You can also query multiple files at once using glob patterns like `read_parquet('data/*.parquet')`.

## Python API

When using DuckDB from Python, create an instance with `duckdb.connect()`.

```python
import duckdb

# In-memory connection
con = duckdb.connect()

# File DB connection
con = duckdb.connect("mydb.duckdb")
```

Here's an example of creating a table, running a query, and receiving the result as a Pandas DataFrame.

```python
import duckdb

con = duckdb.connect()
con.execute("""
    CREATE TABLE products AS
    SELECT * FROM (VALUES
        ('Apple',   'Fruit',     150),
        ('Banana',  'Fruit',      80),
        ('Carrot',  'Vegetable',  90),
        ('Broccoli','Vegetable', 120),
        ('Orange',  'Fruit',     200)
    ) t(name, category, price)
""")

df = con.execute(
    "SELECT category, AVG(price) AS avg_price, COUNT(*) AS cnt FROM products GROUP BY category"
).fetchdf()
print(df)
```

**Output:**

```
    category   avg_price  cnt
0  Vegetable  105.000000    2
1      Fruit  143.333333    3
```

Other retrieval methods besides `.fetchdf()` are also available.

| Method | Return Type |
|--------|-------------|
| `.fetchdf()` | Pandas DataFrame |
| `.fetchone()` | Tuple (single row) |
| `.fetchall()` | List of tuples |
| `.fetch_arrow_table()` | Apache Arrow Table |
| `.pl()` | Polars DataFrame |

### Shortcut: `duckdb.sql()`

You can execute queries directly without creating an instance.

```python
import duckdb

result = duckdb.sql("SELECT 42 AS answer, version() AS ver").fetchdf()
print(result)
# =>    answer     ver
# => 0      42  v1.4.4
```

## Summary

| Operation | Command |
|-----------|---------|
| pip install | `pip install duckdb` |
| Launch CLI (in-memory) | `duckdb` |
| Launch CLI (file DB) | `duckdb mydb.duckdb` |
| Python connection | `duckdb.connect()` |
| Direct CSV query | `SELECT * FROM read_csv_auto('file.csv')` |
| Get DataFrame | `con.execute("...").fetchdf()` |

DuckDB lets you start practical data analysis within 5 minutes of installation. In the next article, we'll dive into the internal architecture and explain why it's so fast.

## References

{{< linkcard "https://duckdb.org/docs/installation/" >}}

{{< linkcard "https://duckdb.org/docs/guides/" >}}

{{< linkcard "https://duckdb.org/docs/api/python/overview" >}}