---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "My Personal Collection of Frequently Used Elasticsearch Commands"
subtitle: ""
summary: " "
tags: ["AWS","Elasticsearch"]
categories: ["AWS","Elasticsearch"]
url: aws-elasticsearch-commands-lists.html
date: 2020-05-05
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

Assumes command execution on Amazon Elasticsearch Service. Updated as needed.

### Create an Index

```sh
curl -X PUT "<Amazon Elasticsearch Service endpoint>/<index_name>"
```

### Check Indices

```sh
curl <Amazon Elasticsearch Service endpoint>/_aliases?pretty
```

### Check Index Details

```sh
curl <Amazon Elasticsearch Service endpoint>/<index_name>/_settings?pretty
```

### Delete an Index

```sh
curl -XDELETE <Amazon Elasticsearch Service endpoint>/<index_name>?pretty=true
```

### Search Data (No Conditions)

```sh
curl <Amazon Elasticsearch Service endpoint>/<index_name>/_search?pretty
```

### Check Index

```sh
curl <Amazon Elasticsearch Service endpoint>/_cat/indices?v
```

### Check Count

```sh
curl <Amazon Elasticsearch Service endpoint>/_cat/count/<index_name>?v
curl <Amazon Elasticsearch Service endpoint>/<index_name>/_count?pretty
```

### Statistics

```sh
curl <Amazon Elasticsearch Service endpoint>/<index_name>/_stats?pretty
```

### Check Aliases

```sh
curl <Amazon Elasticsearch Service endpoint>/_aliases?pretty
```

### Create Aliases

```sh
curl  -H "Content-Type: application/json" -XPOST '<Amazon Elasticsearch Service endpoint>/_aliases' -d '
{
  "actions" : [
    { "add" : { "index" : "my_index1", "alias" : "my_ind1" } },
    { "add" : { "index" : "my_index2", "alias" : "my_ind2" } }
  ]
}'
```

### Delete Aliases

```sh
curl  -H "Content-Type: application/json" -XPOST '<Amazon Elasticsearch Service endpoint>/_aliases' -d '
{
  "actions" : [
    { "remove" : { "index" : "my_index1", "alias" : "my_ind1" } },
    { "remove" : { "index" : "my_index2", "alias" : "my_ind2" } }
  ]
}'
```

### List Available cat Commands

```sh
curl <Amazon Elasticsearch Service endpoint>/_cat
```

### Check Mapping

```sh
curl <Amazon Elasticsearch Service endpoint>/<index_name>/_mapping?pretty
```

### Check Each Node's Role

```sh
curl <Amazon Elasticsearch Service endpoint>/_cat/nodes
```

### Check the Master Node

```sh
curl <Amazon Elasticsearch Service endpoint>/_cat/master
```

### Check Which Node Contains Which Shards

```sh
curl <Amazon Elasticsearch Service endpoint>/_cat/shards
```

### Check Field Data

```sh
curl -XGET <Amazon Elasticsearch Service endpoint>/_stats/fielddata?pretty
```
