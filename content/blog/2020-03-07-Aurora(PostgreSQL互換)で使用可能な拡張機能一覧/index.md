---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora(PostgreSQL互換)で使用可能な拡張機能一覧"
subtitle: ""
summary: " "
tags: ["Aurora","AWS","PostgreSQL"]
categories: ["Aurora","AWS","PostgreSQL"]
url: aws-aurora-postgres-extention-list
date: 2020-03-07
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



明示的なドキュメントは無かったが、RDS(PostgreSQL)と同等の方法で取得可能なはず。

> Amazon RDS for PostgreSQL のバージョンと拡張機能 https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts

使用可能な拡張機能はパラメータグループに定義されているのでそこから確認可能。

#### バージョン

***

```sh
postgres=> select aurora_version();
 aurora_version 
----------------
 2.3.5
(1 row)

postgres=> select version();
                                   version                                   
-----------------------------------------------------------------------------
 PostgreSQL 10.7 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.9.3, 64-bit
(1 row)
```

#### 拡張機能の表示

***

```sh
postgres=> show rds.extensions;

rds.extensions                                   
--------------------------------------------------------------------------------------------------------
amcheck,address_standardizer,address_standardizer_data_us,apg_plan_mgmt,aurora_stat_utils,aws_commons,aws_ml,aws_s3,bloom,btree_gin,btree_gist,chkpass,citext,cube,dblink,dict_int,dict_xsy
n,earthdistance,fuzzystrmatch,hll,hstore,hstore_plperl,intagg,intarray,ip4r,isn,log_fdw,ltree,orafce,pgaudit,pgcrypto,pgrouting,pgrowlocks,pgstattuple,pg_buffercache,pg_freespacemap,pg_hin
t_plan,pg_similarity,pg_prewarm,pg_repack,pg_stat_statements,pg_trgm,pg_visibility,plcoffee,plls,plperl,plpgsql,plprofiler,pltcl,plv8,postgis,postgis_tiger_geocoder,postgis_topology,postgr
es_fdw,prefix,sslinfo,tablefunc,test_parser,tsearch2,tsm_system_rows,tsm_system_time,unaccent,uuid-ossp
(1 row)
```

もしくは

```sh
aws rds describe-engine-default-cluster-parameters --db-parameter-group-family aurora-postgresql10
```

もしくは

```sh
select * FROM pg_available_extensions order by 1;

postgres=> select * FROM pg_available_extensions order by 1;
             name             | default_version | installed_version |                                                       comment                                                       
------------------------------+-----------------+-------------------+---------------------------------------------------------------------------------------------------------------------
 address_standardizer         | 2.4.4           |                   | Used to parse an address into constituent elements. Generally used to support geocoding address normalization step.
 address_standardizer_data_us | 2.4.4           |                   | Address Standardizer US dataset example
 amcheck                      | 1.0             |                   | functions for verifying relation integrity
 apg_plan_mgmt                | 1.0.1           |                   | Amazon Aurora with PostgreSQL compatibility Query Plan Management
 aurora_stat_utils            | 1.0             |                   | Statistics utility functions
 aws_commons                  | 1.0             |                   | Common data types across AWS services
 aws_s3                       | 1.0             |                   | AWS S3 extension for importing data from S3
```

でrds.extensionsを確認する。pg_available_extensionsが一番見やすいかもしれない。

#### 対応している拡張機能一覧

***

| Extention Module             |
| ---------------------------- |
| amcheck                      |
| address_standardizer         |
| address_standardizer_data_us |
| apg_plan_mgmt                |
| aurora_stat_utils            |
| aws_commons                  |
| aws_ml                       |
| aws_s3                       |
| bloom                        |
| btree_gin                    |
| btree_gist                   |
| chkpass                      |
| citext                       |
| cube                         |
| dblink                       |
| dict_int                     |
| dict_xsyn                    |
| earthdistance                |
| fuzzystrmatch                |
| hll                          |
| hstore                       |
| hstore_plperl                |
| intagg                       |
| intarray                     |
| ip4r                         |
| isn                          |
| log_fdw                      |
| ltree                        |
| orafce                       |
| pgaudit                      |
| pgcrypto                     |
| pgrouting                    |
| pgrowlocks                   |
| pgstattuple                  |
| pg_buffercache               |
| pg_freespacemap              |
| pg_hint_plan                 |
| pg_similarity                |
| pg_prewarm                   |
| pg_repack                    |
| pg_stat_statements           |
| pg_trgm                      |
| pg_visibility                |
| plcoffee                     |
| plls                         |
| plperl                       |
| plpgsql                      |
| plprofiler                   |
| pltcl                        |
| plv8                         |
| postgis                      |
| postgis_tiger_geocoder       |
| postgis_topology             |
| postgres_fdw                 |
| prefix                       |
| sslinfo                      |
| tablefunc                    |
| test_parser                  |
| tsearch2                     |
| tsm_system_rows              |
| tsm_system_time              |
| unaccent                     |
| uuid-ossp                    |

