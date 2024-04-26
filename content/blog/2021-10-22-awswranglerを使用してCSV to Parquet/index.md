---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "awswranglerを使用してCSV to Parquet"
subtitle: ""
summary: " "
tags: ["Athena","Glue"]
categories: ["Athena","Glue"]
url: aws-athena-glue-awswrangler-csv-to-parquet
date: 2021-10-22
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

### テスト用CSVの作成

```sh
cat << EOF > testdata.csv
id,name,comment
"1","test1","ゎぶばあちあぬナクバ"
"2","test2","がマうひバぴじクハぺ"
"3","test3","スみでてゥあッあけげ"
EOF
```

#### S3のフォルダのクリーンアップ

awswranglerのオプションでクリーンアップ出来たと思うが、手動で事前に削除

```sh
aws s3 rm s3://202110test/pq/
```

### CSV→Parquetに変換

```sh
import awswrangler as wr
import pandas as pd

#変換
df = pd.read_csv('./testdata.csv')

wr.s3.to_parquet(
    df=df,
    path='s3://202110test/pq/',
    dataset=True,
    partition_cols=['id']
)
```

### Athenaでデータベース、データカタログの作成

コンソールから実施を想定

```sh
DROP TABLE `catalogtest`.`testdata`;

CREATE EXTERNAL TABLE `catalogtest`.`testdata`(
  `id` string, 
  `name` string, 
  `comment` string
  )
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://202110test/pq/'
TBLPROPERTIES (
  'classification'='parquet', 
  'compressionType'='none', 
  'objectCount'='1', 
  'typeOfData'='file')

MSCK REPAIR TABLE catalogtest.testdata;

select name,comment from testdata;

```

athenacliを使用してAthenaのクエリを実行

```sh
athenacli catalogtest -e 'select name,comment from testdata'
```

```sh
[ec2-user@ip-10-0-1-31 pyarrow]$ athenacli catalogtest -e 'select name,comment from testdata'
name,comment
test1,ゎぶばあちあぬナクバ
test3,スみでてゥあッあけげ
test2,がマうひバぴじクハぺ
```

