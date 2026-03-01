---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Cancelling Queries in Redshift"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-query-cancellation
date: 2021-07-06
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

### Get PID

```sql
select pid, trim(starttime) as start, duration, trim(user_name) as user,substring (query,1,40) as querytxt
from stv_recents
where status = 'Running';
```

### Kill the PID

```sql
select pg_cancel_backend(16749);
```

Or:

```sql
cancel 16749;
```

An error message is output on the client side:

```sql
client 2 aborted in command 16 (SQL) of script 0; ERROR:  Query (570) cancelled on user's request
```

> https://docs.aws.amazon.com/redshift/latest/dg/r_CANCEL.html
> https://docs.aws.amazon.com/redshift/latest/dg/PG_CANCEL_BACKEND.html
