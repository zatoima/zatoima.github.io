---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Amazon CloudWatchのメトリクスをCSVで出力する"
subtitle: ""
summary: " "
tags: ["AWS","CloudWatch"]
categories: ["AWS","CloudWatch"]
url: aws-cloudwatch-csv-export-command.html
date: 2020-05-10
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



### 前提

jqを使用するのでyum等で別途インストールが必要。

```sh
sudo yum -y install jq
```

### コマンド

```sh
aws cloudwatch get-metric-statistics --namespace AWS/Neptune --metric-name VolumeBytesUsed --start-time 2020-05-06T00:00:00 --end-time 2020-05-07T12:00:00 --period 300 --statistics Average --dimensions Name=DBClusterIdentifier,Value=neploadtest1   | jq -r '.Datapoints[] | [ .Timestamp ,.Average ,.Unit] | @csv' | sort -t ',' -k 1
```

### 結果

```sh
[ec2-user@bastin ~]$ aws cloudwatch get-metric-statistics --namespace AWS/Neptune --metric-name VolumeBytesUsed --start-time 2020-05-06T00:00:00 --end-time 2020-05-07T12:00:00 --period 300 --statistics Average --dimensions Name=DBClusterIdentifier,Value=neploadtest1   | jq -r '.Datapoints[] | [ .Timestamp ,.Average ,.Unit] | @csv' | sort -t ',' -k 1
"2020-05-06T06:05:00Z",0,"Bytes"
"2020-05-06T06:15:00Z",126189568,"Bytes"
"2020-05-06T06:20:00Z",24679677952,"Bytes"
"2020-05-06T06:25:00Z",24679677952,"Bytes"
"2020-05-06T06:30:00Z",24679677952,"Bytes"
"2020-05-06T06:35:00Z",35896573952,"Bytes"
"2020-05-06T06:40:00Z",35896573952,"Bytes"
"2020-05-06T06:45:00Z",35896573952,"Bytes"
"2020-05-06T06:50:00Z",55787798528,"Bytes"
"2020-05-06T06:55:00Z",55787798528,"Bytes"
"2020-05-06T07:00:00Z",64544718848,"Bytes"
"2020-05-06T07:05:00Z",64544718848,"Bytes"
"2020-05-06T07:10:00Z",64544718848,"Bytes"
"2020-05-06T07:15:00Z",64546799616,"Bytes"
"2020-05-06T07:20:00Z",64546799616,"Bytes"
"2020-05-06T07:25:00Z",64546799616,"Bytes"
"2020-05-06T07:30:00Z",76659359744,"Bytes"
"2020-05-06T07:35:00Z",76659359744,"Bytes"
"2020-05-06T07:40:00Z",92551282688,"Bytes"
"2020-05-06T07:45:00Z",92551282688,"Bytes"
"2020-05-06T07:50:00Z",92551282688,"Bytes"
"2020-05-06T07:55:00Z",93257973760,"Bytes"
```

