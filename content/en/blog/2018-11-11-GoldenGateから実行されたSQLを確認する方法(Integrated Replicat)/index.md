---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Check SQL Executed from GoldenGate (Integrated Replicat)"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-check-exection-sql
date: 2018-11-11
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


GoldenGate internally executes SQL as well, and that information is stored in the Oracle Database shared pool.

Therefore, you can check what SQL is being executed by running the following SQL on the target side where the Replicat operates.

```sql
SELECT sql_id,
       plan_hash_value,
       sql_text,
       module,
       fetches,
       command_type,
       executions,
       first_load_time,
       last_active_time,
       action,
       service,
       is_bind_aware
FROM V$SQL
WHERE module='GoldenGate';
```

- Notes
  - The sql_text column of (g)v$sql is `VARCHAR2(1000)`, so for very long text, use SQL_FULLTEXT of CLOB type. Convert using dbms_lob.substr.
  - To check bind variable values, use v$sql_bind_capture.
