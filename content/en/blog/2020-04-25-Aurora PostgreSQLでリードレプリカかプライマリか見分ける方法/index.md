---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Determine if an Aurora PostgreSQL Instance is a Read Replica or Primary"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-replica-master-check.html
date: 2020-04-25
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

If `session_id='MASTER_SESSION_ID'` appears in `server_id`, the instance is the primary.

```sql
postgres=> select server_id,session_id,highest_lsn_rcvd,cur_replay_latency_in_usec,now(),last_update_timestamp from aurora_replica_status();
     server_id     |    session_id     | highest_lsn_rcvd | cur_replay_latency_in_usec |              now              | last_update_timestamp
-------------------+-------------------+------------------+----------------------------+-------------------------------+------------------------
 aurorapostgresv11 | MASTER_SESSION_ID |                  |                            | 2020-04-24 13:44:30.808061+00 | 2020-04-24 13:44:29+00
(1 row)
```

> https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.BestPractices.html
>
> > Other Options for Getting the Host String
> >
> > An application can connect to all DB instances in the DB cluster and query the `aurora_replica_status` function to identify the cluster writer or find other reader nodes in the cluster.
