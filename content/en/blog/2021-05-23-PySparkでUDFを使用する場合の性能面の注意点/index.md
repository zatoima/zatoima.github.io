---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Performance Considerations When Using UDFs in PySpark"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","EMR"]
url: aws-emr-spark-python-udf-performance
date: 2021-05-23
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



Note that <u>communication round trips occur between Python and JVM</u>.



Reference: O'Reilly Japan - Learning Spark https://www.oreilly.co.jp/books/9784873117348/

> 3.3 Accelerating PySpark with DataFrame
>
> What makes DataFrame and Catalyst Optimizer (and Project Tungsten) stand out is that they improve PySpark query performance compared to non-optimized RDD queries. As shown in the figure below, before the advent of DataFrame, it was not uncommon for the speed of Python queries against RDD to be less than half that of the same Scala queries. This query performance degradation is usually due to the overhead of communication between Python and JVM.
>
> ![image-20210524085439906](image-20210524085439906.png)
>
> The advent of DataFrame not only significantly improved performance in Python, but also made the performance of Python, Scala, SQL, and R equivalent. Even though PySpark is significantly faster with DataFrame, don't forget that there are exceptions. The most common is when using Python UDFs, which create communication round trips between Python and JVM. This can be a worst-case scenario similar to performing operations on RDDs, so caution is needed.
>
> The Catalyst Optimizer codebase is written in Scala, but Python can also benefit from Spark's performance optimizations. Essentially, the code that significantly speeds up queries in DataFrame in PySpark is merely about 2,000 lines of wrappers written in Python.
>
