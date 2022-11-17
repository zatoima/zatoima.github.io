---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "SnowPro Advanced Architect対策メモ"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-certificate-snowpro-advanced-memo
date: 2022-09-10
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



`SNOWPRO ADVANCED: ARCHITECT EXAM STUDY GUIDE`（2022/9/7版）に記載のある内容を参考にしつつ、参考Docを試験ガイドの項目にマッピングしたもの。`SNOWPRO ADVANCED: ARCHITECT EXAM STUDY GUIDE`が頻繁にアップデートされていることとリンク切れをたまに起こしているところは注意する必要があるかも。また試験の使用言語が英語しかないので、単語に慣れる意味でも英語版のマニュアルや資料を読もうと思う。

### 公式ガイド

https://www.snowflake.com/certifications/?lang=ja

### 試験ガイド

## 1.0 Domain: Account and Security

### 1.1 Design a Snowflake account and database strategy, based on business requirements.

- Create and configure Snowflake parameters based on a central account and any additional accounts.
  - [Account Usage — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/account-usage.html#differences-between-account-usage-and-information-schema)

- List the benefits and limitations of one Snowflake account as compared to multiple Snowflake accounts.

### 1.2 Design an architecture that meets data security, privacy, compliance, and governance requirements.

- Configure Role Based Access Control (RBAC) hierarchy
  - [Overview of Access Control — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-access-control-overview.html)

- System roles and associated best practices
- Data Access
  - [Understanding Column\-level Security — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-column-intro.html)
  - [CREATE STORAGE INTEGRATION — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration.html)
  - [Working with Secure Views — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/views-secure.html)
  - [Data Consumers — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-share-consumers.html#general-limitations-for-shared-databases)
    - General Limitations for Shared Databases

- Data Security
- Compliance

### 1.3 Outline Snowflake security principles and identify use cases where they should be applied.

[Managing Security in Snowflake — Snowflake Documentation](https://docs.snowflake.com/en/user-guide-admin-security.html)

- Encryption
  - [ENCRYPT — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/functions/encrypt.html)

- Network security
  - [Azure Private Link & Snowflake — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/privatelink-azure.html#requirements-and-limitations)
  - [SYSTEM$WHITELIST\_PRIVATELINK — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/functions/system_whitelist_privatelink.html)

- User, Role, Grants provisioning
  - [Overview of Access Control — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-access-control-overview.html)

- Authentication
  - [Multi\-Factor Authentication \(MFA\) — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-mfa.html#connecting-to-snowflake-with-mfa)
  - [Managing/Using Federated Authentication — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-use.html#using-sso-with-mfa)


#### STUDY GUIDEには参考資料として掲載されているが、上記の1.1~1.3のどこに紐づくかわからないもの

- [ALTER ACCOUNT — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/alter-account.html)
- [Parameters — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/parameters.html#)

#### WhitePaper/Read Assets

- Cloud Data Platform Security: How Snowflake Sets the Standard
  - https://resources.snowflake.com/white-paper/cloud-data-platform-security-how-snowflake-sets-the-standard#main-content

#### Lab Guides

- Snowflake Pattern - Security - Access to Sensitive Objects
  - https://resources.snowflake.com/architecture-patterns/snowflake-pattern-security-access-to-sensitive-objects
- Snowflake Pattern - Security - Authentication
  - https://resources.snowflake.com/architecture-patterns/snowflake-pattern-security-authentication
- Snowflake Pattern - Security - Network Architecture
  - https://resources.snowflake.com/architecture-patterns/snowflake-pattern-security-network-architecture

## 2.0 Domain:Snowflake Architecture

### 2.1 Outline the benefits and limitations of various data models in a Snowflake environment.

- Data models

### 2.2 Design data sharing solutions, based on different use cases.

- Use Cases
  - Sharing within the same organization/same Snowflake account
  - Sharing within a cloud region
  - Sharing across cloud regions
  - Sharing between different Snowflake accounts
    - [Introduction to Database Replication Across Multiple Accounts — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/database-replication-intro.html)
  - Sharing to a non-Snowflake customer
  - Sharing Across platforms

- Data Exchange
  - [Data Providers — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-sharing-core-tasks-providers.html)

- Data Sharing Methods
  - [Data Providers — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-sharing-core-tasks-providers.html)
  - [Sharing Data Securely in Snowflake — Snowflake Documentation](https://docs.snowflake.com/en/user-guide-data-share.html)


### 2.3 Create architecture solutions that support Development Lifecycles as well as workload requirements.

- Data Lake and Environments
  - [Working with External Tables — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-external.html)
  - [Introduction to External Tables — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-external-intro.html#partitioned-external-tables)
  - [Integrating Apache Hive Metastores with Snowflake — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-external-hive.html)

- Workloads
- Development lifecycle support

### 2.4 Given a scenario, outline how objects exist within the Snowflake Object hierarchy and how the hierarchy impacts an architecture.

- Roles
  - [CREATE USER — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-user.html)
  - [Overview of Access Control — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/security-access-control-overview.html#securable-objects)

- Warehouses
- Object hierarchy
- Database

### 2.5 Determine the appropriate data recovery solution in Snowflake and how data can be restored.

- Backup/Recovery
  - [Cloning Considerations — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/object-clone.html)
  - [Understanding & Using Time Travel — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-time-travel.html#)

- Disaster Recovery
  - [Database Replication and Failover/Failback — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/database-replication-failover.html)
  - [Introduction to Database Replication Across Multiple Accounts — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/database-replication-intro.html)


#### Lab Guides

- [Building an application on Snowflake with data from Snowflake Data Marketplace](https://quickstarts.snowflake.com/guide/vhol_data_marketplace_app/index.html?index=..%2F..index#0)
- [Getting Started with Time Travel](https://quickstarts.snowflake.com/guide/getting_started_with_time_travel/index.html?index=..%2F..index#0)
- [Data Modeling \| Snowflake](https://www.snowflake.com/guides/data-modeling)

#### WhitePaper/Read Assets

- [SNO\-eBook\-7\-Reference\-Architectures\-for\-Application\-Builders\-AppHealth\-SecurityAna\.pdf](https://developers.snowflake.com/wp-content/uploads/2020/09/SNO-eBook-7-Reference-Architectures-for-Application-Builders-AppHealth-SecurityAna.pdf)
- [Support Multiple Data Modeling Approaches with Snowflake](https://www.snowflake.com/blog/support-multiple-data-modeling-approaches-with-snowflake/)
- [Data Modeling in the Age of JSON and Schema\-on\-Read \- Snowflake Blog](https://www.snowflake.com/blog/data-modeling-in-the-age-of-json-and-schema-on-read/)
- [Different Types of Objects in Snowflake](https://community.snowflake.com/s/article/Different-Types-of-Objects-in-Snowflake)

## 3.0 Domain: Data Engineering

### 3.1 Determine the appropriate data loading or data unloading solution to meet business needs.

- Data sources
- Ingestion of the data
- Architecture Changes
- Data unloading

### 3.2 Outline key tools in Snowflake’s ecosystem and how they interact with Snowflake.

- Connectors

- [Connectors & Drivers — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/conns-drivers.html#connectors-drivers)
  - Kafka
  - Spark
  - Python
    - [Using the Python Connector — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/python-connector-example.html#binding-parameters-to-variables-for-batch-inserts)

- Drivers
  - JDBC
  - OBDC
  - API endpoints
  - SnowSQL


### 3.3 Determine the appropriate data transformation solution to meet business needs.

- Materialized Views, Views and Secure Views
- Staging layers and tables
  - [Loading Data into Snowflake — Snowflake Documentation](https://docs.snowflake.com/en/user-guide-data-load.html)
  - [Unloading Data from Snowflake — Snowflake Documentation](https://docs.snowflake.com/en/user-guide-data-unload.html)
  
- Querying semi-structured data
  - [Semi\-structured Data — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/semistructured-concepts.html)
  - [Semi\-structured Data Types — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/data-types-semistructured.html)
  - [Querying Semi\-structured Data — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/querying-semistructured.html)

- Data processing
  - [Continuous Data Pipelines — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-pipelines.html)
  - [Introduction to Snowpipe — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro.html)

- Stored Procedures
  - [Understanding Caller’s Rights and Owner’s Rights Stored Procedures — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/stored-procedures-rights.html)
  - [Stored Procedures — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/stored-procedures.html)

- Streams and Tasks
  - [CREATE STREAM — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-stream.html)

- Functions

#### WhitePaper/Read Assets

- [Snowflake For Data Engineering \- Easily Ingest, Transform, And Deliver Data For Up\-To\-The\-Moment Ins](https://resources.snowflake.com/white-paper/snowflake-for-data-engineering-easily-ingest-transform-and-deliver-data-for-up-to-the-moment-insight#main-content)
- [Using Streams and Tasks in Snowflake](https://community.snowflake.com/s/article/Using-Streams-and-Tasks-inside-Snowflake)
- [Masking Semi\-Structured Data with Snowflake \- Snowflake Blog](https://www.snowflake.com/blog/masking-semi-structured-data-with-snowflake/)
- [Easy Continuous Data Pipelines with GA of Streams and Tasks \- Snowflake Blog](https://www.snowflake.com/blog/easy-continuous-data-pipelines-with-ga-of-streams-and-tasks/)

#### Lab Guides

- [Building a Real\-Time Data Vault in Snowflake](https://quickstarts.snowflake.com/guide/vhol_data_vault/index.html?index=..%2F..index#0)
- [Enrich Salesforce data with Snowflake to deliver your Customer 360](https://quickstarts.snowflake.com/guide/vhol_snowflake_salesforce_tcrm/index.html?index=..%2F..index#0)
- [Auto\-Ingest Twitter Data into Snowflake](https://quickstarts.snowflake.com/guide/auto_ingest_twitter_data/index.html?index=..%2F..index#0)
- [Build a Recommendation Engine with AWS SageMaker](https://quickstarts.snowflake.com/guide/recommendation_engine_aws_sagemaker/index.html?index=..%2F..index#0)
- [Getting Started with Snowpipe](https://quickstarts.snowflake.com/guide/getting_started_with_snowpipe/index.html?index=..%2F..index#0)
- [Accelerating Data Teams with dbt Cloud & Snowflake](https://quickstarts.snowflake.com/guide/data_teams_with_dbt_cloud/?index=..%2F..index#0)
- [Getting Started With User\-Defined SQL Functions](https://quickstarts.snowflake.com/guide/getting_started_with_user_defined_sql_functions/?index=..%2F..index#5)
- [Getting Started with Python](https://quickstarts.snowflake.com/guide/getting_started_with_python/index.html?index=..%2F..index#0)
- [Getting Started with SnowSQL](https://quickstarts.snowflake.com/guide/getting_started_with_snowsql/index.html?index=..%2F..index#0)

## 4.0 Domain: Performance Optimization

### 4.1 Outline performance tools, best practices, and appropriate scenarios where they should be applied.

- Query profiling
- Virtual Warehouse configuration
  - [Virtual Warehouses — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/warehouses.html)
  - [Micro\-partitions & Data Clustering — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions.html#clustering-depth-illustrated)

- Clustering
  - [Clustering Keys & Clustered Tables — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/tables-clustering-keys.html#reclustering)

- Search Optimization
  - [Using the Search Optimization Service — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/search-optimization-service.html#)
  - [Using Persisted Query Results — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/querying-persisted-results.html#retrieval-optimization)

- Caching
- Query rewrite

### 4.2 Troubleshoot performance issues with existing architectures.

- JOIN explosions
  - [MERGE — Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/merge.html#nondeterministic-results-for-update-and-delete)

- Warehouse selection (scaling up as compared to scaling out)
- Best practices and optimization techniques
  - [Working with Materialized Views — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/views-materialized.html#how-the-query-optimizer-uses-materialized-views)

- Duplication of data

#### WhitePaper/Read Assets

- https://developers.snowflake.com/wp-content/uploads/2020/09/SNO-eBook-7-Reference-Architectures-for-Application-Builders-Customer360-2.pdf

#### Lab Guides

- [Resource Optimization: Performance](https://quickstarts.snowflake.com/guide/resource_optimization_performance_optimization/index.html?index=..%2F..index#0)
- [Resource Optimization: Billing Metrics](https://quickstarts.snowflake.com/guide/resource_optimization_billing_metrics/index.html?index=..%2F..index#0)
- [Resource Optimization: Setup & Configuration](https://quickstarts.snowflake.com/guide/resource_optimization_setup/index.html?index=..%2F..index#0)
- [Resource Optimization: Usage Monitoring](https://quickstarts.snowflake.com/guide/resource_optimization_usage_monitoring/index.html?index=..%2F..index#0)
- [Automating Data Pipelines to Drive Marketing Analytics with Snowflake & Fivetran](https://quickstarts.snowflake.com/guide/vhol_fivetran/index.html?index=..%2F..index#0)
- [Building a Data Application](https://quickstarts.snowflake.com/guide/data_app/index.html?index=..%2F..index#0)
- [DevOps: Database Change Management with schemachange and GitHub](https://quickstarts.snowflake.com/guide/devops_dcm_schemachange_github/index.html?index=..%2F..index#0)



