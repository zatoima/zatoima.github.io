---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Overview of Parallel Replicat, New Feature in GoldenGate 12.3"
subtitle: ""
summary: " "
tags: ["Oracle","GoldenGate"]
categories: ["Oracle","GoldenGate"]
url: goldengate-parallel-replicat-overview.html
date: 2019-04-28
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




#### **Introduction**

The traditional Replicat modes were "Classic Replicat" and "Integrated Replicat". Starting from GoldenGate version 12.3, a new Replicat mode called Parallel Replicat was introduced. Based on its new features, it seems capable of solving problems (especially performance issues) that could not be resolved with the traditional modes.

This article summarizes the overview, and the next article will look at the specific behavior.

#### **Overview**

- Parallel Replicat has a highly scalable apply engine capable of achieving apply rates of over 1 million operations per second.

- Five times faster than Integrated Replicat

- Applies a single large transaction in parallel

- Dependency calculation and parallel processing outside the database

- Ability to parallelize a single large transaction

- Dependencies are considered even while parallelizing large transactions

- A feature controlled by the SPLIT_TRANS_RECS parameter which specifies the transaction split size (number of records). The default is 100,000.

  > Reference
  >
  > http://www.oracle-scn.com/oracle-goldengate-parallel-replicat/

With Classic Replicat and Integrated Replicat, large transactions (such as millions of rows updated before a single commit) were prone to replication delays.

If the product claims of "ability to parallelize a single large transaction" and "five times faster than Integrated Replicat" are accurate, significant performance improvements can be expected.

#### **Process Overview**

Mappers operate in parallel, reading the trail, mapping trail records, converting mapped records to integrated Replicat LCR format, and sending LCRs to the Merger for subsequent processing.

The master process has two threads: the Collator and the Scheduler. The Collator receives mapped transactions from the master and restores them to trail order for dependency calculation. The Scheduler calculates dependencies between transactions, groups transactions into independent batches, and sends batches to Appliers for application to the target database.

In contrast, with Integrated Replicat, this process is the "Reader", which operates serially rather than in parallel.

<img src="images/image-20191121164644456.png" alt="image-20191121164644456" style="zoom:50%;" />

#### Reference

This is the Integrated Replicat case. While the Applier is also parallelized, the architecture before the Applier is quite different.

<img src="images/image-20191121164655589.png" alt="image-20191121164655589" style="zoom:50%;" />

#### **Creating the Process**

As before, the process itself is created with the ADD Replicat command.

```sh
ggsci > ADD REPLOCAT R1 ,　INTEGRATED ,　PARALLEL ,　EXTTRAIL　./dirdat/ra　checkpointtable ggadmin.ggs_checkpoint
```

#### **Parameters to Use**

| Parameter                                      | Description                                                  |
| :--------------------------------------------- | :----------------------------------------------------------- |
| `MAP_PARALLELISM`                              | Configures the number of Mappers. Controls the number of threads used to read trail files. Minimum is `1`, maximum is `100`, default is `2`. |
| `APPLY_PARALLELISM`                            | Configures the number of Appliers. Controls the number of target database connections used to apply changes. Default value is 4. |
| `MIN_APPLY_PARALLELISM``MAX_APPLY_PARALLELISM` | Apply parallelism is auto-tuned. Set minimum and maximum values to define the range within which Replicat automatically adjusts parallelism. No default values. Do *not* use together with `APPLY_PARALLELISM`. |
| `SPLIT_TRANS_REC`                              | Specifies that large transactions are split into pieces of the specified size and applied in parallel. Dependencies between pieces are preserved. Disabled by default. |
| `COMMIT_SERIALIZATION`                         | Enables `FULL` serialization mode commits, forcing transactions to commit in trail order. |
| **Advanced Parameters**                        |                                                              |
| `LOOK_AHEAD_TRANSACTIONS`                      | Controls how far ahead the Scheduler looks when batching transactions. Default value is 10000. |
| `CHUNK_SIZE`                                   | Controls what size transaction Parallel Replicat considers large. When Parallel Replicat detects a transaction larger than this size, it serializes that transaction, which reduces performance. However, increasing this value also increases memory consumed by Parallel Replicat. |

#### **Other Notes**

- For Integrated Parallel Replicat, FULL mode of COMMIT_SERIALIZATION is not supported. The only available mode is the default DEPENDENT.

- The target database version must be 12.2 or later.

- Parallel Replicat only supports data replication from trails with full metadata. Therefore, the source side must use GG 12.2 or later.
