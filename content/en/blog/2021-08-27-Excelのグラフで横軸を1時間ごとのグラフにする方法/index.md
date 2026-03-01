---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Create an Hourly X-Axis Chart in Excel"
subtitle: ""
summary: " "
tags: ["その他"]
categories: ["その他"]
url: hourly-graph-for-horizontal-axis-in-excel
date: 2021-08-27
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: f
---

This wasn't immediately obvious, so I'm noting it down.

I wanted to create a chart like the one below with an hourly x-axis (horizontal axis). The data itself is not complete; it is collected only at arbitrary times.

![image-20210826185024343](image-20210826185024343.png)

Instead of a line chart, use a scatter chart, and set the axis unit in the "Format Axis" settings to "0.041666666666", which is the serial value representing one hour. By changing this serial value, you can adjust the unit of the X-axis.

![image-20210826185136781](image-20210826185136781.png)

Reference

> Excel Graph Time: Excel Basic Operations and Tips http://excelwaza.seesaa.net/article/371155163.html
