---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshiftのskew tableを確認する"
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



`amazon-redshift-utils`を使用する

```
git clone https://github.com/awslabs/amazon-redshift-utils.git
```

### SQL実行

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

### 列の説明

| レポート項目           | 意味                                                         |
| ---------------------- | ------------------------------------------------------------ |
| has_dist_key           | テーブルに分散キーが存在するかどうかを示します。  1 はキーが存在することを示し、 0 はキーが存在しないことを示します。 |
| has_sort_key           | テーブルにソートキーが存在するかどうかを示します。  1 はキーが存在することを示し、 0 はキーが存在しないことを示します。 |
| has_col_encoding       | テーブルのいずれかの列に対して圧縮エンコードが定義されているかどうかを示します。  1 は、少なくとも 1 つの列にエンコードが定義されていることを示します。 0 は、エンコードが定義されていないことを示します。 |
| pct_skew_across_slices | データ分散スキューの割合。値が小さいほど結果は良好です。     |
| pct_slices_populated   | 入力されているスライスの割合。値が大きいほど結果は良好です。 |