---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "DBpediaのデータ(turtle)をwgetで一括ダウンロード"
subtitle: " "
summary: " "
tags: ["DBpedia"]
categories: ["DBpedia"]
url: dbpedia-jp-wget-download.html
date: 2020-02-27
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



### 

日本語版のDBpediaの現時点の最新版である http://ja.dbpedia.org/dumps/20160407/ 配下の全データをwgetで再帰的に取得しています。「-np」は親ディレクトリを取得対象しないようにするためのオプションです。

```sh
wget -r -np -R "index.html?*" http://ja.dbpedia.org/dumps/20160407/
```

### 取得結果

```sh
[ec2-user@bastin 20160407]$ pwd
/home/ec2-user/dbpedia/ja.dbpedia.org/dumps/20160407
[ec2-user@bastin 20160407]$ du -sh
4.4G	.
[ec2-user@bastin 20160407]$ ls -l
total 4306268
-rw-rw-r-- 1 ec2-user ec2-user      16381 Feb 25 01:26 index.html
-rw-rw-r-- 1 ec2-user ec2-user   64620507 Apr 27  2016 jawiki-20160407-article-categories.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   36087466 Apr 27  2016 jawiki-20160407-article-categories.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   11199701 Apr 27  2016 jawiki-20160407-article-templates-nested.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user    5854138 Apr 27  2016 jawiki-20160407-article-templates-nested.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   58951338 Apr 27  2016 jawiki-20160407-article-templates.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   29388098 Apr 27  2016 jawiki-20160407-article-templates.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    2441006 Apr 27  2016 jawiki-20160407-category-labels.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user    1416295 Apr 27  2016 jawiki-20160407-category-labels.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    2047854 Apr 27  2016 jawiki-20160407-disambiguations-unredirected.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user    1258154 Apr 27  2016 jawiki-20160407-disambiguations-unredirected.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   35396297 Apr 27  2016 jawiki-20160407-external-links.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   24184031 Apr 27  2016 jawiki-20160407-external-links.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user     586677 Apr 27  2016 jawiki-20160407-geo-coordinates-mappingbased.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user     390558 Apr 27  2016 jawiki-20160407-geo-coordinates-mappingbased.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    1052110 Apr 27  2016 jawiki-20160407-geo-coordinates.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user     710988 Apr 27  2016 jawiki-20160407-geo-coordinates.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    3242564 Apr 27  2016 jawiki-20160407-homepages.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user    2018246 Apr 27  2016 jawiki-20160407-homepages.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   25713177 Apr 27  2016 jawiki-20160407-images.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   18660941 Apr 27  2016 jawiki-20160407-images.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user  146867252 Apr 27  2016 jawiki-20160407-infobox-properties-unredirected.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user  106114414 Apr 27  2016 jawiki-20160407-infobox-properties-unredirected.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user     539768 Apr 27  2016 jawiki-20160407-infobox-property-definitions.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user     257668 Apr 27  2016 jawiki-20160407-infobox-property-definitions.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user         91 Apr 27  2016 jawiki-20160407-infobox-test.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user         92 Apr 27  2016 jawiki-20160407-infobox-test.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    6749954 Apr 27  2016 jawiki-20160407-instance-types.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   20605723 Apr 27  2016 jawiki-20160407-instance-types-transitive.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   12598132 Apr 27  2016 jawiki-20160407-instance-types-transitive.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    3302762 Apr 27  2016 jawiki-20160407-instance-types.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user     777393 Apr 27  2016 jawiki-20160407-interlanguage-links.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user     482555 Apr 27  2016 jawiki-20160407-interlanguage-links.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   30962284 Apr 27  2016 jawiki-20160407-labels.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   19374825 Apr 27  2016 jawiki-20160407-labels.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   23766215 Apr 27  2016 jawiki-20160407-mappingbased-literals.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   14463439 Apr 27  2016 jawiki-20160407-mappingbased-literals.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   28382739 Apr 27  2016 jawiki-20160407-mappingbased-objects-uncleaned-unredirected.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   16038031 Apr 27  2016 jawiki-20160407-mappingbased-objects-uncleaned-unredirected.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   26566377 Apr 27  2016 jawiki-20160407-out-degree.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   14217551 Apr 27  2016 jawiki-20160407-out-degree.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   34738422 Apr 27  2016 jawiki-20160407-page-ids.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   19564834 Apr 27  2016 jawiki-20160407-page-ids.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   28049111 Apr 27  2016 jawiki-20160407-page-length.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   15491318 Apr 27  2016 jawiki-20160407-page-length.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user  569374886 Apr 27  2016 jawiki-20160407-page-links-unredirected.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user  367564292 Apr 27  2016 jawiki-20160407-page-links-unredirected.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   33225236 Apr 27  2016 jawiki-20160407-page_props.sql.gz
-rw-rw-r-- 1 ec2-user ec2-user 2285740564 Apr 27  2016 jawiki-20160407-pages-articles.xml.bz2
-rw-rw-r-- 1 ec2-user ec2-user   12735146 Apr 27  2016 jawiki-20160407-redirects.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user    8214822 Apr 27  2016 jawiki-20160407-redirects.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   36232990 Apr 27  2016 jawiki-20160407-revision-ids.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   22263076 Apr 27  2016 jawiki-20160407-revision-ids.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   38797873 Apr 27  2016 jawiki-20160407-revision-uris.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   29276720 Apr 27  2016 jawiki-20160407-revision-uris.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user    7261254 Apr 27  2016 jawiki-20160407-skos-categories.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user    4328988 Apr 27  2016 jawiki-20160407-skos-categories.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user     751735 Apr 27  2016 jawiki-20160407-specific-mappingbased-properties.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user     381452 Apr 27  2016 jawiki-20160407-specific-mappingbased-properties.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user      12460 Apr 27  2016 jawiki-20160407-topical-concepts-unredirected.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user       7402 Apr 27  2016 jawiki-20160407-topical-concepts-unredirected.ttl.bz2
-rw-rw-r-- 1 ec2-user ec2-user   60923158 Apr 27  2016 jawiki-20160407-wikipedia-links.tql.bz2
-rw-rw-r-- 1 ec2-user ec2-user   37255115 Apr 27  2016 jawiki-20160407-wikipedia-links.ttl.bz2
drwxrwxr-x 2 ec2-user ec2-user        214 Feb 25 01:28 links
[ec2-user@bastin 20160407]$ 
```



