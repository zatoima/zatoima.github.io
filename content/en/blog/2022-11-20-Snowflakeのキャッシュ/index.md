---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Snowflake Cache"
subtitle: ""
summary: " "
tags: ["snowflake"]
categories: ["snowflake"]
url: snowflake-cached-memo
date: 2022-09-30
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

| # | Cache Name | Cache Target | Available Users | Storage Layer | Duration |
| ---- | -------------------- | ---------------------------------------- | ---------------------------------------------- | ------------------- | -------------------- |
| 1 | Result Cache | Query results | All users with the same role that executed the query | Snowflake | 24 hours |
| 2 | Metadata Cache | Information about tables | All users | Snowflake | Always |
| 3 | Data Cache | File headers and column data of query results | Users who ran the same virtual warehouse | Warehouse (SSD) | While warehouse is running |

No compilation cache exists; compilation is always required.

### How to Disable Cache Usage

- Result cache
  - Set `USE_CACHED_RESULT` to `FALSE`
- Metadata cache
  - No method available
- Data cache
  - SUSPEND the warehouse, etc.
    - [Invalidating Data Cache in Snowflake | my opinion is my own](https://zatoima.github.io/snowflake-data-cache-disabled/)

### Notes

#### Result Cache

> https://docs.snowflake.com/en/user-guide/querying-persisted-results.html#retrieval-optimization
>
> Typically, query results are reused when **all** of the following conditions are met:
>
> - The new query syntactically matches a previously executed query.
> - The query does not contain functions that must be evaluated at runtime (e.g., [CURRENT_TIMESTAMP()](https://docs.snowflake.com/en/sql-reference/functions/current_timestamp.html) and [UUID_STRING()](https://docs.snowflake.com/en/sql-reference/functions/uuid_string.html)). The [CURRENT_DATE()](https://docs.snowflake.com/en/sql-reference/functions/current_date.html) function is an exception to this rule. CURRENT_DATE() is evaluated at runtime, but queries using CURRENT_DATE() can still use the query reuse feature.
> - The query does not contain [user-defined functions (UDFs)](https://docs.snowflake.com/en/sql-reference/udf-overview.html) or [external functions](https://docs.snowflake.com/en/sql-reference/external-functions.html).
> - The table data contributing to the query results has not changed.
> - The previously persisted results of the query are still available.
> - The role accessing the cached results has the necessary privileges.
>   - If the query is a SELECT query, the role executing the query must have the required access privileges on all tables used in the cached query.
>   - If the query is a SHOW query, the role executing the query must match the role that generated the cached results.
> - Configuration options that affect how results are generated have not changed.
> - The micro-partitions of the table have not changed due to other data changes within the table (e.g., reclustering or consolidation).

> Even if all these conditions are met, Snowflake does **not** guarantee that query results will be reused.

### References

- [Snowflake's Three Types of Cache](https://zenn.dev/aaizawa/articles/2b06dd50d56438)

- [Using Persisted Query Results — Snowflake Documentation](https://docs.snowflake.com/en/user-guide/querying-persisted-results.html)
