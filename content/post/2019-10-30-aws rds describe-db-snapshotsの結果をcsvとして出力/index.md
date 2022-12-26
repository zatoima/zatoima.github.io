---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "aws rds describe-db-snapshotsの結果をcsvとして出力"
subtitle: ""
summary: " "
tags: ["AWS","RDS"]
categories: ["AWS","RDS"]
url: aws-awscli-rds-descrive-db-snapshot.html
date: 2019-10-30
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



jqコマンドの書式がググらないとわからない

#### コマンド

```sh
aws rds describe-db-snapshots --db-snapshot-identifier rdspostgresqldb-snapshot-test20191130-1 \
--query "DBSnapshots[].{DBInstanceIdentifier:DBInstanceIdentifier,DBSnapshotIdentifier:DBSnapshotIdentifier,SnapshotCreateTime:SnapshotCreateTime}" \
--output json | \
jq -r ".[] | [.DBInstanceIdentifier,.DBSnapshotIdentifier,.SnapshotCreateTime] | @csv"
```

#### 結果

```sh
"rdspostgresqldb","rdspostgresqldb-snapshot-test20191130-1","2019-11-30T06:47:14.370Z"
```

