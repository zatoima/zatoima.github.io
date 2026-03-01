---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Transaction Isolation Levels (ISOLATION LEVEL) and Database Engines"
subtitle: ""
summary: " "
tags: ["Oracle", "MySQL", "PostgreSQL"]
categories: ["Oracle", "MySQL", "PostgreSQL"]
url: oracle-mysql-postgresql-isolation-level.html
date: 2019-11-17
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

Notes on the I (Isolation) aspect of the ACID properties of RDBMS products.

<img src="image-20191118125604554.png" alt="image-20191118125604554" style="zoom:75%;" />



#### What Are Transaction Isolation Levels?

***

First, let's organize the basic concepts of transaction isolation levels.

<br/>

#### SERIALIZABLE

The result of each concurrently executing transaction is the same as if those transactions had been executed sequentially without any time overlap, under any circumstances. This property is called serializability. SERIALIZABLE is the strongest isolation level and allows for the safest data manipulation, but is relatively lower in performance. However, the order of sequential execution that produces the same result is not guaranteed at the transaction processing level.

<br/>

#### REPEATABLE READ

While a transaction is executing, there is no concern that the data being read will be changed by another transaction. Within the same transaction, the same data will always return the same value no matter how many times it is read. However, a phenomenon called Phantom Read may occur. In Phantom Read, data added or deleted by other transactions running concurrently can become visible during the middle of processing, changing the result of the operation.

<br/>

#### READ COMMITTED

For updates from other transactions, only committed data is always read. MVCC is one implementation that realizes READ COMMITTED. In addition to Phantom Read, a phenomenon called Non-Repeatable Read may occur, where the same data read within the same transaction may return different values each time.

<br/>

#### READ UNCOMMITTED

Even data that is being written by other processes is read. PHANTOM, NON-REPEATABLE READ, and a phenomenon called Dirty Read (reading incomplete data or data in the middle of calculation) occur. While there is a high possibility of corrupting data due to concurrent transaction operation, performance is correspondingly high.

