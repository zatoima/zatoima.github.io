---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Notes on Decimal Arithmetic in Redshift"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-decimal-calculate.html
date: 2021-05-13
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

### Introduction

When you want to maintain precision in floating-point arithmetic, you would use `DECIMAL`, but when DECIMAL is <u>used in arithmetic calculations</u>, the precision of the result differs from the DECIMAL of the storage destination.

> https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/r_numeric_computations201.html
>
> Precision and Scale of DECIMAL Calculation Results

### Precision and Scale

First, a basic understanding of precision and scale:

- Precision: Total number of digits
- Scale: Number of digits to the right of the decimal point

| Input Data   | NUMBER Type Definition | Stored Data                                    |
| ------------ | ---------------------- | ---------------------------------------------- |
| 7,456,123.89 | NUMBER                 | 7456123.89                                     |
| 7,456,123.89 | NUMBER(*,1)            | 7456123.9                                      |
| 7,456,123.89 | NUMBER(9)              | 7456124                                        |
| 7,456,123.89 | NUMBER(9,2)            | 7456123.89                                     |
| 7,456,123.89 | NUMBER(9,1)            | 7456123.9                                      |
| 7,456,123.89 | NUMBER(6)              | (Not accepted because it exceeds precision)    |
| 7,456,123.89 | NUMBER(7,-2)           | 7456100                                        |

### Floating-Point Arithmetic Specifications in Redshift

For example, executing the following series of commands. Column `a` is `decimal(8,2)`, column `b` is `decimal(8,7)`, and the pattern divides the values stored in a and b, storing the result in `c` as `decimal(38,23)`. We would want c to store values up to 23 decimal places, but when arithmetic is involved, the precision and scale will not be maintained to 23 decimal places. The result in this pattern is `0.33330000000000000000000`, which is maintained to `4 decimal places`, with zeros padded afterward.

```sql
drop table test;
create table test(a decimal(8,2), b decimal(8,7),c decimal(38,23));
insert into test values(1,3,null);

select * from test;
insert into test(c) select a/b from test;
select * from test;
```

Execution log:

```sql
mydb=# drop table test;
DROP TABLE
mydb=# create table test(a decimal(8,2), b decimal(8,7),c decimal(38,23));
CREATE TABLE
mydb=# insert into test values(1,3,null);
INSERT 0 1
mydb=#
mydb=# select * from test;
  a   |     b     | c
------+-----------+---
 1.00 | 3.0000000 |
(1 row)

mydb=# insert into test(c) select a/b from test;
INSERT 0 1
mydb=# select * from test;
  a   |     b     |             c
------+-----------+---------------------------
 1.00 | 3.0000000 |
      |           | 0.33330000000000000000000
(2 rows)
```

This result occurs because the following calculation formulas are applied. (Excerpt from the manual)

In this case it's division, so the scale is calculated as `max(4,s1+p2-s2+1)` and precision as `p1-s1+s2+scale`.

| Operation  | Category  | Formula                  |
| ---------- | --------- | ------------------------ |
| + or -     | Scale     | max(s1,s2)               |
| + or -     | Precision | max(p1-s1,p2-s2)+1+scale |
| *          | Scale     | s1+s2                    |
| *          | Precision | p1+p2+1                  |
| /          | Scale     | max(4,s1+p2-s2+1)        |
| /          | Precision | p1-s1+s2+scale           |

In table format, it looks like this. There were differences in the `scale` and `precision` that can be stored between the calculation result and the storage destination `c`. Data types must be decided with an understanding of such specifications.

| Column          | Variable                   | Scale, Precision |
| --------------- | -------------------------- | ---------------- |
| a               | p1                         | 8                |
| a               | s1                         | 2                |
| b               | p2                         | 8                |
| b               | s2                         | 7                |
| Calculation result | Precision (total digits) | 17               |
| Calculation result | Scale (decimal digits)   | 4                |
| c (destination) | Precision (total digits)   | 38               |
| c (destination) | Scale (decimal digits)     | 23               |

### Notes

Are the calculation formulas different for each database? Below is SQL Server.

https://docs.microsoft.com/ja-jp/sql/t-sql/data-types/precision-scale-and-length-transact-sql?view=sql-server-ver15

### References

> https://tech.tvisioninsights.co.jp/entry/2018/08/22/100000
>
> https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/r_numeric_computations201.html
>
> https://odashinsuke.hatenablog.com/entry/20100720/1279628893
>
> https://docs.microsoft.com/ja-jp/sql/t-sql/data-types/precision-scale-and-length-transact-sql?redirectedfrom=MSDN&view=sql-server-ver15
