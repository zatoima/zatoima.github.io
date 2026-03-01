---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "PostgreSQLでバッファキャッシュ上にデータをのせる"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: postgres-extension-pg-prewarm-buffer-cache
date: 2021-12-29
featured: false
draft: false

---

pg_prewarmとpg_buffercacheで確認

### pg_prewarm

忘れがちだが、テーブルだけではなくインデックスも対象に出来る

```sql
create extension pg_prewarm;

SELECT
     pg_prewarm('t1', 'buffer', 'main')
    ,pg_prewarm('t2_delta', 'buffer', 'main')
    ,pg_prewarm('t1_PKEY', 'buffer', 'main')
    ; 
```

### pg_buffercache

```sql
create extension pg_buffercache;

select c.relname, count(*) as buffers
from pg_buffercache as b
inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
group by c.relname
order by 2 desc
LIMIT 30;
```

### 実行ログ

```sql
postgres=> SELECT
postgres->      pg_prewarm('t1', 'buffer', 'main')
postgres->     ,pg_prewarm('t2_delta', 'buffer', 'main')
postgres->     ,pg_prewarm('t1_PKEY', 'buffer', 'main')
postgres->     ; 
 pg_prewarm | pg_prewarm | pg_prewarm 
------------+------------+------------
    1818182 |     909091 |      54840
(1 row)

postgres=> select c.relname, count(*) as buffers
postgres-> from pg_buffercache as b
postgres-> inner join pg_class as c on b.relfilenode = pg_relation_filenode(c.oid) and b.reldatabase in (0, (select oid from pg_database where datname = current_database()))
postgres-> group by c.relname
postgres-> order by 2 desc
postgres-> LIMIT 30;
              relname              | buffers 
-----------------------------------+---------
 t1                                | 1818687
 t2_delta                          |  909091
 t1_idx                            |  426172
 t1_pkey                           |   54840
 pg_attribute                      |      60
 pg_toast_2619                     |      36
 pg_class                          |      13
 pg_proc                           |      12
 pg_statistic                      |      11
 pg_attribute_relid_attnum_index   |       9
 pg_proc_oid_index                 |       8
 pg_proc_proname_args_nsp_index    |       6
 pg_amop                           |       6
 pg_class_relname_nsp_index        |       5
 pg_amproc                         |       4
 pg_operator                       |       4
 pg_class_oid_index                |       4
 pg_statistic_relid_att_inh_index  |       4
 pg_index                          |       4
 pg_amop_opr_fam_index             |       4
 pg_operator_oid_index             |       4
 pg_type                           |       3
 pg_amop_fam_strat_index           |       3
 pg_type_oid_index                 |       3
 pg_operator_oprname_l_r_n_index   |       3
 pg_amproc_fam_proc_index          |       3
 pg_depend_reference_index         |       3
 pg_type_typname_nsp_index         |       3
 pg_auth_members_member_role_index |       2
 pg_cast_source_target_index       |       2
(30 rows)

postgres=> 

```

