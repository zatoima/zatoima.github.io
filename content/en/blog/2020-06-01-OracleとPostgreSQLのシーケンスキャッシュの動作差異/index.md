---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Behavioral Differences in Sequence Cache Between Oracle and PostgreSQL"
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



A note on the behavioral differences when using sequence cache between Oracle and PostgreSQL. Since PostgreSQL's `cache` defaults to 1, you might think the numbering would be similar unless changed. However, in practice that is not the case. This article describes the caveats when changing PostgreSQL's cache value.

### Create Sequences

Both Oracle and PostgreSQL sequences start at "1" with a cache of "20".

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

### Oracle Behavior

##### Session A

```sql
select oraseq1.nextval from dual;
```

The sequence value is naturally "1".

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

When getting a sequence from a different session in Oracle, nextval returns "2". This is where Oracle and PostgreSQL differ.

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

### PostgreSQL Behavior

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

### Results

#### Sequence Values When nextval Is Executed on a Sequence Starting at 1 with Cache 20

The results are as follows. (Oracle assumes no ORDER option specified.)

| Execution Order | Session   | Oracle | PostgreSQL |
| --------------- | --------- | ------ | ---------- |
| 1st             | Session A | 1      | 1          |
| 2nd             | Session B | 2      | 21         |
| 3rd             | Session A | 3      | 2          |

### Conclusion

In Oracle, sequence gaps generally don't occur without specific events, but in PostgreSQL, changing the cache value from its default can easily cause them. **Sequences should be used to guarantee uniqueness, not consecutive numbering.** In fact, even with caching, guaranteeing consecutive numbering should be difficult in Oracle too — if an Oracle instance crashes or the sequence is aged out from the shared pool, the cached values are lost.

As noted in the manual, sequences cannot be used for gap-free numbering. Rolling back a transaction does not roll back nextval or setval, creating gaps. Also, cached values stored in memory are lost upon restart.

> - 9.17. Sequence Manipulation Functions https://www.postgresql.jp/document/13/html/functions-sequence.html
>   - Therefore, PostgreSQL sequence objects *cannot be used to obtain gap-free sequences*.
> - CREATE SEQUENCE https://www.postgresql.jp/document/13/html/sql-createsequence.html
>   - Because calls to `nextval` and `setval` are never rolled back, sequence objects cannot be used if "gap-free" assignment of sequence numbers is needed.
