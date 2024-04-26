---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "IIJmioの携帯電話から他番号へ転送設定を行う"
subtitle: ""
summary: " "
tags: ["その他","メモ"]
categories: ["その他","メモ"]
url: iijmio-telephone-transfer.html
date: 2021-02-01
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



IIJmioでは転送でんわサービスを利用出来る。利用したいシチュエーションがあったのでメモ。

# 参考

> https://www.iijmio.jp/hdd/miofone/voiceopt.html#transfer

# 注意点

- 契約の携帯電話から転送先への通話料が、転送でんわサービスの契約者に掛かる。
- 発信元の料金も必要となる。
- 転送設定を行った段階で、留守番電話が無効となる。
- 転送時間までの秒数を指定出来る（デフォルト7秒）
- 転送設定を行った後の状態だと、「この電話を転送しますので、少々お待ちください」というアナウンスが流れる
  - ガイダンス設定を必要に応じて変更する

# 手順

転送時間を5秒に変更し、ガイダンスを無しに設定する場合、下記手順が必要となる。

> https://www.iijmio.jp/hdd/miofone/voiceopt.html#transfer

1. 転送先電話番号の登録・変更
2. 転送でんわサービスの開始
3. ガイダンスを無しに設定
4. 呼び出し時間を「5秒」に設定