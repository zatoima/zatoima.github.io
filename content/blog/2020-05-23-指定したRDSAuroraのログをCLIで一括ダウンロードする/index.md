---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "指定したRDS／AuroraのログをCLIで一括ダウンロードする"
subtitle: ""
summary: " "
tags: ["PostgreSQL","AWS","Aurora","RDS"]
categories: ["PostgreSQL","AWS","Aurora","RDS"]
url: aws-aurora-rds-log-download.html
date: 2020-05-23
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

##### シェルスクリプト

```sh
#!/bin/bash
DB_INSTANCE=$1

logfilelist=$(aws rds describe-db-log-files --db-instance-identifier $DB_INSTANCE --no-paginate --output text | cut -f3 | cut -d '/' -f2 | sort)

for logfile in $logfilelist; do
	echo "`date +%Y-%m-%d-%H-%M-%S`: "Downloading log file = $logfile""
	aws rds download-db-log-file-portion --db-instance-identifier $DB_INSTANCE --output text --starting-token 0 --log-file-name error/$logfile > $logfile
done
```

##### 実行

```sh
[ec2-user@bastin]$ vi rdslog_get.sh
[ec2-user@bastin]$ ./rdslog_get.sh aurorapgsqlv1
2020-05-14-03-35-05: Downloading log file = pg_upgrade_dump_13322.log.1589425177488
2020-05-14-03-35-06: Downloading log file = pg_upgrade_dump_16384.log.1589425177488
2020-05-14-03-35-06: Downloading log file = pg_upgrade_dump_16399.log.1589425177488
2020-05-14-03-35-07: Downloading log file = pg_upgrade_dump_1.log.1589425177488
2020-05-14-03-35-07: Downloading log file = pg_upgrade_internal.log.1589425177488
2020-05-14-03-35-08: Downloading log file = pg_upgrade_server.log.1589425177488
2020-05-14-03-35-08: Downloading log file = postgres.log
2020-05-14-03-35-09: Downloading log file = postgresql.log.2020-05-14-02
2020-05-14-03-35-09: Downloading log file = postgresql.log.2020-05-14-0259
2020-05-14-03-35-10: Downloading log file = postgresql.log.2020-05-14-0300
```

