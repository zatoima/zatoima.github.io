---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "MySQLテーブル内のデータをファイル抽出する"
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



ファイル出力方法は大きく分けて2種類ある

### <u>①リダイレクトによる出力</u>

```sql
echo 'SELECT * FROM t1 ' | mysql -u myuser -p<パスワード> mydb > /tmp/t1.dmp
```

### <u>②SELECT INTO OUTFILE を使用する</u>

```sql
SELECT * FROM t1 INTO OUTFILE '/var/lib/mysql-files/t1.dmp' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
```

ファイルの書き込み先はsecure_file_privで許可されたところを指定する。
上記ディレクトリ以外を指定すると下記エラーが発生する。

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

### 参考

> MySQL :: MySQL 5.6 リファレンスマニュアル :: 13.2.9.1 SELECT ... INTO 構文 https://dev.mysql.com/doc/refman/5.6/ja/select-into.html
>
> ```sql
> SELECT a,b,a+b INTO OUTFILE '/tmp/result.txt'
> FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
> LINES TERMINATED BY '\n'
> FROM test_table;
> ```
>
> 