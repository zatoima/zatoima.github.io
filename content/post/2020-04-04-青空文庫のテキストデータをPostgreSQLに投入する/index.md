---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "青空文庫のテキストデータをPostgreSQLに投入する"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-aozora-date-insert.html
date: 2020-04-04
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



このサイトを参考にさせて頂きました。SQL文作成のところが私の環境では動かなかったので別の方法に変えました。

> 青空文庫のデータでテキストマイニング（の準備） | ACALL BLOG https://blog.acall.jp/2019/11/aozorabunko-textmining/

日本語の大容量のテキストデータが欲しかっただけで、綺麗に整形しておりませんのでご注意ください。

##### 青空文庫のリポジトリからclone

```sh
#sudo yum -y install git
git clone --depth 1 https://github.com/aozorabunko/aozorabunko.git
```

##### nkfのインストール

```sh
wget https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/n/nkf-2.1.3-5.el7.x86_64.rpm
sudo rpm -ivh nkf-2.1.3-5.el7.x86_64.rpm
```

##### テキストファイルのマージ

```sh
cd aozorabunko-master
mdkir text
find cards -name '*.zip' -exec cp {} text \;
cd text
unzip '*.zip'
mkdir matome
cp *.txt matome
cd matome
find . -name "*.txt" -exec cat {} >>matome.txt +
nkf -w --overwrite matome.txt
```

##### テキストファイルから実行用のSQLを作成

```sh
#テキストファイル内のシングルクォートを削除。シングルクォートがあると区切り文字を誤って判断してしまうため。
sed -e "s/'/ /g" matome.txt > matome1.sql

sed "s/^/insert into aozoradata (data) values ('/g" matome1.sql > matome2.sql
sed "s/$/');/g" matome2.sql > matome3.sql
```

##### PostgreSQL側の準備

```sql
CREATE TABLE aozoradata(
id serial not null,
data text not null
);
```

##### SQLファイルの実行 #時間が凄く掛かります。

```sh
psql -d postgres -U postgres -f matome3.sql
```

行数は`3533485件`となります。

```
postgres=# \d+ aozoradata;
                                                Table "public.aozoradata"
 Column |  Type   | Collation | Nullable |                Default                 | Storage  | Stats target | Description 
--------+---------+-----------+----------+----------------------------------------+----------+--------------+-------------
 id     | integer |           | not null | nextval('aozoradata_id_seq'::regclass) | plain    |              | 
 data   | text    |           | not null |                                        | extended |              | 
Indexes:
    "aozoradata_idx" gin (data gin_trgm_ops)

postgres=# select count(*) from aozoradata;
  count  
---------
 3533485
(1 row)
```

pgstattupleで確認してみるとこんな感じに。

```
postgres=# SELECT * FROM pgstattuple('aozoradata');
-[ RECORD 1 ]------+----------
table_len          | 807690240
tuple_count        | 3533485
tuple_len          | 774167704
tuple_percent      | 95.85
dead_tuple_count   | 0
dead_tuple_len     | 0
dead_tuple_percent | 0
free_space         | 3066496
free_percent       | 0.38
```

統計情報(pg_stats)から確認。avg_widthが`190`で意外と小さく感じた。

```sh
postgres=# select schemaname,tablename,attname,null_frac,avg_width,n_distinct,correlation from pg_stats where tablename='aozoradata';
-[ RECORD 1 ]------------
schemaname  | public
tablename   | aozoradata
attname     | id
null_frac   | 0
avg_width   | 4
n_distinct  | -1
correlation | 0.999998
-[ RECORD 2 ]------------
schemaname  | public
tablename   | aozoradata
attname     | data
null_frac   | 0
avg_width   | 190
n_distinct  | 114652
correlation | -0.00665814
```

青空文庫側の注釈や空行、ハイフン区切りが多く残っているので必要に応じて削除する必要があると思いますのでその場合は参考URLの中段以降をどうぞ。

> 青空文庫のデータでテキストマイニング（の準備） | ACALL BLOG https://blog.acall.jp/2019/11/aozorabunko-textmining/

