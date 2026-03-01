---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Exporting Amazon Elasticsearch Service Search Results as CSV"
subtitle: ""
summary: " "
tags: ["AWS","Elasicsearch"]
categories: ["AWS","Elasicsearch"]
url: aws-elasticsearch-csv-output.html
date: 2020-08-13
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

### Prerequisites

Install the `jq` command and `in2csv` (included in csvkit, converts JSON output to CSV) beforehand. A Python environment is also required.

```sh
sudo yum -y install jq
pip install csvkit
```

### Get Elasticsearch Results in CSV Format

```sh
curl https://vpc-xxxxxxx-xxxxxx.ap-northeast-1.es.amazonaws.com/xxxxxxx/_search?pretty | jq [.hits.hits[]._source] | in2csv -f json
```
