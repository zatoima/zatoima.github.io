---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Checking Redshift Skew Tables"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-skew-table-check
date: 2021-05-12
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



Use `amazon-redshift-utils`

```
git clone https://github.com/awslabs/amazon-redshift-utils.git
```

### Execute SQL

```
[ec2-user@bastin ~]$ psql -h redshift-cluster.xxxxx.ap-northeast-1.redshift.amazonaws.com -U awsuser -d tickit -p 5439 -f /home/ec2-user/amazon-redshift-utils-master/src/AdminScripts/table_inspector.sql
 schemaname | tablename | tableid | size_in_mb | has_dist_key | has_sort_key | has_col_encoding | ratio_skew_across_slices | pct_slices_populated
------------+-----------+---------+------------+--------------+--------------+------------------+--------------------------+----------------------
 public     | category  |  203866 |         56 |            1 |            1 |                1 |                        0 |                  100
 public     | date      |  203868 |         88 |            1 |            1 |                1 |                        0 |                  100
 public     | event     |  203871 |         72 |            1 |            1 |                1 |                        0 |                  100
 public     | listing   |  203873 |         88 |            1 |            1 |                1 |                        0 |                  100
 public     | sales     |  203875 |        104 |            1 |            1 |                1 |                        0 |                  100
 public     | users     |  203862 |        168 |            1 |            1 |                1 |                        0 |                  100
 public     | venue     |  203864 |         64 |            1 |            1 |                1 |                        0 |                  100
(7 rows)

```

### Column Descriptions

| Report Column            | Meaning                                                      |
| ------------------------ | ------------------------------------------------------------ |
| has_dist_key             | Indicates whether a distribution key exists for the table. 1 indicates the key exists, 0 indicates it does not. |
| has_sort_key             | Indicates whether a sort key exists for the table. 1 indicates the key exists, 0 indicates it does not. |
| has_col_encoding         | Indicates whether compression encoding is defined for any column in the table. 1 indicates encoding is defined for at least one column. 0 indicates no encoding is defined. |
| pct_skew_across_slices   | Percentage of data distribution skew. Smaller values indicate better results. |
| pct_slices_populated     | Percentage of slices populated. Larger values indicate better results. |
