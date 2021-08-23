---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshiftのdecimalの数値計算時の注意点"
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

### はじめに

浮動小数点演算で細かいところまで保持したい場合は`DECIMAL`を使うことになると思うが、DECIMALを<u>数値計算に使用した場合</u>、計算結果の有効桁数は格納先のDECIMALと異なるという。

> https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/r_numeric_computations201.html
>
> DECIMAL の計算結果の精度とスケール

### 精度とスケール

まずは精度とスケールの基本的理解から。

- 精度(Precision)：全体の桁数
- スケール(Scale)：小数点以下の桁数

| 入力データ   | NUMBER型の定義 | 格納されるデータ                           |
| ------------ | -------------- | ------------------------------------------ |
| 7,456,123.89 | NUMBER         | 7456123.89                                 |
| 7,456,123.89 | NUMBER(*,1)    | 7456123.9                                  |
| 7,456,123.89 | NUMBER(9)      | 7456124                                    |
| 7,456,123.89 | NUMBER(9,2)    | 7456123.89                                 |
| 7,456,123.89 | NUMBER(9,1)    | 7456123.9                                  |
| 7,456,123.89 | NUMBER(6)      | （精度を超えているため、受け入れられない） |
| 7,456,123.89 | NUMBER(7,-2)   | 7456100                                    |

### Redshiftでの浮動小数点演算の仕様

例えば次のように一連のコマンドを実行する。これは`a`というカラムが`decimal(8,2)`、`b`というカラムが`decimal(8,7)`であり、このaとbに格納されている値を除算して、`c`の`decimal(38,23)`に格納するパターンとなる。cに格納される値は小数点23位までしっかりと格納されて欲しいが、計算が入る場合の精度とスケールは小数点23位まで保持されない。このパターンの結果は`0.33330000000000000000000`となり、`小数点4位`まで保持されて、以降はゼロ詰めされている。

```sql
drop table test;
create table test(a decimal(8,2), b decimal(8,7),c decimal(38,23));
insert into test values(1,3,null);

select * from test;
insert into test(c) select a/b from test;
select * from test;
```

実行ログは次の通り。

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

このような結果になるのは次の計算式が適用されるため。（マニュアルからの抜粋）

今回は除算なので、スケールは`max(4,s1+p2-s2+1)`、精度は`p1-s1+s2+scale`で計算する必要がある。

| オペレーション | 分類     | 計算式                   |
| -------------- | -------- | ------------------------ |
| + または -     | スケール | max(s1,s2)               |
| + または -     | 精度     | max(p1-s1,p2-s2)+1+scale |
| *              | スケール | s1+s2                    |
| *              | 精度     | p1+p2+1                  |
| /              | スケール | max(4,s1+p2-s2+1)        |
| /              | 精度     | p1-s1+s2+scale           |

表形式にするとこんな感じ。計算結果と格納先の`c`で格納出来る`スケール`、`精度`で差異が出た。このような仕様を理解した上でデータ型を決める必要がある。

| カラム      | 変数                         | スケール、精度 |
| ----------- | ---------------------------- | -------------- |
| a           | p1                           | 8              |
| a           | s1                           | 2              |
| b           | p2                           | 8              |
| b           | s2                           | 7              |
| 計算結果    | 精度（全体の桁数）           | 17             |
| 計算結果    | スケール（小数点以下の桁数） | 4              |
| c（格納先） | 精度（全体の桁数）           | 38             |
| c（格納先） | スケール（小数点以下の桁数） | 23             |

### 補足

各データベースで計算式が違う？下記はSQL Server。

https://docs.microsoft.com/ja-jp/sql/t-sql/data-types/precision-scale-and-length-transact-sql?view=sql-server-ver15

### 参照

> https://tech.tvisioninsights.co.jp/entry/2018/08/22/100000
>
> https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/r_numeric_computations201.html
>
> https://odashinsuke.hatenablog.com/entry/20100720/1279628893
>
> https://docs.microsoft.com/ja-jp/sql/t-sql/data-types/precision-scale-and-length-transact-sql?redirectedfrom=MSDN&view=sql-server-ver15