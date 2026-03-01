---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Differences in char/varchar Byte vs. Character Count Between Oracle and PostgreSQL (+Redshift)"
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

The argument for char and varchar specifies byte count in Oracle, whereas in PostgreSQL it specifies character count. In a UTF-8 Oracle environment, char(10) can only store 3 multi-byte characters. In PostgreSQL, char(10) can store 10 characters. Note that this incompatibility is not converted by ora2pg or SCT (Schema Conversion Tool).

### Common to Oracle/PostgreSQL

```sql
create table chartest(a char(10));
```

### PostgreSQL

Insert 10 full-width characters into a char(10) column and check length and byte count.

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
#Pattern that exceeds character count
postgres> insert into chartest values('１２３４５６７８９あい');
value too long for type character(10)

Time: 0.004s
postgres>
```

> https://www.postgresql.jp/document/11/html/datatype-character.html
>
> SQL defines two primary character types: character varying(n) and character(n), where n is a positive integer. Both of these types can store strings up to n characters (not bytes) in length.

### Oracle

Similarly, insert 10 bytes of data and check.

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
> Oracle Built-in Data Types

### Addendum: Redshift

I assumed Redshift, being PostgreSQL-based, would also use character count — but when I checked the manual to be sure, it turned out to use byte units. Be careful.

> https://docs.aws.amazon.com/redshift/latest/dg/r_Character_types.html
>
> The CHAR and VARCHAR data types are defined in terms of bytes, not characters. A CHAR column can contain only single-byte characters. Therefore, a CHAR(10) column can contain a string with a maximum length of 10 bytes. VARCHAR can contain multibyte characters (up to a maximum of four bytes per character). For example, a VARCHAR(12) column can contain 12 single-byte characters, 6 two-byte characters, 4 three-byte characters, or 3 four-byte characters.
