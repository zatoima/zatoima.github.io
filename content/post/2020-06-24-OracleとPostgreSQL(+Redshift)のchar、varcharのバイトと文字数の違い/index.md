---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "OracleとPostgreSQL(+Redshift)のchar、varcharのバイトと文字数の違い"
subtitle: ""
summary: " "
tags: ["Oracle","PostgreSQL","DB Migration"]
categories: ["Oracle","PostgreSQL","DB Migration"]
url: oracle-postgresql-char-varchar-byte.html
date: 2020-06-24
lastmod: 2021-06-30
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

charとvarcharの引数指定はOracleはバイト数である一方PostgreSQLは文字数となる。UTF8環境のOracleでchar(10)とした場合は3文字しか格納出来ない。一方、PostgreSQLでchar(10)と設定した場合は、10文字格納出来る。ora2pgやSCT(schema conversion tool)ではこの非互換は変換されないので注意が必要。

### Oracle/PostgreSQL共通

```sql
create table chartest(a char(10));
```

### PostgreSQL

char(10)の列に全角10文字を格納し、長さとバイト数を確認。

```sql
postgres> insert into chartest values('１２３４５６７８９あ');                                                                                                                              
INSERT 0 1
Time: 0.004s
postgres> SELECT LENGTH(a) from chartest;                                                                                                                                                   
+----------+
| length   |
|----------|
| 10       |
+----------+
SELECT 1
Time: 0.017s
postgres> SELECT OCTET_LENGTH(a) from chartest;                                                                                                                                             
+----------------+
| octet_length   |
|----------------|
| 30             |
+----------------+
SELECT 1
Time: 0.017s
#文字数オーバーなパターン
postgres> insert into chartest values('１２３４５６７８９あい');                                                                                                                            
value too long for type character(10)

Time: 0.004s
postgres>  
```

> https://www.postgresql.jp/document/11/html/datatype-character.html
>
> SQLは2つの主要な文字データ型を定義しています。 `character varying(*`n`*)`と`character(*`n`*)`です。 ここで*`n`*は正の整数です。 これらのデータ型は2つとも*`n`*文字長（バイト数ではなく）までの文字列を保存できます。

### Oracle

同様に10バイト分のデータを入れて確認。

```sql
SQL> insert into chartest values('１２３');

1 row inserted.

SQL> SELECT LENGTHB(a) from chartest;
   LENGTHB(A) 
_____________ 
           10 


SQL> SELECT LENGTH(a) from chartest;
   LENGTH(A) 
____________ 
           4 


SQL> insert into chartest values('１２３４');

Error starting at line : 1 in command -
insert into chartest values('１２３４')
Error report -
ORA-12899: value too large for column "ADMIN"."CHARTEST"."A" (actual: 12, maximum: 10)

```

> https://docs.oracle.com/cd/F19136_01/sqlrf/Data-Types.html#GUID-7B72E154-677A-4342-A1EA-C74C1EA928E6
>
> Oracleの組込みデータ型

### 追記：Redshiftの場合

PostgreSQLベースのRedshiftはPostgreSQLと同じで文字数かー、と思っていてマニュアルを念の為に確認してみるとバイト単位だったので注意。

> https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/r_Character_types.html
>
> CHAR および VARCHAR のデータ型は、文字単位でなくバイト単位で定義されます。CHAR 列にはシングルバイト文字のみを含めることができます。したがって、CHAR(10) 列には、最大 10 バイト長の文字列を含めることができます。VARCHAR にはマルチバイト文字 (1 文字あたり最大で 4 バイトまで) を含めることができます。例えば、VARCHAR(12) 列には、シングルバイト文字なら 12 個、2 バイト文字なら 6 個、3 バイト文字なら 4 個、4 バイト文字なら 3 個含めることができます。