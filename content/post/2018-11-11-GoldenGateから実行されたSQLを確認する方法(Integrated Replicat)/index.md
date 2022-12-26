---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GoldenGateから実行されたSQLを確認する方法(Integrated Replicat)"
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


GoldenGateの場合においてもSQLが内部的に実行されており、Oracle Databaseの共有プールに情報が格納されている。

なので、Replicatが動作するターゲット側で下記SQLを実行してどのようなSQLが実行されているか確認出来る。

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

- 注意事項
  - (g)v$sqlのsql_text列は「VARCHAR2(1000)」のため、長過ぎるものはCLOB型のSQL_FULLTEXTで出力。dbms_lob.substrで変換。
  - バインド変数値を確認する場合は、v$sql_bind_captureから
