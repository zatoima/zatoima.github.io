---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Unloading Data from Redshift to S3"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-data-unload-redshift-to-s3.html
date: 2021-04-20
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

# Parallel Mode On

- Files are generated in S3 per node slice
- Can unload at high speed across the number of node slices

```sql
unload ('select * from unloadtest')
to 's3://dataforrs/test20210405/unloadtest_'
iam_role 'arn:aws:iam::xxxxx:role/myRedshiftRole'
header
format csv
gzip
allowoverwrite;
```

- Log

```
mydb=# unload ('select * from unloadtest')
mydb-# to 's3://unloadtest/test20210405/unloadtest_'
mydb-# iam_role 'arn:aws:iam::xx:role/myRedshiftRole'
mydb-# header
mydb-# format csv
mydb-# gzip
mydb-# allowoverwrite;
INFO:  UNLOAD completed, 87701667 record(s) unloaded successfully.
UNLOAD
Time: 38214.953 ms (00:38.215)


 [ec2-user@bastin ~]$ aws s3 ls s3://dataforrs/test20210405/
 2021-04-05 13:14:56  339563139 unloadtest_0000_part_00.gz
 2021-04-05 13:14:56  339528727 unloadtest_0001_part_00.gz
 2021-04-05 13:14:56  339460977 unloadtest_0002_part_00.gz
 2021-04-05 13:14:56  339543307 unloadtest_0003_part_00.gz
 [ec2-user@bastin ~]$
```

# Parallel Mode Off

- Explicitly specify `parallel off`
- Writes to a single file so processes serially. Naturally slower than parallel mode as it cannot leverage MPP advantages.

```sql
unload ('select * from unloadtest')
to 's3://dataforrs/test20210406/unloadtest_'
iam_role 'arn:aws:iam::xxxx:role/myRedshiftRole'
header
format csv
gzip
parallel off
allowoverwrite;
```

- Log

```
mydb=# unload ('select * from unloadtest')
mydb-# to 's3://dataforrs/test20210406/unloadtest_'
mydb-# iam_role 'arn:aws:iam::xxxx:role/myRedshiftRole'
mydb-# header
mydb-# format csv
mydb-# gzip
mydb-# parallel off
mydb-# allowoverwrite;
INFO:  UNLOAD completed, 87701667 record(s) unloaded successfully.
UNLOAD
Time: 151199.736 ms (02:31.200)
mydb=#

[ec2-user@bastin ~]$ aws s3 ls s3://dataforrs/test20210406/
2021-04-05 13:19:18 1382206482 unloadtest_000.gz
[ec2-user@bastin ~]$
```

# Reference

> Unloading data to Amazon S3 - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/t_Unloading_tables.html
