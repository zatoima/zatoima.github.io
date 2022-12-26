---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ドッキングステーション購入の失敗談メモ"
subtitle: ""
summary: " "
tags: ["その他"]
categories: ["その他"]
url: other-docking-station
date: 2021-12-15
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only:
---



### 前提

下記の2台を必要なときにそれぞれドッキングステーションに繋げてWQHD（2,560×1,440）モニター2枚に接続してデュアルディスプレイ環境にしたかった。キーボードやマウス、その他ワイヤレスヘッドフォン等をドッキングステーションに繋げて外部機器を共用したかった。

① thunderbolt3対応の仕事用PC

② thunderbolt3非対応（usb type-c)のPC

### 現状

1. [Thunderbolt™ 3 Dock Pro for Mac & PC](https://www.belkin.com/jp/business/hubs-and-docks-for-business/docking-stations-for-business/thunderbolt-3-dock-pro/p/p-f4u097/)

   - USB Type-Cのデバイス対応と謳っているにも関わらず、下記の注意事項が[belkinの公式ホームページ上](https://www.belkin.com/jp/business/hubs-and-docks-for-business/docking-stations-for-business/thunderbolt-3-dock-pro/p/p-f4u097/)に小さく表示があり。Amazonで購入したがAmazon側には特にこの注意事項が無く見落とす。

   > USB-C端子経由の機能は制限されることがあり、すべてのUSB-C端子がUSB Type-C規格のすべての機能に対応が可能ではないことがありますので、ご注意ください。また、USB-C端子から外部モニターへの拡張表示に対応しない場合があります。

   - ドッキングステーション側でUSB Type Aが認識しなかった。ドライバを色々インストールしたが改善せず。

2. [Anker PowerExpand Elite 13\-in\-1 Thunderbolt 3 Dock ドッキングステーション](https://www.ankerjapan.com/products/a8396)

   - USB Type-Cのデバイス対応と記載あり
   - USB Type-Cのデバイス経由でドッキングステーションに接続後、HDMI経由の外部モニター出力は出力されるが、USB Type-C経由の外部モニター出力が出力されない。
     - サポートに聞いたところ、USB Type-Cでドッキングステーションに接続するデバイスにおいて、USB Type-C経由の外部モニター出力はNGの模様。（ホームページ上に注意事項はどこにも書いていない。）
   - Thunderbolt3対応のパソコンでは問題無かったので、大人しくThunderbolt3対応のデバイスを接続した方が良いのかもしれない。

### 結論

接続回りは非常にややこしくトラブルを引き起こしやすい。`② thunderbolt3非対応（usb type-c)のPC`を買い替えた方が良い気がしてきた…。

