---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQL SQL Processing Order"
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

### Processing Order

1. SELECT within WITH
2. FROM
3. WHERE
4. GROUP BY
5. HAVING
6. SELECT
   - Functions on columns, DISTINCT, etc.
7. UNION, INTERSECT, EXCEPT
8. ORDER BY
9. LIMIT

### Manual

> SELECT https://www.postgresql.org/docs/14/sql-select.html
>
> `SELECT` returns rows from zero or more tables. The general processing of `SELECT` is as follows:
>
> 1. All queries in the `WITH` list are computed. These effectively serve as temporary tables that can be referenced in the `FROM` list. A `WITH` query that is referenced more than once in `FROM` is computed only once, unless `NOT MATERIALIZED` is specified.
> 2. All elements in the `FROM` list are computed. (Each element in the `FROM` list is either a real or virtual table.) If more than one element is specified in the `FROM` list, they are cross-joined together.
> 3. If the `WHERE` clause is specified, all rows that do not satisfy the condition are eliminated from the output.
> 4. If the `GROUP BY` clause is specified, or if there are aggregate function calls, the output is combined into groups of rows that match on one or more values, and the results of aggregate functions are computed. If the `HAVING` clause is present, it eliminates groups that do not satisfy the given condition.
> 5. The actual output rows are computed using the `SELECT` output expressions for each selected row or row group.
> 6. `SELECT DISTINCT` eliminates duplicate rows from the result. `SELECT DISTINCT ON` eliminates rows that match on all the specified expressions. `SELECT ALL` (the default) returns all candidate rows, including duplicates.
> 7. Using the operators `UNION`, `INTERSECT`, and `EXCEPT`, the output of more than one `SELECT` statement can be combined to form a single result set.
> 8. If the `ORDER BY` clause is specified, the returned rows are sorted in the specified order.
> 9. If the `LIMIT` (or `FETCH FIRST`) or `OFFSET` clause is specified, the `SELECT` statement only returns a subset of the result rows.
> 10. If a `FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE`, or `FOR KEY SHARE` clause is specified, the `SELECT` statement locks the selected rows against concurrent updates.

### Side Note

I noticed that the processing order of DISTINCT differs between PostgreSQL 8.0.4 and PostgreSQL 14. I wonder why.
