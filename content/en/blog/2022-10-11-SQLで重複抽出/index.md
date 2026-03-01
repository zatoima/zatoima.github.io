---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Duplicate Extraction with SQL"
subtitle: ""
summary: " "
tags: ["SQL"]
categories: ["SQL"]
url: sql-leetcode-182-duplicate-search
date: 2022-10-11
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

Notes from a LeetCode problem showing different ways to solve it.

182. Duplicate Emails

Table

```
mysql> select * from Person;
+------+---------+
| id   | email   |
+------+---------+
|    1 | a@b.com |
|    2 | c@d.com |
|    3 | a@b.com |
+------+---------+
```

Using HAVING clause

```sql
select Email
from Person
group by Email
having count(Email) > 1;
```

Subquery

```sql
select Email from
(
  select Email, count(Email) as num
  from Person
  group by Email
) as statistic
where num > 1
;
```

Self join

```sql
select distinct a.email from Person as a
join Person as b
on a.email = b.email
where a.Id <> b.Id
```
