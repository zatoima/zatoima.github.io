---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "CLI Operations for Stopping, Starting, and Checking Status of Redshift Clusters"
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

### Stop

```sh
aws redshift pause-cluster --cluster-identifier redshift-ra3
```

### Start (Resume)

```sh
aws redshift resume-cluster --cluster-identifier redshift-ra3
```

### Check Status

```sh
aws redshift describe-clusters --cluster-identifier redshift-ra3
```

Get only the necessary information with `describe-clusters`

```sh
[ec2-user@bastin ~]$ aws redshift describe-clusters --cluster-identifier redshift-ra3 | jq -r '.Clusters[] | [ .ClusterIdentifier, .NodeType, .ClusterStatus] | @csv'
"redshift-ra3","ra3.4xlarge","paused"
```
