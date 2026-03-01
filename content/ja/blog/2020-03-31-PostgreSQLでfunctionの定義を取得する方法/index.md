---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでfunctionの定義を確認する方法"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-function-describe-get.html
date: 2020-03-31
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



#### チェック対象の関数(function)

```sql
DROP FUNCTION IF EXISTS years_ago(INTEGER);

CREATE OR REPLACE FUNCTION years_ago(INTEGER)
RETURNS INTEGER AS $$
  SELECT (extract(year from current_date)::INTEGER - first_appeared)
  FROM programming
  WHERE id = $1;
$$ LANGUAGE sql;
```

#### 方法1 : pg_proc の prosrcを使用

```sql
SELECT proname, prosrc FROM pg_proc WHERE proname = 'years_ago';
```

```sql
postgres=# SELECT proname, prosrc FROM pg_proc WHERE proname = 'years_ago';
  proname  |                                prosrc                                
-----------+----------------------------------------------------------------------
 years_ago |                                                                     +
           |   SELECT (extract(year from current_date)::INTEGER - first_appeared)+
           |   FROM programming                                                  +
           |   WHERE id = $1;                                                    +
           | 
(1 row)
```

#### 方法2 : pg_get_functiondefと組み合わせて使用する

CREATE OR REPLACE FUNCTIONやその他の構文も合わせて出力してくれるので他環境に実行したい時とかに便利。

```sql
SELECT pg_get_functiondef((SELECT oid FROM pg_proc WHERE proname = 'years_ago'));
```

```sql
postgres=# SELECT pg_get_functiondef((SELECT oid FROM pg_proc WHERE proname = 'years_ago'));
                          pg_get_functiondef                          
----------------------------------------------------------------------
 CREATE OR REPLACE FUNCTION public.years_ago(integer)                +
  RETURNS integer                                                    +
  LANGUAGE sql                                                       +
 AS $function$                                                       +
   SELECT (extract(year from current_date)::INTEGER - first_appeared)+
   FROM programming                                                  +
   WHERE id = $1;                                                    +
 $function$                                                          +
 
(1 row)
```

#### 方法3 : information_schema を使用する

```sql
SELECT routine_definition FROM information_schema.routines WHERE routine_name = 'years_ago';
```

```sql
postgres=# SELECT routine_definition FROM information_schema.routines WHERE routine_name = 'years_ago';
                          routine_definition                          
----------------------------------------------------------------------
                                                                     +
   SELECT (extract(year from current_date)::INTEGER - first_appeared)+
   FROM programming                                                  +
   WHERE id = $1;                                                    +
 
(1 row)
```

