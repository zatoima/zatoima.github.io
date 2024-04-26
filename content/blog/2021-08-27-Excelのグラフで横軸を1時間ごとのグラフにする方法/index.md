---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Excelのグラフで横軸を1時間ごとのグラフにする方法"
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

意外とパッとわからなかったのでメモ。

↓のようにx軸（横軸）を1時間ごとのグラフを作りたい。対象のデータ自体は全て揃っておらず、任意のタイミングでのみ取得している前提。

![image-20210826185024343](image-20210826185024343.png)

グラフ自体は折れ線グラフではなく散布図として、軸の書式設定の単位で1時間ごとのシリアル値を示す「0.041666666666」とする。ここのシリアル値を変更することでX軸の単位を変更することが出来る。

![image-20210826185136781](image-20210826185136781.png)

参考

> エクセル グラフ 時間: エクセルの基本操作と小技 http://excelwaza.seesaa.net/article/371155163.html
