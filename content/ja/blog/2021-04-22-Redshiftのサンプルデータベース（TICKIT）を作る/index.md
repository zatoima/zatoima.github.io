---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshiftのサンプルデータベース（TICKIT）を作る"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-sample-database-tickit.html
date: 2021-04-21
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



毎回マニュアル見ている気がするので、DDLコマンド等のメモ。7 個のテーブルで構成されていて、そのうち 2 個はファクトテーブル、5 個はディメンションとなる。

> サンプルデータベース - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/c_sampledb.html

![img](tickitdb.png)

# データベース作成

```sql
create database TICKIT;
```

tickitデータベースに接続しておく。

```sql
\c tickit;
```

# テーブル作成

```sql
create table users(
	userid integer not null distkey sortkey,
	username char(8),
	firstname varchar(30),
	lastname varchar(30),
	city varchar(30),
	state char(2),
	email varchar(100),
	phone char(14),
	likesports boolean,
	liketheatre boolean,
	likeconcerts boolean,
	likejazz boolean,
	likeclassical boolean,
	likeopera boolean,
	likerock boolean,
	likevegas boolean,
	likebroadway boolean,
	likemusicals boolean);
	
create table venue(
  venueid smallint not null distkey sortkey,
  venuename varchar(100),
  venuecity varchar(30),
  venuestate char(2),
  venueseats integer);

create table category(
	catid smallint not null distkey sortkey,
	catgroup varchar(10),
	catname varchar(10),
	catdesc varchar(50));

create table date(
	dateid smallint not null distkey sortkey,
	caldate date not null,
	day character(3) not null,
	week smallint not null,
	month character(5) not null,
	qtr character(5) not null,
	year smallint not null,
	holiday boolean default('N'));

create table event(
	eventid integer not null distkey,
	venueid smallint not null,
	catid smallint not null,
	dateid smallint not null sortkey,
	eventname varchar(200),
	starttime timestamp);

create table listing(
	listid integer not null distkey,
	sellerid integer not null,
	eventid integer not null,
	dateid smallint not null  sortkey,
	numtickets smallint not null,
	priceperticket decimal(8,2),
	totalprice decimal(8,2),
	listtime timestamp);

create table sales(
	salesid integer not null,
	listid integer not null distkey,
	sellerid integer not null,
	buyerid integer not null,
	eventid integer not null,
	dateid smallint not null sortkey,
	qtysold smallint not null,
	pricepaid decimal(8,2),
	commission decimal(8,2),
	saletime timestamp);
	
```

7テーブル作成している。

```sh
tickit=# \dt
          List of relations
 schema |   name   | type  |  owner  
--------+----------+-------+---------
 public | category | table | awsuser
 public | date     | table | awsuser
 public | event    | table | awsuser
 public | listing  | table | awsuser
 public | sales    | table | awsuser
 public | users    | table | awsuser
 public | venue    | table | awsuser
(7 rows)
```

# データロード

サンプル用のデータの取得

```sh
wget https://docs.aws.amazon.com/ja_jp/redshift/latest/gsg/samples/tickitdb.zip
unzip tickitdb.zip -d tickitdb
ls -l tickitdb
```

copyコマンドを使うので、S3にアップロードする。

```sh
aws s3 mb s3://20210420tickit
aws s3 sync ./tickitdb/ s3://20210420tickit
```

S3のバケットにデータが格納された

```sh
[ec2-user@bastin ~]$ aws s3 ls s3://20210420tickit
2021-04-20 20:34:58     445838 allevents_pipe.txt
2021-04-20 20:34:58    5893626 allusers_pipe.txt
2021-04-20 20:34:58        465 category_pipe.txt
2021-04-20 20:34:58      14534 date2008_pipe.txt
2021-04-20 20:34:58   11585036 listings_pipe.txt
2021-04-20 20:34:58   11260097 sales_tab.txt
2021-04-20 20:34:58       7988 venue_pipe.txt
```

データロードコマンド

```sh
copy users from 's3://20210420tickit/allusers_pipe.txt' 
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '|';

copy venue from 's3://20210420tickit/venue_pipe.txt' 
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '|';

copy category from 's3://20210420tickit/category_pipe.txt' 
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '|';

copy date from 's3://20210420tickit/date2008_pipe.txt' 
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '|';

copy event from 's3://20210420tickit/allevents_pipe.txt' 
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '|' timeformat 'YYYY-MM-DD HH:MI:SS';

copy listing from 's3://20210420tickit/listings_pipe.txt' 
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '|';

copy sales from 's3://20210420tickit/sales_tab.txt'
iam_role 'arn:aws:iam::xxxxxx:role/myRedshiftRole'
delimiter '\t' timeformat 'MM/DD/YYYY HH:MI:SS';
```

テーブルごとの行数確認

