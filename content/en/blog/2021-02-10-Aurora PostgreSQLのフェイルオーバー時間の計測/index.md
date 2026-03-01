---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Measuring Aurora PostgreSQL Failover Time"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-failover-time-test
date: 2021-02-10
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



# Introduction

While looking at the Aurora FAQ, I found that failover completes within 30 seconds, so I decided to verify this.

> https://aws.amazon.com/jp/rds/aurora/faqs/
>
> Q: What happens during a failover and how long does it take?
>
> Failover is automatically handled by Amazon Aurora so that your applications can resume database operations as quickly as possible without manual administrative intervention.
>
> - If you have an Amazon Aurora Replica in the same or a different Availability Zone, when failing over, Amazon Aurora flips the canonical name record (CNAME) for your DB Instance to point at the healthy replica, which in turn is promoted to become the new primary. Start-to-finish, failover typically completes within 30 seconds.

# Preparation

Create a test table:

```
create table failovertest(id serial,time timestamp);
```

A rough test script. Exceptions are caught and passed so the test continues even if a connection error occurs.

```python
import psycopg2
import psycopg2.extras
import time
import datetime

for i in range(20000):
  try:
    dt_now = datetime.datetime.now()
    conn = psycopg2.connect("host=xxxxxx.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com port=5432 dbname=xxx user=xxx password=xx")
    cur = conn.cursor()
    cur.execute("insert into failovertest (time) values (current_timestamp)")
    print(dt_now)
    time.sleep(1)
    conn.commit()
    cur.close()
    conn.close()
  except:
    pass
```

# Results

The result was an `average of 12 seconds`.

|         | Start    | End      | Duration |
| ------- | -------- | -------- | -------- |
| 1st     | 2:20:40  | 2:20:53  | 0:00:13  |
| 2nd     | 2:23:19  | 2:23:30  | 0:00:11  |
| 3rd     | 2:24:37  | 2:24:53  | 0:00:16  |
| 4th     | 11:29:03 | 11:29:13 | 0:00:10  |
| 5th     | 11:30:06 | 11:30:18 | 0:00:12  |
