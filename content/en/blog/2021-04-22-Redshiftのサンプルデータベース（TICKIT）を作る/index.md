---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Creating the Redshift Sample Database (TICKIT)"
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



I keep having to look at the manual each time, so here are notes on DDL commands etc. The database consists of 7 tables, of which 2 are fact tables and 5 are dimensions.

> Sample Database - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/c_sampledb.html

![img](tickitdb.png)

# Create Database

```sql
create database TICKIT;
```

Connect to the tickit database:

```sql
\c tickit;
```

# Create Tables

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

7 tables created:

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

# Load Data

Get the sample data:

```sh
wget https://docs.aws.amazon.com/ja_jp/redshift/latest/gsg/samples/tickitdb.zip
unzip tickitdb.zip -d tickitdb
ls -l tickitdb
```

Upload to S3 since we use the copy command:

```sh
aws s3 mb s3://20210420tickit
aws s3 sync ./tickitdb/ s3://20210420tickit
```

Data stored in S3 bucket:

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

Data load commands:

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

Verify row counts per table:

```sh
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
```

A sample query that finds the top 5 sellers in San Diego based on number of tickets sold in 2008:

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

# References

> Sample Database - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/c_sampledb.html
>
> Step 6: Load Sample Data from Amazon S3 - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/gsg/rs-gsg-create-sample-db.html
