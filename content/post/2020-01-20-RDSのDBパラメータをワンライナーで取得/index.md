---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "RDSのDBパラメータをワンライナーで取得"
subtitle: ""
summary: " "
tags: ["AWS","RDS"]
categories: ["AWS","RDS"]
url: aws-rds-oneliner-get.html
date: 2020-01-20
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



RDSのパラメータグループの設定値をawscliを通じて取得する。下記のようなCSVを取得するイメージ。

```text
"名前","値","許可された値","変更可能","送信元","適用タイプ","データ型","説明","ApplyMethod","MinimumEngineVersion"
"application_name",,,true,"engine-default","dynamic","string","Sets the application name to be reported in statistics and logs.","pending-reboot",
"archive_command","/etc/rds/dbbin/pgscripts/rds_wal_archive %p",,false,"system","dynamic","string","Sets the shell command that will be called to archive a WAL file.","pending-reboot",
"archive_timeout","300","0-2147483647",false,"system","dynamic","integer","(s) Forces a switch to the next xlog file if a new file has not been started within N seconds.","pending-reboot",
"array_nulls",,"0,1",true,"engine-default","dynamic","boolean","Enable input of NULL elements in arrays.","pending-reboot",

～中略～
```

##### jqのインストール

```sh
[root@bastin ~]# yum -y install jq
```

##### aws rds describe-db-parametersで実行

```sh
[root@bastin ~]# aws rds describe-db-parameters --db-parameter-group-name db-prm-postgres10 \
    | jq -r '["名前","値","許可された値","変更可能","送信元","適用タイプ","データ型","説明","ApplyMethod","MinimumEngineVersion"], (.Parameters[] | [.ParameterName,.ParameterValue,.AllowedValues,.IsModifiable,.Source,.ApplyType,.DataType,.Description,.ApplyMethod,.MinimumEngineVersion]) | @csv'
```



