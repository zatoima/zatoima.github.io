---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ublacklistでGoogle検索の結果をフィルタリングする"
subtitle: ""
summary: " "
tags: ["その他","メモ"]
categories: ["その他","メモ"]
url: chrome-ublacklist-filter-url.html
date: 2021-04-12
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



Chromeの拡張機能である`ublacklist`を使用して検索結果から特定URLを含むサイトを除外することが出来る。

- Chrome拡張機能

  https://chrome.google.com/webstore/detail/ublacklist/pncfbmialoiaghdehhbnbhkkgmjanfhe/related?hl=ja

- 使い方

  - uBlacklistを使ってDevelopersIOを検索結果から除外する | DevelopersIO https://dev.classmethod.jp/articles/deny-devio-using-ublacklist/

- リスト

  githubやgoogle driveのテキストを拡張機能から読み込めるらしいので、gistにアップロードしてみた。

> https://raw.githubusercontent.com/zatoima/uBlacklist/main/ublacklist.txt

```
*://code-examples.net/*
*://codechacha.com/*
*://codeday.me/*
*://codezine.jp/*
*://daviesmediadesign.com/*
*://ja.coder.work/*
*://ja.ojit.com/*
*://ja.programqa.com/*
*://ja.voidcc.com/*
*://kotaeta.com/*
*://living-sun.com/*
*://matome.naver.jp/*
*://my-best.com/*
*://qastack.jp/*
*://resonate.it/*
*://riptutorial.com/*
*://src-bin.com/*
*://stackoverrun.com/*
*://techacademy.jp/*
*://tutorialmore.com/*
*://webapps.stackovernet.com/*
*://www.366service.com/*
*://www.apowersoft.jp/*
*://www.code-adviser.com/*
*://www.codeflow.site/*
*://www.dev4app.com/*
*://www.hatsune.info/*
*://www.matools.com/*
*://www.sejuku.net/*
*://www.soolide.com/*
/.*it-swarm.*/
/.*pinterest.*/
/.*udemy.*/
```







