---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshiftへのデータロード"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-dataload-from-s3.html
date: 2021-04-01
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



IAMロールと必要なIAMロールのクラスタへのアタッチ等は完了済という想定。

### ロード用のファイルをS3にアップロードする

```sh
aws s3 cp aozora_data.csv s3://xxxx/load/
```

ロード用のファイルは約6G、約1億件弱。(青空文庫のテキストデータ)

```
[ec2-user@bastin ~]$ ls -lh aozora_data.csv
-rw-rw-r-- 1 ec2-user ec2-user 6.1G Dec 16  2012 aozora_data.csv
[ec2-user@bastin ~]$ wc -l aozora_data.csv
87701673 aozora_data.csv
```

### Redshiftにロード先のテーブルを用意

```sh
CREATE TABLE aozora_data(file VARCHAR(100),num INT,row INT,word TEXT,subtype1 VARCHAR(100),subtype2 VARCHAR(100),subtype3 VARCHAR(100),subtype4 VARCHAR(100),conjtype VARCHAR(30),conjugation VARCHAR(30),basic TEXT,ruby TEXT,pronunce TEXT );
```

### データロード実行

```sh
copy aozorabunko_data from 's3://xxxxx/load/aozora_data.csv' 
iam_role 'arn:aws:iam::xxxxx:role/myRedshiftRole'
csv;
```

上記の方法はアンチパターンであり、一つのスライスでしか実行されず、MPPアーキテクチャのRedshiftではリソースを有効活用出来ない。下記のベスト・プラクティスにある通り、ファイル分割、ファイル圧縮を実施した上での実行が望ましい。

> Amazon Redshift データのロードのベストプラクティス - Amazon Redshift https://docs.aws.amazon.com/ja_jp/redshift/latest/dg/c_loading-data-best-practices.html

### データ分割

```
split -n 8 -d aozora_data.csv part-
```



