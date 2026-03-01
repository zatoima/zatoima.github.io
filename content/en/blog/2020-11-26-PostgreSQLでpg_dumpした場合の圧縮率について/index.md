---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Compression Ratio When Using pg_dump in PostgreSQL"
subtitle: ""
summary: " "
tags: ["PostgreSQL"]
categories: ["PostgreSQL"]
url: aws-postgresql-pg_dump_zip.html
date: 2020-11-26
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

Verification of compression ratios. The `-Fc` option was used to output in custom file (compressed) format. Here are the results. Data consisting mainly of integers and strings shows higher compression ratios.

| No   | Test Pattern | DB Name  | DB Size (GB) | Data Content                                    | Dump File Size (GB) | Compression Ratio |
| ---- | ------------ | -------- | ------------ | ----------------------------------------------- | ------------------- | ----------------- |
| 1    | pg_dump      | postgres | 729GB        | Text data from Aozora Bunko                     | 66                  | 9%                |
| 2    |              | tpch     | 45GB         | HammerDB TPC-H data                             | 9.9                 | 22%               |
| 3    |              | tpcc     | 118GB        | HammerDB TPC-C data                             | 34                  | 29%               |
| 4    |              | blob     | 98GB         | Binary data in bytea (25MB files x 4000 files)  | 108                 | 110%              |


