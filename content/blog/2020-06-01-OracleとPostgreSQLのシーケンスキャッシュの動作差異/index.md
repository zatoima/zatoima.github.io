---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "OracleとPostgreSQLのシーケンスキャッシュの動作差異"
subtitle: ""
summary: " "
tags: ["Oracle","PostgreSQL","DB Migration"]
categories: ["Oracle","PostgreSQL","DB Migration"]
url: oracle-postgresql-sequence-cache-incompatible.html
date: 2021-04-30
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



OracleとPostgreSQLのシーケンスキャッシュを使用した場合の動作差異についてメモ。PostgreSQLの`cache`はデフォルト1なので、変更しない限りは同じような採番になると思われるが、実際はそうはならない。ここではPostgreSQLのCache値を変更した場合の注意点を記載。

### シーケンスの作成

OracleとPostgreSQL両方ともシーケンスの始まりを「1」、キャッシュを「20」と設定。

##### Oracle

```sql
drop sequence oraseq1;
create sequence oraseq1 start with 1 increment by 1 cache 20;
```

##### PostgreSQL

```sql
drop sequence pgsqlseq1;
create sequence pgsqlseq1 start with 1 increment by 1 cache 20;
```

### Oracle環境での動作

##### Session A

```sql
select oraseq1.nextval from dual;
```

結果は当然シーケンス値は「1」となる。

```sql
SQL> select oraseq1.nextval from dual;

   NEXTVAL
----------
	 1
```

##### Session B

```sql
select oraseq1.nextval from dual;
```

別セッションでシーケンスを取得する場合、Oracleではnextvalもcurrvalが「2」となる。※ここの動作がOracleとPostgreSQLが異なる

```sql
SQL> select oraseq1.nextval from dual;

   NEXTVAL
----------
	 2
```

##### Session A

```sql
select oraseq1.nextval from dual;
```

```sql
SQL> select oraseq1.nextval from dual;

   NEXTVAL
----------
	 3
```

### PostgreSQL環境での動作

##### Session A

```sql
select nextval('pgsqlseq1');
```

```sql
postgres> select nextval('pgsqlseq1');                                                      
+-----------+
| nextval   |
|-----------|
| 1         |
+-----------+
```

##### Session B

```sql
select nextval('pgsqlseq1');
```

```sql
postgres> select nextval('pgsqlseq1');                                                      
+-----------+
| nextval   |
|-----------|
| 21        |
+-----------+
```

##### Session A

```sql
select nextval('pgsqlseq1');
```

```sql
postgres> select nextval('pgsqlseq1');                                                      
+-----------+
| nextval   |
|-----------|
| 2         |
+-----------+
```

### 結果

#### start 1、cache  20のシーケンスでnextvalを実行した場合のシーケンス値について

こうなる。※OracleはOrderオプション指定無しを前提

| 実行順序 | セッション | Oracle | PostgreSQL |
| -------- | ---------- | ------ | ---------- |
| ↓        | Session A  | 1      | 1          |
| ↓        | Session B  | 2      | 21         |
| ↓        | Session A  | 3      | 2          |

### 最後に

Oracleでは特定事象が起きないとシーケンスは飛び番にはならないと思っているが、Cache値をデフォルトから変更すると、PostgreSQLは安易に起こりうる。**<u>連番ではなく、一意を保証という点でで使うべき</u>**である。そもそもキャッシュしている時点で連番になることを保証するのはOracleでも難しいはず。Oracleのインスタンス障害や共有プールからのエージアウト等があった場合にはキャッシュ分は飛ぶので。

下記の通り、マニュアルでも欠番のないシーケンス用途では使えないと書かれている。トランザクションのロールバックを行った場合、nextval や setval はロールバックされないので欠番になるし、再起動にもメモリ上に格納されたキャッシュは消えてしまう。



> - 9.17. シーケンス操作関数 https://www.postgresql.jp/document/13/html/functions-sequence.html
>   - 従って、PostgreSQLのシーケンスオブジェクトは*「欠番のない」シーケンスを得るために使うことはできません*。
> - CREATE SEQUENCE https://www.postgresql.jp/document/13/html/sql-createsequence.html
>   - `nextval`と`setval`の呼び出しは決してロールバックされないので、シーケンスの番号について「欠番のない」割り当てが必要な場合には、シーケンスオブジェクトを使うことはできません。 









