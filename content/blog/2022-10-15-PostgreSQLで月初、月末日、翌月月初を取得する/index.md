---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLで月初、月末日、翌月月初を取得する"
subtitle: ""
summary: " "
tags: ["PostgreSQL","SQL"]
categories: ["PostgreSQL","SQL"]
url: postgresql-sql-month_first
date: 2022-10-15
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

メモ。

```sql
select date(date_trunc('month',current_date)); -- 月初
select date(date_trunc('month',current_date) + ' 1 month' + '-1 Day'); -- 月末日
select date(date_trunc('month',current_date) + ' 1 month'); -- 翌月の月初
```

```
postgres=# select date(date_trunc('month',current_date)); -- 月初
    date
------------
 2022-10-01
(1 row)

postgres=# select date(date_trunc('month',current_date) + ' 1 month' + '-1 Day'); -- 月末日
    date
------------
 2022-10-31
(1 row)

postgres=# select date(date_trunc('month',current_date) + ' 1 month'); -- 翌月の月初
    date
------------
 2022-11-01
(1 row)
```

