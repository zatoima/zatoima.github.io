---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Outputting aws rds describe-db-snapshots Results as CSV"
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



The jq command syntax is something I always have to look up.

#### Command

```sh
aws rds describe-db-snapshots --db-snapshot-identifier rdspostgresqldb-snapshot-test20191130-1 \
--query "DBSnapshots[].{DBInstanceIdentifier:DBInstanceIdentifier,DBSnapshotIdentifier:DBSnapshotIdentifier,SnapshotCreateTime:SnapshotCreateTime}" \
--output json | \
jq -r ".[] | [.DBInstanceIdentifier,.DBSnapshotIdentifier,.SnapshotCreateTime] | @csv"
```

#### Result

```sh
"rdspostgresqldb","rdspostgresqldb-snapshot-test20191130-1","2019-11-30T06:47:14.370Z"
```
