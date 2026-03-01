---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Estimated pg_dump and pg_restore Times for Aurora PostgreSQL"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","PostgreSQL"]
categories: ["AWS","Aurora","PostgreSQL"]
url: aws-aurora-postgresql-pg_dump_pg_restore_time.html
date: 2020-11-30
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

I measured the time to pg_dump and pg_restore Aurora PostgreSQL data to/from a bastion server on EC2. Note that network bandwidth and disk I/O performance vary by instance type, disk size, and IOPS settings, so treat these as rough estimates.

#### Results

| No   | Test Pattern        | DB Name  | DB Size (GB) | Data Content                                     | Start Time | End Time | Duration |
| ---- | -------------- | -------- | ------------- | -------------------------------------------- | -------- | -------- | -------- |
| 1    | pg_dump        | postgres | 729GB         | Aozora Bunko text data                       | 14:31:33 | 19:01:44 | 4:30:11  |
| 2    | (parallelism=1) | tpch    | 45GB          | HammerDB TPC-H data                          | 12:59:44 | 13:34:22 | 0:34:38  |
| 3    |                | tpcc     | 118GB         | HammerDB TPC-C data                          | 13:43:07 | 14:26:32 | 0:43:25  |
| 4    |                | blob     | 98GB          | Binary in bytea (25MB file × 4000 files)     | 9:26:14  | 12:38:51 | 3:12:37  |
| 5    | pg_dump        | postgres | 729GB         | Same as above                                | 18:30:26 | 19:59:33 | 1:29:07  |
| 6    | (parallelism=8) | tpch    | 45GB          | Same as above                                | 18:11:08 | 18:28:35 | 0:17:27  |
| 7    |                | tpcc     | 118GB         | Same as above                                | 13:16:13 | 13:44:05 | 0:27:52  |
| 8    |                | blob     | 98GB          | Same as above                                | 20:01:51 | 21:04:38 | 1:02:47  |
| 9    | pg_restore     | postgres | 729GB         | Same as above                                | 21:09:34 | 0:26:25  | 3:16:51  |
| 10   | (parallelism=8) | tpch    | 45GB          | Same as above                                | 20:58:25 | 21:06:24 | 0:07:59  |
| 11   |                | tpcc     | 118GB         | Same as above                                | 20:46:58 | 20:56:44 | 0:09:46  |
| 12   |                | blob     | 98GB          | Same as above                                | 12:45:23 | 13:07:43 | 0:22:20  |

#### pg_dump Command with Parallelism 1

```sh
pg_dump -h aurorapgsqlv1.cluster-xxxx.ap-northeast-1.rds.amazonaws.com -U postgres -Fc postgres > postgres.dump
```

#### pg_dump Command with Parallelism 8

```sh
pg_dump -h aurorapgsqlv1.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -j 8 -U postgres -F d -f /data/postgres postgres
```

#### pg_restore Command with Parallelism 8

```sh
pg_restore -h aurorapgsqlv1.cluster-xxxxx.ap-northeast-1.rds.amazonaws.com -U postgres -j 8 -d postgres postgres.dump
```
