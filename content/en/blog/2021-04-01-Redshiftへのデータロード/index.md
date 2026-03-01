---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Loading Data into Redshift"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-dataload-from-s3.html
date: 2021-04-01
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



Assumes that IAM roles and the required IAM role attachments to the cluster are already complete.

### Upload the Load File to S3

```sh
aws s3 cp aozora_data.csv s3://xxxx/load/
```

The load file is about 6GB, approximately 87 million rows (Aozora Bunko text data).

```
[ec2-user@bastin ~]$ ls -lh aozora_data.csv
-rw-rw-r-- 1 ec2-user ec2-user 6.1G Dec 16  2012 aozora_data.csv
[ec2-user@bastin ~]$ wc -l aozora_data.csv
87701673 aozora_data.csv
```

### Create the Destination Table in Redshift

```sh
CREATE TABLE aozora_data(file VARCHAR(100),num INT,row INT,word TEXT,subtype1 VARCHAR(100),subtype2 VARCHAR(100),subtype3 VARCHAR(100),subtype4 VARCHAR(100),conjtype VARCHAR(30),conjugation VARCHAR(30),basic TEXT,ruby TEXT,pronunce TEXT );
```

### Execute Data Load

```sh
copy aozorabunko_data from 's3://xxxxx/load/aozora_data.csv'
iam_role 'arn:aws:iam::xxxxx:role/myRedshiftRole'
csv;
```

The above method is an anti-pattern and runs only on a single slice, failing to effectively utilize resources in Redshift's MPP architecture. As per the best practices below, it is preferable to split files and compress them before loading.

> Amazon Redshift Data Loading Best Practices - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/c_loading-data-best-practices.html

### Data Splitting

```
split -n 8 -d aozora_data.csv part-
```
