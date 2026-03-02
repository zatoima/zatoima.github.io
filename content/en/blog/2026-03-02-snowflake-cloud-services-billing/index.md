---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Understanding and Optimizing Snowflake Cloud Services Billing"
subtitle: ""
summary: " "
tags: ["Snowflake", "Cost Management"]
categories: ["Snowflake"]
url: snowflake-cloud-services-billing
date: 2026-03-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false
---

## Introduction

When reviewing Snowflake usage statements, you'll notice credit consumption recorded under "Cloud Services" separately from warehouse compute. This article covers what Cloud Services are, under what conditions they are billed, and how to track and reduce them.

Official documentation: [Understanding compute cost](https://docs.snowflake.com/en/user-guide/cost-understanding-compute) / [Optimizing cloud services for cost](https://docs.snowflake.com/en/user-guide/cost-optimize-cloud-services)

---

## What Is the Cloud Services Layer?

Snowflake's architecture is broadly divided into three layers.

```
┌────────────────────────────────────────────┐
│        Cloud Services Layer                │  ← Focus of this article
│  Authentication / Metadata management /    │
│  Query compilation / Access control /      │
│  Transaction management                    │
├────────────────────────────────────────────┤
│        Compute Layer (Virtual Warehouses)  │  ← Query & DML execution
├────────────────────────────────────────────┤
│        Storage Layer                       │  ← Data persistence
└────────────────────────────────────────────┘
```

The Cloud Services layer is a component that Snowflake keeps running internally at all times, even when users have not explicitly started a warehouse. Its main responsibilities are as follows.

| Function | Description |
|----------|-------------|
| Authentication & Authorization | Login verification, role resolution, row policy evaluation |
| Metadata Management | Table definitions, partition information, statistics management |
| Query Compilation | SQL parsing, optimization plan generation, pruning |
| Transaction Management | ACID guarantees, snapshot management |

---

## The 10% Rule (Cloud Services Adjustment)

### How Billing Works

Cloud Services credit consumption **always occurs**, but it is only billed (charged) when it exceeds a certain threshold.

> **Cloud Services consumption is only billed when it exceeds 10% of the virtual warehouse consumption for the same day (UTC). Only the excess amount is charged.**

This mechanism where only the excess is billed is called the "Cloud Services Adjustment." The `CREDITS_ADJUSTMENT_CLOUD_SERVICES` column in the METERING_DAILY_HISTORY view records a negative value, representing the adjusted (deducted) amount.

{{< callout "info" >}}
Serverless compute (Snowpipe, Automatic Clustering, etc.) is excluded from this 10% adjustment calculation. Only **virtual warehouse credits** are used for the adjustment.
{{< /callout >}}

### Calculation Examples

Here are specific examples from the official documentation.

| Date | VW Credits Used | CS Credits Used | Adjustment (full deduction if ≤10%) | Billed Credits |
|------|----------------|----------------|-------------------------------------|---------------|
| Nov 1 | 100 | 20 | −10 | 110 |
| Nov 2 | 120 | 10 | −10 | 120 |
| Nov 3 | 80 | 5 | −5 | 80 |
| Nov 4 | 100 | 13 | −10 | 103 |
| **Total** | **400** | **48** | **−35** | **413** |

- Nov 1: CS=20 > VW×10%=10 → 10 excess credits are billed. Adjustment is −10
- Nov 2: CS=10 < VW×10%=12 → CS is under 10% → Adjustment is −10 (full CS deduction)
- Nov 3: CS=5 < VW×10%=8 → Full adjustment. Adjustment is −5 (full CS deduction)
- Nov 4: CS=13 > VW×10%=10 → 3 excess credits are billed. Adjustment is −10

---

## Use Cases That Generate Cloud Services Costs

The following patterns all consume Cloud Services resources **without using** a virtual warehouse.

| Pattern | Root Cause | Recommended Action |
|---------|-----------|-------------------|
| Low selectivity in COPY commands | S3 file listing runs on CS only | Add date prefixes to S3 buckets to narrow target files |
| Frequent DDL & cloning | CREATE/DROP/CLONE are metadata-only operations | Review clone granularity (switch from full schema to individual tables) |
| Frequent simple queries | Mass execution of `SELECT 1`, `SELECT CURRENT_SESSION()` | Use the JDBC driver's `getSessionId()` method with caching |
| Frequent INFORMATION_SCHEMA queries | I_S queries do not use a warehouse | Switch to the `ACCOUNT_USAGE` schema |
| Frequent SHOW commands | Apps or third-party tools frequently fetch metadata | Review polling frequency in tool configurations |
| Single-row INSERTs & fine-grained schemas | Accumulation of small metadata operations | Switch to bulk loading. For multi-tenant, use shared schemas with `customer_id` clustering |
| Complex SQL queries | Many JOINs, large lists in `IN` clauses | Review queries with long compilation times |

---

## How to Track Cloud Services Costs

### 1. Daily Billing Summary (METERING_DAILY_HISTORY)

The `SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY` view shows daily CS usage and the actual billed amount after adjustments.

```sql
-- CS billing summary for the past month (ordered by highest billed amount)
SELECT
    usage_date,
    credits_used_cloud_services,
    credits_adjustment_cloud_services,
    credits_used_cloud_services + credits_adjustment_cloud_services AS billed_cloud_services
FROM snowflake.account_usage.metering_daily_history
WHERE usage_date >= DATEADD(month, -1, CURRENT_TIMESTAMP())
    AND credits_used_cloud_services > 0
ORDER BY 4 DESC;
```

Example output:

| USAGE_DATE | CREDITS_USED_CLOUD_SERVICES | CREDITS_ADJUSTMENT_CLOUD_SERVICES | BILLED_CLOUD_SERVICES |
|------------|---------------------------|-----------------------------------|-----------------------|
| 2026-03-01 | 15.234 | -10.000 | 5.234 |
| 2026-02-28 | 8.120 | -8.120 | 0.000 |
| 2026-02-27 | 12.500 | -10.000 | 2.500 |

Rows where `billed_cloud_services` is 0 indicate that the day's CS consumption stayed within 10% of VW usage and was not billed.

Key column definitions:

| Column | Description |
|--------|-------------|
| `CREDITS_USED_CLOUD_SERVICES` | Actual CS consumption for the day |
| `CREDITS_ADJUSTMENT_CLOUD_SERVICES` | Adjustment amount (negative value, up to the 10% threshold) |
| `CREDITS_BILLED` | Total credits actually charged |

### 2. Per-Warehouse Analysis (WAREHOUSE_METERING_HISTORY)

Identifying warehouses with a high CS ratio helps narrow down problematic workloads.

```sql
-- Identify warehouses with high CS ratios
SELECT
    warehouse_name,
    SUM(credits_used)                AS credits_used,
    SUM(credits_used_cloud_services) AS credits_used_cloud_services,
    ROUND(
        SUM(credits_used_cloud_services) / NULLIF(SUM(credits_used), 0) * 100,
        2
    )                                AS pct_cloud_services
FROM snowflake.account_usage.warehouse_metering_history
WHERE TO_DATE(start_time) >= DATEADD(month, -1, CURRENT_TIMESTAMP())
    AND credits_used_cloud_services > 0
GROUP BY 1
ORDER BY 4 DESC;
```

Example output:

| WAREHOUSE_NAME | CREDITS_USED | CREDITS_USED_CLOUD_SERVICES | PCT_CLOUD_SERVICES |
|---------------|-------------|----------------------------|-------------------|
| ANALYTICS_WH | 45.200 | 9.800 | 21.68 |
| ETL_WH | 120.500 | 18.200 | 15.10 |
| ADHOC_WH | 30.100 | 2.500 | 8.31 |

Warehouses where `PCT_CLOUD_SERVICES` significantly exceeds 10% likely have workloads matching the patterns described in the previous section.

### 3. Per-Query-Type Analysis (QUERY_HISTORY)

Check which types of operations are consuming the most CS credits.

```sql
-- CS consumption by query type over the past 7 days
SELECT
    query_type,
    ROUND(SUM(credits_used_cloud_services), 6) AS cs_credits,
    COUNT(1)                                   AS num_queries
FROM snowflake.account_usage.query_history
WHERE start_time >= TIMESTAMPADD(day, -7, CURRENT_TIMESTAMP)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

Example output:

| QUERY_TYPE | CS_CREDITS | NUM_QUERIES |
|-----------|-----------|-------------|
| SELECT | 0.024500 | 15823 |
| COPY | 0.018200 | 342 |
| INSERT | 0.009100 | 5621 |
| SHOW | 0.005800 | 12045 |
| CREATE_TABLE | 0.001200 | 87 |

If SHOW queries have a high count and significant CS consumption, it's likely that third-party tools are frequently fetching metadata.

### 4. Checking in Snowsight

You can visually review costs from **Admin > Cost Management** in Snowsight. It supports filtering by service type and time period, making it useful for understanding trends without writing queries.

---

## Additional Notes

### Differences Between INFORMATION_SCHEMA and ACCOUNT_USAGE

When writing tracking queries, be aware that the choice of schema affects behavior.

| Comparison | INFORMATION_SCHEMA | ACCOUNT_USAGE |
|-----------|-------------------|---------------|
| Data retrieval method | Cloud Services only | Uses a virtual warehouse |
| Impact on CS consumption | Increases with frequent execution | Charged to the warehouse |
| Data freshness | Real-time | Up to 180 minutes latency |
| Retention period | 7 days to 6 months | Up to 365 days |

For monitoring purposes, using `ACCOUNT_USAGE` is often more cost-effective.

### Notes on METERING_DAILY_HISTORY

- View latency is up to **180 minutes (3 hours)**
- The `CREDITS_USED_CLOUD_SERVICES` column has up to **6 hours** of latency (on the `WAREHOUSE_METERING_HISTORY` side)
- When reconciling with monthly billing, set the session timezone to UTC before querying

```sql
ALTER SESSION SET TIMEZONE = UTC;
```

### Cost Reduction Priority

Listed in order of typical effectiveness:

1. **Switch from INFORMATION_SCHEMA to ACCOUNT_USAGE** — Can be addressed with code changes alone
2. **Reduce frequent SHOW commands** — Can be addressed by reviewing tool configurations
3. **Convert single-row INSERTs to bulk loading** — Requires architectural changes but yields significant results
4. **Restructure S3 buckets for COPY commands** — Can be addressed incrementally

---

## Summary

- The Cloud Services layer handles authentication, metadata management, and query compilation, consuming credits at all times
- Billing follows the rule that "only the excess beyond 10% of daily VW consumption is charged," and in many cases the adjustment covers the full amount
- Three views — `METERING_DAILY_HISTORY`, `WAREHOUSE_METERING_HISTORY`, and `QUERY_HISTORY` — allow you to progressively identify the root cause
- When CS costs are high, first investigate "frequent SHOW/INFORMATION_SCHEMA queries" and "single-row INSERTs"

## References

{{< linkcard "https://docs.snowflake.com/en/user-guide/cost-understanding-compute" >}}

{{< linkcard "https://docs.snowflake.com/en/user-guide/cost-optimize-cloud-services" >}}

{{< linkcard "https://docs.snowflake.com/en/user-guide/cost-exploring-compute" >}}

{{< linkcard "https://docs.snowflake.com/en/sql-reference/account-usage/metering_daily_history" >}}