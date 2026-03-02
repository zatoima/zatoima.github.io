---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "DuckDB とは何か"
subtitle: ""
summary: "DuckDB は OLAP に特化した組み込み型のオープンソースデータベース。サーバー不要で pip install だけで動作し、CSV・Parquet・JSON を直接 SQL でクエリできる。列指向ストレージにより Pandas より高速で Spark より軽量な分析環境を単一マシンで実現する。"
tags: ["DuckDB", "OLAP", "データ分析"]
categories: ["DuckDB", "データ分析"]
url: what-is-duckdb
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

[DuckDB](https://duckdb.org/) は、分析クエリ（OLAP）に特化した組み込み型のオープンソースデータベース。サーバーを立てる必要がなく、`pip install duckdb` の一行で使い始められる。2019年にオランダのCWI（数学・情報科学研究所）で生まれ、2025年時点で最も注目されているOSSデータベースの一つとなった。

## DuckDB の概要と位置づけ

DuckDB を一言で表すなら「**SQLite のOLAP版**」。SQLite と同様にサーバーレスで単一ファイルで動くが、得意とする操作が根本的に異なる。

| 項目 | SQLite | DuckDB |
|------|--------|--------|
| 主な用途 | アプリ組み込みDB（OLTP） | データ分析（OLAP） |
| ストレージ形式 | 行指向 | 列指向 |
| 得意な操作 | 点クエリ・行の追加/更新 | 大量行の集計・フィルタ・JOIN |
| 読み込み速度（集計） | 遅い | 非常に速い |
| 対応形式 | SQLite独自形式 | CSV, Parquet, JSON, Arrow |
| 多言語対応 | 多数 | Python, R, Go, Java, Rust など |

## OLTP vs OLAP — なぜ別物なのか

データベースの処理パターンは大きく2種類に分かれる。

```
OLTP（Online Transaction Processing）
  → 1行を素早く追加・更新・検索する
  → 例: ECサイトの注文処理、銀行振込
  → 行指向ストレージが得意

OLAP（Online Analytical Processing）
  → 大量の行をまとめて集計・分析する
  → 例: 売上の月次集計、ユーザー行動分析
  → 列指向ストレージが得意
```

DuckDB は後者のOLAP向けに設計されている。1億行のデータから特定の列だけを高速に読み出し、集計するような処理が得意となる。

## なぜ今 DuckDB が注目されるのか

### Pandas の限界

Python のデータ分析といえば Pandas だが、大きなデータになると限界が見えてくる。

- **メモリ制限**: データ全体をメモリに載せる必要がある
- **処理速度**: 列単位の最適化がない、シングルスレッド中心
- **複雑なSQL**: GroupBy + JOIN の組み合わせが書きづらい

DuckDB はこれらを解決する。ディスク上のParquetやCSVを直接クエリでき、メモリに収まらない大規模データも out-of-core 処理で扱える。

### Spark の重さ

ビッグデータといえば Apache Spark だが、単一マシンで使うには重すぎる場面が多い。

- クラスタのセットアップが必要
- JVM のオーバーヘッド
- 起動が遅い

DuckDB は `pip install` だけで動き、単一マシンでも Spark に匹敵する分析速度を出せる。

## 主なユースケース

| ユースケース | 具体例 |
|------------|--------|
| ローカルデータ探索 | Jupyter Notebook で CSV/Parquet をインタラクティブに探索 |
| ETLパイプライン | データ変換・クレンジングの中間処理 |
| BI・レポート | dbt + DuckDB でローカル完結のデータ変換 |
| クラウドストレージ分析 | S3/GCS のファイルをダウンロードせずに直接クエリ |
| 組み込み分析 | アプリケーションにSQLエンジンを埋め込む |
| AI/ML前処理 | ベクトルDB用データの変換・集計 |

## 動作確認

インストールと基本的な動作確認の手順を示す。

**インストール**

```bash
pip install duckdb
```

追加の依存関係は不要で、これだけで完結する。インストール直後からSQLを実行できる。

```bash
$ python3 -c "
import duckdb
result = duckdb.sql('SELECT 42 AS answer, version() AS duckdb_version').fetchdf()
print(result)
"
```

**実行結果:**

```
   answer duckdb_version
0      42         v1.4.4
```

CLI版も同様に動作する。

```bash
$ duckdb --version
v1.4.4 (Andium) 6ddac802ff

$ duckdb -c "SELECT 'Hello, DuckDB!' AS greeting;"
┌────────────────┐
│    greeting    │
│    varchar     │
├────────────────┤
│ Hello, DuckDB! │
└────────────────┘
```

サーバーを起動せず、コマンド一発でSQLが実行できる。

## DuckDB エコシステム

DuckDB 単体にとどまらず、周辺ツールとの連携が充実している。

```
DuckDB
  ├── 入力
  │     ├── CSV / TSV（read_csv_auto）
  │     ├── Parquet（read_parquet）
  │     ├── JSON（read_json_auto）
  │     ├── S3 / GCS / Azure Blob（httpfs 拡張）
  │     └── Apache Iceberg（iceberg 拡張）
  ├── 出力
  │     ├── Pandas DataFrame
  │     ├── Polars DataFrame
  │     └── Apache Arrow
  └── 連携ツール
        ├── dbt（dbt-duckdb アダプタ）
        ├── MotherDuck（クラウド版）
        └── DuckDB-WASM（ブラウザ版）
```

## まとめ

DuckDB を使う理由は明快。

- サーバー不要、`pip install` だけで始められる
- CSV / Parquet / JSON を直接SQLでクエリできる
- Pandas より高速、Spark より軽量
- 無料環境でも十分に動く

次の記事では、インストールから基本操作まで CLI と Python API を使って実際に手を動かす。

## 参考資料

{{< linkcard "https://duckdb.org/why_duckdb" >}}

{{< linkcard "https://duckdb.org/docs/stable/" >}}
