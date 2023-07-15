---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "バックスラッシュがあるデータをSnowflakeにロードする"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: aws-dynamodb-to-s3-csv-transform-python-lamdba
date: 2022-05-06
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

バックスラッシュが含まれているデータをロードしようとしたところエラーが発生した。

### エラー

```sh
100068 (22000): End of record reached while expected to parse column '"TESTTBL"["COL2":3]'
  ファイル「test_data.csv」、行 330145、文字 236
  行 3 "COL2"["COL2":3]
  エラーが発生してもロードを継続したい場合は、ON_ERRORオプションに「SKIP_FILE」または「CONTINUE」などの別の値を使用します。ロードのオプションの詳細については、SQLクライアントで「info loading_data」を実行してください。
```

### 原因・対策

ESCAPE_UNENCLOSED_FIELDのデフォルト値が'\\\'であるため、ファイルフォーマットかデータロード時にESCAPE_UNENCLOSED_FIELDをNONEに設定する。

```sql
COPY INTO testtable
FROM @S3_ext_stage/
file_format = (format_name = tsv_format ESCAPE_UNENCLOSED_FIELD = NONE)
pattern='*.csv';
```

> [How To: Load data with backslash\(\\\) in Snowflake table](https://community.snowflake.com/s/article/How-To-Load-data-with-backslash-in-Snowflake-table)
