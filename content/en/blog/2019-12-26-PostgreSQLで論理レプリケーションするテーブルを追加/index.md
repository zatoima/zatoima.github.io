---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Adding Tables to PostgreSQL Logical Replication"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgresql-addtable-logical-replication.html
date: 2019-12-26
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



#### Introduction

***

I mistakenly assumed that when using "FOR ALL TABLES" in CREATE PUBLICATION, any tables created after that would automatically become replication targets. This may be a basic thing, but since I wasn't aware of this behavior, I'm documenting it.

The conclusion is: even when using "FOR ALL TABLES," the `ALTER SUBSCRIPTION xxxxxxx REFRESH PUBLICATION` command is still required when adding new tables.



#### Pre-check

***

Confirm Publisher settings. All tables is set to True:

```sql
repdb=> \dRp+
                Publication alltables
  Owner   | All tables | Inserts | Updates | Deletes
----------+------------+---------+---------+---------
 postgres | t          | t       | t       | t
(1 row)
```

Confirm Subscriber settings. logicalreplicationtest is already a replication target:

```sql
repdb=> SELECT
repdb->     a3.subname,
repdb->     a2.relname,
repdb->     a1.srsubstate,
repdb->     a1.srsublsn
repdb-> FROM
repdb->     pg_subscription_rel AS a1
repdb->     LEFT OUTER JOIN
repdb->     pg_class AS a2 ON
repdb->     a1.srrelid = a2.oid
repdb->     LEFT OUTER JOIN
repdb->     pg_stat_subscription AS a3 ON
repdb->     a1.srsubid = a3.subid;
      subname       |        relname         | srsubstate | srsublsn
--------------------+------------------------+------------+-----------
 auroratopostgresql | logicalreplicationtest | r          | 0/1220050
(1 row)
```



#### Add a Table

***

Create a table on both Publisher and Subscriber sides:

```sql
repdb=> CREATE TABLE addtable1 (a int PRIMARY KEY);
CREATE TABLE
```

Check. I expected it to be added to the replication targets at this point:

```sql
repdb=> SELECT
repdb->     a3.subname,
repdb->     a2.relname,
repdb->     a1.srsubstate,
repdb->     a1.srsublsn
repdb-> FROM
repdb->     pg_subscription_rel AS a1
repdb->     LEFT OUTER JOIN
repdb->     pg_class AS a2 ON
repdb->     a1.srrelid = a2.oid
repdb->     LEFT OUTER JOIN
repdb->     pg_stat_subscription AS a3 ON
repdb->     a1.srsubid = a3.subid;
      subname       |        relname         | srsubstate | srsublsn
--------------------+------------------------+------------+-----------
 auroratopostgresql | logicalreplicationtest | r          | 0/1220050
(1 row)

repdb=>
```

REFRESH the SUBSCRIPTION using ALTER SUBSCRIPTION:

```sql
repdb=> ALTER SUBSCRIPTION auroratopostgresql REFRESH PUBLICATION;
ALTER SUBSCRIPTION
```

> ALTER SUBSCRIPTION [https://www.postgresql.jp/document/10/html/sql-altersubscription.html](https://www.postgresql.jp/document/10/html/sql-altersubscription.html)
>
> REFRESH PUBLICATION
>
> Fetches missing table information from the publisher. This starts replication of tables that were added to the subscribed-for publications since CREATE SUBSCRIPTION was last run, or since the last invocation of REFRESH PUBLICATION.

Now the replication target has been added:

```sql
repdb=> SELECT
repdb->     a3.subname,
repdb->     a2.relname,
repdb->     a1.srsubstate,
repdb->     a1.srsublsn
repdb-> FROM
repdb->     pg_subscription_rel AS a1
repdb->     LEFT OUTER JOIN
repdb->     pg_class AS a2 ON
repdb->     a1.srrelid = a2.oid
repdb->     LEFT OUTER JOIN
repdb->     pg_stat_subscription AS a3 ON
repdb->     a1.srsubid = a3.subid;
      subname       |        relname         | srsubstate | srsublsn
--------------------+------------------------+------------+-----------
 auroratopostgresql | logicalreplicationtest | r          | 0/1220050
 auroratopostgresql | addtable1              | r          | 0/5030740
(2 rows)

```

#### Summary

***

I assumed that since the CREATE PUBLICATION manual says "replicates changes for all tables in the database, including tables created in the future," new tables would automatically be replicated.

> https://www.postgresql.jp/document/10/html/sql-createpublication.html
> > CREATE PUBLICATION
> > FOR ALL TABLES
> > Marks the publication as one that replicates changes for all tables in the database, including tables created in the future.

The takeaway is: when new tables are added to the replication targets, you need to run the `ALTER SUBSCRIPTION xxxxxxx REFRESH PUBLICATION` command.
