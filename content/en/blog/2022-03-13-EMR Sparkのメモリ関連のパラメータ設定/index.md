---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Memory-Related Parameter Settings for EMR Spark"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","EMR"]
url: aws-emr-memory-parameter-settiong
date: 2022-03-13
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



### Spark Overview

Prerequisite concepts such as Executors and Partitions for Spark components:

- [Apache Sparkの構成要素、概要、用語について \| my opinion is my own](https://zatoima.github.io/aws-emr-spark-concept-component.html)
- [Spark on EMRの基礎をおさらいする \- Qiita](https://qiita.com/uryyyyyyy/items/34f3d228f339b32e6fb0?utm_source=pocket_mylist)

### Spark Memory Management Overview

- [Amazon EMR で Apache Spark アプリケーションのメモリをうまく管理するためのベストプラクティス \| Amazon Web Services ブログ](https://aws.amazon.com/jp/blogs/news/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/)

![image-20220203161417108](image-20220203161417108.png)

### Memory Management Parameters

Calculations for each parameter based on instance type and node count when `spark.dynamicAllocation.enabled` is set to `False`, as described in the blog above. The calculation formulas are embedded in [this Excel file](https://github.com/zatoima/zatoima.github.io/blob/master/content/post/2022-03-13-EMR%20Spark%E3%81%AE%E3%83%A1%E3%83%A2%E3%83%AA%E9%96%A2%E9%80%A3%E3%81%AE%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E8%A8%AD%E5%AE%9A/Spark%E3%83%A1%E3%83%A2%E3%83%AA%E8%A8%88%E7%AE%97%E3%83%A1%E3%83%A2.xlsx). By changing the yellow cells to match each instance type and actual environment, calculations should be done automatically.

This should only be used as initial sizing and should be tuned appropriately. In particular, the number of partitions should be determined by actually running the job.

| Instance type                                               | r5.12xlarge | m5.8xlarge |
| ----------------------------------------------------------- | ----------- | ---------- |
| vCPU                                                        | 48          | 32         |
| Memory                                                      | 384         | 128        |
| Node count                                                  | 5           | 5          |
| spark.executor.cores: Number of virtual cores per executor  | 5           | 5          |
| spark.executor.memory: Memory size used by Executor         | 9g          | 6g         |
| spark.yarn.executor.memoryOverhead: Overhead memory size for Executor | 1g   | 1g         |
| spark.driver.memory: Memory size for Driver                 | 9g          | 6g         |
| spark.driver.cores: Number of virtual cores for Driver      | 5           | 5          |
| spark.executor.instances: Number of Executors per instance  | 44          | 29         |
| spark.default.parallelism: Default value for number of Partitions | 440    | 290        |

### Other Parameters

For other parameters, refer to the parameters listed in the blog and the Spark manual, and configure what is needed.

```json
[
  {
    "Classification": "yarn-site",
    "Properties": {
      "yarn.nodemanager.vmem-check-enabled": "false",
      "yarn.nodemanager.pmem-check-enabled": "false"
    }
  },
  {
    "Classification": "spark",
    "Properties": {
      "maximizeResourceAllocation": "false"
    }
  },
  {
    "Classification": "spark-defaults",
    "Properties": {
      "spark.driver.memory": "39G",
      "spark.driver.cores": "5",
      "spark.executor.memory": "39G",
      "spark.executor.cores": "5",
      "spark.executor.instances": "14",
      "spark.executor.memoryOverhead": "5G",
      "spark.driver.memoryOverhead": "5G",
      "spark.default.parallelism": "140",
      "spark.sql.shuffle.partitions": "140",

      "spark.network.timeout": "800s",
      "spark.executor.heartbeatInterval": "60s",
      "spark.dynamicAllocation.enabled": "false",
      "spark.memory.fraction": "0.80",
      "spark.memory.storageFraction": "0.30",
      "spark.executor.extraJavaOptions": "-XX:+UseG1GC -XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark -XX:InitiatingHeapOccupancyPercent=35 -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p'",
      "spark.driver.extraJavaOptions": "-XX:+UseG1GC -XX:+UnlockDiagnosticVMOptions -XX:+G1SummarizeConcMark -XX:InitiatingHeapOccupancyPercent=35 -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:OnOutOfMemoryError='kill -9 %p'",
      "spark.yarn.scheduler.reporterThread.maxFailures": "5",
      "spark.storage.level": "MEMORY_AND_DISK_SER",
      "spark.rdd.compress": "true",
      "spark.shuffle.compress": "true",
      "spark.shuffle.spill.compress": "true",
      "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
    }
  }
]
```

### Reference Materials

[Apache Hadoop 3\.3\.1 – Using Memory Control in YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/NodeManagerCGroupsMemory.html)

[Configuration \- Spark 3\.2\.1 Documentation](https://spark.apache.org/docs/latest/configuration.html)

[アプリケーションの設定 \- Amazon EMR](https://docs.aws.amazon.com/ja_jp/emr/latest/ReleaseGuide/emr-configure-apps.html)

- [Amazon EMR で Apache Spark アプリケーションのメモリをうまく管理するためのベストプラクティス \| Amazon Web Services ブログ](https://aws.amazon.com/jp/blogs/news/best-practices-for-successfully-managing-memory-for-apache-spark-applications-on-amazon-emr/)
