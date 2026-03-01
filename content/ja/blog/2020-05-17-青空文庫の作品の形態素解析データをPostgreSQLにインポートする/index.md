---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "青空文庫作品の形態素解析データをRDS PostgreSQLにインポートする"
subtitle: ""
summary: " "
tags: ["PostgreSQL","AWS","Aurora","RDS"]
categories: ["PostgreSQL","AWS","Aurora","RDS"]
url: postgresql-aozora-bunko-data-import.html
date: 2020-05-17
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

形態素解析データを使用した分析をPostgreSQL上で実施したく、AWS上のRDS(PostgreSQL)へのロード方法をメモ。形態素解析データについてはこちらを使用させて頂きました。

> 青空文庫形態素解析データ集 http://aozora-word.hahasoha.net/

### 対象データ

全データが含まれているこちらのファイルをPostgreSQLにロードすることにしました。

> http://aozora-word.hahasoha.net/utf8/utf8_all.csv.gz

こちらには青空文庫の全文章が下記のように形態素解析済のデータが格納されています。87701673行、ファイルサイズは約6GB。

```
1000_15021.html,1,1,一,名詞,数,,,,,一,イチ,イチ
1000_15021.html,2,1,「,記号,括弧開,,,,,「,「,「
1000_15021.html,2,2,むかし,名詞,副詞可能,,,,,むかし,ムカシ,ムカシ
1000_15021.html,2,3,者,名詞,接尾,一般,,,,者,シャ,シャ
1000_15021.html,2,4,の,助詞,連体化,,,,,の,ノ,ノ
1000_15021.html,2,5,お話,名詞,サ変接続,,,,,お話,オハナシ,オハナシ
1000_15021.html,2,6,は,助詞,係助詞,,,,,は,ハ,ワ
1000_15021.html,2,7,とかく,名詞,副詞可能,,,,,とかく,トカク,トカク
1000_15021.html,2,8,前置き,名詞,サ変接続,,,,,前置き,マエオキ,マエオキ
1000_15021.html,2,9,が,助詞,格助詞,一般,,,,が,ガ,ガ
1000_15021.html,2,10,長い,形容詞,自立,,,形容詞・アウオ段,基本形,長い,ナガイ,ナガイ
1000_15021.html,2,11,ので,助詞,接続助詞,,,,,ので,ノデ,ノデ
1000_15021.html,2,12,、,記号,読点,,,,,、,、,、
1000_15021.html,2,13,今,名詞,副詞可能,,,,,今,イマ,イマ
1000_15021.html,2,14,の,助詞,連体化,,,,,の,ノ,ノ
1000_15021.html,2,15,若い,形容詞,自立,,,形容詞・アウオ段,基本形,若い,ワカイ,ワカイ
1000_15021.html,2,16,方,名詞,接尾,特殊,,,,方,カタ,カタ
1000_15021.html,2,17,たち,名詞,接尾,一般,,,,たち,タチ,タチ
1000_15021.html,2,18,に,助詞,格助詞,一般,,,,に,ニ,ニ
1000_15021.html,2,19,は,助詞,係助詞,,,,,は,ハ,ワ
1000_15021.html,2,20,小,名詞,一般,,,,,小,ショウ,ショー
1000_15021.html,2,21,焦れったい,形容詞,自立,,,形容詞・アウオ段,基本形,焦れったい,ジレッタイ,ジレッタイ
1000_15021.html,2,22,かも,助詞,副助詞,,,,,かも,カモ,カモ
1000_15021.html,2,23,知れ,動詞,自立,,,一段,連用形,知れる,シレ,シレ
```

##### PostgreSQL側のテーブル作成

データ型はざっくりと。

```sql
CREATE TABLE aozora_kaiseki(file VARCHAR(30),num INT,row INT,word TEXT,subtype1 VARCHAR(30),subtype2 VARCHAR(30),subtype3 VARCHAR(30),subtype4 VARCHAR(10),conjtype VARCHAR(15),conjugation VARCHAR(15),basic TEXT,ruby TEXT,pronunce TEXT );
```

##### COPYコマンドでロード

データをwgetで取得

```sh
wget http://aozora-word.hahasoha.net/utf8/utf8_all.csv.gz
gzip -d utf8_all.csv.gz
```

copyコマンドでロード

```sh
psql -h rdspgsqlv1.xxxxxx.ap-northeast-1.rds.amazonaws.com -d postgres -U postgres -c "COPY aozora_kaiseki(file,num,row,word,subtype1,subtype2,subtype3,subtype4,conjtype,conjugation,basic,ruby,pronunce) from stdin with csv DELIMITER ','" < /home/ec2-user/utf8_all.csv
```

##### 事後確認

約9.35GBのテーブルサイズでした。

```sh
postgres@rdspgsqlv1:postgres> select COUNT(*) from aozora_kaiseki;                                                                                                                          
+----------+
| count    |
|----------|
| 87701673 |
+----------+
SELECT 1
Time: 78.574s (a minute), executed in: 78.562s (a minute)
postgres@rdspgsqlv1:postgres>  

postgres@rdspgsqlv1:postgres> SELECT * FROM pgstattuple('aozora_kaiseki');                                                                                                                  
-[ RECORD 1 ]-------------------------
table_len          | 10039386112
tuple_count        | 87701673
tuple_len          | 9306566707
tuple_percent      | 92.7
dead_tuple_count   | 0
dead_tuple_len     | 0
dead_tuple_percent | 0.0
free_space         | 48754128
free_percent       | 0.49
SELECT 1
Time: 21.117s (21 seconds), executed in: 21.111s (21 seconds)
postgres@rdspgsqlv1:postgres>  
```

