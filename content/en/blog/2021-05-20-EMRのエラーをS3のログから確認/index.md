---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Checking EMR Errors from S3 Logs"
subtitle: ""
summary: " "
tags: ["AWS","EMR"]
categories: ["AWS","EMR"]
url: aws-emr-error-log-s3-command.html
date: 2021-05-20
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



### Create and Navigate to Log Download Directory

```csharp
mkdir j-3PS6MU0W27GMG
cd j-3PS6MU0W27GMG
```

### Download Logs

Note: `j-3PS6MU0W27GMG` is the Cluster ID

```sh
aws s3 sync s3://aws-logs-xxx-ap-northeast-1/elasticmapreduce/j-3PS6MU0W27GMG .
```

### Decompress

```sh
find . -type f -exec gunzip {} \;
```

### Search for Errors and Warnings

Sort in chronological order

```sh
find . | grep log | xargs egrep "WARN|ERROR" | sort -k2
```
