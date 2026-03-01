---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Extracting Data from a MySQL Table to a File"
subtitle: ""
summary: " "
tags: ["MySQL"]
categories: ["MySQL"]
url: mysql-file-exporttable.html
date: 2019-06-28
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



There are two main methods for file output.

### <u>Method 1: Output via Redirect</u>

```sql
echo 'SELECT * FROM t1 ' | mysql -u myuser -p<password> mydb > /tmp/t1.dmp
```

### <u>Method 2: Using SELECT INTO OUTFILE</u>

```sql
SELECT * FROM t1 INTO OUTFILE '/var/lib/mysql-files/t1.dmp' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
```

Specify a file write destination that is permitted by secure_file_priv.
If you specify a directory other than the above, the following error will occur:

```sql
ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
```

```sql
mysql> SELECT @@secure_file_priv;
+-----------------------+
| @@secure_file_priv    |
+-----------------------+
| /var/lib/mysql-files/ |
+-----------------------+
1 row in set (0.00 sec)
```

### Reference

> MySQL :: MySQL 5.6 Reference Manual :: 13.2.9.1 SELECT ... INTO Syntax https://dev.mysql.com/doc/refman/5.6/ja/select-into.html
>
> ```sql
> SELECT a,b,a+b INTO OUTFILE '/tmp/result.txt'
> FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
> LINES TERMINATED BY '\n'
> FROM test_table;
> ```
