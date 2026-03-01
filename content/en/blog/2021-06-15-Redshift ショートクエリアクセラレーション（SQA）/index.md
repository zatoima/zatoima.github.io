---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshift Short Query Acceleration (SQA)"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-short-query-acceleration-sqa
date: 2021-06-15
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



  <iframe src="//www.slideshare.net/slideshow/embed_code/key/Efsko7wlMOc3lQ?startSlide=45" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/20210127-aws-black-belt-online-seminar-amazon-redshift" title="20210127 AWS Black Belt Online Seminar Amazon Redshift 運用管理" target="_blank">20210127 AWS Black Belt Online Seminar Amazon Redshift Operations Management</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>

# What is Short Query Acceleration (SQA)?


- A feature that runs some queries with short execution times in a dedicated queue with priority over queries with longer execution times

  - Avoids situations where short queries are blocked while long queries are running



- By default, WLM dynamically assigns the SQA maximum execution time value based on analysis of the cluster's workload

  - Users don't need to be particularly aware of this

# Verification

- The following query shows the dynamically assigned execution time for short queries

  ```sql
  select least(greatest(percentile_cont(0.7)
  within group (order by total_exec_time / 1000000) + 2, 2), 20)
  from stl_wlm_query
  where userid >= 100
  and final_state = 'Completed';
  ```

  ```sql
  mydb=# tpcds_100gb=# select least(greatest(percentile_cont(0.7)
  mydb(# tpcds_100gb(# within group (order by total_exec_time / 1000000) + 2, 2), 20)
  mydb(# tpcds_100gb-# from stl_wlm_query
  mydb(# tpcds_100gb-# where userid >= 100
  mydb(# tpcds_100gb-# and final_state = 'Completed';
  mydb(#  least
  mydb(# -------
  mydb(#    8.0
  mydb(# (1 row)
  ```

- Verify enabled status

  ```sql
  select * from stv_wlm_service_class_config
  where service_class = 14;
  ```

  ```sql
  mydb=# select * from stv_wlm_service_class_config
  mydb-# where service_class = 14;
  -[ RECORD 1 ]------------+-----------------------------------------------------------------
  service_class            | 14
  queueing_strategy        | Predicted Time queue policy
  num_query_tasks          | 6
  target_num_query_tasks   | 6
  evictable                | true
  eviction_threshold       | 0
  query_working_mem        | 264
  target_query_working_mem | 264
  min_step_mem             | 5
  name                     | Short query queue
  max_execution_time       | 0
  user_group_wild_card     | false
  query_group_wild_card    | false
  concurrency_scaling      | off
  query_priority           | Normal
  ```



- Check queries that passed through each query queue (service class)



  ```sql
  select final_state, service_class, count(*), avg(total_exec_time),
  percentile_cont(0.9) within group (order by total_queue_time), avg(total_queue_time)
  from stl_wlm_query where userid >= 100 group by 1,2 order by 2,1;
  ```

  ```sql
  mydb=# select final_state, service_class, count(*), avg(total_exec_time),
  mydb-# percentile_cont(0.9) within group (order by total_queue_time), avg(total_queue_time)
  mydb-# from stl_wlm_query where userid >= 100 group by 1,2 order by 2,1;
     final_state    | service_class | count |   avg   | percentile_cont |  avg
  ------------------+---------------+-------+---------+-----------------+--------
   Completed        |           100 |   283 | 1789760 |        550958.6 | 421287
  (1 row)
  ```




- Information about queries successfully completed by SQA

  ```sql
  select a.queue_start_time, a.total_exec_time,trim(querytxt)
  from stl_wlm_query a, stl_query b
  where a.query = b.query and a.service_class = 14 and a.final_state = 'Completed'
  order by a.queue_start_time desc limit 1;
  ```

  ```sql
  mydb=# select a.queue_start_time, a.total_exec_time,trim(querytxt)
  mydb-# from stl_wlm_query a, stl_query b
  mydb-# where a.query = b.query and a.service_class = 14 and a.final_state = 'Completed'
  mydb-# order by a.queue_start_time desc limit 1;
        queue_start_time      | total_exec_time |  btrim
   2021-06-11 12:38:23.935373 |         1983019 | with /* TPC-DS query27a.tpl 0.16 */ results as (select i_item_id, s_state, 0 as g_state, ss_quantity agg1, ss_list_price agg2, ss_coupon_amt agg3, ss_sales_price agg4 from store_sales, customer_demographics, date_dim,
  store, item where ss_sold_date_sk = d_date_sk and ss_item_sk = i_item_sk and ss_store_sk = s_store_sk and ss_cdemo_sk = cd_demo_sk and cd_gender = 'F' and cd_marital_status = 'S' and cd_education_status = 'Primary' and d_year = 1999 and s_state in ('FL','NC', 'MN',
  'CO', 'MI', 'SC') ) select i_item_id, s_state, g_state, agg1, agg2, agg3, agg4 from ( select i_item_id, s_state, 0 as g_state, avg(agg1) agg1, avg(agg2) agg2, avg(agg3) agg3, avg(agg4) agg4 from results group by i_item_id, s_state union all select i_item_id, NULL AS
   s_state, 1 AS g_state, avg(agg1) agg1, avg(agg2) agg2, avg(agg3) agg3, avg(agg4) agg4 from results group by i_item_id union all select NULL AS i_item_id, NULL as s_state, 1 as g_state, avg(agg1) agg1, avg(agg2) agg2, avg(agg3) agg3, avg(agg4) agg4 from results ) fo
  o order by i_item_id, s_state limit 100;
  (1 row)

  ```
