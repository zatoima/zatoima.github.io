---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Configure Elasticsearch Aliases"
subtitle: ""
summary: " "
tags: ["AWS","Elasticsearch"]
categories: ["AWS","Elasticsearch"]
url: aws-elasticsearch-alias-setting.html
date: 2020-05-04
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

This was performed on Amazon Elasticsearch Service on AWS.

As the name suggests, aliases allow you to assign alternative names to indices. The relationship between aliases and indices is not one-to-one; you can associate multiple indices with a single alias.

#### Create Indices

First, create indices as preparation.

```sh
curl -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index1"
curl -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index2"
```

#### Register Data (for my_index1)

Insert test data for later alias-based searches.

```sh
curl -H "Content-Type: application/json" -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index1/_doc/1" -d '
{
  "title": "my_index1",
  "comments": {
    "name": "my_index1",
    "comment": "Data for my_index1"
  }
}'
```

#### Register Data (for my_index2)

```sh
curl -H "Content-Type: application/json" -X PUT "https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_index2/_doc/1" -d '
{
  "title": "my_index2",
  "comments": {
    "name": "my_index2",
    "comment": "Data for my_index2"
  }
}'
```

#### Check Aliases

No aliases are configured in the initial state.

```sh
{
  "amazon_neptune" : {
    "aliases" : { }
  },
  ".kibana_1" : {
    "aliases" : {
      ".kibana" : { }
    }
  },
  "my_index2" : {
    "aliases" : { }
  },
  "my_index1" : {
    "aliases" : { }
  }
}
```

#### Create an Alias

Create an alias `my_ind` for `my_index1`.

```sh
curl  -H "Content-Type: application/json" -XPOST 'https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases' -d '
{
  "actions" : [
    { "add" : { "index" : "my_index1", "alias" : "my_ind" } }
  ]
}'
```

#### Check Aliases

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases?pretty
```

`my_ind` has been created.

```sh
  "my_index2" : {
    "aliases" : { }
  },
  "my_index1" : {
    "aliases" : {
      "my_ind" : { }
    }
```

Searching now returns data from `my_index1`.

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_ind/_search?pretty
```

#### Change an Alias

Next, switch the index by updating the alias configuration.

```sh
curl  -H "Content-Type: application/json" -XPOST 'https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases' -d '
{
  "actions" : [
    { "remove" : { "index" : "my_index1", "alias" : "my_ind" } },
    { "add"    : { "index" : "my_index2", "alias" : "my_ind" } }
  ]
}'
```

#### Check Aliases

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/_aliases?pretty
```

Unlike before, the alias now points to `my_index2`. The alias for `my_index1` has been removed.

```sh
  "my_index2" : {
    "aliases" : {
      "my_ind" : { }
    }
  },
  "my_index1" : {
    "aliases" : { }
  }

```

#### Search Using the Alias

```sh
curl https://vpc-xxxxxxxx-xxxxxxxxxxxxxx.ap-northeast-1.es.amazonaws.com/my_ind/_search?pretty
```

By using this alias feature, you can switch indices with zero downtime.

> Changing Mapping with Zero Downtime | Elastic Blog https://www.elastic.co/jp/blog/changing-mapping-with-zero-downtime/
>
> Rebuilding Elasticsearch Indices with Zero Downtime - Cookpad Developer Blog https://techlife.cookpad.com/entry/2015/09/25/170000
