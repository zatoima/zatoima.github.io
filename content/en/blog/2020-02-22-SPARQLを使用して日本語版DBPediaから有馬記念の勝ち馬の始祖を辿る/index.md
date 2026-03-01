---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Tracing the Ancestors of Arima Kinen Winners Using SPARQL on Japanese DBPedia"
subtitle: ""
summary: " "
tags: ["Graph","SPARQL","DBPedia","Neptune"]
categories: ["Graph","SPARQL","DBPedia","Neptune"]
url: sparql-graph-thoroughbred-search.html
date: 2020-02-22
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



## Introduction

DBpedia is a community project that extracts information from Wikipedia and publishes it as LOD (Linked Open Data), with both English and Japanese versions. The Japanese version extracts data from `ja.wikipedia.org`. The extracted data is stored as structured data (RDF). You can retrieve information from an RDF store using a query language called SPARQL. This time, I'll try retrieving information from the Japanese version of DBpedia.

<iframe src="//www.slideshare.net/slideshow/embed_code/key/8lHvTVasgBvWtE" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/takeda/what-isdpbedia" title="DBpedia Japaneseとは？" target="_blank">What is DBpedia Japanese?</a> </strong> from <strong><a href="https://www.slideshare.net/takeda" target="_blank">National Institute of Informatics (NII)</a></strong> </div>

## SPARQL Endpoint

The DBpedia endpoint is here:

> Virtuoso SPARQL Query Editor http://ja.dbpedia.org/sparql

## Information About Arima Kinen Winners

### Exploring Properties

Starting with winners, let's first find out what properties they have.

```SQL
select distinct ?p {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    ?p ?o .
}
```

<img src="image-20200222142308680.png" alt="image-20200222142308680" style="zoom:50%;" />

### Checking Sample Values

Output sample values to see what properties the winners have.

```SQL
select ?p (SAMPLE(?o) AS ?sample_value)
WHERE {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    ?p ?o .
} order by (?p)
```

<img src="image-20200222142141557.png" alt="image-20200222142141557" style="zoom:50%;" />

### Tracing Bloodlines

Next, let's trace the bloodline by looking at father, father's father, father's father's father, and so on, to see how far we can go.

With data stored in an RDBMS, tracing the father of a specific horse's father would require joining the same table with subqueries, and performance would likely hit limits after just a few generations due to repeated joins.

On the other hand, RDF stores and SPARQL are languages well-suited for extracting relationships, so even as the number of relationship extractions increases, it doesn't affect query performance.

By the way, horses that race are called thoroughbreds, but tracing their bloodlines leads back to just 3 horses (Darley Arabian, Godolphin Arabian, Byerley Turk). **If Wikipedia and DBPedia data are correct**, we should be able to trace back to one of these 3.

> Three Foundation Sires and World Bloodlines: Thoroughbred Course - JRA http://www.jra.go.jp/kouza/thoroughbred/founder/

#### 1st Generation

First, let's look up the fathers of the winners.

```SQL
select distinct ?parent_f_name (count(?parent_f_name) AS ?count) {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    prop-ja:父 ?parent_f_name .
} ORDER BY DESC(?count)
```

<img src="image-20200222142450812.png" alt="image-20200222142450812" style="zoom:50%;" />

#### 2nd Generation

Look up the father of the winner's father

```SQL
select distinct ?parent_f_f_name (count(?parent_f_f_name) AS ?count) {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    prop-ja:父 ?parent_f_name .
   ?parent_f_name prop-ja:父 ?parent_f_f_name .
} ORDER BY DESC(?count)
```

<img src="image-20200222144157168.png" alt="image-20200222144157168" style="zoom:50%;" />

#### 18th Generation

Jumping ahead to the 18th generation. Let's see how far we can trace. "Whalebone" is a British horse from `1807-1831`. We've now gone back `18 generations`.

```SQL
select distinct ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name (count(?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name) AS ?count) {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    prop-ja:父 ?parent_f_name .
   ?parent_f_name prop-ja:父 ?parent_f_f_name .
   ?parent_f_f_name prop-ja:父 ?parent_f_f_f_name .
   ?parent_f_f_f_name prop-ja:父 ?parent_f_f_f_f_name .
   ?parent_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
} ORDER BY DESC(?count)
```

<img src="image-20200222144259529.png" alt="image-20200222144259529" style="zoom:50%;" />

#### 19th Generation

```SQL

select distinct ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name (count(?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name) AS ?count) {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    prop-ja:父 ?parent_f_name .
   ?parent_f_name prop-ja:父 ?parent_f_f_name .
   ?parent_f_f_name prop-ja:父 ?parent_f_f_f_name .
   ?parent_f_f_f_name prop-ja:父 ?parent_f_f_f_f_name .
   ?parent_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
} ORDER BY DESC(?count)

```

<img src="image-20200222145756017.png" alt="image-20200222145756017" style="zoom:50%;" />

#### 21st Generation

Going back 21 generations, it narrows down to a single horse called "Waxy." Whalebone's father is Waxy.

```SQL
select distinct ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name (count(?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name) AS ?count) {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    prop-ja:父 ?parent_f_name .
   ?parent_f_name prop-ja:父 ?parent_f_f_name .
   ?parent_f_f_name prop-ja:父 ?parent_f_f_f_name .
   ?parent_f_f_f_name prop-ja:父 ?parent_f_f_f_f_name .
   ?parent_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
} ORDER BY DESC(?count)
```

<img src="image-20200222150544445.png" alt="image-20200222150544445" style="zoom:50%;" />

#### 22nd Generation

When trying to find Waxy's parent, nothing came up. [Whalebone](https://ja.wikipedia.org/wiki/%E3%83%9B%E3%82%A8%E3%83%BC%E3%83%AB%E3%83%9C%E3%83%BC%E3%83%B3)'s father is "[Waxy](https://ja.wikipedia.org/wiki/ワクシー)," but the actual Wikipedia page is "https://ja.wikipedia.org/wiki/ワキシー." The URIs differ between "ワクシー" and "ワキシー," which is why I suspect we cannot trace further.

```SQL
select distinct ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name (count(?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name) AS ?count) {
  {
    ?name prop-ja:wikiPageUsesTemplate template-ja:有馬記念勝ち馬.
  }

  ?name rdfs:label ?label ;
    prop-ja:父 ?parent_f_name .
   ?parent_f_name prop-ja:父 ?parent_f_f_name .
   ?parent_f_f_name prop-ja:父 ?parent_f_f_f_name .
   ?parent_f_f_f_name prop-ja:父 ?parent_f_f_f_f_name .
   ?parent_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
   ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name prop-ja:父 ?parent_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_f_name .
} ORDER BY DESC(?count)
```

![image-20200222150814920](image-20200222150814920.png)

### Conclusion

Next, I'll try the same thing with the English version.

This time I traced only the father, but I'd like to try combining other properties for analysis. I'd also like to try building my own RDF store for horse racing analysis.
