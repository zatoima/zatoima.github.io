---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Parameters to Consider Changing for RDS and Aurora (PostgreSQL)"
subtitle: ""
summary: " "
tags: ["AWS","Aurora","RDS","PostgreSQL"]
categories: ["AWS","Aurora","RDS","PostgreSQL"]
url: aws-aurora-rds-postgresql-parameter-change.html
date: 2021-01-21
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

# Introduction

Since Aurora and RDS are managed services, parameter tuning is generally not required, but depending on requirements or performance issues, tuning may be necessary. This is a summary of those parameters.

# List of Parameters to Consider Changing

Added as I notice them. Current parameter values (setting column) are extracted from Aurora and RDS using `r5.large` instance type.

Note that even though these are "parameters to consider changing," the modifiable parameters differ between Aurora and RDS, and some cannot be changed. For example, checkpoint_timeout is typically adjusted for checkpoint tuning, but it appears that RDS allows changes while Aurora does not.

> List of Non-Modifiable Parameters for RDS and Aurora PostgreSQL | my opinion is my own https://zatoima.github.io/aws-aurora-rds-postgresql-parameter-modifiable.html

| name                             | setting(Aurora)              | setting(RDS)               | boot_val                       | unit | context       |
| -------------------------------- | ---------------------------- | -------------------------- | ------------------------------ | ---- | ------------- |
| archive_timeout                  | 300 (non-modifiable)         | 300 (non-modifiable)       | 0                              | s    | sighup        |
| autovacuum_max_workers           | 3                            | 3                          | 3                              |      | postmaster    |
| checkpoint_completion_target     | 0.5                          | 0.9                        | 0.5                            |      | sighup        |
| checkpoint_timeout               | 60                           | 300 (non-modifiable)       | 300                            | s    | sighup        |
| deadlock_timeout                 | 1000                         | 1000                       | 1000                           | ms   | superuser     |
| effective_io_concurrency         | 256                          | 1 (non-modifiable)         | 256                            |      | user          |
| lc_messages                      |                              |                            |                                |      | superuser     |
| log_filename                     | postgresql.log.%Y-%m-%d-%H%M | postgresql.log.%Y-%m-%d-%H | postgresql-%Y-%m-%d_%H%M%S.log |      | sighup        |
| log_hostname                     | off                          | on                         | off                            |      | sighup        |
| log_min_duration_statement       | -1                           | -1                         | -1                             | ms   | rds_superuser |
| log_rotation_age                 | 60                           | 60                         | 1440                           | min  | sighup        |
| log_rotation_size                | 100000                       | 10240                      | 10240                          | kB   | sighup        |
| log_timezone                     | UTC (non-modifiable)         | UTC (non-modifiable)       | GMT                            |      | sighup        |
| max_connections                  | 1710                         | 1710                       | 100                            |      | postmaster    |
| max_parallel_maintenance_workers | 2                            | 2                          | 2                              |      | user          |
| max_parallel_workers             | 8                            | 8                          | 8                              |      | user          |
| max_parallel_workers_per_gather  | 2                            | 2                          | 2                              |      | user          |
| max_worker_processes             | 8                            | 8                          | 8                              |      | postmaster    |
| random_page_cost                 | 4                            | 4                          | 4                              |      | user          |
| shared_buffers                   | 1304235                      | 497507                     | 1024                           | 8kB  | postmaster    |
| superuser_reserved_connections   | 3                            | 3                          | 3                              |      | postmaster    |
| wal_buffers                      | 2048                         | 8192                       | -1                             | 8kB  | postmaster    |

# SQL for Extraction

```sql
SELECT
    name,
    setting,
    boot_val,
    unit,
    context
FROM
    pg_settings
WHERE
    name IN ('max_connections','superuser_reserved_connections','lc_messages','archive_timeout','log_filename','log_rotation_age','log_rotation_size','log_min_duration_statement','log_hostname','log_timezone','shared_buffers','effective_io_concurrency','max_worker_processes','max_parallel_maintenance_workers','max_parallel_workers_per_gather','max_parallel_workers','wal_buffers','checkpoint_timeout','checkpoint_completion_target','random_page_cost','autovacuum_max_workers','deadlock_timeout')
ORDER BY 1;
```

# Individual Parameter Notes

#### deadlock_timeout

Since deadlock detection is costly, it may be worth raising this above the default of 1000ms (1 second).

#### checkpoint_completion_target

#### checkpoint_timeout

Default values differ between Aurora and RDS. Consider changing if performance issues arise.

Note: Aurora has no concept of checkpoints itself, and memory coming into log_buffer flows directly to the storage side, so it's unclear whether changing this has any effect.

> Notes on PostgreSQL's checkpoint_completion_target | my opinion is my own https://zatoima.github.io/postgresql-about-checkpoint_completion_target.html

#### log_filename

#### log_hostname

#### log_min_duration_statement

#### log_rotation_age

#### log_rotation_size

#### log_timezone

