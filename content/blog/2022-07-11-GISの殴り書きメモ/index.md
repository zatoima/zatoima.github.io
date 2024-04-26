---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GISの殴り書きメモ"
subtitle: ""
summary: " "
tags: ["Other"]
categories: ["Other"]
url: other-geographic-information-system-desc
date: 2022-07-11
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



用語のメモ。GISは奥が深い…GIS屋という職業が存在するわけだ

-----

- GIS
  - Geographic Information System
- 民間のWeb地図には著作権の壁がある
  - オープンな地図データ
    - OpenStreetMap（OSM）
      - https://www.openstreetmap.org
    - 国土地理院の地理院地図
      - https://maps.gsi.go.jp/

- 位置情報を使用した有名なWebサービス
  - https://flightradars24.info/ja/
  - https://www.marinetraffic.com/

- GISのデータ構造

  - ベクター形式

    - 点、線、多角形

      - ポイント（点）
      - ライン（線）
      - ポリゴン（面）

      ![image-20220705180458220](image-20220705180458220.png)

  - ラスター形式

    - 行と列の格子状（グリッド状）に並んだセル（ピクセル）で構成されるデータ
      - 地図と組み合わせてデータを表示したい場合に使われる
        - 降水量や気温、標高データなど

- アドレスマッチング

- 逆GEO

- ジオコーダー

> https://qiita.com/uhey22e/items/69285a14b4476dc73664
>
