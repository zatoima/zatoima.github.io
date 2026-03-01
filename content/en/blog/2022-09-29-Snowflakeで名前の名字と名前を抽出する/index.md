---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Extracting Last Name and First Name in Snowflake (POSITION Function)"
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

### Extracting Last Name and First Name (Space-Delimited)

Target data

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

Use the POSITION function. Equivalent to *STRPOS* in PostgreSQL, INSTR in Oracle.

[POSITION — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/functions/position.html#position)

> ```
> POSITION( <expr1>, <expr2> [ , <start_pos> ] )
>
> POSITION( <expr1> IN <expr2> )
>
> Arguments
> Required:
>
> expr1
> A string or binary expression representing the value to search for.
>
> expr2
> A string or binary expression representing the value to search.
>
> Optional:
>
> start_pos
> A number indicating the position to start the search (1 represents the start of expr2).
>
> Default: 1
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
