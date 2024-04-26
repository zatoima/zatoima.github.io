---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Oracle Database 19c Standard Edition 2のReal Application Clustersの非サポート"
subtitle: ""
summary: " "
tags: ["Oracle"]
categories: ["Oracle"]
url: oracle-19c-se2-desupport.html
date: 2019-07-15
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


<iframe src="//www.slideshare.net/slideshow/embed_code/key/F2k57INtgh6w87?startSlide=2" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/MarkusMichalewicz/oracle-rac-19c-with-standard-edition-se-2-support-update" title="Oracle RAC 19c with Standard Edition (SE) 2 - Support Update" target="_blank">Oracle RAC 19c with Standard Edition (SE) 2 - Support Update</a> </strong> from <strong><a href="//www.slideshare.net/MarkusMichalewicz" target="_blank">Markus Michalewicz</a></strong> </div>
### Upgrade Paths

- Convert SE2 RAC Databases to Single Instance
- Migrate your SE2 RAC Databases to Enterprise Edition (EE) and purchase the RAC Database Option
- Migrate your SE2 RAC to the Oracle Cloud

### 備考：19c SE2でOracle RACを構築しようとした場合

Oracle Universal Installer（OUI）またはOracle Database Upgrade Assistant（DBUA）の使用に関しては、[INS-35465]、及び[DBT-20011]エラーが出力されてしまいます。他バージョンで非サポートの場合でも使い続けることが出来る機能は多かったですが、RACの場合は構成自体が不可の模様です。

##### [INS-35465] Standard Edition(SE) is not supported for this installation.
<img src="images/image-20191121214621763.png" alt="image-20191121214621763" style="zoom: 67%;" />

##### [DBT-20011] Oracle home xxxxxx is not enabled with RAC option.

<img src="images/image-20191121214638304.png" alt="image-20191121214638304" style="zoom:67%;" />

### 参考

My Oracle Suppot
> Desupport of Oracle Real Application Clusters (RAC) with Oracle Database Standard Edition 19c (Doc ID 2504078.1)


Manual
> Licensing Information https://docs.oracle.com/en/database/oracle/oracle-database/19/dblic/Licensing-Information.html#GUID-0F9EB85D-4610-4EDF-89C2-4916A0E7AC87

Blog

> Oracle database 19c Standard Edition 2 sem suporte para Real Application Clusters (RAC) ~ DBA Anderson Graf http://www.andersondba.com.br/2019/05/oracle-database-19c-standard-edition-2.html