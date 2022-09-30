---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflakeで名字と名前を抽出する(POSITION関数)"
subtitle: ""
summary: " "
tags: ["Snowflake","SQL"]
categories: ["Snowflake","SQL"]
url: snowflake-extract-name-position-function
date: 2022-09-29
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

### 名前の名字と名前を抽出する（スペース区切りの場合）

対象データ

```sql
imazaj#XSMALL@SQLDB.PUBLIC>select name from CUSTOMERS limit 5;
+-------------+
| NAME        |
|-------------|
| 石塚 拓     |
| 長坂 賢介   |
| 野中 裕之   |
| 髙松 龍     |
| 小倉 慎太郎 |
+-------------+
```

Position関数を使う。PostgreSQLの場合の*STRPOS*、Oracleの場合のINSTR。

[POSITION — Snowflake Documentation](https://docs.snowflake.com/ja/sql-reference/functions/position.html#position)

> ```
> POSITION( <expr1>, <expr2> [ , <start_pos> ] )
> 
> POSITION( <expr1> IN <expr2> )
> 
> 引数
> 必須：
> 
> expr1
> 検索する値を表す文字列またはバイナリ式。
> 
> expr2
> 検索する値を表す文字列またはバイナリ式。
> 
> オプション:
> 
> start_pos
> 検索を開始する位置を示す番号です（1 は expr2 の開始を表します）。
> 
> デフォルト： 1
> ```

```sql
select
  name,
  SUBSTR(name, 1, POSITION(' ', name) -1) as lastname,
  SUBSTR(name, POSITION(' ', name)) as firstname
from
  customers
limit 5;
```

```sql
imazaj#XSMALL@SQLDB.PUBLIC>select
                             name,
                             SUBSTR(name, 1, POSITION(' ', name) -1) as lastname,
                             SUBSTR(name, POSITION(' ', name)) as firstname
                           from
                             customers
                           limit 5;
+-------------+----------+-----------+
| NAME        | LASTNAME | FIRSTNAME |
|-------------+----------+-----------|
| 石塚 拓     | 石塚     |  拓       |
| 長坂 賢介   | 長坂     |  賢介     |
| 野中 裕之   | 野中     |  裕之     |
| 髙松 龍     | 髙松     |  龍       |
| 小倉 慎太郎 | 小倉     |  慎太郎   |
+-------------+----------+-----------+
5 Row(s) produced. Time Elapsed: 0.974s
```

