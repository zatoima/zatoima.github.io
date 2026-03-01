---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Checking the Elasticsearch Master Node"
subtitle: ""
summary: " "
tags: ["AWS","Elasticsearch"]
categories: ["AWS","Elasticsearch"]
url: aws-elasticsearch-masternode-check.html
date: 2020-04-29
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



### Check the Role of Each Node

`di` indicates a data node and `m` indicates a master-eligible node. The one with an asterisk among them is the currently active master node.

#### Command

```
curl https://vpc-xxxxxxxxx-xxxxxxxxx.ap-northeast-1.es.amazonaws.com/_cat/nodes
```

#### Result

```
[ec2-user@bastin ~]$ curl https://vpc-xxxxxxxxx-xxxxxxxxx.ap-northeast-1.es.amazonaws.com/_cat/nodes
x.x.x.x 14 84 7 0.56 0.34 0.14 di - d80e9ad21a626ddb1cd444cf42921a08
x.x.x.x 11 87 6 0.10 0.07 0.02 m  - dd1a87f44380da342e4e72c3195e0ebd
x.x.x.x 15 86 0 0.22 0.13 0.06 m  * 73cde264f7a37e9ca4b5b95ae7f69565
x.x.x.x   15 87 0 0.05 0.06 0.02 m  - 9fc04f6429d0471cdfd8e31b0ab73f46
x.x.x.x  14 84 1 0.22 0.18 0.06 di - 2245efa92445b06e79699db2acd06091
```

### Check the Master Node

#### Command

```
curl https://vpc-xxxxxxxxx-xxxxxxxxx.ap-northeast-1.es.amazonaws.com/_cat/master
```

#### Result

```
[ec2-user@bastin ~]$ curl https://vpc-xxxxxxxxx-xxxxxxxxx.ap-northeast-1.es.amazonaws.com/_cat/master
V9KHonTYTWOtt4vsGs2NBw x.x.x.x x.x.x.x 73cde264f7a37e9ca4b5b95ae7f69565
```
