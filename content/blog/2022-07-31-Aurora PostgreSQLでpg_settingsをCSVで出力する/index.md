---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Aurora PostgreSQLでpg_settingsをCSVで出力する"
subtitle: ""
summary: " "
tags: ["AWS","Aurora"]
categories: ["AWS","Aurora"]
url: aws-aurora-postgresql-pg_settings-csv-output
date: 2022-07-31
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



#### コマンド

-----

区切り文字をコンマ（,）でなく、"|"としている

```sql
psql -h auroraserverlessv2.cluster-xxxxxx.ap-northeast-1.rds.amazonaws.com -c "select * from pg_settings;" -U postgres -d postgres  -A -F"|" > pg_settings.csv
```