> Transaction Isolation Level - Wikipedia [https://ja.wikipedia.org/wiki/Transaction_isolation_level](https://ja.wikipedia.org/wiki/%E3%83%88%E3%83%A9%E3%83%B3%E3%82%B6%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E5%88%86%E9%9B%A2%E3%83%AC%E3%83%99%E3%83%AB)

The Transaction Anomalies that can occur vary depending on the above transaction isolation levels.

<br/>

#### Dirty Read

***

Transaction T1 modifies data, and before it COMMITs or ROLLBACKs, Transaction T2 reads that data. If T1 then ROLLBACKs, T2 has read data that was not committed = data that doesn't exist.

<img src="image-20191118125351011.png" alt="image-20191118125351011" style="zoom:75%;" />

<br/>

#### Fuzzy Read (Non-Repeatable Read)

***

After Transaction T1 reads data, Transaction T2 modifies or deletes that data and COMMITs. When T1 then tries to read the data again, it detects that the data has been modified or deleted.

<img src="image-20191118125451710.png" alt="image-20191118125451710" style="zoom:75%;" />

<br/>

#### Phantom Read

***

Transaction T1 reads a set of data based on certain search conditions. Transaction T2 then creates data that satisfies those search conditions and COMMITs. When T1 performs the same search again with the same conditions, it obtains a different set of data than the first time.

<img src="image-20191118125508054.png" alt="image-20191118125508054" style="zoom:75%;" />

<br/>

#### Lost Update

***

Transaction T1 reads a data item, T2 updates the data item based on the previous read value, and T1 updates the data item based on its previous read value and commits. T2's update is overwritten by T1, so T2's Update is Lost - hence "Lost Update."

<img src="image-20191118125523779.png" alt="image-20191118125523779" style="zoom:75%;" />


This is the phenomenon where data that should have been updated is lost. I've heard it also called "last-write-wins" processing. So it doesn't feel as anomalous compared to other Anomalies. I think the message is: manage your transactions properly.

A concrete example: Assume a transaction for managing book inventory.

(1) Currently there are 90 books in stock, and there is a process that makes additional orders if stock falls below 100 books.

(2) [Tx2] Tx2 retrieves the current 90 books.

(3) [Tx1] Tx1 also retrieves the current 90 books.

(4) [Tx1] Processes the purchase of 10 books and updates inventory to 100 books.

<br/>

#### Write Skew

***

T1 reads x and y, then T2 reads x and y, writes x and commits. Then T1 writes y. If there is a constraint between x and y, a violation occurs. In other words, when two concurrent transactions each decide what to write based on reading data sets that overlap with what the other is writing (e.g., y=x+1), a state can be obtained that could not occur if one had executed before the other.

<img src="image-20191118125542982.png" alt="image-20191118125542982" style="zoom:75%;" />

<br/>

For concrete cases, look at "Black and White" and "Intersecting Data" cases to understand transaction behavior.

> ssi - postgresql wiki  https://wiki.postgresql.org/wiki/SSI

<br/>

#### Isolation Levels and Possible Transaction Anomalies

***

According to the ISO definition of transaction isolation levels, the presence or absence of the above three Transaction Anomalies is as follows. However, note that in actual DB engine implementations, there are cases where even READ COMMITTED doesn't produce Fuzzy Read.

<img src="image-20191118125604554.png" alt="image-20191118125604554" style="zoom:75%;" />

> A Critique of ANSI SQL Isolation Levels [https://arxiv.org/ftp/cs/papers/0701/0701157.pdf](https://arxiv.org/ftp/cs/papers/0701/0701157.pdf)

<br/>

#### Comparison Table of DB Engines and Transaction Isolation Levels

***

The isolation levels selectable in DB engines differ. When changing DB engines, it is necessary to understand the transaction isolation levels. The data retrieved may differ depending on the timing of SQL execution in transactions.

<br/>

| Isolation Level  | Oracle             | PostgreSQL         | MySQL                    |
| ---------------- | ------------------ | ------------------ | ------------------------ |
| SERIALIZABLE     | Available          | Available          | Available                |
| REPEATABLE READ  | Not Available      | Available          | Available (default)      |
| READ COMMITTED   | Available (default)| Available (default)| Available                |
| READ UNCOMMITTED | Not Available      | Available          | Available                |

<br/>

> MySQL :: MySQL 5.6 Reference Manual :: 13.3.6 SET TRANSACTION Syntax [https://dev.mysql.com/doc/refman/5.6/ja/set-transaction.html](https://dev.mysql.com/doc/refman/5.6/ja/set-transaction.html)

> POSTGRESQL: DOCUMENTATION: 11: 13.2. TRANSACTION ISOLATION HTTPS[://WWW.POSTGRESQL.ORG/DOCS/11/TRANSACTION-ISO.HTML#MVCC-ISOLEVEL-TABLE](https://www.postgresql.org/docs/11/transaction-iso.html#MVCC-ISOLEVEL-TABLE)

<br/>

#### Oracle Database

***

In Oracle Database, **SERIALIZABLE** and **READ COMMITTED** isolation levels are available.

READ COMMITTED requires prior understanding of read consistency using UNDO. This is a technology called MVCC (Multi-Version Concurrency Control). Oracle Database uses UNDO data to achieve consistency.

When a user modifies data, Oracle Database always creates an UNDO entry and writes it to the undo segment. The undo segment contains old values of data changed by uncommitted transactions and recently committed transactions. This means multiple versions of the same data at different points in time exist in the database.

<br/>

#### PostgreSQL/MySQL

***

All isolation levels are available.

The actual implementation differs for each DB engine. It appears that even when selecting `REPEATABLE READ` in PostgreSQL or MySQL, `Phantom Read` does not occur in their implementations.

> 13.2. Transaction Isolation [http://pgsql-jp.github.io/current/html/transaction-iso.html](http://pgsql-jp.github.io/current/html/transaction-iso.html)

<br/>

#### Testing Write Skew with SERIALIZABLE Isolation Level

***

> The result of each concurrently executing transaction is the same as if those transactions had been executed sequentially without any time overlap, under any circumstances.

No matter how many times I read this sentence about Serializable, I can never quite understand it, so I tested it hands-on.

#### How to Change

```sql
· Using SET statement (per session)
SET default_transaction_isolation TO 'isolation_level';

· Using SET statement (per transaction)
SET TRANSACTION ISOLATION LEVEL isolation_level;

· Using transaction control commands (per transaction)
Specify at transaction start
BEGIN ISOLATION LEVEL isolation_level;
START TRANSACTION ISOLATION LEVEL isolation_level;
```

#### Create Table/Data in Advance

```sql
drop table mytab;
CREATE TABLE mytab
(
  class int NOT NULL,
  value int NOT NULL
);
INSERT INTO mytab VALUES
(1, 10), (1, 20), (2, 100), (2, 200);
```

<br/>

| Session1                                        | Session2                                        |
| ----------------------------------------------- | ----------------------------------------------- |
| BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE; |                                                 |
| SELECT SUM(value) FROM mytab WHERE class = 1;   |                                                 |
| INSERT INTO mytab VALUES(2,30);                 |                                                 |
|                                                 | BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE; |
|                                                 | SELECT SUM(value) FROM mytab WHERE class = 2;   |
|                                                 | INSERT INTO mytab VALUES (1, 300);              |
|                                                 | commit;                                         |
| commit;                                         |                                                 |
| BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE; |                                                 |
| SELECT SUM(value) FROM mytab WHERE class = 1;   |                                                 |
| INSERT INTO mytab VALUES (2, 330);              |                                                 |
| COMMIT;                                         |                                                 |
| SELECT * FROM mytab;                            |                                                 |

<br/>

#### Session1

```sql
aurorapostdb=> select * from mytab;
 class | value
-------+-------
     1 |    10
     1 |    20
     2 |   100
     2 |   200
(4 rows)

aurorapostdb=>
aurorapostdb=> BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN
aurorapostdb=> SELECT SUM(value) FROM mytab WHERE class = 1;
 sum
-----
  30
(1 row)

aurorapostdb=> INSERT INTO mytab VALUES(2,30);
INSERT 0 1
aurorapostdb=>

```

<br/>

#### Session2

```sql
aurorapostdb=> BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN
aurorapostdb=> SELECT SUM(value) FROM mytab WHERE class = 2;
 sum
-----
 300
(1 row)

aurorapostdb=> INSERT INTO mytab VALUES (1, 300);
INSERT 0 1
aurorapostdb=> commit;
COMMIT
aurorapostdb=>

```

<br/>

#### **Session1**

```sql
# Executed in Session 2
aurorapostdb=> commit;
ERROR:  could not serialize access due to read/write dependencies among transactions
DETAIL:  Reason code: Canceled on identification as a pivot, during commit attempt.
HINT:  The transaction might succeed if retried.
aurorapostdb=> BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN
aurorapostdb=> SELECT SUM(value) FROM mytab WHERE class = 1;
 sum
-----
 330
(1 row)

aurorapostdb=> INSERT INTO mytab VALUES (2, 330);
INSERT 0 1
aurorapostdb=> COMMIT;
COMMIT
aurorapostdb=> SELECT * FROM mytab;
 class | value
-------+-------
     1 |    10
     1 |    20
     2 |   100
     2 |   200
     1 |   300
     2 |   330
(6 rows)

aurorapostdb=>
```

<br/>

**Differences Between Oracle and PostgreSQL Transactions**

***

I organized the differences in transactions between Oracle and PostgreSQL, which are both Read Committed but can produce different results for certain transactions.

> Organizing Transaction Differences Between Oracle and PostgreSQL | my opinion is my own https://zatoima.github.io/oracle-postgresql-transaction-different.html

### **References**

***

> Data Concurrency and Consistency [https://docs.oracle.com/cd/E57425_01/121/CNCPT/consist.htm](https://docs.oracle.com/cd/E57425_01/121/CNCPT/consist.htm)

> Chapter 18: Locks [https://www.oracle.com/technetwork/jp/database/articles/tsushima/tsm18-1610822-ja.html](https://www.oracle.com/technetwork/jp/database/articles/tsushima/tsm18-1610822-ja.html)

> SSI - PostgreSQL wiki https://wiki.postgresql.org/wiki/SSI
>
> About postgresql isolation - qiita https://qiita.com/kimullaa/items/ed12fa8f6cb993eee5cd
>
> Phantom reads don't occur but it's not serializable - that's PostgreSQL's repeatable read - qiita https://qiita.com/yuba/items/89496dda291edb2e558c
