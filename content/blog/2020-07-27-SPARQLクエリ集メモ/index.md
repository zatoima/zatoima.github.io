---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "SPARQLクエリ集メモ"
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

初見のSPARQLエンドポイントに向けて実行するSPARQLクエリをメモ。DBPediaのSPARQLエンドポイントでお試しください。

> http://ja.dbpedia.org/sparql

#### エンドポイントにどんなトリプルがあるのか

```sql
SELECT *
WHERE {
  ?s ?p ?o .
}
LIMIT 100
OFFSET 0 
```

#### エンドポイントのトリプル数

```sql
SELECT (COUNT(*) AS ?count)
WHERE {
  ?s ?p ?o .
}
```

#### 型の確認

```sql
SELECT DISTINCT ?type WHERE {
  ?s a ?type
}
```

#### どのようなプロパティがあるかを確認

```sql
SELECT DISTINCT ?p WHERE {
  ?s a <http://dbpedia.org/ontology/Anime> ;
    ?p ?o.
}
```

#### 名前付きグラフも合算してトリプル数を検索する

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

#### 名前付きグラフの一覧を取得する

```sql
SELECT DISTINCT ?g
WHERE {
  GRAPH ?g { 
    ?s ?p ?o . 
  }
}
```

#### 名前付きグラフ毎の件数を集計

```sql
SELECT ?g count(?g) WHERE {GRAPH ?g {?s ?p ?o}} GROUP BY ?g
```

#### 名前付きグラフのデータを検索

```sql
SELECT * WHERE { GRAPH <あるグラフ> {?s ?p ?o }}
```

#### プロパティの一覧を取得する

```sql
SELECT DISTINCT ?p
WHERE {
  ?s ?p ?o .
}
LIMIT 100
```

#### プロパティの一覧を使用頻度順に取得する

```sql
SELECT ?p (COUNT(?p) AS ?count)
WHERE {
  ?s ?p ?o .
} 
GROUP BY ?p
ORDER BY DESC(?count)
LIMIT 100
```

#### 主語あたりの平均プロパティ数

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

#### <検索データ>が含まれるデータを探したい（主語から探す）

```sql
SELECT * { GRAPH ?g { ?s ?p ?o . FILTER( contains(str(?s),'<検索データ>') ) }}
```

#### <検索データ>が含まれるデータを探したい（述語から探す）

```sql
SELECT * { GRAPH ?g { ?s ?p ?o . FILTER( contains(str(?p),'<検索データ>') ) }}
```

#### <検索データ>が含まれるデータを探したい（目的語から探す）

```sql
SELECT * { GRAPH ?g { ?s ?p ?o . FILTER( contains(str(?o),'<検索データ>') ) }}
```

#### **グラフ**完全一致でデータを探す

```sql
SELECT * { GRAPH <グラフ> {?s ?p ?o}}
```

#### **主語**完全一致でデータを探す

```sql
SELECT * { GRAPH ?g {<主語> ?p ?o}}
```

#### **述語**完全一致でデータを探す

```sql
SELECT * { GRAPH ?g {?s <述語> ?o}}
```

#### **目的語**完全一致でデータを探す

```sql
SELECT * { GRAPH ?g {?s ?p '目的語'}}
```

参考サイト：

> よく使うSPARQLサンプル集 - Qiita https://qiita.com/hodade/items/30158fba9e943132023f
>
> SPARQL入門 http://www.aise.ics.saitama-u.ac.jp/~gotoh/IntroSPARQL.html



