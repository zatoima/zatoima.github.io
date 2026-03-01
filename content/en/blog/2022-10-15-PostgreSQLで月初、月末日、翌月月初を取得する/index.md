---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Getting First Day of Month, Last Day of Month, and First Day of Next Month in PostgreSQL"
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

Notes.

```sql
select date(date_trunc('month',current_date)); -- First day of month
select date(date_trunc('month',current_date) + ' 1 month' + '-1 Day'); -- Last day of month
select date(date_trunc('month',current_date) + ' 1 month'); -- First day of next month
```

```
postgres=# select date(date_trunc('month',current_date)); -- First day of month
    date
------------
 2022-10-01
(1 row)

postgres=# select date(date_trunc('month',current_date) + ' 1 month' + '-1 Day'); -- Last day of month
    date
------------
 2022-10-31
(1 row)

postgres=# select date(date_trunc('month',current_date) + ' 1 month'); -- First day of next month
    date
------------
 2022-11-01
(1 row)
```
