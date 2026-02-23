---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GA4のデータをPython（Analytics Data API）で取得する"
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

## はじめに

PythonのAnalytics Data APIを利用すると、GA4のデータを柔軟に取得し、分析やレポーティングに活用できる。GA4のデータをPythonから扱ってHugoの静的ジェネレーターに貼り付けるためのステップを検討。

## Analytics Data APIとは

Analytics Data APIは、GA4のデータにプログラムでアクセスするためのAPI。レポートのデータを取得したり、カスタムレポートを作成したりできる。GCPの使用が前提でアカウントは必須な模様。

## Pythonでの利用方法

PythonからAnalytics Data APIを使う場合、`google-api-python-client`と`google-analytics-data `パッケージを利用する。

```python
pip install google-api-python-client
pip install google-analytics-data
```

## Analytics Data APIの有効化

https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries?hl=ja

> API を有効にする
>
> - Cloud Platform プロジェクトを作成し、Google Analytics Data API v1 を有効にする
> - `credentials.json` ファイルをダウンロードし、作業ディレクトリに保存する
>
> Google アナリティクス 4 プロパティにサービス アカウントを追加する
>
> - `credentials.json` ファイルから `client_email` フィールドのサービス アカウントのメールアドレスを取得する
> - 取得したメールアドレスを使用して、Google アナリティクス 4 プロパティにユーザーを追加する（閲覧者権限のみ）
>
> 認証を構成する
>
> - サービス アカウントの認証情報を指定するために、`GOOGLE_APPLICATION_CREDENTIALS` 環境変数を設定する
> - 環境変数の値として、ステップ 1 でダウンロードしたサービス アカウント JSON ファイルのパスを指定する
>
> クライアント ライブラリをインストールする
>
> - 選択したプログラミング言語に応じて、Google Analytics Data API のクライアント ライブラリをインストールする
>
> API 呼び出しを行う
>
> - 認証とクライアント ライブラリのセットアップが完了したら、Google Analytics Data API を使用して Google アナリティクス 4 プロパティにクエリを実行する

credentials.jsonの名前を`ga4_prifile.json`に変更した。

## 環境変数の設定

```python
export GOOGLE_APPLICATION_CREDENTIALS=./ga4_prifile.json
export GA_PROPERTY_ID=384740337
```

パッケージのインストールと環境変数を設定後、以下のようにAPIを呼び出してレポートデータを取得できる。

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

このスクリプトでは、`過去1年間のページ別のページビュー数を、ページビューの多い順に15件取得`。

## アウトプット

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
