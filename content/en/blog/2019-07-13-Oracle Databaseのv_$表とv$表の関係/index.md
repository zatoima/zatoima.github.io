---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "The Relationship Between V_$ Views and V$ Views in Oracle Database"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-dynamic-performance-view.html
date: 2019-07-13
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



### Introduction

**Dynamic performance views (V$ views)** are special views that the database server continuously updates while the database is running. Oracle Database's dynamic performance views are outstanding in their variety compared to other databases.

When accessing them, you issue SELECT statements against `V$ views`, but occasionally in various documents you see the notation "V_$ views". For example, in the AWS DMS manual there is this statement:

> https://docs.aws.amazon.com/ja_jp/dms/latest/userguide/CHAP_Source.Oracle.html
>
> When granting permissions, use the actual name of the object, not a synonym for the object. For example, use V_$OBJECT with the underscore, not V$OBJECT without the underscore.

Also, when granting permissions to reference dictionary views, you need to specify `V_$LICENSE` **with an underscore**.

```sql
SQL> GRANT SELECT ON SYS.V_$LICENSE TO rivus;

Grant succeeded.
```

### What Is a V_$ View?

As stated in the manual below, technically, V$ views are **PUBLIC synonyms**. In the case of V$ARCHIVE, V_$ARCHIVE is the `actual view` and V$ARCHIVE is the `synonym`. When granting permissions, you must grant permissions to the actual view rather than the synonym, which is why you need to include the underscore as noted above.

> https://docs.oracle.com/cd/E16338_01/server.112/b56311/dynviews_1001.htm
>
> The actual dynamic performance views are identified by the prefix `V_$`. Public synonyms for these views have the prefix `V$`. Database administrators and other users should access only the `V$` objects, not the `V_$` objects.

The actual verification result is as follows:

```sql
SQL> set pages 2000 lin 2000
col OWNER for a10
col SYNONYM_NAME for a15
col TABLE_OWNER for a15
col TABLE_NAME for a15

select OWNER,SYNONYM_NAME,TABLE_OWNER,TABLE_NAME from ALL_SYNONYMS where TABLE_NAME like 'V_$ARCHIVE';
SQL> SQL> SQL> SQL> SQL> SQL>
OWNER      SYNONYM_NAME    TABLE_OWNER     TABLE_NAME
---------- --------------- --------------- ---------------
PUBLIC     V$ARCHIVE       SYS             V_$ARCHIVE
```