Change based on logging requirements.

#### max_connections

Compared to the OSS PostgreSQL default of `100`, the parameter is already adjusted, but the actual number of connections depends on requirements. When the instance type is scaled up, max_connections increases as well.

#### autovacuum_max_workers

#### max_parallel_maintenance_workers

#### max_parallel_workers

#### max_parallel_workers_per_gather

#### max_worker_processes

Fine-tune when tuning Vacuum and Analyze.

#### shared_buffers

For Aurora, the default value in the DB parameter group is set to 75% of total memory. This is because Aurora PostgreSQL does not use double buffering and does not need the OS filesystem cache. Fine-tune if you want to allocate more to other memory parameters.

> Understanding why there is a difference in shared_buffers DB parameter default values between Amazon RDS PostgreSQL and Aurora PostgreSQL https://aws.amazon.com/jp/premiumsupport/knowledge-center/rds-aurora-postgresql-shared-buffers/

#### wal_buffers

The amount of shared memory used for WAL data not yet written to disk. This buffer is written to disk at commit time. If writes are high and there are many CPUs, extending to a few MB can be effective, but the default value should generally be fine for both Aurora and RDS.

#### random_page_cost

Sets the planner's estimate for the cost of a non-sequentially fetched disk page. Reducing this value makes index scans relatively more attractive. Since SSDs are generally faster than HDDs for random reads, setting this to `1.0` for SSD is common. It may be worth lowering below the default of 4.0 in some cases.

# Parameters That Change with Instance Type Scale-Up

I investigated which parameters change among the above when scaling up. `max_connections` and `shared_buffers` change. On the other hand, despite increases in CPU and memory, parallelism settings and wal_buffers don't change.

| name                             | setting(Aurora) r5.large | setting(Aurora) r5.2xlarge | setting(RDS) r5.large | setting(RDS) r5.2xlarge |
| -------------------------------- | ----------------------- | ------------------------- | --------------------- | ----------------------- |
| archive_timeout                  | 300                     | 300                       | 300                   | 300                     |
| autovacuum_max_workers           | 3                       | 3                         | 3                     | 3                       |
| checkpoint_completion_target     | 0.5                     | 0.5                       | 0.9                   | 0.9                     |
| checkpoint_timeout               | 60                      | 60                        | 300                   | 300                     |
| deadlock_timeout                 | 1000                    | 1000                      | 1000                  | 1000                    |
| effective_io_concurrency         | 256                     | 256                       | 1                     | 1                       |
| lc_messages                      |                         |                           |                       |                         |
| log_filename                     | postgresql.log.%Y-%m-%d-%H%M | postgresql.log.%Y-%m-%d-%H%M | postgresql.log.%Y-%m-%d-%H | postgresql.log.%Y-%m-%d-%H |
| log_hostname                     | off                     | off                       | on                    | on                      |
| log_min_duration_statement       | -1                      | -1                        | -1                    | -1                      |
| log_rotation_age                 | 60                      | 60                        | 60                    | 60                      |
| log_rotation_size                | 100000                  | 100000                    | 10240                 | 10240                   |
| log_timezone                     | UTC                     | UTC                       | UTC                   | UTC                     |
| max_connections                  | 1710                    | 5000                      | 1710                  | 5000                    |
| max_parallel_maintenance_workers | 2                       | 2                         | 2                     | 2                       |
| max_parallel_workers             | 8                       | 8                         | 8                     | 8                       |
| max_parallel_workers_per_gather  | 2                       | 2                         | 2                     | 2                       |
| max_worker_processes             | 8                       | 8                         | 8                     | 8                       |
| random_page_cost                 | 4                       | 4                         | 4                     | 4                       |
| shared_buffers                   | 1304235                 | 5474754                   | 497507                | 2029633                 |
| superuser_reserved_connections   | 3                       | 3                         | 3                     | 3                       |
| wal_buffers                      | 2048                    | 2048                      | 8192                  | 8192                    |

# References

> PostgresqlCO.NF: PostgreSQL configuration for humans https://postgresqlco.nf/doc/ja/param/

> PostgreSQL 11 parameter dissection - Speaker Deck https://speakerdeck.com/ester41/postgresql-11-parameter?slide=2
>
> PostgreSQL stable operation: failure prevention and detection https://www.ospn.jp/osc2014.enterprise/pdf/OSC2014_Enterprise_hp.pdf
>
> PostgreSQL Performance Tuning - Qiita https://qiita.com/cuzic/items/f9b846e6171a54079d77
>
> Best Practices for Migrating an Oracle Database to Amazon RDS PostgreSQL or Amazon Aurora PostgreSQL: Target Database Considerations for the PostgreSQL Environment | Amazon Web Services Blog https://aws.amazon.com/jp/blogs/news/best-practices-for-migrating-an-oracle-database-to-amazon-rds-postgresql-or-amazon-aurora-postgresql-target-database-considerations-for-the-postgresql-environment/
