---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "SnowCLIを使用したデータのアンロード/アップロード"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: snowflake-snowcli-data-unload-upload
date: 2024-05-02
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

## 前提条件

1. CLIツールのインストール：

   - SnowSQLのインストール
   - SnowCLIのインストール
2. サンプルデータベースの有効化

   - サンプルデータベースの使用

     - https://docs.snowflake.com/ja/user-guide/sample-data-using

## 手順

### 作業用ディレクトリを削除し、再作成

```sql
#rm -rf ~/work/temp/upload
mkdir -p ~/work/temp/upload
```

### SnowSQLを使用して新しいデータベースを作成

```sql
snow sql -q 'create or replace database sandbox';
```

### 新しいステージを作成

```sql
snow object stage create sandbox.public.my_stage;
```

### 指定されたフォーマットでデータをステージにアンロード

```sql
snow sql -q 'copy into @sandbox.public.my_stage/data.csv from (select * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM limit 1000) file_format = (format_name = CSV_FORMAT compression = NONE) SINGLE=TRUE HEADER=TRUE OVERWRITE = TRUE';
```

### ステージ内のファイルリストを表示

```sql
snow object stage list @sandbox.public.my_stage
```

### ステージからローカルのディレクトリにファイルをコピー

```sql
cd ~/work/temp/upload
snow object stage copy @sandbox.public.my_stage .
```

### ローカルからステージへファイルをアップロード（SnowCLIを使用）

```sql
snow object stage copy data.csv @sandbox.public.my_stage
```

### ローカルファイルをステージにアップロード（SnowSQLを使用）

※ログインは省略

```sql
use database sandbox;
put file://~/work/temp/upload/* @my_stage;
```

## 参照

> [Snowflake CLI \| Snowflake Documentation](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/index)
>
> [snowflakedb/snowflake\-cli: Snowflake CLI is an open\-source command\-line tool explicitly designed for developer\-centric workloads in addition to SQL operations\.](https://github.com/snowflakedb/snowflake-cli)
