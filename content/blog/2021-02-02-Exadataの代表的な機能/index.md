---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Exadataの代表的な機能"
subtitle: ""
summary: " "
tags: ["Oracle","Exadata"]
categories: ["Oracle","Exadata"]
url: oracle-exadata-typical-functions.html
date: 2021-02-02
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

# Exadataの代表的な機能（性能面）

![image-20210202110349035](image-20210202110349035.png)

> Oracle Exadata System Softwareの概要 https://docs.oracle.com/cd/F19137_01/sagug/exadata-storage-server-software-introduction.html#GUID-D6856B9A-DBB2-44DF-8632-01637AFAE962

# 性能分析時に必要な統計値など

SmartScanを始めとした効果を分析する際はこちらの統計を参照するのが良さそう。Oracle製品の良いところは機能面もそうだが、調べると情報が出てきやすいところ。

> 津島博士のパフォーマンス講座　第69回　Oracle Exadata Database Machineについて | Oracle Technology Network Japan Blog https://blogs.oracle.com/otnjp/tsushima-hakushi-69

![image-20210131214828557](image-20210131214828557.png)

| 統計名                                                      | 意味                                                         | V$SQLの統計                    |
| ----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------ |
| cell  physical IO interconnect bytes                        | DBサーバーとCellの間でやりとりされたIOサイズで、Smart  Scan以外も含む（解凍後のサイズ） | IO_INTERCONNECT_BYTES          |
| cell  physical IO interconnect bytes returned by smart scan | Smart  ScanによりCellから返されたIOサイズ（解凍後のサイズ）  | IO_CELL_OFFLOAD_RETURNED_BYTES |
| cell  physical IO bytes eligible for predicate offload      | Smart  Scanの対象となったIOサイズ（physical read total bytesとの違いはSmart Scan以外が含まない） | IO_CELL_OFFLOAD_ELIGIBLE_BYTES |
| cell  IO uncompressed bytes                                 | cellで処理された非圧縮のデータ・サイズ                       | IO_CELL_UNCOMPRESSED_BYTES     |
| cell  physical IO bytes saved by storage index              | Storage indexによるIO削減サイズ                              | OPTIMIZED_PHY_READ_REQUESTS    |
| cell  flash cache read hits                                 | Smart  Flash Cacheに対するリクエスト回数                     |                                |
| physical  read total IO requests                            | 物理読込みI/Oリクエスト回数                                  | PHYSICAL_READ_REQUESTS         |
| physical  read total Bytes                                  | 物理読込みサイズ（バイト）                                   | PHYSICAL_READ_BYTES            |

# その他参考

> Exadataフラッシュキャッシュの謎：オラクルデータベースの技術メモ：So-netブログ https://tech-oracle.blog.ss-blog.jp/2019-02-06