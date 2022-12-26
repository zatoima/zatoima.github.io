---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EMR Pysparkでデータフレームを縦に連結してデータを増幅させる"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","EMR"]
url: aws-emr-spark-dataframe-data.html
date: 2021-04-13
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



手っ取り早くPysparkのデータフレームのデータを増やしたい場合に、データフレームを縦方向に結合することで増やそうと思った時に調べたメモ。S3上のCSVを読み込んだ後に、複数データフレームを一つのデータフレームに読み込んでいるだけ。

```python
from pyspark.sql.types import *
from functools import reduce
from pyspark.sql import DataFrame

schema = StructType([
        StructField('file', StringType(), False),
        StructField('num', IntegerType(), False),
        StructField('row', IntegerType(), False),
        StructField('word', StringType(), False),
        StructField('subtype1', StringType(), False),
        StructField('subtype2', StringType(), False),
        StructField('subtype3', StringType(), False),
        StructField('subtype4', StringType(), False),
        StructField('conjtype', StringType(), False),
        StructField('conjugation', StringType(), False),
        StructField('basic', StringType(), False),
        StructField('ruby', StringType(), False),
        StructField('pronunce', StringType(), False)
     ])

df1 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df2 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df3 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df4 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df5 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df6 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df7 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df8 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df9 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)
df10 = spark.read.csv(f's3://xxxxx/aozora_data.csv', schema=schema, header=True)

df_union=reduce(DataFrame.unionByName, [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10])
df_union.count()
```

