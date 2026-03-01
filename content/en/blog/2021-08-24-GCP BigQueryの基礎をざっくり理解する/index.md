---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Understanding the Basics of GCP BigQuery"
subtitle: ""
summary: " "
tags: ["GCP","BigQuery"]
categories: ["GCP","BigQuery"]
url: gcp-bigquery-google-cloud-overview-basic
date: 2021-08-24
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

In AWS terms, I understand it as a service similar to Athena, Redshift, and Aurora all in one.

## BigQuery Components

- BigQuery Managed Storage
  - Scalable data storage
- BigQuery Analysis
  - Parallel SQL engine based on Dremel query engine technology

## Architecture

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=15" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## Data Storage Format

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=14" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## Distributed Data Placement

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=17" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## Parallel Query Processing

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=19" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## Data Types

> https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=ja

## Data Storage Approach

In BigQuery, charges are based on the amount of data read, so using these features should be actively considered.

- Partitioned tables
  - Partition pruning, per-partition export, etc.
- Clustered tables
  - Data placement and order adjusted based on clustering columns

## Slots

Slots represent the degree of processing parallelism, with a default maximum of 2000. BigQuery achieves its fast parallel processing through distributed storage and slot distribution, but note that it's not guaranteed to scale up to this limit. It does not seem to refer to CPU core count.

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=50" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

> https://cloud.google.com/bigquery/docs/slots?hl=ja
>
> BigQuery slots are virtual CPUs used by BigQuery to run SQL queries. BigQuery automatically calculates the number of slots required per query based on the size and complexity of the query.

> The unknown world of Google BigQuery - Qiita https://qiita.com/AkiQ/items/9c5eefb7953409aa2eda
>
> As mentioned, by default a project is given a maximum of 2,000 slots. Query speed is achieved through slot parallel processing. Slots are allocated from resources currently available in BigQuery, which makes sense when you think about it. Slots are essentially a global resource.
> Therefore, even though you can use up to 2,000 slots, it doesn't mean you can always use all 2,000 slots simultaneously.

## BigQuery Hierarchy

<iframe src="//www.slideshare.net/slideshow/embed_code/key/24fB9HWkiPJDUz?startSlide=20" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/GoogleCloudPlatformJP/cloud-onair-bigquery-201896-113180907" title="[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送" target="_blank">[Cloud OnAir] BigQuery の仕組みからベストプラクティスまでのご紹介 2018年9月6日 放送</a> </strong> from <strong><a href="//www.slideshare.net/GoogleCloudPlatformJP" target="_blank">Google Cloud Platform - Japan</a></strong> </div>

## Cost Optimization

- The "BigQuery bankruptcy" topic was discussed previously. When running analytical queries on large volumes of data, you need to be careful about costs.
  - BigQuery Cost Optimization Best Practices | Google Cloud Blog https://cloud.google.com/blog/ja/products/data-analytics/cost-optimization-best-practices-for-bigquery?utm_source=pocket_mylist

## Pricing

> Pricing | BigQuery: Cloud Data Warehouse | Google Cloud https://cloud.google.com/bigquery/pricing?hl=ja

- Query pricing
- Storage pricing

## Transferring Data from Other Clouds

Without data, an analytics platform is useless. Using `BigQuery Data Transfer Service for Amazon S3`, you can automatically schedule recurring load jobs from Amazon S3 to BigQuery. The reverse is also possible.

> Amazon S3 Transfer | BigQuery Data Transfer Service | Google Cloud https://cloud.google.com/bigquery-transfer/docs/s3-transfer?hl=ja
>
> Thinking about and summarizing data migration from GCP to AWS | DevelopersIO https://dev.classmethod.jp/articles/data-migration-from-gcp-to-aws-matome/#a-4

## References

> BigQuery Documentation | Google Cloud https://cloud.google.com/bigquery/docs
