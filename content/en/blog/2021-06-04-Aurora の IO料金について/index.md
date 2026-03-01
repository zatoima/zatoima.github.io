---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "About Aurora PostgreSQL I/O Pricing"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-aurora-cost-io-input-output.html
date: 2021-06-04
lastmod : 2022-02-02
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

Aurora costs are broadly classified into the following 4 categories. Other RDBMS database services like RDS PostgreSQL do not incur I/O charges, which may be why Aurora I/O charges are easy to overlook in cost estimates. (I have a sense that I/O charges range from a few percent to at most 10% of instance charges, but depending on how the database is used, it could be higher.)

1. Instance charges
2. Database storage
3. I/O charges
4. Data transfer

For details, please refer to the following. Usage charges for cloning and global databases are omitted as they depend on usage patterns.

> Pricing - Amazon Aurora | AWS https://aws.amazon.com/jp/rds/aurora/pricing/

For the Tokyo region, I/O charges are `0.24 USD per 1 million requests`. Also, 1 I/O operation is charged for up to 4KB of changes per data page. If a workload generates 2,000 IOPS per second, the monthly cost is calculated as follows. (Note: 2,000 IOPS per second is just a rough example.)

```
1,000 Reads/Second + 1,000 Writes/Second = 2,000 Number of I/Os per second
2,000 I/Os per second x 730 hours x 60 minutes x 60 Seconds = 5,256,000,000 Number of I/Os per month
5,256,000,000 x 0.00000024 USD = 1,261.44 USD (I/O Rate Cost)
```

Pricing itself can be calculated using the Pricing Calculator.

- [AWS Pricing Calculator](https://calculator.aws/#/createCalculator/AuroraPostgreSQL)
  - https://calculator.aws/#/createCalculator/AuroraPostgreSQL

When Aurora I/O charges are high, check the following:

- Check `Billed IOPS` in CloudWatch
  - When there are spikes, check what operations are happening and whether I/O volume can be reduced
    - pg_dump, batch processing, full scans, etc.
- Use `Performance Insights` to identify SQLs generating `IO: DataFileRead` or `IO:DataFilePrefetch` events
- Check the buffer cache hit rate
  - Since data file I/O is occurring, adjust parameters to maximize in-memory processing

Actions to reduce I/O charges primarily include:

- Increase memory to enable in-memory processing
- Tune full scan SQLs
- Use indexes and partitioning to reduce unnecessary I/O

### Update (2022/02/02)

The following article is also helpful - in fact, it's better to carefully read the AWS Database Blog officially published in January 2022.

- [Planning I/O in Amazon Aurora | AWS Database Blog](https://aws.amazon.com/jp/blogs/database/planning-i-o-in-amazon-aurora/)
