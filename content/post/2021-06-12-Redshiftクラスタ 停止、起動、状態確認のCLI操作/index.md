---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshiftクラスタ 停止、起動、状態確認のCLI操作"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-cluster-stop-start-check-status
date: 2021-06-12
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

### 停止

```sh
aws redshift pause-cluster --cluster-identifier redshift-ra3
```

### 起動（再開）

```sh
aws redshift resume-cluster --cluster-identifier redshift-ra3
```

### 状態確認

```sh
aws redshift describe-clusters --cluster-identifier redshift-ra3
```

`describe-clusters`で必要な情報だけ取得する

```sh
[ec2-user@bastin ~]$ aws redshift describe-clusters --cluster-identifier redshift-ra3 | jq -r '.Clusters[] | [ .ClusterIdentifier, .NodeType, .ClusterStatus] | @csv'
"redshift-ra3","ra3.4xlarge","paused"
```

