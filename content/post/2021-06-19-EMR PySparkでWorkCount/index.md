---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "EMR PySparkでWorkCount"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","Redshift"]
url: aws-emr-spark-python-wordcount
date: 2021-06-19
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



### WorkCountするデータの準備

```
head -c 200m /dev/urandom > test.txt
hadoop fs -put test.txt /home/hadoop/data/
hadoop fs -ls /home/hadoop/data/
```

### 実行用PySparkのスクリプト

```python
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext
from pyspark.sql.session import SparkSession
from operator import add

sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

inputFile = "/home/hadoop/data/test.txt"
lines = sc.textFile(inputFile)
lines_nonempty = lines.filter( lambda x: len(x) > 0 )
counts = lines_nonempty.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
output = counts.collect()
for (word, count) in output:
    print("%s: %i" % (word, count))
sc.stop()
```

### 実行

```
spark-submit test.py
```

