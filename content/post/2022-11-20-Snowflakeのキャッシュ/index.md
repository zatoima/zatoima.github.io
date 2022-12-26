---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflakeのキャッシュ"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-cached-memo
date: 2022-09-30
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

| #    | キャッシュ名         | キャッシュ対象                           | 使用可能なユーザー                             | 保存レイヤー        | 有効期間             |
| ---- | -------------------- | ---------------------------------------- | ---------------------------------------------- | ------------------- | -------------------- |
| 1    | 結果キャッシュ       | クエリの結果                             | クエリが実行された同じロールのすべてのユーザー | Snowflake           | 24時間               |
| 2    | メタデータキャッシュ | テーブルに関する情報                     | すべてのユーザー                               | Snowflake           | 常に                 |
| 3    | データキャッシュ     | クエリ結果のファイルヘッダとカラムデータ | 同じ仮想ウェアハウスを実行したユーザー         | ウェアハウス（SSD） | ウェアハウスの稼働中 |

コンパイルキャッシュは存在せず常にコンパイルが必要

### キャッシュを使用しないようにするためには？？

- 結果キャッシュ
  - `USE_CACHED_RESULT`を`FALSE`に
- メタデータキャッシュ
  - 方法無し
- データキャッシュ
  - ウェアハウスのSUSPENDなど
    - [Snowflakeのデータキャッシュの無効化 \| my opinion is my own](https://zatoima.github.io/snowflake-data-cache-disabled/)

### 注意事項

#### 結果キャッシュ

> https://docs.snowflake.com/ja/user-guide/querying-persisted-results.html#retrieval-optimization
>
> 通常、次の条件の **すべて** が満たされる場合、クエリ結果が再利用されます。
>
> - 新しいクエリは、以前に実行したクエリと構文的に一致する。
> - クエリには、実行時に評価する必要のある関数が含まれていない（例: [CURRENT_TIMESTAMP()](https://docs.snowflake.com/ja/sql-reference/functions/current_timestamp.html) および [UUID_STRING()](https://docs.snowflake.com/ja/sql-reference/functions/uuid_string.html)）。 [CURRENT_DATE()](https://docs.snowflake.com/ja/sql-reference/functions/current_date.html) 関数はこのルールの例外です。CURRENT_DATE() は実行時に評価されますが、 CURRENT_DATE() を使用するクエリは、クエリ再利用機能を引き続き使用できます。
> - クエリには、 [ユーザー定義関数（UDFs）](https://docs.snowflake.com/ja/sql-reference/udf-overview.html) または [外部関数](https://docs.snowflake.com/ja/sql-reference/external-functions.html) が含まれていない。
> - クエリ結果に寄与するテーブルデータが変更されていない。
> - 以前のクエリの永続化された結果が引き続き利用可能である。
> - キャッシュされた結果にアクセスするロールには、必要な権限がある。
>   - クエリが SELECT クエリの場合、クエリを実行するロールには、キャッシュされたクエリで使用されるすべてのテーブルに必要なアクセス権限が必要です。
>   - クエリが SHOW クエリの場合、クエリを実行するロールは、キャッシュされた結果を生成したロールと一致する必要があります。
> - 結果の生成方法に影響する構成オプションが変更されていない。
> - テーブル内にある他のデータ変更によって、テーブルのマイクロパーティションが変更されていない（例: 再クラスタ化または統合化）。

> これらの条件をすべて満たしても、Snowflakeがクエリ結果を再利用することは **保証されません**。

### 参照

- [Snowflakeの３つのキャッシュ](https://zenn.dev/aaizawa/articles/2b06dd50d56438)

- [保存済みのクエリ結果の使用 — Snowflake Documentation](https://docs.snowflake.com/ja/user-guide/querying-persisted-results.html)
