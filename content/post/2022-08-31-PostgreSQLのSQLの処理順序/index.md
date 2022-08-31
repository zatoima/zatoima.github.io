---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLのSQLの処理順序"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-sql-process-order
date: 2022-08-31
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

### 処理順序

1. WITH内のSELECT
2. FROM
3. WHERE
4. GROUP BY
5. HAVING
6. SELECT
   - 列に対する関数やDISTINTなど
7. UNION、INTERSECT、EXCEPT
8. ORDER BY
9. LIMIT

### マニュアル

> SELECT https://www.postgresql.jp/document/14/html/sql-select.html
>
> `SELECT`は0個以上のテーブルから行を返します。 `SELECT`の一般的な処理は以下の通りです。
>
> 1. `WITH`リスト内のすべての問い合わせが計算されます。 これらは実質的には、`FROM`リスト内から参照可能な一時テーブルとして提供されます。 `NOT MATERIALIZED`が指定された場合を除き、`FROM`内で2回以上参照される`WITH`問い合わせは一度のみ計算されます。 （後述の[WITH Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-WITH)を参照してください。）
> 2. `FROM`リストにある全要素が計算されます （`FROM`リストの要素は実テーブルか仮想テーブルのいずれかです）。 `FROM`リストに複数の要素が指定された場合、それらはクロス結合されます （後述の[FROM Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-FROM)を参照してください）。
> 3. `WHERE`句が指定された場合、条件を満たさない行は全て出力から取り除かれます （後述の[WHERE Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-WHERE)を参照してください）。
> 4. `GROUP BY`句が指定された場合、および集約関数の呼び出しがある場合は、1つまたは複数の値が条件に合う行ごとにグループに組み合わせて出力され、また集約関数の結果が計算されます。 `HAVING`句が指定された場合、指定した条件を満たさないグループは取り除かれます （後述の[GROUP BY Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-GROUPBY)と[HAVING Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-HAVING)を参照してください）。
> 5. 実際には、選択された各行または行グループに対して、`SELECT`の出力式を使用して計算した結果の行が出力されます （後述の[SELECT List](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-SELECT-LIST)を参照してください）。
> 6. `SELECT DISTINCT`は結果から重複行を取り除きます。 `SELECT DISTINCT ON`は指定した全ての式に一致する行を取り除きます。 `SELECT ALL`では、重複行も含め、全ての候補行を返します（これがデフォルトです。 詳しくは、後述の[DISTINCT Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-DISTINCT)を参照してください）。
> 7. `UNION`、`INTERSECT`、`EXCEPT`演算子を使用すると、複数の`SELECT`文の出力を1つの結果集合にまとめることができます。 `UNION`演算子は、両方の結果集合に存在する行と、片方の結果集合に存在する行を全て返します。 `INTERSECT`演算子は、両方の結果集合に存在する行を返します。 `EXCEPT`演算子は、最初の結果集合にあり、2番目の結果集合にない行を返します。 `ALL`が指定されない限り、いずれの場合も、重複する行は取り除かれます。 無意味な`DISTINCT`という単語を付けて、明示的に重複行を除去することを指定することができます。 `SELECT`自体は`ALL`がデフォルトですが、この場合は`DISTINCT`がデフォルトの動作であることに注意してください。 （後述の[UNION Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-UNION)、[INTERSECT Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-INTERSECT)、[EXCEPT Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-EXCEPT)を参照してください。）
> 8. `ORDER BY`句が指定された場合、返される行は指定した順番でソートされます。 `ORDER BY`が指定されない場合は、システムが計算過程で見つけた順番で行が返されます （後述の[ORDER BY Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-ORDERBY)を参照してください）。
> 9. `LIMIT`（または`FETCH FIRST`）あるいは`OFFSET`句が指定された場合、`SELECT`文は結果行の一部分のみを返します （詳しくは、後述の[LIMIT Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-LIMIT)を参照してください）。
> 10. `FOR UPDATE`、`FOR NO KEY UPDATE`、`FOR SHARE`または`FOR KEY SHARE`句を指定すると、`SELECT`文は引き続き行われる更新に備えて選択行をロックします （詳しくは、後述の[The Locking Clause](https://www.postgresql.jp/document/14/html/sql-select.html#SQL-FOR-UPDATE-SHARE)を参照してください）。

### 余談

PostgreSQL 8.0.4とPostgreSQL 14系だとDistinctの処理順序が異なることに気がついた。なんでなんだろう。
