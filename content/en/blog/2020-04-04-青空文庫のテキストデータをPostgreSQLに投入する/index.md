---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Inserting Aozora Bunko Text Data into PostgreSQL"
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



I referenced this site for guidance. Since the SQL statement creation part didn't work in my environment, I switched to a different approach.

> Text Mining with Aozora Bunko Data (Preparation) | ACALL BLOG https://blog.acall.jp/2019/11/aozorabunko-textmining/

Note that I simply wanted large-volume Japanese text data without proper formatting, so please be aware of that.

##### Clone from the Aozora Bunko Repository

```sh
#sudo yum -y install git
git clone --depth 1 https://github.com/aozorabunko/aozorabunko.git
```

##### Install nkf

```sh
wget https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/n/nkf-2.1.3-5.el7.x86_64.rpm
sudo rpm -ivh nkf-2.1.3-5.el7.x86_64.rpm
```

##### Merge Text Files

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

##### Create SQL from Text File for Execution

```sh
# Remove single quotes from text file. Single quotes cause incorrect delimiter detection.
sed -e "s/'/ /g" matome.txt > matome1.sql

sed "s/^/insert into aozoradata (data) values ('/g" matome1.sql > matome2.sql
sed "s/$/');/g" matome2.sql > matome3.sql
```

##### Prepare PostgreSQL

```sql
CREATE TABLE aozoradata(
id serial not null,
data text not null
);
```

##### Execute SQL File (This takes a very long time)

```sh
psql -d postgres -U postgres -f matome3.sql
```

The number of rows becomes `3,533,485`.

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

Checking with pgstattuple shows the following:

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

Checking from statistics (pg_stats). The avg_width is `190`, which feels surprisingly small.

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

Aozora Bunko annotations, blank lines, and hyphen separators remain in the data, so you'll likely need to remove them as needed. In that case, please refer to the middle section onwards of the reference URL.

> Text Mining with Aozora Bunko Data (Preparation) | ACALL BLOG https://blog.acall.jp/2019/11/aozorabunko-textmining/
