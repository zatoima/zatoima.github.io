---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Fetching GA4 Data with Python (Analytics Data API)"
subtitle: ""
summary: " "
tags: ["python"]
categories: ["python"]
url: ga4-data-analytics-api-python
date: 2024-04-30
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

## Introduction

Using Python's Analytics Data API, you can flexibly retrieve GA4 data for analysis and reporting. Exploring the steps for handling GA4 data from Python to incorporate into a Hugo static site generator.

## What is the Analytics Data API?

The Analytics Data API is an API for programmatically accessing GA4 data. It allows you to retrieve report data and create custom reports. It requires a GCP account.

## Using from Python

When using the Analytics Data API from Python, use the `google-api-python-client` and `google-analytics-data` packages.

```python
pip install google-api-python-client
pip install google-analytics-data
```

## Enabling the Analytics Data API

https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries?hl=ja

> Enable the API
>
> - Create a Cloud Platform project and enable the Google Analytics Data API v1
> - Download the `credentials.json` file and save it to your working directory
>
> Add a service account to your Google Analytics 4 property
>
> - Get the service account email address from the `client_email` field in the `credentials.json` file
> - Add the user to your Google Analytics 4 property using the obtained email address (viewer permission only)
>
> Configure authentication
>
> - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to specify the service account credentials
> - Set the environment variable value to the path of the service account JSON file downloaded in step 1
>
> Install the client library
>
> - Install the Google Analytics Data API client library for your chosen programming language
>
> Make API calls
>
> - Once authentication and client library setup is complete, use the Google Analytics Data API to query your Google Analytics 4 property

Renamed the credentials.json file to `ga4_prifile.json`.

## Setting Environment Variables

```python
export GOOGLE_APPLICATION_CREDENTIALS=./ga4_prifile.json
export GA_PROPERTY_ID=384740337
```

After installing the packages and setting environment variables, you can call the API to retrieve report data as follows.

```python
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

def run_report(property_id):
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="365daysAgo", end_date="today")],
    )

    response = client.run_report(request)

    print("Report result:")
    for row in response.rows:
        print(row.dimension_values[0].value, row.metric_values[0].value)

def main():
    ga_property_id = os.environ['GA_PROPERTY_ID']
    run_report(ga_property_id)

if __name__ == "__main__":
    main()
```

This script retrieves `the top 15 most viewed pages by page views in the past year`.

## Output

> Most viewed articles in the last year:
>
> 1. `10713` views: [PostgreSQLのpg_dump、pg_restoreについてまとめる](https://zatoima.github.io/postgresql-about-pg_dump-pg_restore.html)
> 2. `6917` views: [Excelのグラフで横軸を1時間ごとのグラフにする方法](https://zatoima.github.io/hourly-graph-for-horizontal-axis-in-excel/)
> 3. `4065` views: [MySQLのFLUSH PRIVILEGESが必要なケース](https://zatoima.github.io/mysql-flush-privileges.html)
> 4. `3971` views: [Auroraの各バージョンのサポート期間](https://zatoima.github.io/aws-aurora-support-eol/)
> 5. `3616` views: [EC2上からpsqlでAurora(PostgreSQL)に接続するまで](https://zatoima.github.io/aws-ec2-psql-install.html)
> 6. `3573` views: [PostgreSQLでfunctionの定義を確認する方法](https://zatoima.github.io/postgresql-function-describe-get.html)
> 7. `2768` views: [OracleとPostgreSQL(+Redshift)のchar、varcharのバイトと文字数の違い](https://zatoima.github.io/oracle-postgresql-char-varchar-byte.html)
> 8. `2720` views: [Data Pump(expdp/impdp)使用時のコマンドとオプション](https://zatoima.github.io/oracle-datapump-command.html)
> 9. `2610` views: [PostgreSQLの監視のためのログ設定について](https://zatoima.github.io/postgresql-about-monitoring-log.html)
> 10. `2385` views: [いまいちどOracle Databaseのデータ移行方法について考えてみる](https://zatoima.github.io/oracle-jpoug-migration-database.html)
> 11. `2193` views: [PostgreSQLでja_JP.UTF-8のデータベース作成時のlocaleエラー](https://zatoima.github.io/postgresql-create-database-locale-error.html)
> 12. `2115` views: [サーバ側と通信するCipher suite (暗号スイート) の調査方法](https://zatoima.github.io/other-cipher-suite-confirm/)
> 13. `2060` views: [PostgreSQLの自動Vacuumの実行タイミングと関連するパラメータ](https://zatoima.github.io/postgresql-auto-vacuum-parameter-timing.html)
> 14. `1940` views: [PostgreSQLで月初、月末日、翌月月初を取得する](https://zatoima.github.io/postgresql-sql-month_first/)
> 15. `1709` views: [S3オブジェクトのmd5やEtagの関係性について整理する](https://zatoima.github.io/aws-s3-object-md5-etag/)
