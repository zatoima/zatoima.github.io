---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshiftから特定区切り文字でファイル出力する"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-system-table-unload
date: 2022-01-27
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---



検証時にRedshiftのシステムテーブルなどのデータを抜いて退避させたい。

ヘッダー出力ONで、デフォルトだとスライス数分ファイルが分割して、マージするのも面倒なためパラレルをオフにして「|」区切りにしてgzip形式で出力するコマンド。ファイル重複する場合、上書きする。

```sql
unload ('select * from svl_s3query_summary order by elapsed;')
to 's3://ssbgz-spectrum/svl_s3query_summary_log' 
iam_role 'arn:aws:iam::xxxxxxxxxxxx:role/myRedshiftRole'
delimiter '|'
header
format csv
gzip
parallel off
allowoverwrite;
```

> 区切り文字付きまたは固定幅形式でデータをアンロードする - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/t_unloading_fixed_width_data.html

