---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "SPARQL Query Collection Notes"
subtitle: ""
summary: " "
tags: ["SPARQL","Neptune","DBpedia"]
categories: ["SPARQL","Neptune","DBpedia"]
url: sparql-query-note.html
date: 2020-07-27
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

Notes on SPARQL queries to run against an unfamiliar SPARQL endpoint. Try these on the DBPedia SPARQL endpoint:

> http://ja.dbpedia.org/sparql

#### What Triples Exist at the Endpoint

```sql
SELECT *
WHERE {
  ?s ?p ?o .
}
LIMIT 100
OFFSET 0
```

#### Number of Triples at the Endpoint

```sql
SELECT (COUNT(*) AS ?count)
WHERE {
  ?s ?p ?o .
}
```

#### Check Types

```sql
SELECT DISTINCT ?type WHERE {
  ?s a ?type
}
```

#### Check What Properties Exist

```sql
SELECT DISTINCT ?p WHERE {
  ?s a <http://dbpedia.org/ontology/Anime> ;
    ?p ?o.
}
```

#### Count Triples Including Named Graphs

```sql
SELECT (COUNT(*) AS ?count)
WHERE {
  {
    ?s ?p ?o .
  } UNION {
    GRAPH ?g {
      ?s ?p ?o .
    }
  }
}
```

#### Get a List of Named Graphs

```sql
SELECT DISTINCT ?g
WHERE {
  GRAPH ?g {
    ?s ?p ?o .
  }
}
```

#### Count Records Per Named Graph

```sql
SELECT ?g count(?g) WHERE {GRAPH ?g {?s ?p ?o}} GROUP BY ?g
```

#### Search Data in a Named Graph

```sql
SELECT * WHERE { GRAPH <some-graph> {?s ?p ?o }}
```

#### Get a List of Properties

```sql
SELECT DISTINCT ?p
WHERE {
  ?s ?p ?o .
}
LIMIT 100
```

#### Get Properties Ordered by Frequency of Use

```sql
SELECT ?p (COUNT(?p) AS ?count)
WHERE {
  ?s ?p ?o .
}
GROUP BY ?p
ORDER BY DESC(?count)
LIMIT 100
```

#### Average Number of Properties per Subject

```sql
SELECT (AVG(?count) AS ?average)
WHERE {
  SELECT ?s (COUNT(?p) as ?count)
  WHERE {
    ?s ?p ?o .
  }
  GROUP BY ?s
}
```

#### Find Data Containing \<search-value\> (Search by Subject)

```sql
SELECT * { GRAPH ?g { ?s ?p ?o . FILTER( contains(str(?s),'<search-value>') ) }}
```

#### Find Data Containing \<search-value\> (Search by Predicate)

```sql
SELECT * { GRAPH ?g { ?s ?p ?o . FILTER( contains(str(?p),'<search-value>') ) }}
```

#### Find Data Containing \<search-value\> (Search by Object)

```sql
SELECT * { GRAPH ?g { ?s ?p ?o . FILTER( contains(str(?o),'<search-value>') ) }}
```

#### Find Data with Exact Match on **Graph**

```sql
SELECT * { GRAPH <graph> {?s ?p ?o}}
```

#### Find Data with Exact Match on **Subject**

```sql
SELECT * { GRAPH ?g {<subject> ?p ?o}}
```

#### Find Data with Exact Match on **Predicate**

```sql
SELECT * { GRAPH ?g {?s <predicate> ?o}}
```

#### Find Data with Exact Match on **Object**

```sql
SELECT * { GRAPH ?g {?s ?p 'object'}}
```

References:

> Frequently Used SPARQL Sample Queries - Qiita https://qiita.com/hodade/items/30158fba9e943132023f
>
> Introduction to SPARQL http://www.aise.ics.saitama-u.ac.jp/~gotoh/IntroSPARQL.html
