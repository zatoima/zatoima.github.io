---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "VSCodeのシンタックスハイライトのコピー機能の無効化"
subtitle: ""
summary: " "
tags: ["VSCode","Tools"]
categories: ["VSCode","Tools"]
url: vscore-syntax-highlighting-disabled.html
date: 2019-06-23
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



## はじめに

------

teratailに数年前に質問して回答ゼロだったシンタックスハイライトのコピー機能の無効化についてようやく方法がわかった。

```
Visual Studio Code February 2017 | 非公式 - Visual Studio Code Docs https://vscode-doc-jp.github.io/updates/v1_10.html

シンタックスハイライトのコピー (Copy with syntax highlighting)
選択されたテキストは、シンタックスハイライトが適用された状態でクリップボードにコピーされるようになりました。
これは、コンテンツを別のアプリケーション (たとえば、Outlook など) に貼り付けるときに非常に便利です。
アプリケーションへ貼り付けられる内容は、正しいフォーマットと色付けを保持しています。
```

> Visual Studio Code - vscodeのシンタックスハイライトのコピー機能の無効化について｜teratail https://teratail.com/questions/119990

```html
Visual Studio Codeを使用しています。(Windows版)
下記に示す機能を無効化する方法や手段はありますでしょうか。

https://vscode-doc-jp.github.io/updates/v1_10.html
>シンタックスハイライトのコピー (Copy with syntax highlighting)

コピーアンドペーストした際に書式情報も一緒にコピーされ困っています。
一度メモ帳に貼り付けたりCtrl+Shift+Vで回避もできますが設定で無効化できるとしたら
その方法を知りたいです。
```

## 設定方法

------

「File」-「Preferences」-「Settings」を選択し、その中から`Editor: Copy With Syntax Highlighting`のチェックを外すこと。

<img src="images/image-20191121172147714.png" alt="image-20191121172147714"  />

※VSCodeが古いバージョン（例：1.22）の場合は、上記の方法は実施できなかった。上記が見つからない場合は、まずは最新化を検討した方が良い。今回は1.35.1のバージョンで実施。teratailに質問したときに回答無かったのはシンタックスハイライトを無効化機能が実装されていなかったからかもしれない。

## 参考

------

> VSCodeでコピーする時に「書式なし」をデフォルトにする - Qiita https://qiita.com/kaityo256/items/d39884c36bd5b35e6427