```sh
[ec2-user@bastin AdminScripts]$ pwd
/home/ec2-user/amazon-redshift-utils-master/src/AdminScripts
[ec2-user@bastin AdminScripts]$ ls -l
total 112
-rw-rw-r-- 1 ec2-user ec2-user  899 Mar 26 03:15 commit_stats.sql
-rw-rw-r-- 1 ec2-user ec2-user 1163 Mar 26 03:15 copy_performance.sql
-rw-rw-r-- 1 ec2-user ec2-user  527 Mar 26 03:15 current_session_info.sql
-rw-rw-r-- 1 ec2-user ec2-user 1466 Mar 26 03:15 filter_used.sql
-rw-rw-r-- 1 ec2-user ec2-user 2553 Mar 26 03:15 generate_calendar.sql
-rw-rw-r-- 1 ec2-user ec2-user 1940 Mar 26 03:15 insert_into_table_dk_mismatch.sql
-rw-rw-r-- 1 ec2-user ec2-user 3440 Mar 26 03:15 lock_wait.sql
-rw-rw-r-- 1 ec2-user ec2-user  309 Mar 26 03:15 missing_table_stats.sql
-rw-rw-r-- 1 ec2-user ec2-user 2312 Mar 26 03:15 perf_alert.sql
-rw-rw-r-- 1 ec2-user ec2-user 2389 Mar 26 03:15 predicate_columns.sql
-rw-rw-r-- 1 ec2-user ec2-user 3019 Mar 26 03:15 queue_resources_hourly.sql
-rw-rw-r-- 1 ec2-user ec2-user  787 Mar 26 03:15 queuing_queries.sql
-rw-rw-r-- 1 ec2-user ec2-user 3279 Mar 26 03:15 README.md
-rw-rw-r-- 1 ec2-user ec2-user 2978 Mar 26 03:15 running_queues.sql
-rw-rw-r-- 1 ec2-user ec2-user 2054 Mar 26 03:15 table_alerts.sql
-rw-rw-r-- 1 ec2-user ec2-user 4584 Mar 26 03:15 table_info.sql
-rw-rw-r-- 1 ec2-user ec2-user 1688 Mar 26 03:15 table_inspector.sql
-rw-rw-r-- 1 ec2-user ec2-user 3504 Mar 26 03:15 top_queries_and_cursors.sql
-rw-rw-r-- 1 ec2-user ec2-user 2431 Mar 26 03:15 top_queries.sql
-rw-rw-r-- 1 ec2-user ec2-user 3060 Mar 26 03:15 unscanned_table_summary.sql
-rw-rw-r-- 1 ec2-user ec2-user 1876 Mar 26 03:15 user_to_be_dropped_objs.sql
-rw-rw-r-- 1 ec2-user ec2-user 5410 Mar 26 03:15 user_to_be_dropped_privs.sql
-rw-rw-r-- 1 ec2-user ec2-user 2876 Mar 26 03:15 wlm_apex_hourly.sql
-rw-rw-r-- 1 ec2-user ec2-user 3302 Mar 26 03:15 wlm_apex.sql
-rw-rw-r-- 1 ec2-user ec2-user 7567 Mar 26 03:15 wlm_qmr_rule_candidates.sql
[ec2-user@bastin AdminScripts]$ psql -h redshift-cluster.ciwori21oiel.ap-northeast-1.redshift.amazonaws.com -U awsuser -d tickit -p 5439
psql (11.5, server 8.0.2)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
Type "help" for help.

tickit=# \i table_info.sql
 schema |  table   | tableid | distkey |  skew  | sortkey | #sks |  rows  | mbytes | enc |        pct_enc        | pct_of_total | pct_stats_off | pct_unsorted 
--------+----------+---------+---------+--------+---------+------+--------+--------+-----+-----------------------+--------------+---------------+--------------
 public | users    |  203862 | userid  | 1.0000 | userid  |    1 |  49990 |    168 | Y   | 33.333333333333333300 |         0.00 |          0.00 |         0.00
 public | sales    |  203875 | listid  | 1.0000 | dateid  |    1 | 172456 |    104 | Y   | 57.894736842105263100 |         0.00 |          0.00 |         0.00
 public | date     |  203868 | dateid  | 1.0000 | dateid  |    1 |    365 |     88 | Y   | 47.058823529411764700 |         0.00 |          0.00 |         0.00
 public | listing  |  203873 | listid  | 1.0000 | dateid  |    1 | 192497 |     88 | Y   | 52.941176470588235200 |         0.00 |          0.00 |         0.00
 public | event    |  203871 | eventid | 1.0000 | dateid  |    1 |   8798 |     72 | Y   | 46.666666666666666600 |         0.00 |          0.00 |         0.00
 public | venue    |  203864 | venueid | 1.0000 | venueid |    1 |    202 |     64 | Y   | 42.857142857142857100 |         0.00 |          0.00 |         0.00
 public | category |  203866 | catid   | 1.0000 | catid   |    1 |     11 |     56 | Y   | 38.461538461538461500 |         0.00 |          0.00 |         0.00
(7 rows)

tickit=# 

```



サンプルクエリとして用意されているものだが、2008 年に販売されたチケット数に基づき、サンディエゴで最も販売数の多かった販売者 5 名を検出

```sql
select sellerid, username, (firstname ||' '|| lastname) as name,
city, sum(qtysold)
from sales, date, users
where sales.sellerid = users.userid
and sales.dateid = date.dateid
and year = 2008
and city = 'San Diego'
group by sellerid, username, name, city
order by 5 desc
limit 5;
```

```
tickit=# select sellerid, username, (firstname ||' '|| lastname) as name,
tickit-# city, sum(qtysold)
tickit-# from sales, date, users
tickit-# where sales.sellerid = users.userid
tickit-# and sales.dateid = date.dateid
tickit-# and year = 2008
tickit-# and city = 'San Diego'
tickit-# group by sellerid, username, name, city
tickit-# order by 5 desc
tickit-# limit 5;
 sellerid | username |       name        |   city    | sum 
----------+----------+-------------------+-----------+-----
    49977 | JJK84WTE | Julie Hanson      | San Diego |  22
    19750 | AAS23BDR | Charity Zimmerman | San Diego |  21
    29069 | SVL81MEQ | Axel Grant        | San Diego |  17
    43632 | VAG08HKW | Griffin Dodson    | San Diego |  16
    18888 | KMQ52NVN | Joan Wright       | San Diego |  14
(5 rows)

tickit=# 
```

# 参考

> サンプルデータベース - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/c_sampledb.html
>
> ステップ 6: Amazon S3 のサンプルデータをロードする - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/gsg/rs-gsg-create-sample-db.html

