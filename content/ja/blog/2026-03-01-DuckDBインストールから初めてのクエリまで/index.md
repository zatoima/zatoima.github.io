---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "DuckDB インストール入門"
subtitle: ""
summary: "DuckDB v1.4.4 を CLI と Python API の両面からゼロから導入するガイド。pip / curl インストール、ドットコマンド、インメモリ・ファイルDB切り替え、CSV直接クエリ、fetchdf / pl 取得メソッドまでをカバーする。"
tags: ["DuckDB", "インストール", "SQL", "Python"]
categories: ["DuckDB", "データ分析"]
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

## はじめに

[DuckDB](https://duckdb.org/) をゼロから使い始めるためのガイド。CLI と Python API の両方を使って、インストール・基本操作・CSV ファイルの分析までを一通り体験する。記事中の実行結果はすべて実際の出力を掲載している。

## インストール

### Python パッケージ（最も簡単）

```bash
pip install duckdb
```

追加の依存関係は不要で、これだけで完結する。インストール後すぐにPythonからSQLを実行できる。

### CLI バイナリ

公式からバイナリを直接ダウンロードする方法もある。

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

バージョン確認:

```bash
$ duckdb --version
v1.4.4 (Andium) 6ddac802ff
```

## CLI 基本操作

DuckDB CLI は REPL 形式で動作する。

```bash
$ duckdb              # インメモリモード
$ duckdb mydb.duckdb  # ファイルDBモード（永続化）
```

起動後は `D` プロンプトが表示され、SQL を直接入力できる。

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

`-c` オプションを使えばワンライナーでも実行できる。

```bash
$ duckdb -c "SELECT 'Hello, DuckDB!' AS greeting;"
```

### 便利なドットコマンド

| コマンド | 説明 |
|---------|------|
| `.help` | ヘルプ一覧 |
| `.tables` | テーブル一覧 |
| `.schema テーブル名` | スキーマ確認 |
| `.mode markdown` | 出力を Markdown 表形式に変更 |
| `.timer on` | クエリ実行時間を表示 |
| `.output file.csv` | 結果をファイルに書き出す |
| `.quit` | 終了 |

## インメモリ DB vs ファイル DB

DuckDB は2つのモードで動作する。

```
インメモリモード: duckdb
  → プロセス終了でデータが消える
  → 一時的な分析・実験向け

ファイルモード: duckdb mydb.duckdb
  → .duckdb ファイルにデータが永続化される
  → 繰り返し使うDBとして利用可能
```

実際にファイルDBで操作してみた。

```bash
$ duckdb /tmp/demo.duckdb -c "
CREATE TABLE IF NOT EXISTS events (id INTEGER, ts TIMESTAMP, value DOUBLE);
INSERT INTO events VALUES (1, NOW(), 3.14), (2, NOW(), 2.71);
SELECT * FROM events;
"
```

**実行結果:**

```
┌───────┬────────────────────────────┬────────┐
│  id   │             ts             │ value  │
│ int32 │         timestamp          │ double │
├───────┼────────────────────────────┼────────┤
│     1 │ 2026-03-01 23:06:08.892993 │   3.14 │
│     2 │ 2026-03-01 23:06:08.892993 │   2.71 │
└───────┴────────────────────────────┴────────┘
```

## テーブル操作の基本

```sql
-- テーブル作成
CREATE TABLE users (id INTEGER, name VARCHAR, score DOUBLE);

-- データ挿入（複数行を一括）
INSERT INTO users VALUES
    (1, 'Alice',   95.5),
    (2, 'Bob',     87.0),
    (3, 'Charlie', 92.3);

-- 並び替えて取得
SELECT * FROM users ORDER BY score DESC;
```

**実行結果:**

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

集計も直感的に書ける。

```sql
SELECT AVG(score) AS avg_score FROM users;
-- 91.6
```

## CSV ファイルの読み込み

DuckDB の大きな強みの一つが、CSV をそのままクエリできること。`read_csv_auto` はヘッダーと型を自動推論する。

```sql
-- テーブルとしてインポートせずに直接クエリ
SELECT * FROM read_csv_auto('sales.csv');
```

以下の sales.csv（8行）をカテゴリ別に集計した。

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

**実行結果:**

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

Parquet も同様に `read_parquet('file.parquet')` で直接読める。グロブパターン `read_parquet('data/*.parquet')` で複数ファイルをまとめてクエリすることもできる。

## Python API

Python から使う場合は `duckdb.connect()` でインスタンスを作成する。

```python
import duckdb

# インメモリ接続
con = duckdb.connect()

# ファイルDB接続
con = duckdb.connect("mydb.duckdb")
```

テーブルを作成してクエリし、Pandas DataFrame として受け取る例。

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

**実行結果:**

```
    category   avg_price  cnt
0  Vegetable  105.000000    2
1      Fruit  143.333333    3
```

`.fetchdf()` 以外の取得メソッドも使える。

| メソッド | 戻り値 |
|---------|--------|
| `.fetchdf()` | Pandas DataFrame |
| `.fetchone()` | タプル（1行） |
| `.fetchall()` | タプルのリスト |
| `.fetch_arrow_table()` | Apache Arrow Table |
| `.pl()` | Polars DataFrame |

### ショートカット: `duckdb.sql()`

インスタンスを作らずに直接クエリを実行できる。

```python
import duckdb

result = duckdb.sql("SELECT 42 AS answer, version() AS ver").fetchdf()
print(result)
# =>    answer     ver
# => 0      42  v1.4.4
```

## まとめ

| 操作 | コマンド |
|------|---------|
| pip インストール | `pip install duckdb` |
| CLI 起動（インメモリ） | `duckdb` |
| CLI 起動（ファイルDB） | `duckdb mydb.duckdb` |
| Python 接続 | `duckdb.connect()` |
| CSV 直接クエリ | `SELECT * FROM read_csv_auto('file.csv')` |
| DataFrame 取得 | `con.execute("...").fetchdf()` |

DuckDB はインストールから5分で実用的なデータ分析が始められる。次の記事ではアーキテクチャの内部構造を掘り下げ、なぜ速いのかを解説する。

## 参考資料

{{< linkcard "https://duckdb.org/docs/installation/" >}}

{{< linkcard "https://duckdb.org/docs/guides/" >}}

{{< linkcard "https://duckdb.org/docs/api/python/overview" >}}
